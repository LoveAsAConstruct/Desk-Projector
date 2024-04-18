import sys
import cv2
import pickle
import numpy as np
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

# Global variables
global mousepos
mousepos = (0, 0)
global projection_window

# Load the perspective transformation matrix
with open('perspective_matrix.pkl', 'rb') as f:
    perspective_matrix = pickle.load(f)

class CheckerboardWindow(QMainWindow):
    def __init__(self, monitor_position, width, height):
        super().__init__()
        self.monitor_position = monitor_position
        self.setFixedSize(width, height)
        self.move(*monitor_position)
        self.setWindowTitle('Checkerboard Pattern')
        self.showFullScreen()
        self.pointxy = None

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setBrush(QBrush(QColor(255, 255, 255)))  # White background
        qp.drawRect(self.rect())  # Draw the full background

        if self.pointxy:
            qp.setPen(QColor(255, 0, 0))
            qp.setBrush(QBrush(QColor(255, 0, 0)))
            qp.drawEllipse(*self.pointxy, 20, 20)  # Draw red circle

def mouse_callback(event, x, y, flags, param):
    global mousepos, projection_window
    if event == cv2.EVENT_LBUTTONDOWN:
        mousepos = (x, y)  # Store mouse position
        if projection_window:
            # Transform coordinates to projection window scale and update
            projection_window.pointxy = (x, y)  # Adjust scaling here if necessary
            projection_window.update()  # Trigger repaint

def stream_transformed_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        sys.exit(1)

    cv2.namedWindow("Transformed Video")
    cv2.setMouseCallback("Transformed Video", mouse_callback)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Apply perspective transformation
        transformed_frame = cv2.warpPerspective(frame, perspective_matrix, (1920, 1080))

        cv2.imshow('Transformed Video', transformed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    global projection_window
    app = QApplication(sys.argv)
    projection_window = CheckerboardWindow(monitor_position=(0, 2160), width=1920, height=1080)
    
    camera_thread = threading.Thread(target=stream_transformed_image, daemon=True)
    camera_thread.start()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
