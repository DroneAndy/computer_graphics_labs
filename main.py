import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLineEdit
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt
from numpy import linalg as LA
import numpy as np
import math

BUTTON_Y = 600
""" Y координата первой кнопки """

BUTTON_X = 100
""" X координата первой кнопки """

BUTTON_DELTA_Y = 50
""" Смещение второго и последующих рядов кнопок по оси Y относительно предыдущего ряда """


class Point:
    """ Класс точка """

    x = 0
    """ Координата X """

    y = 0
    """ Координата Y """

    z = 0
    """ Координата Z """

    def __init__(self, _x, _y, _z):
        """ Конструктор класса """
        self.x = _x
        self.y = _y
        self.z = _z


class Line:
    """ Класс линия """

    a = Point(0, 0, 0)
    """ Точка A """

    b = Point(0, 0, 0)
    """ Точка B """

    def __init__(self, _a, _b):
        """ Конструктор класса """
        self.a = _a
        self.b = _b


class Polygon:
    """ Класс многоугольник """
    lines = []

    def __init__(self, _lines):
        """ Конструктор класса """
        self.lines = _lines


# FIXME change coordinates to center of the letter
Lines = [Line(Point(100, 100, 0), Point(100, 500, 0)),
         Line(Point(100, 500, 0), Point(300, 500, 0)),
         Line(Point(300, 500, 0), Point(300, 100, 0)),
         Line(Point(300, 100, 0), Point(100, 100, 0))]
Outer_polygon = Polygon(Lines)
Lines = [Line(Point(150, 150, 0), Point(150, 450, 0)),
         Line(Point(150, 450, 0), Point(250, 450, 0)),
         Line(Point(250, 450, 0), Point(250, 150, 0)),
         Line(Point(250, 150, 0), Point(150, 150, 0))]
Inner_polygon = Polygon(Lines)
Lines = [Line(Point(150, 150, 100), Point(150, 450, 100)),
         Line(Point(150, 450, 100), Point(250, 450, 100)),
         Line(Point(250, 450, 100), Point(250, 150, 100)),
         Line(Point(250, 150, 100), Point(150, 150, 100))]
Inner_polygon_rear = Polygon(Lines)
Lines = [Line(Point(100, 100, 100), Point(100, 500, 100)),
         Line(Point(100, 500, 100), Point(300, 500, 100)),
         Line(Point(300, 500, 100), Point(300, 100, 100)),
         Line(Point(300, 100, 100), Point(100, 100, 100))]
Outer_polygon_rear = Polygon(Lines)
Lines = [Line(Point(100, 100, 0), Point(100, 100, 100)),
         Line(Point(100, 500, 0), Point(100, 500, 100)),
         Line(Point(100, 500, 0), Point(100, 100, 0)),
         Line(Point(100, 500, 100), Point(100, 100, 100))]
right_polygon = Polygon(Lines)
Lines = [Line(Point(300, 100, 0), Point(300, 100, 100)),
         Line(Point(300, 500, 0), Point(300, 500, 100)),
         Line(Point(300, 500, 0), Point(300, 100, 0)),
         Line(Point(300, 500, 100), Point(300, 100, 100))]
left_polygon = Polygon(Lines)
Lines = [Line(Point(150, 150, 0), Point(150, 150, 100)),
         Line(Point(150, 450, 0), Point(150, 450, 100)),
         Line(Point(150, 450, 0), Point(150, 150, 0)),
         Line(Point(150, 450, 100), Point(150, 150, 100))]
right_inner_polygon = Polygon(Lines)
Lines = [Line(Point(250, 150, 0), Point(250, 150, 100)),
         Line(Point(250, 450, 0), Point(250, 450, 100)),
         Line(Point(250, 450, 0), Point(250, 150, 0)),
         Line(Point(250, 450, 100), Point(250, 150, 100))]
left_inner_polygon = Polygon(Lines)
Polygons = [Outer_polygon, Inner_polygon, Outer_polygon_rear, Inner_polygon_rear,
            right_polygon, left_polygon, right_inner_polygon, left_inner_polygon]


class Main(QMainWindow):
    """ Основной класс с приложением """

    changes = np.matrix([[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
    """ Матрица изменений """

    center = Point(200, 300, 0)
    """ Центральная точка фигуры, относительно которой происходит поворот """

    x = 0
    """ Координата X луча """
    y = 0
    """ Координата Y луча """
    z = 0
    """ Координата Z луча """

    def __init__(self):
        super().__init__()
        self.pix = QPixmap()
        self.ev = ""
        self.initUI()

    def initUI(self):
        coordinates = QLineEdit(self)
        coordinates.setInputMask("(999,999,999)")
        coordinates.setText("(0,0,0)")
        coordinates.move(650, 100)
        coordinates.resize(100, 32)
        coordinates.setAlignment(Qt.AlignCenter)
        coordinates.textChanged[str].connect(self.save_coordinates)
        rotate = QPushButton("rotate", self)
        rotate.move(650, 150)
        rotate.clicked.connect(self.btn_clicked)
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
                        QPushButton("z+", self),
                        QPushButton("z-", self),
                        QPushButton("rot_x+", self),
                        QPushButton("rot_x-", self),
                        QPushButton("rot_y+", self),
                        QPushButton("rot_y-", self),
                        QPushButton("rot_z+", self),
                        QPushButton("rot_z-", self)]
        i = 1
        delta_y = 0
        for button in button_array:
            if i > 6:
                i = 1
                delta_y += BUTTON_DELTA_Y
            button.move(BUTTON_X * i, BUTTON_Y + delta_y)
            button.clicked.connect(self.btn_clicked)
            i += 1

        self.statusBar()
        self.pix = QPixmap(400, 400)
        self.pix.fill(Qt.black)
        self.setGeometry(300, 200, 800, 800)
        self.setWindowTitle('Points')
        self.show()

    def save_coordinates(self, text):
        coordinates = text[1:-1].split(",")
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        self.z = int(coordinates[2])

    def btn_clicked(self):
        """ Обработчик события нажатия кнопки """
        command = self.sender().text()
        match command:
            case "right": self.move_letter(50, 0, 0)
            case "left": self.move_letter(-50, 0, 0)
            case "up": self.move_letter(0, -50, 0)
            case "down": self.move_letter(0, 50, 0)
            case "x+": self.resize_letter(1.25, 1, 1)
            case "x-": self.resize_letter(0.75, 1, 1)
            case "y+": self.resize_letter(1, 1.25, 1)
            case "y-": self.resize_letter(1, 0.75, 1)
            case "z+": self.resize_letter(1, 1, 1.25)
            case "z-": self.resize_letter(1, 1, 0.75)
            case "rot_x+": self.rotate_letter(math.pi / 10, 0, 0)
            case "rot_x-": self.rotate_letter(-math.pi / 10, 0, 0)
            case "rot_y+": self.rotate_letter(0, math.pi / 10, 0)
            case "rot_y-": self.rotate_letter(0, -math.pi / 10, 0)
            case "rot_z+": self.rotate_letter(0, 0, math.pi / 10)
            case "rot_z-": self.rotate_letter(0, 0, -math.pi / 10)
            case "refl_x": self.resize_letter(-1, 1, 1)
            case "refl_y": self.resize_letter(1, -1, 1)
            case "rotate": self.rotate_relative_to_beam(self.x, self.y, self.z, math.pi / 10)
        self.update()

    def paintEvent(self, e):
        """ Обработчик события отрисовки """
        qp = QPainter()
        qp.begin(self)
        self.draw_letter(qp)
        qp.end()

    def draw_letter(self, qp):
        """
        Функция рисования буквы
        :param qp: Объект типа QPainter
        :return: Ничего
        """
        self.pix.fill(Qt.white)
        qp.setPen(Qt.red)
        for polygon in Polygons:
            for line in polygon.lines:
                new_a = np.matmul([[line.a.x, line.a.y, line.a.z, 1]], self.changes)
                new_b = np.matmul([[line.b.x, line.b.y, line.b.z, 1]], self.changes)
                qp.drawLine(int(new_a.item(0)), int(new_a.item(1)), int(new_b.item(0)), int(new_b.item(1)))

    def rotate_letter(self, angle_x, angle_y, angle_z):
        """
        Функция поворота буквы
        :param angle_x: Угол поворота относительно оси X
        :param angle_y: Угол поворота относительно оси Y
        :param angle_z: Угол поворота относительно оси Z
        :return: Ничего
        """
        self.changes = np.matmul(self.changes, np.matrix([[1, 0, 0, -self.center.x],
                                                          [0, 1, 0, -self.center.y],
                                                          [0, 0, 1, -self.center.z],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[math.cos(angle_y), 0, -math.sin(angle_y), 0],
                                                          [0, 1, 0, 0],
                                                          [math.sin(angle_y), 0, math.cos(angle_y), 0],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[1, 0, 0, 0],
                                                          [0, math.cos(angle_x), -math.sin(angle_x), 0],
                                                          [0, math.sin(angle_x), math.cos(angle_x), 0],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[math.cos(angle_z), -math.sin(angle_z), 0, 0],
                                                          [math.sin(angle_z), math.cos(angle_z), 0, 0],
                                                          [0, 0, 1, 0],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[1, 0, 0, self.center.x],
                                                          [0, 1, 0, self.center.y],
                                                          [0, 0, 1, self.center.z],
                                                          [0, 0, 0, 1]]).transpose())

    def move_letter(self, delta_x, delta_y, delta_z):
        """
        Функция перемещения буквы
        :param delta_x: Изменение координаты X
        :param delta_y: Изменение координаты Y
        :param delta_z: Изменение координаты Z
        :return: Ничего
        """
        self.changes = np.matmul(self.changes, [[1, 0, 0, 0],
                                                [0, 1, 0, 0],
                                                [0, 0, 1, 0],
                                                [delta_x, delta_y, delta_z, 1]])
        self.center.x += delta_x
        self.center.y += delta_y
        self.center.z += delta_z

    def resize_letter(self, size_x, size_y, size_z):
        """
        Функция масштабирования буквы
        :param size_x: Коэффициент масштабирования по оси X
        :param size_y: Коэффициент масштабирования по оси Y
        :param size_z: Коэффициент масштабирования по оси Z
        :return: Ничего
        """
        self.changes = np.matmul(self.changes, np.matrix([[1, 0, 0, -self.center.x],
                                                          [0, 1, 0, -self.center.y],
                                                          [0, 0, 1, -self.center.z],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[size_x, 0, 0, 0],
                                                          [0, size_y, 0, 0],
                                                          [0, 0, size_z, 0],
                                                          [0, 0, 0, 1]]).transpose())
        self.changes = np.matmul(self.changes, np.matrix([[1, 0, 0, self.center.x],
                                                          [0, 1, 0, self.center.y],
                                                          [0, 0, 1, self.center.z],
                                                          [0, 0, 0, 1]]).transpose())

    def rotate_relative_to_beam(self, l, m, n, fi):
        """
        Функция для поворота буквы относительно произвольного луча
        :param l: Координата X
        :param m: Координата X
        :param n: Координата X
        :param fi: Угол поворота
        :return: Ничего
        """
        Ry = np.matrix([[l/math.sqrt(l*l + n*n), 0, -n/math.sqrt(l*l + n*n), 0],
                        [0, 1, 0, 0],
                        [n/math.sqrt(l*l + n*n), 0, l/math.sqrt(l*l + n*n), 0],
                        [0, 0, 0, 1]])
        """ Матрица перемещения луча в плоскость xOy"""
        Rz = np.matrix([[m/math.sqrt(l*l + n*n + m*m), -math.sqrt(l*l + n*n)/math.sqrt(l*l + n*n + m*m), 0, 0],
                        [math.sqrt(l*l + n*n)/math.sqrt(l*l + n*n + m*m), m/math.sqrt(l*l + n*n + m*m), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
        """ Матрица совмещения луча с ось oY """
        Rfi = np.matrix([[math.cos(fi), 0, -math.sin(fi), 0],
                         [0, 1, 0, 0],
                         [math.sin(fi), 0, math.cos(fi), 0],
                         [0, 0, 0, 1]])
        """ Матрица поворота на угол fi """
        self.changes = np.matmul(self.changes, Ry.transpose())
        self.changes = np.matmul(self.changes, Rz.transpose())
        self.changes = np.matmul(self.changes, Rfi.transpose())
        self.changes = np.matmul(self.changes, LA.inv(Rz).transpose())
        self.changes = np.matmul(self.changes, LA.inv(Ry).transpose())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
