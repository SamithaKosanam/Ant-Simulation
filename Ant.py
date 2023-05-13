import Graphics
import drawing_utils
import math
import random
from Constants import *
import pygame


# Copied from https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame


class Ant:
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
        self.animation_time = 0
        self.animation_step = 0.2
        self.sense_predator = False
        self.saw_predator = False
        self.predator_time = 0
        self.food_removed = False

    def draw(self, screen):
        pos_1 = (self.x - ANT_PIVOT * ANT_LENGTH * math.cos(self.angle),
                 self.y - ANT_PIVOT * ANT_LENGTH * math.sin(self.angle))
        pos_2 = (self.x + (1 - ANT_PIVOT) * ANT_LENGTH * math.cos(self.angle),
                 self.y + (1 - ANT_PIVOT) * ANT_LENGTH * math.sin(self.angle))

        if BLOCK:
            drawing_utils.draw_line(screen, pos_1, pos_2, color=self.color, width=ANT_WIDTH)
        else:
            img = Graphics.ant_anim[int(self.animation_time)]
            facing_left = (math.pi / 2 < self.angle <= 3 * math.pi / 2)
            # if self.next_point is None:
            #     facing_left = (math.pi / 2 < self.angle <= 3 * math.pi / 2)
            # else:
            #     facing_left = (self.next_point[0] <= self.x)
            if facing_left:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x - ANT_LENGTH / 2, self.y - ANT_WIDTH / 2))
            if self.has_food:
                points = drawing_utils.get_polygon_points(5,
                                                          (self.x - ANT_LENGTH / 2, self.y) if facing_left else
                                                          (self.x + ANT_LENGTH / 2, self.y), radius=4)
                drawing_utils.draw_filled_polygon(screen, points, color=(255, 206, 132))

        # pygame.draw.circle(screen, drawing_utils.RED, pos_2, 2)

    def step(self):
        self.animation_time = (self.animation_time + self.animation_step) % 4
        if self.going_home:
            for idx in range(len(GRAPH)):
                point, _ = GRAPH[idx]
                if get_dist((self.x, self.y), point) < 5:
                    new_idx = AntHillDijkstra['prev'][idx]
                    if new_idx is None:
                        self.next_point = None
                        self.has_food = False
                        self.going_home = False
                        self.on_line = False
                        self.saw_predator = False
                    else:
                        self.next_point, _ = GRAPH[new_idx]
                        self.on_line = True
        if self.next_point is not None:
            dist = get_dist(self.next_point, (self.x, self.y))
            self.angle = math.acos((self.next_point[0] - self.x) / dist)
            if self.next_point[1] <= self.y:
                self.angle = 2 * math.pi - self.angle
            self.moving = True
            # self.x += MOVEMENT_SPEED * ((self.next_point[0] - self.x) / dist)
            # self.y += MOVEMENT_SPEED * ((self.next_point[1] - self.y) / dist)
        if self.moving:
            multiplier = 1
            if self.sense_predator:
                if self.next_point is not None:
                    multiplier = ANT_ESCAPING_SPEEDUP
                else:
                    multiplier = 0
                self.predator_time += 1
            self.x += MOVEMENT_SPEED * multiplier * math.cos(self.angle)
            self.y += MOVEMENT_SPEED * multiplier * math.sin(self.angle)
        else:
            if not self.turning:
                print('??')
            if self.has_food:
                print('???')
                if self.next_point is not None:
                    print('a')
                else:
                    print('b')
            if self.next_point is not None:
                print('????')
        if self.predator_time >= 2400:
            self.predator_time = 0
            self.sense_predator = False
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
        if not self.moving or self.next_point is not None:
            # Only check collisions when moving randomly
            return
        head = (int(round(self.x + (1 - ANT_PIVOT) * ANT_LENGTH * math.cos(self.angle))),
                int(round(self.y + (1 - ANT_PIVOT) * ANT_LENGTH * math.sin(self.angle))))
        in_window = 0 <= head[1] < len(limits) and 0 <= head[0] < len(limits[0])
        if not in_window or limits[head[1]][head[0]] == 1:
            found = False
            new_angle = 0
            while not found:
                new_angle = random.random() * math.pi * 2
                new_head = self.get_head(angle=new_angle)
                if 0 <= new_head[1] < len(limits) and 0 <= new_head[0] < len(limits[0]):
                    if limits[new_head[1]][new_head[0]] == 0:
                        found = True
            self.moving = False
            self.turn(new_angle)

    def get_head(self, angle=None):
        if angle is None:
            angle = self.angle
        head = (int(round(self.x + (1 - ANT_PIVOT) * ANT_LENGTH * math.cos(angle))),
                int(round(self.y + (1 - ANT_PIVOT) * ANT_LENGTH * math.sin(angle))))
        return head

    def return_food(self):
        self.has_food = True
        self.going_home = True
        self.next_point = get_nearest_point(self.x, self.y)

    def run_away(self, saw_predator=True):
        self.going_home = True
        self.sense_predator = True
        self.saw_predator = saw_predator
        self.next_point = get_nearest_point(self.x, self.y)

    def smell_pheromone(self, pheromone):
        if not self.sense_predator:
            self.angle = pheromone.angle

    def get_rect(self):
        return pygame.Rect((self.x - ANT_LENGTH / 2, self.y - ANT_WIDTH / 2), (ANT_LENGTH, ANT_WIDTH))

