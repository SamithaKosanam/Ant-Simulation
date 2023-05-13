from lib2to3.pygram import python_grammar_no_print_statement
import math
import random
from Predator import Predator

import pygame

import Graphics
import drawing_utils
import ctypes
from PIL import Image

from Constants import *
from Ant import Ant
import Map
from Food import Food
from Pheromone import Pheromone
from Predator import Predator


def main():
    seed = 860
    # seed = random.randint(0, 1000)
    print(seed)
    random.seed(seed)

    ctypes.windll.user32.SetProcessDPIAware()

    pygame.init()
    screen = pygame.display.set_mode((1152, 648))   # Change to size of map
    screen_width, screen_height = screen.get_size()
    pygame.display.set_caption("Ant Colony Simulation")
    Graphics.load_sprites()
    clock = pygame.time.Clock()

    background = pygame.image.load("Map.png").convert()

    ants = []   # List of ants on screen
    foods = [Food(400, 300),
             Food(1050, 580),
             Food(120, 110),
             Food(967, 140)]
    pheromones = []
    for i in range(math.ceil(screen_width / PH_GRID)):
        pheromones.append([])
        for _ in range(math.ceil(screen_height / PH_GRID)):
            pheromones[i].append(None)
    anteater = Predator(PREDATOR_X, PREDATOR_Y)
    predator_pheromones = []
    for i in range(math.ceil(screen_width / PH_GRID)):
        predator_pheromones.append([])
        for _ in range(math.ceil(screen_height / PH_GRID)):
            predator_pheromones[i].append(None)
    frame = 0
    while True:
        frame = (frame + 1) % 600

        if frame % ANT_EVERY == 0 and len(ants) < MAX_ANTS:
            # Add new ant on screen every ANT_EVERY frames up to no more than MAX_ANTS ants
            ants.append(Ant(ANT_HILL_X, ANT_HILL_Y, random.random() * math.pi * 2))

        # Set frames per second
        clock.tick(TICKS)

        # Draw map image in background
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))

        for l in pheromones:
            for pheromone in l:
                if pheromone is not None:
                    pheromone.draw(screen)

        for l in predator_pheromones:
            for predator_pheromone in l:
                if predator_pheromone is not None:
                    predator_pheromone.draw(screen)
        # Drawing

        for ant in ants:
            ant.draw(screen)
            if DEBUG_VISUALS:
                pygame.draw.circle(screen, (100, 255, 0), ant.get_head(), radius=3)
            ant.step()
            ant.collision(Map.pixels)
            if ant.next_point is None:
                if random.random() < TURN_PROBABILITY:
                    ant.turn(random.random() * math.pi * 2)
                ph_x = int(ant.x // PH_GRID)
                ph_y = int(ant.y // PH_GRID)
                pheromone = None
                predator_pheromone = None
                min_dist = math.inf
                min_dist_pred = math.inf
                for add_x in [-1, 0, 1]:
                    for add_y in [-1, 0, 1]:
                        idx_1 = ph_x + add_x
                        idx_2 = ph_y + add_y
                        if 0 <= idx_1 < len(pheromones) and 0 <= idx_2 < len(pheromones[0]):
                            new_ph = pheromones[idx_1][idx_2]
                            if new_ph is not None:
                                d = get_dist((ant.x, ant.y), (new_ph.x, new_ph.y))
                                if d < min_dist:
                                    pheromone = pheromones[idx_1][idx_2]
                                    min_dist = d
                        if 0 <= idx_1 < len(predator_pheromones) and 0 <= idx_2 < len(predator_pheromones[0]):
                            new_ph = predator_pheromones[idx_1][idx_2]
                            if new_ph is not None:
                                d = get_dist((ant.x, ant.y), (new_ph.x, new_ph.y))
                                if d < min_dist_pred:
                                    predator_pheromone = predator_pheromones[idx_1][idx_2]
                                    min_dist_pred = d

                if pheromone is not None and pheromone.active:
                    ant.smell_pheromone(pheromone)
                if predator_pheromone is not None and predator_pheromone.active:
                    ant.run_away(saw_predator=False)

            if ant.sense_predator and ant.saw_predator and ant.on_line:
                if frame % (60 // ANT_ESCAPING_SPEEDUP) == 0 and \
                        get_dist((ant.x, ant.y), (ANT_HILL_X, ANT_HILL_Y)) >= ANT_HILL_RADIUS:
                    ph_x = int(ant.x // PH_GRID)
                    ph_y = int(ant.y // PH_GRID)
                    # red pheromones
                    predator_pheromones[ph_x][ph_y] = Pheromone(ant.x, ant.y, ant.angle % (2 * math.pi), True)
            if ant.has_food and ant.on_line:
                if frame % 60 == 0 and get_dist((ant.x, ant.y), (ANT_HILL_X, ANT_HILL_Y)) >= ANT_HILL_RADIUS:
                    ph_x = int(ant.x // PH_GRID)
                    ph_y = int(ant.y // PH_GRID)
                    pheromones[ph_x][ph_y] = Pheromone(ant.x, ant.y, (ant.angle + math.pi) % (2 * math.pi), False)
            if not ant.has_food:
                collided = False
                for food in foods:
                    if food.get_rect().collidepoint(ant.get_head()):
                        collided = True
                        ant.return_food()
                        if not ant.food_removed:
                            food.life -= 1
                            ant.food_removed = True
                            if food.life == 0:
                                foods.remove(food)
                if not collided:
                    ant.food_removed = False
            
            if not ant.sense_predator:
                if anteater.get_detection_rect().collidepoint(ant.get_head()):
                    ant.run_away(saw_predator=True)
            if anteater.get_rect().colliderect(ant.get_rect()) and \
                    get_dist((ANT_HILL_X, ANT_HILL_Y), (ant.x, ant.y)) > ANT_HILL_RADIUS:
                ants.remove(ant)
                        

        for food in foods:
            food.draw(screen)

        anteater.draw(screen)
        anteater.step()
        anteater.collision(Map.pixels)
        if anteater.next_point is None:
            if random.random() < PREDATOR_TURN_PROBABILITY:
                anteater.turn(random.random() * math.pi * 2)

        drawing_utils.draw_filled_polygon(screen, drawing_utils.get_polygon_points(5, (ANT_HILL_X, ANT_HILL_Y),
                                                                                   ANT_HILL_RADIUS),
                                          color=ANT_HILL_COLOR)

        # for idx in range(len(GRAPH)):
        #     point, _ = GRAPH[idx]
        #     pygame.draw.circle(screen, (255, 0, 0), point, radius=AntHillDijkstra['dist'][idx])

        if DEBUG_VISUALS:
            pygame.draw.rect(screen, (0, 100, 255), anteater.get_detection_rect(), 3)
            pygame.draw.rect(screen, (0, 100, 255), anteater.get_rect(), 3)
            pygame.draw.circle(screen, (255, 100, 0), anteater.get_head(), radius=3)

        pygame.display.flip()

        # Close window when pressing escape
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                return


if __name__ == "__main__":
    main()
