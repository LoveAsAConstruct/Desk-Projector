import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

class CheckerboardWindow(QMainWindow):
    def __init__(self, monitor_position, width, height):
        super().__init__()
        self.monitor_position = monitor_position
        self.setFixedSize(width, height)
        self.move(*monitor_position)
        self.setWindowTitle('Checkerboard Pattern')

        # Enable fullscreen mode
        self.showFullScreen()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QBrush(QColor(255, 255, 255)))  # Initial white background
        qp.drawRect(self.rect())  # Draw the full background

        grid_size = 8
        cell_width = self.width() // grid_size
        cell_height = self.height() // grid_size

        for row in range(grid_size):
            for col in range(grid_size):
                if (row + col) % 2 == 0:
                    color = QColor(255, 255, 255)  # White
                else:
                    color = QColor(0, 0, 0)  # Black
                qp.setBrush(QBrush(color))
                qp.drawRect(col * cell_width, row * cell_height, cell_width, cell_height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Set monitor position and dimensions (x, y, width, height)
    # Assume the monitor is positioned at the bottom-left of the primary monitor:
    window = CheckerboardWindow(monitor_position=(0, 2160), width=1920, height=1080)
    sys.exit(app.exec_())
