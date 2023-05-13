
import Graphics
import drawing_utils
import math
import random
from Constants import *
import pygame


# Copied from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame


class Predator:
    def __init__(self, x, y, angle: float = 0):
        self.x = x
        self.y = y
        self.angle = angle
        self.target_angle = None
        self.turning = False
        self.turning_direction = None
        self.moving = True
        self.color = drawing_utils.BLACK
        self.has_food = False
        self.going_home = False
        self.next_point = None
        self.on_line = False


    def draw(self, screen):
        pos_1 = (self.x - PREDATOR_PIVOT * PREDATOR_LENGTH * math.cos(self.angle),
                 self.y - PREDATOR_PIVOT * PREDATOR_LENGTH * math.sin(self.angle))
        pos_2 = (self.x + (1 - PREDATOR_PIVOT) * PREDATOR_LENGTH * math.cos(self.angle),
                 self.y + (1 - PREDATOR_PIVOT) * PREDATOR_LENGTH * math.sin(self.angle))

        if BLOCK:
            drawing_utils.draw_line(screen, pos_1, pos_2, color=self.color, width=PREDATOR_WIDTH)
        else:
            img = Graphics.predator_img
            facing_left = (math.pi / 2 < self.angle <= 3 * math.pi / 2)
            # if self.next_point is None:
            #     facing_left = (math.pi / 2 < self.angle <= 3 * math.pi / 2)
            # else:
            #     facing_left = (self.next_point[0] <= self.x)
            if facing_left:
                img = pygame.transform.flip(img, True, False)
            img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x - PREDATOR_LENGTH / 2, self.y - PREDATOR_WIDTH / 2))
           
        # pygame.draw.circle(screen, drawing_utils.RED, pos_2, 2)

    def step(self):
        #if self.going_home:
        #    for idx in range(len(GRAPH)):
        #        point, _ = GRAPH[idx]
        #        if get_dist((self.x, self.y), point) < 5:
        #            new_idx = AntHillDijkstra['prev'][idx]
        #            if new_idx is None:
        #                self.next_point = None
        #                self.has_food = False
        #                self.going_home = False
        #                self.on_line = False
        #            else:
        #                self.next_point, _ = GRAPH[new_idx]
        #                self.on_line = True
        if self.next_point is not None:
            dist = get_dist(self.next_point, (self.x, self.y))
            self.angle = math.acos((self.next_point[0] - self.x) / dist)
            if self.next_point[1] <= self.y:
                self.angle = 2 * math.pi - self.angle
            # self.x += MOVEMENT_SPEED * ((self.next_point[0] - self.x) / dist)
            # self.y += MOVEMENT_SPEED * ((self.next_point[1] - self.y) / dist)
        if self.moving:
            self.x += MOVEMENT_SPEED * math.cos(self.angle)
            self.y += MOVEMENT_SPEED * math.sin(self.angle)
        if self.turning:
            self.angle += (self.turning_direction * TURNING_SPEED)
            self.angle %= math.pi * 2
            if abs(self.target_angle - self.angle) <= TURNING_SPEED:
                self.angle = self.target_angle
                self.turning = False
                self.moving = True

    def turn(self, angle):
        self.target_angle = angle
        self.turning = True
        if (self.target_angle - self.angle) % (math.pi * 2) <= math.pi:
            self.turning_direction = 1
        else:
            self.turning_direction = -1

    def collision(self, limits):
        if not self.moving:
            # Only check collisions when moving
            return
        head = self.get_head()
        in_window = 0 <= head[1] < len(limits) and 0 <= head[0] < len(limits[0])
        if not in_window or limits[head[1]][head[0]] == 1:
            found = False
            new_angle = 0
            while not found:
                new_angle = random.random() * math.pi * 2
                new_head = (int(round(self.x + (1 - PREDATOR_PIVOT) * PREDATOR_LENGTH * math.cos(new_angle))),
                            int(round(self.y + (1 - PREDATOR_PIVOT) * PREDATOR_LENGTH * math.sin(new_angle))))
                if 0 <= new_head[1] < len(limits) and 0 <= new_head[0] < len(limits[0]):
                    if limits[new_head[1]][new_head[0]] == 0:
                        found = True
            self.moving = False
            self.turn(new_angle)

    def get_head(self):
        head = (int(round(self.x + (1 - PREDATOR_PIVOT) * PREDATOR_WIDTH * math.cos(self.angle))),
                int(round(self.y + (1 - PREDATOR_PIVOT) * PREDATOR_WIDTH * math.sin(self.angle))))
        return head

    def get_rect(self):
        return pygame.Rect((self.x - PREDATOR_LENGTH/2, self.y - PREDATOR_WIDTH/2), (PREDATOR_LENGTH, PREDATOR_WIDTH))

    def get_detection_rect(self):
        rect = self.get_rect()
        inflation = min(PREDATOR_WIDTH, PREDATOR_LENGTH) * (PREDATOR_DETECTION - 1)
        return rect.inflate(inflation, inflation)
