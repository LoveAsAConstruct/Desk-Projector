import cv2
import numpy as np

# Parameters
checkerboard_size = (6, 9)  # Number of inner corners in the checkerboard (cols, rows)
square_size = 25  # Size of a square in your units (e.g., mm)

# Generate checkerboard pattern
def generate_checkerboard(width, height, checkerboard_size):
    board = np.zeros((height, width), dtype=np.uint8)
    step_y, step_x = height // checkerboard_size[1], width // checkerboard_size[0]
    white = False
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            if white:
                board[y:y + step_y, x:x + step_x] = 255
            white = not white
        if checkerboard_size[0] % 2 == 0:
            white = not white
    return board

# Load or capture an image from the camera
def load_image(file_path):
    return cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Find corners in the image
def find_corners(img, checkerboard_size):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    ret, corners = cv2.findChessboardCorners(img, checkerboard_size, None)
    if ret:
        corners2 = cv2.cornerSubPix(img, corners, (11, 11), (-1, -1), criteria)
        return corners2
    return None

# Calculate homography
def calculate_homography(projector_points, image_points):
    H, _ = cv2.findHomography(projector_points, image_points, cv2.RANSAC)
    return H

# Main function to execute the calibration
def perform_calibration(image_path):
    # Generate the pattern
    projector_image = generate_checkerboard(800, 600, checkerboard_size)  # Dimensions of your projector's resolution
    cv2.imwrite("checkerboard_pattern.png", projector_image)  # Save or project this image

    # Load the camera image
    camera_image = load_image(image_path)
    
    # Detect corners
    detected_corners = find_corners(camera_image, checkerboard_size)
    if detected_corners is None:
        print("Corners could not be detected.")
        return None

    # Projector points (assuming top-left corner is (0,0))
    projector_points = np.zeros((checkerboard_size[0]*checkerboard_size[1], 3), dtype=np.float32)
    projector_points[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2) * square_size

    # Compute homography
    H = calculate_homography(projector_points[:, :2], detected_corners)
    print("Homography Matrix:\n", H)
    return H

# Example usage
homography = perform_calibration('path_to_your_image.jpg')
