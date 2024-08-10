import pygame
from settings import *


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = CHAR_SIZE
        self.color = RED
        self.initial_health = 5
        self.health = self.initial_health
        self.speed = BLUE_SQUARE_SPEED
        self.is_targeted = False

    def move_towards(self, player, room_boundaries):
        # Move towards the player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        dx /= distance
        dy /= distance
        self.x += dx * self.speed
        self.y += dy * self.speed
        # Ensure the enemy stays within the room boundaries
        self.x = max(
            room_boundaries["LEFT"], min(self.x, room_boundaries["RIGHT"] - self.size)
        )
        self.y = max(
            room_boundaries["TOP"], min(self.y, room_boundaries["BOTTOM"] - self.size)
        )

    def check_collision_with_player(self, player):
        return (
            self.x < player.x + player.size
            and self.x + self.size > player.x
            and self.y < player.y + player.size
            and self.y + self.size > player.y
        )

    def draw(self, screen):
        # Draw the enemy
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        # Draw the health bar (White outline with red fill)
        health_bar_width = self.size
        health_bar_height = 5
        pygame.draw.rect(
            screen, WHITE, (self.x, self.y - 10, health_bar_width, health_bar_height)
        )
        pygame.draw.rect(
            screen,
            RED,
            (
                self.x,
                self.y - 10,
                (self.health / self.initial_health) * health_bar_width,
                health_bar_height,
            ),
        )

        # Draw the outline if targeted
        if self.is_targeted:
            pygame.draw.rect(
                screen, WHITE, (self.x, self.y, self.size, self.size), 2
            )  # 2 is the thickness of the outline

    def increase_attributes(self):
        # Increase health and speed
        self.initial_health = int(self.initial_health * 1.1)  # Increase health by 10%
        self.health = int(self.health * 1.1)  # Update current health
        self.speed = self.speed * 1.1  # Increase speed by 10%
