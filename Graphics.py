from ast import Constant
import pygame

import Constants

ant_img = None
food_img = None
food_one = None
food_two = None
food_three = None
ant_anim = []


def load_sprites():
    global ant_img
    global food_img
    global food_one
    global food_two
    global food_three
    global ant_anim
    global predator_img
    ant_img = pygame.image.load("ant.png").convert_alpha()
    ant_img = pygame.transform.scale(ant_img, (Constants.ANT_LENGTH, Constants.ANT_WIDTH))
    for i in range(4):
        ant_anim.append(pygame.image.load(f'Ant_{i}.png').convert_alpha())
        ant_anim[i] = pygame.transform.scale(ant_anim[i], (Constants.ANT_LENGTH, Constants.ANT_WIDTH))
    food_img = pygame.image.load('apple.png').convert_alpha()
    food_img = pygame.transform.scale(food_img, (40, 40))
    predator_img = pygame.image.load("anteater.png").convert_alpha()
    predator_img = pygame.transform.scale(predator_img, (Constants.PREDATOR_LENGTH, Constants.PREDATOR_WIDTH))
    food_one = pygame.image.load('apple1.png').convert_alpha()
    food_one = pygame.transform.scale(food_one, (40, 40))
    food_two = pygame.image.load('apple2.png').convert_alpha()
    food_two = pygame.transform.scale(food_two, (40, 40))
    food_three = pygame.image.load('apple3.png').convert_alpha()
    food_three = pygame.transform.scale(food_three, (40, 40))
