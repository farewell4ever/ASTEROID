import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # For spaceship
RED = (255, 0, 0)    # For meteors

# Player settings
player_width = 30
player_height = 30
player_speed = 7

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 9

# Enemy settings (meteors)
enemy_radius = 20
enemy_speed = 2

# Game variables
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
bullets = []
enemies = []
score = 0

# Timer for enemy respawn
last_respawn_time = time.time()
respawn_interval = random.uniform(3, 5)

# Bullet cooldown settings
last_bullet_time = time.time()
bullet_cooldown = 0.2

# Function to create a new enemy (meteor)
def create_enemy(num_enemies):
    for _ in range(num_enemies):
        enemy_x = random.randint(enemy_radius, WIDTH - enemy_radius)
        enemy_y = random.randint(50, 150)
        enemies.append([enemy_x, enemy_y])

# Initial enemy creation
for _ in range(5):
    create_enemy(1)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Bullet firing logic
    current_time = time.time()
    if keys[pygame.K_SPACE] and (current_time - last_bullet_time) > bullet_cooldown:
        bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
        last_bullet_time = current_time

    # Update bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            running = False  # Game over if an enemy reaches the bottom

    # Check for collisions
    for bullet in bullets:
        for enemy in enemies:
            if (bullet[0] > enemy[0] - enemy_radius and bullet[0] < enemy[0] + enemy_radius) and (bullet[1] > enemy[1] - enemy_radius and bullet[1] < enemy[1] + enemy_radius):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

    # Respawn enemies
    if current_time - last_respawn_time > respawn_interval:
        if random.choice([True, False]):
            create_enemy(random.randint(2, 4))
        else:
            create_enemy(1)
        last_respawn_time = current_time
        respawn_interval = random.uniform(3, 5)

    # Draw player (spaceship)
    pygame.draw.polygon(screen, GREEN, [
        (player_x + player_width // 2, player_y),
        (player_x, player_y + player_height),
        (player_x + player_width, player_y + player_height)
    ])

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw enemies (meteors as circles)
    for enemy in enemies:
        pygame.draw.circle(screen, RED, (enemy[0], enemy[1]), enemy_radius)

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()