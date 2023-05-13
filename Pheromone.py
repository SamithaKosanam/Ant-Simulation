from Constants import *
import pygame


class Pheromone:
    def __init__(self, x, y, angle, predator):
        self.x = x
        self.y = y
        self.angle = angle
        self.predator = predator
        self.time = 0
        self.active = True

    def draw(self, screen):
        if self.time < PHEROMONE_LIFE:
            if self.predator is True:
                pygame.draw.circle(screen, (186, 11, 11), (self.x, self.y), PHEROMONE_RADIUS)
            else:
                pygame.draw.circle(screen, (123, 255, 96), (self.x, self.y), PHEROMONE_RADIUS)
        else:
            self.active = False
        self.time = self.time + 1
        # min_x, min_y = (self.x - PHEROMONE_RADIUS, self.y - PHEROMONE_RADIUS)
        # max_x, max_y = (self.x + PHEROMONE_RADIUS, self.y + PHEROMONE_RADIUS)
        # target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        # surface = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        # pygame.draw.circle(surface, (0, 255, 0, 255), (self.x, self.y), PHEROMONE_RADIUS)
        # screen.blit(surface, target_rect)
