import pygame
import sys
import os

WIDTH, HEIGHT = 1920, 1080

# Set the position of the window to the third monitor, directly below the main monitor
os.environ['SDL_VIDEO_WINDOW_POS'] = '960,2160'

# Initialize Pygame
pygame.init()

# Set the size of the projector display and make it fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # Adjust to your projector's resolution

# Set background color
screen.fill((0, 0, 0))  # White background

# Grid settings
grid_color = (255, 255, 255)  # Black grid lines
spacing = 8  # Adjust this value based on your calibration for 1 cm grid lines

# Draw the grid
for x in range(0, WIDTH, spacing):  # Adjust the range to your projector's dimensions
    pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT))
for y in range(0, HEIGHT, spacing):
    pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y))

# Update the display
pygame.display.flip()

# Run until closed
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
except Exception as e:
    pygame.quit()
    print(str(e))
