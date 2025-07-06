import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BLOCK_WIDTH, BLOCK_HEIGHT = 50, 50
PLAYER_SPEED = 5
BLOCK_SPEED = 5
SPAWN_INTERVAL = 30  # frames

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Clock
clock = pygame.time.Clock()

# Player setup
player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)

# Blocks setup
blocks = []
frame_count = 0

# Game loop
running = True
while running:
    clock.tick(60)  # 60 FPS
    frame_count += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += PLAYER_SPEED

    # Spawn new block
    if frame_count % SPAWN_INTERVAL == 0:
        block_x = random.randint(0, WIDTH - BLOCK_WIDTH)
        new_block = pygame.Rect(block_x, 0, BLOCK_WIDTH, BLOCK_HEIGHT)
        blocks.append(new_block)

    # Move blocks
    for block in blocks:
        block.y += BLOCK_SPEED

    # Remove off-screen blocks
    blocks = [block for block in blocks if block.y < HEIGHT]

    # Check collision
    for block in blocks:
        if player.colliderect(block):
            print("Game Over!")
            running = False

    # Drawing
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player)
    for block in blocks:
        pygame.draw.rect(screen, BLUE, block)
    pygame.display.flip()

pygame.quit()
sys.exit()
