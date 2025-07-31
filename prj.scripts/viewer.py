# -*- coding: utf-8 -*-
import math
import pygame
import random
import sys
from pygame.locals import *

# Явный импорт surfarray (важно для Pygame 2)
import pygame.surfarray


def getImage(filename):
    """Get image for dissolving."""
    sys.path.append("../prj.core")
    try:
        from utils import load_png  # Предполагается, что load_png есть
    except Exception as e:
        print(e)
    finally:
        sys.path.pop()  # Удаляем последний элемент

    try:
        image = load_png(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    else:
        return image


def getPixelArray(image, rect=None):
    """Get pixel array of given rect."""
    if not rect:
        width, height = image.get_size()
        dimension = min(width, height)
        rect = pygame.Rect(0, 0, dimension, dimension)
    part = image.subsurface(rect)
    assert part.get_size()[0] == part.get_size()[1], "Only square images supported"
    return pygame.surfarray.pixels3d(part)


class ColorCell:
    """Cell with the color of corresponding pixel in the field area."""
    def __init__(self, x, y, size, color, padding=1):
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.color = color
        self.padding = padding

    def draw_cell(self, surface, background_color=None):
        """Draws cell with padding."""
        fill_color = background_color or pygame.Color("gray")
        surface.fill(fill_color, self.rect)
        inner_rect = self.rect.inflate(-self.padding, -self.padding)
        surface.fill(self.color, inner_rect)

    def highlight_cell(self, surface):
        """Draw cell with highlighted padding."""
        surface.fill(pygame.Color("red"), self.rect)
        inner_rect = self.rect.inflate(-self.padding, -self.padding)
        surface.fill(self.color, inner_rect)


class Button:
    """Button for tools"""
    def __init__(self, rect, text, padding=1):
        self.rect = rect
        self.color = pygame.Color(
            random.randrange(0, 255),
            random.randrange(0, 255),
            random.randrange(0, 255)
        )
        self.padding = padding
        self.text = text

    def draw_button(self, surface, background_color=None):
        """Draw button with padding"""
        inner_rect = self.rect.inflate(-self.padding, -self.padding)
        surface.fill(self.color, inner_rect)
        font = pygame.font.Font(None, 15)
        text_surface = font.render(self.text, True, pygame.Color("black"))
        surface.blit(text_surface, (self.rect.x, self.rect.y))


class FieldGrid:
    """FieldGrid describing loading image"""
    def __init__(self, pxarray):
        self.pxarray = pxarray
        self.field = pygame.Surface((800, 800))
        self.data = []
        self.update_data()

    def update_data(self):
        width_px = len(self.pxarray[0])
        self.step = 800 / width_px
        self.data = [[None for _ in range(width_px)] for _ in range(width_px)]

    def image_to_grid(self):
        palette = []
        temp_set = set()
        size = len(self.pxarray[0])

        for row in range(size):
            for col in range(size):
                r, g, b = self.pxarray[row][col]
                color = pygame.Color(int(r), int(g), int(b))
                temp_set.add((int(r), int(g), int(b)))
                cell = ColorCell(row, col, self.step, color)
                self.data[row][col] = cell

        palette = [pygame.Color(r, g, b) for r, g, b in temp_set]
        return self.pxarray, palette

    def change_pixel(self, row, col, selected_color):
        self.pxarray[row][col][0] = selected_color.r
        self.pxarray[row][col][1] = selected_color.g
        self.pxarray[row][col][2] = selected_color.b
        self.image_to_grid()  # Перестраиваем сетку

    def draw_field(self, padding=1):
        for row in self.data:
            for cell in row:
                if cell:
                    cell.padding = padding
                    cell.draw_cell(self.field)

    def get_idx(self, pos):
        """Return cell of field grid for given position."""
        row = int(math.ceil(pos[0] / self.step))
        col = int(math.ceil(pos[1] / self.step))
        # Ограничиваем индексы
        row = max(0, min(row, len(self.data) - 1))
        col = max(0, min(col, len(self.data) - 1))
        return row, col

    def redraw_pixel(self, row, col, color):
        cell = self.data[row][col]
        if cell:
            cell.color = color
            cell.draw_cell(self.field)


class ToolsGrid:
    """Grid for tools area."""
    def __init__(self, step=20):
        self.data = [[0 for _ in range(23)] for _ in range(29)]  # 29x23
        self.buttons = [0] * 11
        self.tools = pygame.Surface((475, 600))
        self.tools.fill(pygame.Color("grey"))
        self.step = step

    def insert_palette(self, palette):
        """Insert given palette into the grid."""
        palette_iter = iter(palette)
        for x in range(29):
            for y in range(23):
                try:
                    color = next(palette_iter)
                    self.data[x][y] = ColorCell(y, x, self.step, color)
                except StopIteration:
                    break

        # Добавляем кнопки
        for x in range(11):
            rect = pygame.Rect(0 + (20 * x * 2), 580, 40, 20)
            self.buttons[x] = Button(rect, "Resize")

    def draw_tools(self, padding=1):
        """Draw palette and buttons."""
        for row in self.data:
            for cell in row:
                if cell != 0:
                    cell.padding = padding
                    cell.draw_cell(self.tools)

        for button in self.buttons:
            if button != 0:
                button.draw_button(self.tools)

    def get_cell(self, pos):
        """Return cell of tools grid for given position."""
        x, y = pos
        grid_x = int(math.ceil((x - 805) / self.step))
        grid_y = int(math.ceil(y / self.step))

        if 0 <= grid_y < len(self.data) and 0 <= grid_x < len(self.data[0]):
            cell = self.data[grid_y][grid_x]
            return cell if cell != 0 else None
        return None

    def get_button(self, pos):
        """Return button on given coordinates."""
        x, y = pos
        for button in self.buttons:
            if button != 0 and button.rect.collidepoint(x - 805, y):
                return button
        return None


def main(image_name, target_rect):
    size = width, height = 1280, 800
    FPS = 10

    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    pygame.font.init()  # Опционально, но безопасно

    try:
        image = getImage(image_name)
    except Exception as e:
        print("Failed to load image:", e)
        pygame.quit()
        return

    pxarray = getPixelArray(image, target_rect)
    grid = FieldGrid(pxarray)
    tools = ToolsGrid()

    # Миниатюра
    thumbnails = pygame.Surface((480, 195))
    thumbnails.fill(pygame.Color("grey"))

    # Получаем пиксель-массив и палитру
    image_pixel, image_palette = grid.image_to_grid()
    tools.insert_palette(image_palette)

    # Первоначальная отрисовка
    te = pygame.surfarray.make_surface(image_pixel)
    thumbnails.blit(te, (10, 10))
    tools.draw_tools()
    grid.draw_field()

    done = False
    selected_color = None

    while not done:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    target_rect = target_rect.move(0, -1)
                elif event.key == pygame.K_DOWN:
                    target_rect = target_rect.move(0, 1)
                elif event.key == pygame.K_LEFT:
                    target_rect = target_rect.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    target_rect = target_rect.move(1, 0)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = mouse_pos
                if event.button == 1:  # ЛКМ
                    if 0 <= x <= 800 and 0 <= y <= 800:
                        row, col = grid.get_idx((x, y))
                        if selected_color:
                            grid.change_pixel(row, col, selected_color)
                            selected_color = None
                            grid.draw_field()
                    elif 805 <= x <= 1280 and 0 <= y < 580:
                        tools_cell = tools.get_cell((x, y))
                        if tools_cell:
                            selected_color = tools_cell.color
                            tools_cell.draw_cell(tools.tools, pygame.Color("red"))
                    elif 805 <= x <= 1280 and 580 <= y <= 600:
                        button = tools.get_button((x, y))
                        if button:
                            print("Button pressed:", button.color)

                elif event.button in (4, 5):  # Колёсико
                    rm = 5 if pygame.key.get_mods() & pygame.KMOD_CTRL else 1
                    if event.button == 4:  # Вверх
                        target_rect = target_rect.inflate(rm, rm)
                    elif event.button == 5:  # Вниз
                        target_rect = target_rect.inflate(-rm, -rm)
                        target_rect = target_rect.inflate(-rm, -rm)  # Защита от отрицательных размеров

                elif event.button == 3:  # ПКМ
                    print("Right click at:", x, y)

        # Обновление пикселей при изменении rect
        try:
            new_pxarray = getPixelArray(image, target_rect)
            grid.pxarray = new_pxarray
            grid.update_data()
            new_image_pixel, _ = grid.image_to_grid()
            grid.draw_field()
            te = pygame.surfarray.make_surface(new_image_pixel)
            thumbnails.fill(pygame.Color("grey"))
            thumbnails.blit(te, (10, 10))
        except Exception as e:
            print("Error updating pixel array:", e)

        # Отрисовка всего
        screen.fill(pygame.Color("black"))
        screen.blit(grid.field, (0, 0))
        screen.blit(tools.tools, (805, 0))
        screen.blit(thumbnails, (805, 605))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Image viewer and pixel editor')
    parser.add_argument('-i', '--image', required=True, help="Name of image in data/images dir (only .png)")
    parser.add_argument('-l', '--left', default=0, type=int, help="Left corner of the rect")
    parser.add_argument('-t', '--top', default=0, type=int, help="Top corner of the rect")
    parser.add_argument('-w', '--width', default=32, type=int, required=True, help="Width of the rect")
    parser.add_argument('-he', '--height', default=32, type=int, required=True, help="Height of the rect")
    args = parser.parse_args()

    target_rect = pygame.Rect(args.left, args.top, args.width, args.height)
    main(args.image, target_rect)