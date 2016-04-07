# -*- coding: utf-8 -*-
import os
import os.path as osp
import sys
import random
import pygame
from pygame.locals import *
from utils import *

if not pygame.font:
    print "Warning! Fonts disabled"
if not pygame.mixer:
    print "Warning! Sounds disabled"


class Animal(pygame.sprite.Sprite):
    """Basic animal that can move."""

    def __init__(self, animal_images):
        super(Animal, self).__init__()

        self.image_down = [animal_images[str(self.animal_name) + '_down0'],
                           animal_images[str(self.animal_name) + '_down1'],
                           animal_images[str(self.animal_name) + '_down2']]
        self.iter_down = 0

        self.image_left = [animal_images[str(self.animal_name) + '_left0'],
                           animal_images[str(self.animal_name) + '_left1'],
                           animal_images[str(self.animal_name) + '_left2']]
        self.iter_left = 0

        self.image_right = [animal_images[str(self.animal_name) + '_right0'],
                            animal_images[str(self.animal_name) + '_right1'],
                            animal_images[str(self.animal_name) + '_right2']]
        self.iter_right = 0

        self.image_up = [animal_images[str(self.animal_name) + '_up0'],
                         animal_images[str(self.animal_name) + '_up1'],
                         animal_images[str(self.animal_name) + '_up2']]
        self.iter_up = 0

        self.image = self.image_down[0]  # init image
        self.rect = self.image.get_rect()
        # if animal_name == "sheep":
        #     self.rect.center = (width / 2, height / 2)

    def move_down(self):
        self.rect.move_ip(0, 5)

        self.iter_down += 1
        if self.iter_down >= len(self.image_down):
            self.iter_down = 0

        self.image = self.image_down[self.iter_down]

    def move_left(self):
        self.rect.move_ip(-5, 0)

        self.iter_left += 1
        if self.iter_left >= len(self.image_left):
            self.iter_left = 0

        self.image = self.image_left[self.iter_left]

    def move_right(self):
        self.rect.move_ip(5, 0)

        self.iter_right += 1
        if self.iter_right >= len(self.image_right):
            self.iter_right = 0

        self.image = self.image_right[self.iter_right]

    def move_up(self):
        self.rect.move_ip(0, -5)

        self.iter_up += 1
        if self.iter_up >= len(self.image_up):
            self.iter_up = 0

        self.image = self.image_up[self.iter_up]


class Sheep(Animal):
    """Sheep animal, controlled with direction keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__
        super(Sheep, self).__init__(animal_images)
        self.rect.center = (width / 2, height / 2)

    def update(self, pressed_keys):
        affected_rects = []
        affected_rects.append(grid_point_check(self.rect.x, self.rect.y))
        affected_rects.append(self.rect)  # before move

        if pressed_keys[K_DOWN]:
            self.move_down()
        elif pressed_keys[K_LEFT]:
            self.move_left()
        elif pressed_keys[K_RIGHT]:
            self.move_right()
        elif pressed_keys[K_UP]:
            self.move_up()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = height

        affected_rects.append(grid_point_check(self.rect.x, self.rect.y))
        affected_rects.append(self.rect)  # before move
        return affected_rects


class Wolf(Animal):
    """Sheep animal, controlled with direction keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__
        super(Wolf, self).__init__(animal_images)

    def update(self, pressed_keys):
        affected_rects = []
        affected_rects.append(grid_point_check(self.rect.x, self.rect.y))
        affected_rects.append(self.rect)  # before move

        # print(self.rect)
        if pressed_keys[K_s]:
            self.move_down()
        elif pressed_keys[K_a]:
            self.move_left()
        elif pressed_keys[K_d]:
            self.move_right()
        elif pressed_keys[K_w]:
            self.move_up()

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= height:
            self.rect.bottom = height
        # print(self.rect.x, self.rect.y)
        # import pdb; pdb.set_trace()

        affected_rects.append(grid_point_check(self.rect.x, self.rect.y))
        affected_rects.append(self.rect)  # after move

        return affected_rects


class Item(pygame.sprite.Sprite):
    """Items on the ground."""

    def __init__(self):
        super(Item, self).__init__()

        self.image = env_images[random.choice(env_images.keys())]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(width), random.randrange(height))


class Grass(pygame.sprite.Sprite):
    """Grass sprie"""

    def __init__(self):
        super(Grass, self).__init__()

        self.image = grass_images[random.choice(grass_images.keys())]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(width), random.randrange(height))


def grid_point_check(x, y, base=32):
    """Return grid indexes of given point"""
    ind_x = round_32(x, base=base)
    ind_y = round_32(y, base=base)

    grid[ind_x][ind_y] = 1

    return pygame.Rect(ind_x * 32, ind_y * 32, base, base)


if __name__ == '__main__':

    size = width, height = 1280, 800
    # size = width, height = 1920, 1080
    grid = []
    FPS = 20
    done = False
    clock = pygame.time.Clock()

    update_rects = []  # list of rects to update

    pygame.init()
    # display_mode = pygame.FULLSCREEN | pygame.HWSURFACE
    display_mode = 0
    screen = pygame.display.set_mode(size, display_mode)

    env_images, grass_images, animal_images = import_images()

    background = pygame.Surface(screen.get_size())
    for x in range(width / 32):
        grid.append([])
        for y in range(height / 32):
            background.blit(env_images['background_tile'], (x * 32, y * 32))
            grid[x].append(0)

    animals = pygame.sprite.Group()
    items = pygame.sprite.Group()
    grass = pygame.sprite.Group()

    sheep = Sheep(animal_images)
    animals.add(sheep)

    wolf = Wolf(animal_images)
    animals.add(wolf)

    new_item = Item()
    items.add(new_item)

    for i in range(40):
        new_grass = Grass()
        grass.add(new_grass)

    # initial screen
    screen.blit(background, (0, 0))  # first background update
    for entity in grass:
        screen.blit(entity.image, entity.rect)
    for entity in items:
        screen.blit(entity.image, entity.rect)  # second items update
    for entity in animals:
        screen.blit(entity.image, entity.rect)  # tird animals update
    pygame.display.update()

    while not done:
        del update_rects[:]

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == K_p:
                    new_item = Item(env_images)
                    items.add(new_item)
            elif event.type == pygame.QUIT:
                done = True
        
        pressed_keys = pygame.key.get_pressed()
        update_rects += sheep.update(pressed_keys)
        update_rects += wolf.update(pressed_keys)

        if pygame.sprite.collide_mask(sheep, wolf):
            sheep.kill()

        for x in range(width / 32):
            for y in range(height / 32):
                if grid[x][y] == 1:
                    screen.blit(env_images['background_tile'], (x * 32, y * 32))
                    grid[x][y] == 0
        screen.blit(background, (0, 0))  # first background update
        for entity in grass:
            screen.blit(entity.image, entity.rect)
        for entity in items:
            screen.blit(entity.image, entity.rect)  # second items update
        for entity in animals:
            screen.blit(entity.image, entity.rect)  # tird animals update

        pygame.display.update(update_rects)
        # print(update_rects)
        clock.tick(FPS)

    pygame.quit()
    # print(grid)
