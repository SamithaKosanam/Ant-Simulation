import pygame
import pygame.gfxdraw
import math
from math import cos, sin

BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (147, 112, 219), (160, 82, 45), (255, 105, 180)]


def draw_arrow(screen, pos1, pos2, color=BLACK, width=10):
    draw_line(screen, pos1, pos2, color, width)
    magnitude = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    direction = ((pos2[0] - pos1[0]) / magnitude, (pos2[1] - pos1[1]) / magnitude)
    perpendicular = (direction[1], -direction[0])
    base = (pos2[0] - 3 * direction[0] * width, pos2[1] - 3 * direction[1] * width)
    point1 = (base[0] + 1.2 * perpendicular[0] * width, base[1] + 1.2 * perpendicular[1] * width)
    point2 = (base[0] - 1.2 * perpendicular[0] * width, base[1] - 1.2 * perpendicular[1] * width)

    pygame.gfxdraw.aapolygon(screen, [pos2, point1, point2], color)
    pygame.gfxdraw.filled_polygon(screen, [pos2, point1, point2], color)


def draw_filled_polygon(screen, points, color):
    for i in range(len(points)):
        points[i][0] = round(points[i][0])
        points[i][1] = round(points[i][1])
    pygame.gfxdraw.aapolygon(screen, points, color)
    pygame.gfxdraw.filled_polygon(screen, points, color)


def draw_filled_circle(screen, center, radius, interior_color, outline_color=BLACK, width=0):
    radius = round(radius)
    x = round(center[0])
    y = round(center[1])
    pygame.gfxdraw.aacircle(screen, x, y, radius, outline_color)
    pygame.gfxdraw.filled_circle(screen, x, y, radius, outline_color)
    pygame.gfxdraw.aacircle(screen, x, y, radius - width, interior_color)
    pygame.gfxdraw.filled_circle(screen, x, y, radius - width, interior_color)


def draw_line(screen, pos1, pos2, color, width):
    # https://stackoverflow.com/a/30599392
    center = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2)

    magnitude = math.sqrt((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2)
    angle = math.atan2(pos2[1] - pos1[1], pos2[0] - pos1[0])
    line_length = magnitude

    ul = (center[0] + (line_length / 2.) * cos(angle) - (width / 2.) * sin(angle),
          center[1] + (width / 2.) * cos(angle) + (line_length / 2.) * sin(angle))
    ur = (center[0] - (line_length / 2.) * cos(angle) - (width / 2.) * sin(angle),
          center[1] + (width / 2.) * cos(angle) - (line_length / 2.) * sin(angle))
    bl = (center[0] + (line_length / 2.) * cos(angle) + (width / 2.) * sin(angle),
          center[1] - (width / 2.) * cos(angle) + (line_length / 2.) * sin(angle))
    br = (center[0] - (line_length / 2.) * cos(angle) + (width / 2.) * sin(angle),
          center[1] - (width / 2.) * cos(angle) - (line_length / 2.) * sin(angle))

    pygame.gfxdraw.aapolygon(screen, (ul, ur, br, bl), color)
    pygame.gfxdraw.filled_polygon(screen, (ul, ur, br, bl), color)


def get_polygon_points(num_sides, center, radius, rotation=0):
    theta = 2 * math.pi / num_sides

    points = [
        [radius * math.sin(theta * i + rotation) + center[0],
         -radius * math.cos(theta * i + rotation) + center[1]]
        for i in range(num_sides)
    ]

    return points