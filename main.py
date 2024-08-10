import pygame
import sys
import random
from settings import *
from player import Player
from enemies import Enemy

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ordeal")

# Initialize fonts for timer and cooldown bar
font = pygame.font.SysFont(None, 36)

# Calculate the position for the dungeon room
start_x = (WIDTH - ROOM_SIZE) // 2
start_y = (HEIGHT - ROOM_SIZE) // 2

# Define the room boundaries
room_boundaries = get_room_boundaries(start_x, start_y)

# Initialize the player
player = Player((WIDTH - CHAR_SIZE) // 2, (HEIGHT - CHAR_SIZE) // 2)

# Initialize enemies
enemies = []

# Timer settings for enemy spawning
spawn_timer = pygame.time.get_ticks()  # Current time in milliseconds
spawn_interval = 3000  # Time in milliseconds between enemy spawns (3 seconds)

# Timer settings for increasing enemy attributes
attribute_timer = pygame.time.get_ticks()  # Current time in milliseconds
attribute_interval = (
    60000  # Time in milliseconds between attribute increases (1 minute)
)

# Cooldown settings
shoot_cooldown = 1000  # Cooldown period in milliseconds (e.g., 1 second)
last_shoot_time = pygame.time.get_ticks()  # Last time the player shot
cooldown_start_time = last_shoot_time  # Start cooldown time

# Timer settings for rest phase
rest_period = 30000  # 30 seconds rest period
rest_start_time = None  # Time when resting starts
resting = False  # Whether the player is in the resting state

# Initialize the game start time
start_time = pygame.time.get_ticks()

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    # Handle resting phase
    if resting:
        if current_time - rest_start_time >= rest_period:
            # End resting period
            resting = False

            spawn_timer = current_time  # Reset enemy spawn timer
            start_time = current_time  # Reset game start time
        else:
            # Draw the countdown bar
            cooldown_width = WIDTH // 10
            cooldown_height = 10
            cooldown_bar_x = WIDTH // 2 - cooldown_width // 2
            cooldown_bar_y = HEIGHT - cooldown_height - 30
            pygame.draw.rect(
                screen,
                WHITE,
                (cooldown_bar_x, cooldown_bar_y, cooldown_width, cooldown_height),
            )

            # Calculate remaining rest time
            rest_elapsed = current_time - rest_start_time
            rest_remaining = max(0, rest_period - rest_elapsed)
            rest_progress = (rest_period - rest_remaining) / rest_period
            pygame.draw.rect(
                screen,
                BLUE,
                (
                    cooldown_bar_x,
                    cooldown_bar_y,
                    cooldown_width * rest_progress,
                    cooldown_height,
                ),
            )

            # Draw the rest timer text
            rest_seconds = rest_remaining // 1000
            rest_text = f"{rest_seconds:02}"
            rest_surface = font.render(rest_text, True, WHITE)
            rest_text_rect = rest_surface.get_rect(
                center=(WIDTH // 2, cooldown_bar_y + cooldown_height // 2)
            )
            screen.blit(rest_surface, rest_text_rect)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle movement input
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_LEFT]:
        dx = -CHAR_SPEED
    if keys[pygame.K_RIGHT]:
        dx = CHAR_SPEED
    if keys[pygame.K_UP]:
        dy = -CHAR_SPEED
    if keys[pygame.K_DOWN]:
        dy = CHAR_SPEED

    # Handle tab key to switch target
    if keys[pygame.K_TAB]:
        player.switch_target(enemies)

    # Handle shooting
    if keys[pygame.K_q]:
        # Check cooldown
        if current_time - last_shoot_time >= shoot_cooldown:
            player.shoot()
            last_shoot_time = current_time
            cooldown_start_time = current_time

    # Move the player manually based on keyboard input
    player.move(dx, dy, room_boundaries)

    # Set the target and update target status
    player.set_target(enemies)

    # Update bullets and check collisions
    player.update_bullets(enemies)

    # Spawn new enemies periodically
    if not resting:
        if current_time - spawn_timer >= spawn_interval:
            new_x = random.randint(
                room_boundaries["LEFT"], room_boundaries["RIGHT"] - CHAR_SIZE
            )
            new_y = random.randint(
                room_boundaries["TOP"], room_boundaries["BOTTOM"] - CHAR_SIZE
            )
            enemies.append(Enemy(new_x, new_y))
            spawn_timer = current_time

    # Increase enemy attributes periodically
    if current_time - attribute_timer >= attribute_interval:
        for enemy in enemies:
            enemy.increase_attributes()
        attribute_timer = current_time

    # Check if one minute has passed to trigger the resting period
    if current_time - start_time >= 60000 and not resting:
        # Stop spawning and remove all enemies
        enemies.clear()
        resting = True
        rest_start_time = current_time

    # Clear the screen
    screen.fill(BLACK)

    # Draw the hollow dungeon room
    pygame.draw.rect(
        screen, WHITE, (start_x, start_y, ROOM_SIZE, ROOM_SIZE), WALL_THICKNESS
    )

    # Calculate elapsed time
    elapsed_time = current_time - start_time
    minutes = (elapsed_time // 60000) % 60
    seconds = (elapsed_time // 1000) % 60
    timer_text = f"{minutes:02}:{seconds:02}"
    timer_surface = font.render(timer_text, True, WHITE)
    timer_rect = timer_surface.get_rect(center=(WIDTH // 2, 30))
    screen.blit(timer_surface, timer_rect)

    # Draw the cooldown bar
    cooldown_width = WIDTH // 10
    cooldown_height = 10
    cooldown_bar_x = 10
    cooldown_bar_y = HEIGHT - cooldown_height - 10
    pygame.draw.rect(
        screen, WHITE, (cooldown_bar_x, cooldown_bar_y, cooldown_width, cooldown_height)
    )

    # Calculate remaining cooldown
    cooldown_elapsed = current_time - cooldown_start_time
    cooldown_remaining = max(0, shoot_cooldown - cooldown_elapsed)
    cooldown_progress = (shoot_cooldown - cooldown_remaining) / shoot_cooldown
    pygame.draw.rect(
        screen,
        BLUE,
        (
            cooldown_bar_x,
            cooldown_bar_y,
            cooldown_width * cooldown_progress,
            cooldown_height,
        ),
    )

    # Move and draw enemies
    for enemy in enemies:
        enemy.move_towards(player, room_boundaries)
        enemy.draw(screen)

    # Draw the player and its bullets
    player.draw(screen)

    # Draw the player experience and level bar
    player.draw_experience_bar(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(30)
