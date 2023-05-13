import pygame
import Graphics
from Constants import *
import math


class Food:
    def __init__(self, x, y, ):
        self.x = x
        self.y = y
        self.life = FOOD_LIFE

    def draw(self, screen):
        if self.life >= (3*FOOD_LIFE)/4:
            screen.blit(Graphics.food_img, (self.x - 50 / 2, self.y - 50 / 2))
        elif self.life >= FOOD_LIFE/2:
            screen.blit(Graphics.food_one, (self.x - 50 / 2, self.y - 50 / 2))
        elif self.life >= FOOD_LIFE/4:
            screen.blit(Graphics.food_two, (self.x - 50 / 2, self.y - 50 / 2))
        else:
            screen.blit(Graphics.food_three, (self.x - 50 / 2, self.y - 50 / 2))

    def get_rect(self):
        return pygame.Rect((self.x - 50/2, self.y - 50/2), (50, 50))