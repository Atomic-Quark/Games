import pygame
import random
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 600, 700
PLAYER_SIZE = 50
RAY_WIDTH, RAY_HEIGHT = 10, 60  # Thin and tall rays
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BULLET_WIDTH, BULLET_HEIGHT = 5, 20
LIVES = 3  # Player starts with 3 lives

# Load Assets
SPACE_BG = pygame.image.load("space_bg.jpg")  # Load space-themed background
SPACE_BG = pygame.transform.scale(SPACE_BG, (WIDTH, HEIGHT))  # Auto-fit background
PLAYER_SHIP = pygame.image.load("spaceship.png")  # Load spaceship image
PLAYER_SHIP = pygame.transform.scale(PLAYER_SHIP, (PLAYER_SIZE, PLAYER_SIZE))
HEART_IMG = pygame.image.load("heart.png")  # Load heart image for lives
HEART_IMG = pygame.transform.scale(HEART_IMG, (30, 30))

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge Challenge")

# Player setup
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE - 10
player_speed = 10  # Increased speed for faster movement

# Enemy Rays Setup
rays = []
bullets = []
score = 0
lives = LIVES
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
paused = False
score_history = []

# Difficulty Levels
difficulty_settings = {
    "Easy": 3,
    "Medium": 5,
    "Hard": 7,
    "Insane": 10
}
difficulty = "Medium"
RAY_SPEED = difficulty_settings[difficulty]

# Performance Graph
def show_performance_graph():
    plt.plot(score_history, marker='o', linestyle='-', color='b', label='Score Progress')
    plt.xlabel("Attempts")
    plt.ylabel("Score")
    plt.title("Player Performance Over Time")
    plt.legend()
    plt.show()

# Menu Function
def show_menu():
    global difficulty, RAY_SPEED, lives, score_history
    menu = True
    while menu:
        screen.fill(BLACK)
        title = font.render("Space Dodge Challenge", True, WHITE)
        screen.blit(title, (WIDTH // 4, 50))
        
        start_text = font.render("Press S to Start", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {difficulty} (Press D to Change)", True, WHITE)
        exit_text = font.render("Press Q to Quit", True, WHITE)
        
        screen.blit(start_text, (WIDTH // 4, 150))
        screen.blit(difficulty_text, (WIDTH // 4, 200))
        screen.blit(exit_text, (WIDTH // 4, 250))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    lives = LIVES  # Reset lives
                    menu = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_d:
                    difficulty = next(iter(difficulty_settings.keys())) if difficulty == "Insane" else list(difficulty_settings.keys())[list(difficulty_settings.keys()).index(difficulty) + 1]
                    RAY_SPEED = difficulty_settings[difficulty]

# Pause Function
def pause_game():
    global paused
    paused = True
    while paused:
        screen.fill(BLACK)
        pause_text = font.render("Game Paused - Press P to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH // 6, HEIGHT // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

# Game Loop
show_menu()
running = True
while running:
    screen.blit(SPACE_BG, (0, 0))  # Set space-themed background
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause_game()
            if event.key == pygame.K_SPACE:
                bullets.append([player_x + PLAYER_SIZE // 2 - BULLET_WIDTH // 2, player_y])
    
    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += player_speed
    
    # Spawn rays (enemies)
    if random.randint(1, 20) == 1:
        rays.append([random.randint(0, WIDTH - RAY_WIDTH), 0])
    
    # Move rays
    for ray in rays[:]:
        ray[1] += RAY_SPEED
        if ray[1] > HEIGHT:
            rays.remove(ray)
            score += 1
            if score % 10 == 0:
                RAY_SPEED += 1  # Increase difficulty
    
    # Move bullets
    for bullet in bullets[:]:
        bullet[1] -= 10
        if bullet[1] < 0:
            bullets.remove(bullet)
    
    # Check collisions
    for ray in rays[:]:
        if (player_x < ray[0] < player_x + PLAYER_SIZE or player_x < ray[0] + RAY_WIDTH < player_x + PLAYER_SIZE) and \
           (player_y < ray[1] < player_y + PLAYER_SIZE or player_y < ray[1] + RAY_HEIGHT < player_y + PLAYER_SIZE):
            lives -= 1
            rays.remove(ray)
            if lives == 0:
                score_history.append(score)
                show_performance_graph()
                show_menu()
                rays.clear()
                bullets.clear()
                player_x = WIDTH // 2 - PLAYER_SIZE // 2
                RAY_SPEED = difficulty_settings[difficulty]  # Reset difficulty
                score = 0
                lives = LIVES
        
    # Draw spaceship
    screen.blit(PLAYER_SHIP, (player_x, player_y))
    
    # Draw enemy rays
    for ray in rays:
        pygame.draw.rect(screen, RED, (ray[0], ray[1], RAY_WIDTH, RAY_HEIGHT))
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], BULLET_WIDTH, BULLET_HEIGHT))
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw lives
    for i in range(lives):
        screen.blit(HEART_IMG, (WIDTH - (i + 1) * 40, 10))
    
    # Refresh screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
