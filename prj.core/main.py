# -*- coding: utf-8 -*-
import random
import pygame
import math  # Добавлено: используется math.ceil
import os
import sys
from pygame.locals import *

# Убедимся, что мы в корне проекта
if not os.path.exists('prj.core') or not os.path.exists('prj.data'):
    print("Ошибка: Запускайте скрипт из корневой директории проекта!")
    print("Текущая директория:", os.getcwd())
    sys.exit(1)

if not pygame.font:
    print("Warning! Fonts disabled")
if not pygame.mixer:
    print("Warning! Sounds disabled")

class Animal(pygame.sprite.Sprite):
    """Basic animal that can move."""

    def __init__(self, animal_images):
        super().__init__()

        self.image_down = [
            animal_images[self.animal_name + '_down0'],
            animal_images[self.animal_name + '_down1'],
            animal_images[self.animal_name + '_down2']
        ]
        self.iter_down = 0

        self.image_left = [
            animal_images[self.animal_name + '_left0'],
            animal_images[self.animal_name + '_left1'],
            animal_images[self.animal_name + '_left2']
        ]
        self.iter_left = 0

        self.image_right = [
            animal_images[self.animal_name + '_right0'],
            animal_images[self.animal_name + '_right1'],
            animal_images[self.animal_name + '_right2']
        ]
        self.iter_right = 0

        self.image_up = [
            animal_images[self.animal_name + '_up0'],
            animal_images[self.animal_name + '_up1'],
            animal_images[self.animal_name + '_up2']
        ]
        self.iter_up = 0

        self.image = self.image_down[0]  # init image
        self.rect = self.image.get_rect()


    def move_down(self, speed):
        self.rect.move_ip(0, speed)

        self.iter_down += 1
        if self.iter_down >= len(self.image_down):
            self.iter_down = 0

        self.image = self.image_down[self.iter_down]

    def move_left(self, speed):
        self.rect.move_ip(-speed, 0)

        self.iter_left += 1
        if self.iter_left >= len(self.image_left):
            self.iter_left = 0

        self.image = self.image_left[self.iter_left]

    def move_right(self, speed):
        self.rect.move_ip(speed, 0)

        self.iter_right += 1
        if self.iter_right >= len(self.image_right):
            self.iter_right = 0

        self.image = self.image_right[self.iter_right]

    def move_up(self, speed):
        self.rect.move_ip(0, -speed)

        self.iter_up += 1
        if self.iter_up >= len(self.image_up):
            self.iter_up = 0

        self.image = self.image_up[self.iter_up]


class Sheep(Animal):
    """Sheep animal, controlled with direction keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__.lower()  # важно: имя в нижнем регистре
        super().__init__(animal_images)
        self.rect.center = (width // 2, height // 2)

    def update(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.move_down(2)
        elif pressed_keys[K_LEFT]:
            self.move_left(2)
        elif pressed_keys[K_RIGHT]:
            self.move_right(2)
        elif pressed_keys[K_UP]:
            self.move_up(2)

        # Ограничение по границам экрана
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height


class Pig(Animal):
    """Pig animal, controlled with direction keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__.lower()
        super().__init__(animal_images)
        self.rect.center = (width // 2, height // 2)

    def update(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.move_down(2)
        elif pressed_keys[K_LEFT]:
            self.move_left(2)
        elif pressed_keys[K_RIGHT]:
            self.move_right(2)
        elif pressed_keys[K_UP]:
            self.move_up(2)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height


class Goat(Animal):
    """Goat animal, controlled with direction keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__.lower()
        super().__init__(animal_images)
        self.rect.center = (width // 2, height // 2)

    def update(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.move_down(3)
        elif pressed_keys[K_LEFT]:
            self.move_left(3)
        elif pressed_keys[K_RIGHT]:
            self.move_right(3)
        elif pressed_keys[K_UP]:
            self.move_up(3)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height


class Wolf(Animal):
    """Wolf animal, controlled with WASD keys."""

    def __init__(self, animal_images):
        self.animal_name = self.__class__.__name__.lower()
        super().__init__(animal_images)
        self.down_spd = self.left_spd = self.right_spd = self.up_spd = 1

        self.directions = ["down", "left", "right", "up"]
        self.previos_direction = None

    def update(self, pressed_keys):
        moved = False
        if pressed_keys[K_s]:
            self.move_down(self.down_spd)
            if self.previos_direction == "down":
                self.down_spd += 1
            else:
                self.down_spd = 1
            self.previos_direction = "down"
            moved = True
        elif pressed_keys[K_a]:
            self.move_left(self.left_spd)
            if self.previos_direction == "left":
                self.left_spd += 1
            else:
                self.left_spd = 1
            self.previos_direction = "left"
            moved = True
        elif pressed_keys[K_d]:
            self.move_right(self.right_spd)
            if self.previos_direction == "right":
                self.right_spd += 1
            else:
                self.right_spd = 1
            self.previos_direction = "right"
            moved = True
        elif pressed_keys[K_w]:
            self.move_up(self.up_spd)
            if self.previos_direction == "up":
                self.up_spd += 1
            else:
                self.up_spd = 1
            self.previos_direction = "up"
            moved = True

        # Если не двигался — сбрасываем ускорение
        if not moved:
            self.down_spd = self.left_spd = self.right_spd = self.up_spd = 1

        # Ограничение по границам
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > height:
            self.rect.bottom = height


class Item(pygame.sprite.Sprite):
    """Items on the ground."""

    def __init__(self):
        super().__init__()
        # Преобразуем ключи в список
        key = random.choice(list(env_images.keys()))
        self.image = env_images[key]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(width), random.randrange(height))


class Grass(pygame.sprite.Sprite):
    """Grass sprite"""

    def __init__(self):
        super().__init__()
        key = random.choice(list(grass_images.keys()))
        self.image = grass_images[key]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(width), random.randrange(height))


# ================== ОСНОВНОЙ ЦИКЛ ==================
if __name__ == '__main__':

    # Размер экрана
    size = width, height = 1920, 1080
    FPS = 20
    done = False
    clock = pygame.time.Clock()

    pygame.init()
    display_mode = pygame.FULLSCREEN | pygame.HWSURFACE
    # display_mode = 0  # Раскомментировать для оконного режима
    screen = pygame.display.set_mode(size, display_mode)

    # Предполагается, что у тебя есть функция import_images() в utils.py
    # Она должна возвращать три словаря: env_images, grass_images, animal_images
    from utils import import_images

    env_images, grass_images, animal_images = import_images()

    background = pygame.Surface(screen.get_size())

    # Заполняем фон плиткой
    for x in range(int(math.ceil(float(width) / 32))):
        for y in range(int(math.ceil(float(height) / 32))):
            background.blit(env_images['background_tile'], (x * 32, y * 32))

    animals = pygame.sprite.Group()
    items = pygame.sprite.Group()
    grass = pygame.sprite.Group()

    cattle = Sheep(animal_images)
    animals.add(cattle)

    wolf = Wolf(animal_images)
    animals.add(wolf)

    new_item = Item()
    items.add(new_item)

    for i in range(40):
        new_grass = Grass()
        grass.add(new_grass)

    # Главный цикл
    while not done:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == K_p:
                    new_item = Item()
                    items.add(new_item)
            elif event.type == pygame.QUIT:
                done = True

        pressed_keys = pygame.key.get_pressed()
        cattle.update(pressed_keys)
        wolf.update(pressed_keys)

        # Проверка столкновения овцы и волка
        if pygame.sprite.collide_mask(cattle, wolf):
            cattle.kill()  # Овца исчезает

        # Отрисовка
        screen.blit(background, (0, 0))
        grass.draw(screen)
        items.draw(screen)
        animals.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()