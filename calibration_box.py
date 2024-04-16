import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QRect, QTimer
import random

class CheckerboardWindow(QMainWindow):
    def __init__(self, monitor_position, width, height):
        super().__init__()
        self.monitor_position = monitor_position
        self.setFixedSize(width, height)
        self.move(*monitor_position)
        self.setWindowTitle('Checkerboard Pattern')

        # Enable fullscreen mode
        self.showFullScreen()

        # Set up QTimer for periodic repaint
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(200)  # 200 milliseconds, i.e., 5 times a second

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QBrush(QColor(255, 255, 255)))  # Initial white background
        qp.drawRect(self.rect())  # Draw the full background

        grid_size = 10
        cell_width = self.width() // grid_size
        cell_height = self.height() // grid_size

        font = QFont()
        font.setPixelSize(60)  # Increased font size
        qp.setFont(font)

        for row in range(grid_size):
            for col in range(grid_size):
                if (row + col) % 2 == 0:
                    color = QColor(255, 255, 255)  # White
                    text_color = QColor(0, 0, 0)  # Black text on white squares
                else:
                    color = QColor(0, 0, 0)  # Black
                    text_color = QColor(255, 255, 255)  # White text on black squares

                qp.setBrush(QBrush(color))
                qp.drawRect(col * cell_width, row * cell_height, cell_width, cell_height)

                qp.setPen(text_color)  # Set text color
                qp.drawText(QRect(col * cell_width, row * cell_height, cell_width, cell_height), Qt.AlignCenter, f"{row * grid_size + col}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set monitor position and dimensions (x, y, width, height)
    # Assume the monitor is positioned at the bottom-left of the primary monitor:
    window = CheckerboardWindow(monitor_position=(0, 2160), width=1920, height=1080)
    sys.exit(app.exec_())
