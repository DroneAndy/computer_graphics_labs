import sys, random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt
import numpy
import math
# TODO отражение


class Point:
    x = 0
    y = 0

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y


class Line:
    a = Point(0, 0)
    b = Point(0, 0)

    def __init__(self, _a, _b):
        self.a = _a
        self.b = _b


class Polygon:
    lines = []

    def __init__(self, _lines):
        self.lines = _lines


# FIXME change coordinates to center of the letter
Lines = [Line(Point(100, 100), Point(100, 500)),
         Line(Point(100, 500), Point(300, 500)),
         Line(Point(300, 500), Point(300, 100)),
         Line(Point(300, 100), Point(100, 100))]
Outer_polygon = Polygon(Lines)
Lines = [Line(Point(150, 150), Point(150, 450)),
         Line(Point(150, 450), Point(250, 450)),
         Line(Point(250, 450), Point(250, 150)),
         Line(Point(250, 150), Point(150, 150))]
Inner_polygon = Polygon(Lines)
Polygons = [Outer_polygon, Inner_polygon]


def rotate(change, angle):
    s = 200  # FIXME change to center coordinates
    t = 300
    change = numpy.matmul(change, numpy.matrix([[1, 0, -s],
                                                [0, 1, -t],
                                                [0, 0, 1]]).transpose())
    change = numpy.matmul(change, numpy.matrix([[math.cos(angle), -math.sin(angle), 0],
                                                [math.sin(angle), math.cos(angle), 0],
                                                [0, 0, 1]]).transpose())
    change = numpy.matmul(change, numpy.matrix([[1, 0, s],
                                                [0, 1, t],
                                                [0, 0, 1]]).transpose())
    return change


def move_letter(change, delta_x, delta_y):
    change = numpy.matmul(change, [[1, 0, 0], [0, 1, 0], [delta_x, delta_y, 1]])
    return change


def resize_letter(change, size_x, size_y):
    change = numpy.matmul(change, numpy.matrix([[size_x, 0, 0],
                                                [0, size_y, 0],
                                                [0, 0, 1]]).transpose())
    return change


class Example(QMainWindow):
    changes = numpy.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def __init__(self):
        super().__init__()
        self.pix = QPixmap()
        self.ev = ""
        self.initUI()

    def initUI(self):
        btn_move_left = QPushButton("left", self)
        btn_move_left.move(100, 600)
        btn_move_left.clicked.connect(self.btn_clicked)

        btn_move_right = QPushButton("right", self)
        btn_move_right.move(200, 600)
        btn_move_right.clicked.connect(self.btn_clicked)

        btn_move_up = QPushButton("up", self)
        btn_move_up.move(300, 600)
        btn_move_up.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("down", self)
        btn_move_down.move(400, 600)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("x+", self)
        btn_move_down.move(100, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("x-", self)
        btn_move_down.move(200, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("y+", self)
        btn_move_down.move(300, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("y-", self)
        btn_move_down.move(400, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("rot+", self)
        btn_move_down.move(500, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        btn_move_down = QPushButton("rot-", self)
        btn_move_down.move(600, 700)
        btn_move_down.clicked.connect(self.btn_clicked)

        self.statusBar()
        self.pix = QPixmap(400, 400)
        self.pix.fill(Qt.black)
        self.setGeometry(300, 200, 800, 800)
        self.setWindowTitle('Points')
        self.show()

    def btn_clicked(self):
        command = self.sender().text()
        # TODO rewrite to match-case (update python to 3.10)
        if command == "right":
            self.changes = move_letter(self.changes, 50, 0)
        elif command == "left":
            self.changes = move_letter(self.changes, -50, 0)
        elif command == "up":
            self.changes = move_letter(self.changes, 0, -50)
        elif command == "down":
            self.changes = move_letter(self.changes, 0, 50)
        elif command == "x+":
            self.changes = resize_letter(self.changes, 1.25, 1)
        elif command == "x-":
            self.changes = resize_letter(self.changes, 0.75, 1)
        elif command == "y+":
            self.changes = resize_letter(self.changes, 1, 1.25)
        elif command == "y-":
            self.changes = resize_letter(self.changes, 1, 0.75)
        elif command == "rot+":
            self.changes = rotate(self.changes, 0.5)
        elif command == "rot-":
            self.changes = rotate(self.changes, -0.5)
        elif command == "refl_x":
            self.changes = resize_letter(self.changes, -1, 1)
        elif command == "refl_y":
            self.changes = resize_letter(self.changes, 1, -1)
        self.update()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_letter(qp)
        qp.end()

    def draw_letter(self, qp):
        self.pix.fill(Qt.white)
        qp.setPen(Qt.red)
        for polygon in Polygons:
            for line in polygon.lines:
                new_a = numpy.matmul([[line.a.x, line.a.y, 1]], self.changes)
                new_b = numpy.matmul([[line.b.x, line.b.y, 1]], self.changes)
                qp.drawLine(int(new_a.item(0)), int(new_a.item(1)), int(new_b.item(0)), int(new_b.item(1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# autodoc