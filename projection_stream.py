import cv2
import pickle
import numpy as np

# Load the perspective transformation matrix
print("Loading the perspective transformation matrix...")
with open('perspective_matrix.pkl', 'rb') as f:
    perspective_matrix = pickle.load(f)
print("Matrix loaded.")

# Initialize video capture from camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit(1)

# Optionally adjust camera settings for consistent frame size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

global mousepos 
mousepos = (0, 0)

def mouse_callback(event, x, y, flags, param):
    global mousepos
    if event == cv2.EVENT_LBUTTONDOWN:
        mousepos = (x, y)

def stream_transformed_image():
    ret, test_frame = cap.read()
    if not ret:
        print("Failed to get frame from camera.")
        exit(1)
    frame_height, frame_width = test_frame.shape[:2]
    print(frame_width, frame_height)

    cv2.namedWindow("Transformed Video")
    cv2.setMouseCallback("Transformed Video", mouse_callback)

    # Main loop for transforming and displaying video
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break

            # Apply the perspective transformation to the frame
            output_size = (1920, 1080)
            transformed_frame = cv2.warpPerspective(frame, perspective_matrix, output_size)

            # Draw a circle at the mouse position
            cv2.circle(transformed_frame, mousepos, 10, (255, 0, 0), -1)  # Blue circle with a radius of 10

            # Display the transformed frame
            cv2.imshow('Transformed Video', transformed_frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # Clean up: release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    stream_transformed_image()
