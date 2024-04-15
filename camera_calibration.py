import cv2
import pygame
import numpy as np
import time
import os

def generate_checkerboard(width, height, checkerboard_size):
    """Generates a checkerboard pattern as a numpy array."""
    board = np.zeros((height, width), dtype=np.uint8)
    step_y, step_x = height // checkerboard_size[1], width // checkerboard_size[0]
    for y in range(checkerboard_size[1]):
        for x in range(checkerboard_size[0]):
            if (x + y) % 2:
                board[y * step_y:(y + 1) * step_y, x * step_x:(x + 1) * step_x] = 255
    return board

def project_checkerboard(checkerboard):
    """Projects a checkerboard pattern using Pygame."""
    # Position the window below the middle of the main monitor
    os.environ['SDL_VIDEO_WINDOW_POS'] = '960,2160'
    
    pygame.init()
    screen = pygame.display.set_mode((checkerboard.shape[1], checkerboard.shape[0]), pygame.NOFRAME)
    pygame.display.set_caption('Checkerboard Projection')
    # Convert checkerboard to Pygame surface
    surface = pygame.surfarray.make_surface(np.stack([checkerboard]*3, axis=-1))
    screen.blit(surface, (0, 0))
    pygame.display.flip()

def capture_image():
    """Captures an image from the default camera source."""
    cap = cv2.VideoCapture(0)  # Open the default camera
    if not cap.isOpened():
        print("Cannot open camera")
        return None
    # Allow some time for camera to warm up
    time.sleep(2)  # Adjust this delay based on your camera
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return None
    return frame

def main():
    # Parameters for the checkerboard
    checkerboard_size = (8, 6)  # dimensions in terms of number of squares
    projector_resolution = (800, 600)  # resolution to project checkerboard

    # Generate checkerboard pattern
    checkerboard = generate_checkerboard(projector_resolution[0], projector_resolution[1], checkerboard_size)
    
    # Project the checkerboard
    project_checkerboard(checkerboard)
    
    # Capture image from the camera
    image = capture_image()
    
    # Save the captured image
    if image is not None:
        cv2.imwrite('captured_checkerboard.jpg', image)
        print("Image saved successfully.")
    else:
        print("Failed to capture image.")

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
