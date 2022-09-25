import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
import numpy
import math

BUTTON_Y = 600
BUTTON_X = 100
BUTTON_DELTA_Y = 50


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


class Example(QMainWindow):
    changes = numpy.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    center = Point(200, 300)

    def __init__(self):
        super().__init__()
        self.pix = QPixmap()
        self.ev = ""
        self.initUI()

    def initUI(self):
        button_array = [QPushButton("left", self),
                        QPushButton("right", self),
                        QPushButton("up", self),
                        QPushButton("down", self),
                        QPushButton("refl_x", self),
                        QPushButton("refl_y", self),
                        QPushButton("x+", self),
                        QPushButton("x-", self),
                        QPushButton("y+", self),
                        QPushButton("y-", self),
                        QPushButton("rot+", self),
                        QPushButton("rot-", self)]
        i = 1
        delta_y = 0
        for button in button_array:
            if i > (len(button_array) / 2):
                i = 1
                delta_y = BUTTON_DELTA_Y
            button.move(BUTTON_X * i, BUTTON_Y + delta_y)
            button.clicked.connect(self.btn_clicked)
            i += 1

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
            self.move_letter(50, 0)
        elif command == "left":
            self.move_letter(-50, 0)
        elif command == "up":
            self.move_letter(0, -50)
        elif command == "down":
            self.move_letter(0, 50)
        elif command == "x+":
            self.resize_letter(1.25, 1)
        elif command == "x-":
            self.resize_letter(0.75, 1)
        elif command == "y+":
            self.resize_letter(1, 1.25)
        elif command == "y-":
            self.resize_letter(1, 0.75)
        elif command == "rot+":
            self.rotate_letter(math.pi / 10)
        elif command == "rot-":
            self.rotate_letter(-math.pi / 10)
        elif command == "refl_x":
            self.resize_letter(-1, 1)
        elif command == "refl_y":
            self.resize_letter(1, -1)
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

    def rotate_letter(self, angle):
        self.changes = numpy.matmul(self.changes, numpy.matrix([[1, 0, -self.center.x],
                                                                [0, 1, -self.center.y],
                                                                [0, 0, 1]]).transpose())
        self.changes = numpy.matmul(self.changes, numpy.matrix([[math.cos(angle), -math.sin(angle), 0],
                                                                [math.sin(angle), math.cos(angle), 0],
                                                                [0, 0, 1]]).transpose())
        self.changes = numpy.matmul(self.changes, numpy.matrix([[1, 0, self.center.x],
                                                                [0, 1, self.center.y],
                                                                [0, 0, 1]]).transpose())

    def move_letter(self, delta_x, delta_y):
        self.changes = numpy.matmul(self.changes, [[1, 0, 0], [0, 1, 0], [delta_x, delta_y, 1]])
        self.center.x += delta_x
        self.center.y += delta_y

    def resize_letter(self, size_x, size_y):
        self.changes = numpy.matmul(self.changes, numpy.matrix([[1, 0, -self.center.x],
                                                                [0, 1, -self.center.y],
                                                                [0, 0, 1]]).transpose())
        self.changes = numpy.matmul(self.changes, numpy.matrix([[size_x, 0, 0],
                                                                [0, size_y, 0],
                                                                [0, 0, 1]]).transpose())
        self.changes = numpy.matmul(self.changes, numpy.matrix([[1, 0, self.center.x],
                                                                [0, 1, self.center.y],
                                                                [0, 0, 1]]).transpose())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
