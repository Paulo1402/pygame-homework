import pygame
import random
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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

# Fonts
font = pygame.font.SysFont(None, 36)
name_font = pygame.font.SysFont(None, 24)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")

# Game state
game_over = False
score = 0

def run_game():
    global score, game_over
    
    pygame.mixer.music.load("assets/background.mp3")  # background music
    pygame.mixer.music.play(-1)  # loop forever
    
    hit_sound = pygame.mixer.Sound("assets/bump.wav")  # when the player is hit
    
    # Reset game state
    score = 0
    game_over = False

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
        score += 1
        BLOCK_SPEED = 5 + score // 500  # Increase speed every 500 points

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
                hit_sound.play()
                pygame.mixer.music.stop()
            
                game_over = True
                break  # exit for loop

        # Drawing
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, player)
        for block in blocks:
            pygame.draw.rect(screen, BLUE, block)
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw name and RU
        name = name_font.render("Paulo Cesar Benatto Junior", True, BLACK)
        ru = name_font.render("RU: 4575578", True, BLACK)
        screen.blit(name, (WIDTH - 230, 10))
        screen.blit(ru, (WIDTH - 230, 40))
        
        # Check for game over
        if game_over:
            running = False
            continue

        pygame.display.flip()


while True:
    run_game()
    
    if game_over:
        # Game Over screen
        pygame.mixer.music.load("assets/game_over.mp3")
        pygame.mixer.music.play(-1)
        
        screen.fill(WHITE)
        msg = font.render("Game Over!", True, RED)
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(msg, msg_rect)

        score_msg = font.render(f"Final Score: {score}", True, BLACK)
        score_rect = score_msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(score_msg, score_rect)
        
        msg = font.render("Press R to Restart or Q to Quit", True, BLACK)
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        screen.blit(msg, msg_rect)

        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False  # Restart
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
    else:
        # If the game is not over, it means the player has quit the game so we exit the loop
        pygame.quit()
        sys.exit()
