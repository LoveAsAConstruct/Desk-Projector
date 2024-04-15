import pygame
import sys
import os

# Set the resolution of the grid
WIDTH, HEIGHT = 1920, 1080

# Number of cells in the grid
GRID_SIZE = 8

# Set the position of the window to the third monitor, directly below the main monitor
os.environ['SDL_VIDEO_WINDOW_POS'] = '960,2160'

# Initialize Pygame
pygame.init()

# Set the size of the projector display and make it fullscreen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)  # Adjust to your projector's resolution

# Calculate the size of each cell
cell_width = WIDTH // GRID_SIZE
cell_height = HEIGHT // GRID_SIZE

# Font for numbering
pygame.font.init()  # You need to call this before using fonts
font_size = min(cell_width, cell_height) // 4  # Size of the font relative to cell size
font = pygame.font.Font(None, font_size)

# Draw the grid and number each cell
number = 1
for row in range(GRID_SIZE):
    for col in range(GRID_SIZE):
        # Alternate colors
        color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
        rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
        pygame.draw.rect(screen, color, rect)
        
        # Text rendering - render the number in black or white depending on the background
        text_color = (0, 0, 0) if color == (255, 255, 255) else (255, 255, 255)
        text_surface = font.render(str(number), True, text_color)
        text_rect = text_surface.get_rect(center=(col * cell_width + cell_width // 2, row * cell_height + cell_height // 2))
        screen.blit(text_surface, text_rect)
        
        number += 1  # Increment the number for the next square

# Update the display
pygame.display.flip()

# Run until closed
try:
    while True:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                sys.exit()
except Exception as e:
    pygame.quit()
    print(str(e))
