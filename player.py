import pygame
from settings import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CHAR_SIZE
        self.color = GREEN
        self.bullets = []
        self.target = None
        self.last_shoot_time = pygame.time.get_ticks()
        self.shoot_cooldown = 500  # milliseconds
        self.current_target_index = 0
        # Experience and level
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 5
        # Gold and skill points
        self.gold = 0
        self.skill_points = 0

    def move(self, dx, dy, room_boundaries):
        self.x += dx
        self.y += dy
        # Ensure the player stays within the room boundaries
        self.x = max(
            room_boundaries["LEFT"], min(self.x, room_boundaries["RIGHT"] - self.size)
        )
        self.y = max(
            room_boundaries["TOP"], min(self.y, room_boundaries["BOTTOM"] - self.size)
        )

    def switch_target(self, enemies):
        if enemies:
            self.current_target_index = (self.current_target_index + 1) % len(enemies)
            self.target = enemies[self.current_target_index]

    def set_target(self, enemies):
        if enemies:
            self.target = enemies[self.current_target_index]

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shoot_cooldown:
            if self.target:
                bullet_x = self.x + self.size // 2
                bullet_y = self.y
                dx = (self.target.x + self.target.size // 2 - bullet_x) / 10
                dy = (self.target.y + self.target.size // 2 - bullet_y) / 10
                self.bullets.append([bullet_x, bullet_y, dx, dy])
                self.last_shoot_time = current_time

    def update_bullets(self, enemies):
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            # Check collision with enemies
            for enemy in enemies[:]:
                if (
                    bullet[0] >= enemy.x
                    and bullet[0] <= enemy.x + enemy.size
                    and bullet[1] >= enemy.y
                    and bullet[1] <= enemy.y + enemy.size
                ):
                    enemy.health -= 1  # Bullet deals 1 damage
                    self.bullets.remove(bullet)
                    if enemy.health <= 0:
                        enemies.remove(enemy)
                        self.gain_experience(3)  # Gain experience per enemy kill
                        self.gold += 1  # Gain 1 gold per enemy kill
                    break

    def gain_experience(self, amount):
        self.experience += amount
        if self.experience >= self.experience_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(
            self.experience_to_next_level * 1.5
        )  # Example: Increase the next level's experience requirement
        self.skill_points += 1  # Gain 1 skill point per level up

    def draw(self, screen):
        # Draw the player
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # Draw the bullets
        for bullet in self.bullets:
            pygame.draw.rect(
                screen, RED, (bullet[0], bullet[1], 5, 5)
            )  # Bullet size is 5x5

        # Draw target outline
        if self.target:
            pygame.draw.rect(
                screen,
                WHITE,
                (self.target.x, self.target.y, self.target.size, self.target.size),
                2,
            )

    def draw_experience_bar(self, screen):
        font = pygame.font.SysFont(None, 24)

        # Draw vertical experience bar on the left side
        bar_width = 20
        bar_height = 150
        bar_x = 10
        bar_y = (HEIGHT - bar_height) // 2
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Draw experience progress
        progress_height = (self.experience / self.experience_to_next_level) * bar_height
        pygame.draw.rect(
            screen,
            GREEN,
            (bar_x, bar_y + bar_height - progress_height, bar_width, progress_height),
        )

        # Draw level, experience, and gold text
        level_text = f"{self.level}"
        exp_text = f"EXP: {self.experience}/{self.experience_to_next_level}"
        gold_text = f"Gold: {self.gold}"
        skill_points_text = f"SP: {self.skill_points}"
        font = pygame.font.SysFont(None, 24)
        level_surface = font.render(level_text, True, WHITE)
        exp_surface = font.render(exp_text, True, WHITE)
        gold_surface = font.render(gold_text, True, YELLOW)
        skill_points_surface = font.render(
            skill_points_text, True, CYAN
        )  # Assuming CYAN is defined

        exp_surface = pygame.transform.rotate(exp_surface, 90)

        screen.blit(exp_surface, (bar_x, bar_y - 90))
        screen.blit(level_surface, (bar_x, bar_y + bar_height + 10))
        screen.blit(gold_surface, (bar_x, bar_y - 270))
        screen.blit(skill_points_surface, (bar_x, bar_y - 250))
