# -*- coding: utf-8 -*-
"""Main game module for Animal Game."""
import math
import os
import random
import sys
from typing import Optional, Tuple, Dict

import pygame

# Initialize pygame modules
pygame.init()

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_SETTINGS = 2
STATE_MODE_SELECT = 3
STATE_CRITTER_SELECT = 4

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 20


def check_project_root() -> None:
    """Verify that the script is run from the project root directory."""
    if not os.path.exists('prj.core') or not os.path.exists('prj.data'):
        print("Ошибка: Запускайте скрипт из корневой директории проекта!")
        print("Текущая директория:", os.getcwd())
        sys.exit(1)


class Button(pygame.sprite.Sprite):
    """Button for menu interfaces."""

    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150)
    ):
        super().__init__()
        self.text = text
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

        # Create button surface
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Render text
        self._render_text()

        # Store original image for reset
        self.original_image = self.image.copy()

    def _render_text(self) -> None:
        """Render text on the button surface."""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.image.blit(text_surface, text_rect)

    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Update button appearance based on mouse position."""
        if self.rect.collidepoint(mouse_pos):
            if not self.is_hovered:
                self.is_hovered = True
                self.image.fill(self.hover_color)
                self._render_text()
        else:
            if self.is_hovered:
                self.is_hovered = False
                self.image = self.original_image.copy()

    def is_clicked(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> bool:
        """Check if the button was clicked."""
        return self.rect.collidepoint(mouse_pos) and mouse_pressed


class Menu:
    """Main game menu."""

    def __init__(self, screen_width: int, screen_height: int):
        self.buttons = pygame.sprite.Group()

        button_width = 300
        button_height = 60
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100

        self.start_button = Button("Начать", center_x, start_y, button_width, button_height)
        self.settings_button = Button("Параметры", center_x, start_y + 80, button_width, button_height)
        self.quit_button = Button("Выйти", center_x, start_y + 160, button_width, button_height)

        self.buttons.add(self.start_button, self.settings_button, self.quit_button)

        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Игра с животными", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

    def draw(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        """Draw the menu on screen."""
        screen.blit(background, (0, 0))
        screen.blit(self.title_text, self.title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            screen.blit(button.image, button.rect)

    def handle_click(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> Optional[str]:
        """Handle button clicks. Returns action string or None."""
        if self.start_button.is_clicked(mouse_pos, mouse_pressed):
            return "start"
        elif self.settings_button.is_clicked(mouse_pos, mouse_pressed):
            return "settings"
        elif self.quit_button.is_clicked(mouse_pos, mouse_pressed):
            return "quit"
        return None


class SettingsMenu:
    """Settings menu."""

    def __init__(self, screen_width: int, screen_height: int):
        self.back_button = Button("Назад", screen_width // 2, screen_height // 2 + 150, 200, 50)

        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Параметры", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

        font_small = pygame.font.Font(None, 36)
        self.info_text = font_small.render("Настройки пока не реализованы", True, (200, 200, 200))
        self.info_rect = self.info_text.get_rect(center=(screen_width // 2, screen_height // 2))

    def draw(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        """Draw the settings menu."""
        screen.blit(background, (0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.info_text, self.info_rect)

        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)
        screen.blit(self.back_button.image, self.back_button.rect)

    def handle_click(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> Optional[str]:
        """Handle back button click."""
        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return "back"
        return None


class ModeSelectMenu:
    """Game mode selection menu (single/two player)."""

    def __init__(self, screen_width: int, screen_height: int):
        self.buttons = pygame.sprite.Group()

        button_width = 300
        button_height = 60
        center_x = screen_width // 2
        start_y = screen_height // 2 - 50

        self.single_player_button = Button("Одиночная игра", center_x, start_y, button_width, button_height)
        self.two_player_button = Button("Играть вдвоем", center_x, start_y + 80, button_width, button_height)
        self.back_button = Button("Назад", center_x, start_y + 160, button_width, button_height)

        self.buttons.add(self.single_player_button, self.two_player_button, self.back_button)

        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Выберите режим", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))

    def draw(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        """Draw the mode selection menu."""
        screen.blit(background, (0, 0))
        screen.blit(self.title_text, self.title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            screen.blit(button.image, button.rect)

    def handle_click(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> Optional[str]:
        """Handle button clicks. Returns action string or None."""
        if self.single_player_button.is_clicked(mouse_pos, mouse_pressed):
            return "single_player"
        elif self.two_player_button.is_clicked(mouse_pos, mouse_pressed):
            return "two_player"
        elif self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return "back"
        return None


class CritterSelectMenu:
    """Animal selection menu for player."""

    def __init__(self, screen_width: int, screen_height: int):
        self.buttons = pygame.sprite.Group()

        button_width = 300
        button_height = 60
        center_x = screen_width // 2
        start_y = screen_height // 2 - 100

        self.sheep_button = Button("Овца (Sheep)", center_x, start_y, button_width, button_height)
        self.pig_button = Button("Свинья (Pig)", center_x, start_y + 80, button_width, button_height)
        self.goat_button = Button("Коза (Goat)", center_x, start_y + 160, button_width, button_height)
        self.back_button = Button("Назад", center_x, start_y + 240, button_width, button_height)

        self.buttons.add(self.sheep_button, self.pig_button, self.goat_button, self.back_button)

        font = pygame.font.Font(None, 72)
        self.title_text = font.render("Выберите животное", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 200))

    def draw(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        """Draw the animal selection menu."""
        screen.blit(background, (0, 0))
        screen.blit(self.title_text, self.title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            screen.blit(button.image, button.rect)

    def handle_click(self, mouse_pos: Tuple[int, int], mouse_pressed: bool) -> Optional[str]:
        """Handle button clicks. Returns selected animal or 'back' or None."""
        if self.sheep_button.is_clicked(mouse_pos, mouse_pressed):
            return "sheep"
        elif self.pig_button.is_clicked(mouse_pos, mouse_pressed):
            return "pig"
        elif self.goat_button.is_clicked(mouse_pos, mouse_pressed):
            return "goat"
        elif self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return "back"
        return None


class Animal(pygame.sprite.Sprite):
    """Base animal class with movement capabilities."""

    def __init__(self, animal_images: Dict[str, pygame.Surface], animal_name: str):
        super().__init__()
        self.animal_name = animal_name

        self.image_down = [
            animal_images[f'{animal_name}_down{i}'] for i in range(3)
        ]
        self.iter_down = 0

        self.image_left = [
            animal_images[f'{animal_name}_left{i}'] for i in range(3)
        ]
        self.iter_left = 0

        self.image_right = [
            animal_images[f'{animal_name}_right{i}'] for i in range(3)
        ]
        self.iter_right = 0

        self.image_up = [
            animal_images[f'{animal_name}_up{i}'] for i in range(3)
        ]
        self.iter_up = 0

        self.image = self.image_down[0]
        self.rect = self.image.get_rect()

    def move_down(self, speed: int) -> None:
        """Move down and update animation."""
        self.rect.move_ip(0, speed)
        self.iter_down = (self.iter_down + 1) % len(self.image_down)
        self.image = self.image_down[self.iter_down]

    def move_left(self, speed: int) -> None:
        """Move left and update animation."""
        self.rect.move_ip(-speed, 0)
        self.iter_left = (self.iter_left + 1) % len(self.image_left)
        self.image = self.image_left[self.iter_left]

    def move_right(self, speed: int) -> None:
        """Move right and update animation."""
        self.rect.move_ip(speed, 0)
        self.iter_right = (self.iter_right + 1) % len(self.image_right)
        self.image = self.image_right[self.iter_right]

    def move_up(self, speed: int) -> None:
        """Move up and update animation."""
        self.rect.move_ip(0, -speed)
        self.iter_up = (self.iter_up + 1) % len(self.image_up)
        self.image = self.image_up[self.iter_up]

    def clamp_to_screen(self, screen_width: int, screen_height: int) -> None:
        """Keep the animal within screen bounds."""
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))


class Sheep(Animal):
    """Sheep animal, controlled with arrow keys."""

    def __init__(self, animal_images: Dict[str, pygame.Surface]):
        super().__init__(animal_images, 'sheep')

    def update(self, pressed_keys: Tuple[bool, ...], screen_width: int, screen_height: int) -> None:
        """Update sheep position based on key input."""
        if pressed_keys[pygame.K_DOWN]:
            self.move_down(2)
        elif pressed_keys[pygame.K_LEFT]:
            self.move_left(2)
        elif pressed_keys[pygame.K_RIGHT]:
            self.move_right(2)
        elif pressed_keys[pygame.K_UP]:
            self.move_up(2)

        self.clamp_to_screen(screen_width, screen_height)


class Pig(Animal):
    """Pig animal, controlled with arrow keys."""

    def __init__(self, animal_images: Dict[str, pygame.Surface]):
        super().__init__(animal_images, 'pig')

    def update(self, pressed_keys: Tuple[bool, ...], screen_width: int, screen_height: int) -> None:
        """Update pig position based on key input."""
        if pressed_keys[pygame.K_DOWN]:
            self.move_down(2)
        elif pressed_keys[pygame.K_LEFT]:
            self.move_left(2)
        elif pressed_keys[pygame.K_RIGHT]:
            self.move_right(2)
        elif pressed_keys[pygame.K_UP]:
            self.move_up(2)

        self.clamp_to_screen(screen_width, screen_height)


class Goat(Animal):
    """Goat animal, controlled with arrow keys (faster)."""

    def __init__(self, animal_images: Dict[str, pygame.Surface]):
        super().__init__(animal_images, 'goat')

    def update(self, pressed_keys: Tuple[bool, ...], screen_width: int, screen_height: int) -> None:
        """Update goat position based on key input."""
        if pressed_keys[pygame.K_DOWN]:
            self.move_down(3)
        elif pressed_keys[pygame.K_LEFT]:
            self.move_left(3)
        elif pressed_keys[pygame.K_RIGHT]:
            self.move_right(3)
        elif pressed_keys[pygame.K_UP]:
            self.move_up(3)

        self.clamp_to_screen(screen_width, screen_height)


class Wolf(Animal):
    """Wolf animal, controlled with WASD keys."""

    def __init__(self, animal_images: Dict[str, pygame.Surface]):
        super().__init__(animal_images, 'wolf')
        self.speeds = {'down': 1, 'left': 1, 'right': 1, 'up': 1}
        self.previous_direction: Optional[str] = None

    def update(self, pressed_keys: Tuple[bool, ...], screen_width: int, screen_height: int) -> None:
        """Update wolf position based on WASD input with acceleration."""
        moved = False

        if pressed_keys[pygame.K_s]:
            self._move_with_acceleration('down', self.move_down)
            moved = True
        elif pressed_keys[pygame.K_a]:
            self._move_with_acceleration('left', self.move_left)
            moved = True
        elif pressed_keys[pygame.K_d]:
            self._move_with_acceleration('right', self.move_right)
            moved = True
        elif pressed_keys[pygame.K_w]:
            self._move_with_acceleration('up', self.move_up)
            moved = True

        if not moved:
            self.speeds = {'down': 1, 'left': 1, 'right': 1, 'up': 1}

        self.clamp_to_screen(screen_width, screen_height)

    def _move_with_acceleration(self, direction: str, move_func: callable) -> None:
        """Move with acceleration based on continuous direction."""
        if self.previous_direction == direction:
            self.speeds[direction] += 1
        else:
            self.speeds[direction] = 1
        self.previous_direction = direction
        move_func(self.speeds[direction])


class Item(pygame.sprite.Sprite):
    """Random item sprite on the ground."""

    def __init__(self, env_images: Dict[str, pygame.Surface], screen_width: int, screen_height: int):
        super().__init__()
        key = random.choice(list(env_images.keys()))
        self.image = env_images[key]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(screen_width), random.randrange(screen_height))


class Grass(pygame.sprite.Sprite):
    """Grass sprite."""

    def __init__(self, grass_images: Dict[str, pygame.Surface], screen_width: int, screen_height: int):
        super().__init__()
        key = random.choice(list(grass_images.keys()))
        self.image = grass_images[key]
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(screen_width), random.randrange(screen_height))


def create_background(
    screen_size: Tuple[int, int],
    env_images: Dict[str, pygame.Surface],
    tile_size: int = 32
) -> pygame.Surface:
    """Create tiled background surface."""
    width, height = screen_size
    background = pygame.Surface(screen_size)

    tiles_x = math.ceil(width / tile_size)
    tiles_y = math.ceil(height / tile_size)

    for x in range(tiles_x):
        for y in range(tiles_y):
            background.blit(env_images['background_tile'], (x * tile_size, y * tile_size))

    return background


def main() -> None:
    """Main game loop."""
    check_project_root()

    screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    clock = pygame.time.Clock()
    display_mode = pygame.FULLSCREEN | pygame.HWSURFACE
    screen = pygame.display.set_mode(screen_size, display_mode)

    from utils import import_images
    env_images, grass_images, animal_images = import_images()

    background = create_background(screen_size, env_images)

    animals = pygame.sprite.Group()
    items = pygame.sprite.Group()
    grass = pygame.sprite.Group()

    items.add(Item(env_images, SCREEN_WIDTH, SCREEN_HEIGHT))
    for _ in range(40):
        grass.add(Grass(grass_images, SCREEN_WIDTH, SCREEN_HEIGHT))

    main_menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
    settings_menu = SettingsMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    mode_select_menu = ModeSelectMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
    critter_select_menu = CritterSelectMenu(SCREEN_WIDTH, SCREEN_HEIGHT)

    game_state = STATE_MENU
    cattle: Optional[Animal] = None
    wolf: Optional[Wolf] = None
    game_initialized = False

    done = False
    while not done:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == STATE_PLAYING:
                        game_state = STATE_MENU
                    else:
                        done = True
                elif event.key == pygame.K_p and game_state == STATE_PLAYING:
                    items.add(Item(env_images, SCREEN_WIDTH, SCREEN_HEIGHT))

            elif event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == STATE_MENU:
                    action = main_menu.handle_click(mouse_pos, True)
                    if action == "start":
                        game_state = STATE_MODE_SELECT
                    elif action == "settings":
                        game_state = STATE_SETTINGS
                    elif action == "quit":
                        done = True

                elif game_state == STATE_SETTINGS:
                    action = settings_menu.handle_click(mouse_pos, True)
                    if action == "back":
                        game_state = STATE_MENU

                elif game_state == STATE_MODE_SELECT:
                    action = mode_select_menu.handle_click(mouse_pos, True)
                    if action == "single_player":
                        print("Одиночная игра пока не реализована. Выберите 'Играть вдвоем'.")
                    elif action == "two_player":
                        game_state = STATE_CRITTER_SELECT
                    elif action == "back":
                        game_state = STATE_MENU

                elif game_state == STATE_CRITTER_SELECT:
                    action = critter_select_menu.handle_click(mouse_pos, True)
                    if action in ("sheep", "pig", "goat"):
                        animals.empty()

                        if action == "sheep":
                            cattle = Sheep(animal_images)
                        elif action == "pig":
                            cattle = Pig(animal_images)
                        elif action == "goat":
                            cattle = Goat(animal_images)

                        cattle.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                        animals.add(cattle)

                        wolf = Wolf(animal_images)
                        wolf.rect.center = (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2)
                        animals.add(wolf)

                        game_initialized = True
                        game_state = STATE_PLAYING
                    elif action == "back":
                        game_state = STATE_MODE_SELECT

        if game_state == STATE_MENU:
            main_menu.draw(screen, background)
        elif game_state == STATE_SETTINGS:
            settings_menu.draw(screen, background)
        elif game_state == STATE_MODE_SELECT:
            mode_select_menu.draw(screen, background)
        elif game_state == STATE_CRITTER_SELECT:
            critter_select_menu.draw(screen, background)
        elif game_state == STATE_PLAYING:
            if game_initialized and cattle is not None and wolf is not None:
                pressed_keys = pygame.key.get_pressed()
                cattle.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)
                wolf.update(pressed_keys, SCREEN_WIDTH, SCREEN_HEIGHT)

                if pygame.sprite.collide_mask(cattle, wolf):
                    cattle.kill()

                screen.blit(background, (0, 0))
                grass.draw(screen)
                items.draw(screen)
                animals.draw(screen)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
