import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QSlider, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

from lab1 import RotationWidget

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