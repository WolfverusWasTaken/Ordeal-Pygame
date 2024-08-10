import pygame
from settings import *


class Gold:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, GOLD_SIZE, GOLD_SIZE)
        self.color = YELLOW

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
