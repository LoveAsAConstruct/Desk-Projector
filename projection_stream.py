import cv2
import numpy as np
import pickle

# Load the perspective transformation matrix
with open('perspective_matrix.pkl', 'rb') as f:
    perspective_matrix = pickle.load(f)

# Capture a single frame from the camera
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("Error: Failed to capture frame.")
    exit(1)

# Apply perspective transformation to the frame
transformed_frame = cv2.warpPerspective(frame, perspective_matrix, (frame.shape[1], frame.shape[0]))

# Define the scale factor for resizing the transformed frame
scale_factor = 0.5  # Adjust as needed

# Resize the transformed frame for better display
transformed_frame_resized = cv2.resize(transformed_frame, None, fx=scale_factor, fy=scale_factor)

# Display the original and transformed frames
cv2.imshow('Original Frame', frame)
cv2.imshow('Transformed Frame', transformed_frame_resized)

# Wait for a key press and then close OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()
