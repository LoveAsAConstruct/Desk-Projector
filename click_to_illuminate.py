from projection_stream import *
from calibration_box import *
import threading

global projection_window

def project():
    app = QApplication(sys.argv)
    # Set monitor position and dimensions (x, y, width, height)
    # Assume the monitor is positioned at the bottom-left of the primary monitor:
    projection_window = CheckerboardWindow(monitor_position=(0, 2160), width=1920, height=1080)
    sys.exit(app.exec_())
def sync_window():
    print(f"syncing {projection_window.pointxy} to {mousepos}")
    projection_window.pointxy = mousepos
if __name__ == '__main__':
    # Correct threading approach
    projection_stream = threading.Thread(target=stream_transformed_image, daemon=True)
    sync_thread = threading.Thread(target=sync_window, daemon=True)

    projection_stream.start()
    sync_thread.start()

    # Start PyQt application on the main thread
    app = QApplication(sys.argv)
    projection_window = CheckerboardWindow(monitor_position=(0, 2160), width=1920, height=1080)
    sys.exit(app.exec_())
