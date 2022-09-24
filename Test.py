import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import Qt, QPoint


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        # Установить заголовок
        self.setWindowTitle("«Примеры рисования»")
        # Создание класса QPixmap
        self.pix = QPixmap()
        # Начало, конец
        self.lastPoint = QPoint()
        self.endPoint = QPoint()
        # Initialize
        self.initUi()

    def initUi(self):
        # Размер окна установлен на 600 * 500
        self.resize(600, 500)

        # Размер холста 400 * 400, фон белый
        self.pix = QPixmap(400, 400)
        self.pix.fill(Qt.white)

    def paintEvent(self, event):
        pp = QPainter(self.pix)
        # Нарисуйте прямые линии в соответствии с двумя позициями указателя мыши
        pp.drawLine(self.lastPoint, self.endPoint)
        # Пусть предыдущее значение координаты будет равно последнему значению координаты,
        # Таким образом, вы можете рисовать непрерывные линии
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        # Перетащите холст в указанную позицию окна
        painter.drawPixmap(0, 0, self.pix)

    def mousePressEvent(self, event):
        # Нажмите левую кнопку мыши
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.endPoint = self.lastPoint

    def mouseMoveEvent(self, event):
        # Переместите мышь, пока нажата левая кнопка мыши
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos()
            # Перерисовать
            self.update()

    def mouseReleaseEvent(self, event):
        # Левое нажатие кнопки мыши
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            # Перерисовать
            self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()
    sys.exit(app.exec_())