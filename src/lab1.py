import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QLineEdit
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Поворот объекта относительно точки")
        self.setFixedSize(500, 500)

        # Основной виджет для рисования
        self.rotation_widget = RotationWidget()

        # Слайдер для изменения угла поворота
        self.angle_slider = QSlider(Qt.Horizontal)
        self.angle_slider.setRange(0, 360)
        self.angle_slider.setValue(0)
        self.angle_slider.valueChanged.connect(self.on_angle_change)

        # Метки и поля ввода для изменения положения точки вращения
        self.x_input = QLineEdit("100")
        self.y_input = QLineEdit("100")

        # Кнопка для обновления положения центра вращения
        self.update_button = QPushButton("Обновить центр вращения")
        self.update_button.clicked.connect(self.on_update_center)

        # Настройка компоновки
        layout = QVBoxLayout()
        layout.addWidget(self.rotation_widget)
        layout.addWidget(QLabel("Угол поворота:"))
        layout.addWidget(self.angle_slider)

        center_layout = QHBoxLayout()
        center_layout.addWidget(QLabel("X:"))
        center_layout.addWidget(self.x_input)
        center_layout.addWidget(QLabel("Y:"))
        center_layout.addWidget(self.y_input)
        layout.addLayout(center_layout)
        layout.addWidget(self.update_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_angle_change(self, value):
        """Изменение угла вращения."""
        self.rotation_widget.update_rotation(value)

    def on_update_center(self):
        """Изменение центра вращения."""
        try:
            x = float(self.x_input.text())
            y = float(self.y_input.text())
            self.rotation_widget.update_center_of_rotation(x, y)
        except ValueError:
            pass  # Игнорировать ошибку, если введены некорректные данные

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())