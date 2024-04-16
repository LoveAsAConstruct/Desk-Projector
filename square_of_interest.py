import cv2
import numpy as np
import pickle

# Load the perspective transformation matrix
with open('perspective_matrix.pkl', 'rb') as f:
    perspective_matrix = pickle.load(f)

# Function to draw a rectangle on an image
def draw_rect(event, x, y, flags, params):
    global pt1, pt2, drawing, completed

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        pt1 = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        pt2 = (x, y)
        completed = True

# Initialize variables
drawing = False
completed = False
pt1 = (-1, -1)
pt2 = (-1, -1)

# Create a window
cv2.namedWindow('Draw Square on Camera Stream')
cv2.setMouseCallback('Draw Square on Camera Stream', draw_rect)

# Capture video from the camera
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Apply perspective transformation to the frame
    transformed_frame = cv2.warpPerspective(frame, perspective_matrix, (frame.shape[1], frame.shape[0]))

    # Draw the square on the transformed frame
    if drawing:
        cv2.rectangle(transformed_frame, pt1, pt2, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Draw Square on Camera Stream', transformed_frame)

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s') and completed:
        # Save the square as an image file
        square_img = transformed_frame[min(pt1[1], pt2[1]):max(pt1[1], pt2[1]), min(pt1[0], pt2[0]):max(pt1[0], pt2[0])]
        cv2.imwrite('square_image.jpg', square_img)
        print("Square image saved as 'square_image.jpg'")
        completed = False

# Release the camera and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
