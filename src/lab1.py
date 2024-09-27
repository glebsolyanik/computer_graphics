import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF

class RotationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0  # Угол поворота в градусах
        self.center_of_rotation = QPointF(100, 100)  # Центр вращения
        self.triangle = [QPointF(100, 100), QPointF(150, 150), QPointF(50, 200)]  # Вершины треугольника

        self.setWindowTitle("Поворот плоского объекта")
        self.setFixedSize(400, 400)

    def rotate_point(self, point, angle, center):
        """Функция для поворота точки вокруг другой точки."""
        rad = math.radians(angle)
        translated_x = point.x() - center.x()
        translated_y = point.y() - center.y()
        rotated_x = translated_x * math.cos(rad) - translated_y * math.sin(rad)
        rotated_y = translated_x * math.sin(rad) + translated_y * math.cos(rad)
        return QPointF(rotated_x + center.x(), rotated_y + center.y())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Вращаем каждую вершину треугольника вокруг центра вращения
        rotated_triangle = [self.rotate_point(p, self.angle, self.center_of_rotation) for p in self.triangle]

        # Рисуем треугольник
        painter.drawPolygon(*rotated_triangle)

        # Рисуем центр вращения
        painter.setPen(QPen(Qt.red, 4))
        painter.drawPoint(self.center_of_rotation)

    def update_rotation(self, angle):
        """Обновление угла поворота."""
        self.angle = angle
        self.update()

    def update_center_of_rotation(self, x, y):
        """Обновление положения центра вращения."""
        self.center_of_rotation = QPointF(x, y)
        self.triangle = [QPointF(x, y), QPointF(x+50, y+50), QPointF(x-50, y+100)]
        self.update()