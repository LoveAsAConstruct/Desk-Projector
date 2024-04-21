import cv2
import numpy as np
import pickle

# Global variables to store selected points
selected_camera_points = []
selected_projector_points = []

# Mouse callback function for camera image
def select_camera_point(event, x, y, flags, param):
    global selected_camera_points
    
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_camera_points.append((x, y))

# Mouse callback function for projector image
def select_projector_point(event, x, y, flags, param):
    global selected_projector_points
    
    if event == cv2.EVENT_LBUTTONDOWN:
        selected_projector_points.append((x, y))

# Load the camera image
camera_img = cv2.imread(r'C:\Users\isaia\Documents\Desk Projector\calibration_images\camera\WIN_20240420_23_02_07_Pro.jpg')
clone_camera = camera_img.copy()

# Create a window for camera image and set mouse callback
cv2.namedWindow('Select Camera Points')
cv2.setMouseCallback('Select Camera Points', select_camera_point)

while True:
    # Display the camera image and selected points
    temp_camera_img = clone_camera.copy()
    for point in selected_camera_points:
        cv2.circle(temp_camera_img, point, 5, (0, 255, 0), -1)
    cv2.imshow('Select Camera Points', temp_camera_img)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        selected_camera_points = []
        clone_camera = camera_img.copy()
    elif key == ord('n'):
        break

cv2.destroyAllWindows()

# Load the projector image
projector_img = cv2.imread(r'calibration_images\projector\Screenshot 2024-04-15 213926.png')
clone_projector = projector_img.copy()

# Create a window for projector image and set mouse callback
cv2.namedWindow('Select Projector Points')
cv2.setMouseCallback('Select Projector Points', select_projector_point)

while True:
    # Display the projector image and selected points
    temp_projector_img = clone_projector.copy()
    for point in selected_projector_points:
        cv2.circle(temp_projector_img, point, 5, (0, 255, 0), -1)
    cv2.imshow('Select Projector Points', temp_projector_img)
    
    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        selected_projector_points = []
        clone_projector = projector_img.copy()
    elif key == ord('q'):
        break

cv2.destroyAllWindows()

# Convert selected points to numpy arrays
camera_grid_corners = np.array(selected_camera_points, dtype=np.float32)
projector_grid_corners = np.array(selected_projector_points, dtype=np.float32)

# Calculate the perspective transformation matrix
if len(camera_grid_corners) == 4 and len(projector_grid_corners) == 4:
    perspective_matrix = cv2.getPerspectiveTransform(camera_grid_corners, projector_grid_corners)

    # Save the perspective transformation matrix to a file
    with open('perspective_matrix.pkl', 'wb') as f:
        pickle.dump(perspective_matrix, f)

    # Apply the perspective transformation to the camera image
    projected_camera_img = cv2.warpPerspective(camera_img, perspective_matrix, (projector_img.shape[1], projector_img.shape[0]))

    # Display the original camera image and the projected camera image
    cv2.imshow('Original Camera Image', camera_img)
    cv2.imshow('Projected Camera Image', projected_camera_img)
    cv2.imshow('Projector Image', projector_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Please select exactly four points on both the camera and projector images.")
