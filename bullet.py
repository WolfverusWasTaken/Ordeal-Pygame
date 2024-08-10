# bullet.py
import pygame
from settings import *


class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = 5  # Size of the bullet
        self.color = RED  # Color of the bullet
        self.speed = 15  # Speed of the bullet

        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        self.dx = (dx / distance) * self.speed
        self.dy = (dy / distance) * self.speed

    def move(self):
        # Update the bullet's position
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        # Draw the bullet on the screen
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def check_collision(self, enemy):
        # Check if the bullet collides with an enemy
        return (
            self.x < enemy.x + enemy.size
            and self.x + self.size > enemy.x
            and self.y < enemy.y + enemy.size
            and self.y + self.size > enemy.y
        )
