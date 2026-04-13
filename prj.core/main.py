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

# Состояния игры
STATE_MENU = 0
STATE_PLAYING = 1
STATE_SETTINGS = 2


class Button(pygame.sprite.Sprite):
    """Кнопка для меню."""

    def __init__(self, text, x, y, width, height, color=(100, 100, 100), hover_color=(150, 150, 150)):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        
        # Создаем поверхность кнопки
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Рендерим текст
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        self.image.blit(text_surface, text_rect)
        
        self.original_image = self.image.copy()
        self.is_hovered = False

    def update(self, mouse_pos):
        """Проверяет, находится ли курсор над кнопкой."""
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(self.hover_color)
                font = pygame.font.Font(None, 36)
                text_surface = font.render(self.text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
                self.image.blit(text_surface, text_rect)
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.image = self.original_image.copy()

    def is_clicked(self, mouse_pos, mouse_pressed):
        """Проверяет, была ли кнопка нажата."""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


class Menu:
    """Главное меню игры."""

    def __init__(self, screen_width, screen_height):
        self.buttons = pygame.sprite.Group()
        
        # Создаем кнопки
        button_width = 300
        button_height = 60
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100
        
        self.start_button = Button("Начать", center_x, start_y, button_width, button_height)
        self.settings_button = Button("Параметры", center_x, start_y + 80, button_width, button_height)
        self.quit_button = Button("Выйти", center_x, start_y + 160, button_width, button_height)
        
        self.buttons.add(self.start_button)
        self.buttons.add(self.settings_button)
        self.buttons.add(self.quit_button)
        
        # Заголовок
        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Игра с животными", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

    def draw(self, screen, background):
        """Отрисовывает меню."""
        screen.blit(background, (0, 0))
        
        # Рисуем заголовок
        screen.blit(self.title_text, self.title_rect)
        
        # Обновляем и рисуем кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            screen.blit(button.image, button.rect)

    def handle_click(self, mouse_pos, mouse_pressed):
        """Обрабатывает клик по кнопкам. Возвращает действие."""
        if self.start_button.is_clicked(mouse_pos, mouse_pressed):
            return "start"
        elif self.settings_button.is_clicked(mouse_pos, mouse_pressed):
            return "settings"
        elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
            return "quit"
        return None


class SettingsMenu:
    """Меню параметров."""

    def __init__(self, screen_width, screen_height):
        self.back_button = Button("Назад", screen_width // 2, screen_height // 2 + 150, 200, 50)
        
        # Заголовок
        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Параметры", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        
        # Пример параметра (можно расширить)
        font_small = pygame.font.Font(None, 36)
        self.info_text = font_small.render("Настройки пока не реализованы", True, (200, 200, 200))
        self.info_rect = self.info_text.get_rect(center=(screen_width // 2, screen_height // 2))

    def draw(self, screen, background):
        """Отрисовывает меню параметров."""
        screen.blit(background, (0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.info_text, self.info_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        screen.blit(self.back_button.image, self.back_button.rect)

    def handle_click(self, mouse_pos, mouse_pressed):
        """Обрабатывает клик по кнопке 'Назад'."""
        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return "back"
        return None

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

    # Создаем меню
    main_menu = Menu(width, height)
    settings_menu = SettingsMenu(width, height)
    
    # Текущее состояние игры
    game_state = STATE_MENU

    # Главный цикл
    while not done:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # Левая кнопка мыши
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if game_state == STATE_PLAYING:
                        game_state = STATE_MENU
                    else:
                        done = True
                elif event.key == K_p and game_state == STATE_PLAYING:
                    new_item = Item()
                    items.add(new_item)
            elif event.type == pygame.QUIT:
                done = True
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Обработка кликов мышью
                if game_state == STATE_MENU:
                    action = main_menu.handle_click(mouse_pos, True)
                    if action == "start":
                        game_state = STATE_PLAYING
                    elif action == "settings":
                        game_state = STATE_SETTINGS
                    elif action == "quit":
                        done = True
                elif game_state == STATE_SETTINGS:
                    action = settings_menu.handle_click(mouse_pos, True)
                    if action == "back":
                        game_state = STATE_MENU

        # Отрисовка в зависимости от состояния
        if game_state == STATE_MENU:
            main_menu.draw(screen, background)
        elif game_state == STATE_SETTINGS:
            settings_menu.draw(screen, background)
        elif game_state == STATE_PLAYING:
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