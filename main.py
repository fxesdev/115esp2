import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1260, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("115esp2 drawer")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define constants
PIXEL_SIZE = 12
SPRITE_WIDTH = 96
SPRITE_HEIGHT = 8

# Create sprite data with every 8th character set to 1
sprite_data = [[0] * SPRITE_WIDTH for _ in range(SPRITE_HEIGHT)]
for row in sprite_data:
    for i in range(7, SPRITE_WIDTH, 8):
        row[i] = 1

# Function to draw the sprite
def draw_sprite():
    for y in range(SPRITE_HEIGHT):
        for x in range(SPRITE_WIDTH):
            if y == 3 and 32 <= x <= 47:  # Check if pixel is in the specified range
                color = RED if sprite_data[y][x] == 1 else BLACK
            else:
                color = WHITE if sprite_data[y][x] == 1 else BLACK
            pygame.draw.rect(screen, color, (x * PIXEL_SIZE, y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

# Function to translate sprite data to hexadecimal
def translate_to_hex(line_wrap=32):
    hex_data = []
    for row in sprite_data:
        binary_string = ''.join(str(bit) for bit in row)
        hex_string = hex(int(binary_string, 2))[2:].zfill(SPRITE_WIDTH // 4)
        hex_data.extend(hex_string[i:i+2] + " " for i in range(0, len(hex_string), 2))
    # Update specific indices with the desired values
    hex_data[40:42] = ["06 ", "75 ", "31 "]
    
    # Add line wrap
    hex_data_wrapped = []
    for i in range(0, len(hex_data), line_wrap):
        hex_data_wrapped.append(''.join(hex_data[i:i+line_wrap]))
    
    return hex_data_wrapped

# Main loop
running = True
drawing = False
output = []

while running:
    screen.fill(BLACK)
    draw_sprite()

    # Display hexadecimal representation
    font = pygame.font.SysFont(None, 24)
    hex_data = translate_to_hex()
    for i, row in enumerate(hex_data):
        text = font.render(row, True, WHITE)
        screen.blit(text, (20, SPRITE_HEIGHT * PIXEL_SIZE + 20 + i * 30))
        if 41 <= i <= 44:
            output.append(row)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                x //= PIXEL_SIZE
                y //= PIXEL_SIZE
                if 0 <= x < SPRITE_WIDTH and 0 <= y < SPRITE_HEIGHT:
                    sprite_data[y][x] = 1 - sprite_data[y][x]  # Invert the pixel color

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

