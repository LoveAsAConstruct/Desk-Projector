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

ret, test_frame = cap.read()
if not ret:
    print("Failed to get frame from camera.")
    exit(1)
frame_height, frame_width = test_frame.shape[:2]
print(frame_width, frame_height)
# Define desired output size, you may adjust these values
output_width, output_height = frame_width, frame_height

# Adjust the perspective matrix if needed (manual tweaking might be required)
# perspective_matrix[0, 2] -= 100  # Adjust x translation if needed
# perspective_matrix[1, 2] -= 50   # Adjust y translation if needed

# Main loop for transforming and displaying video
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Apply the perspective transformation to the frame
        # You might want to experiment with different sizes here.
        output_size = (1920,1080)
        transformed_frame = cv2.warpPerspective(frame, perspective_matrix, output_size)


        # Display the transformed frame
        cv2.imshow('Transformed Video', transformed_frame)

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Clean up: release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()