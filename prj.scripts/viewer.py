# -*- coding: utf-8 -*-
import os
import os.path as osp
import math
import numpy as np
import pygame
import random
import sys
from pygame.locals import *


def getPixelArray(filename, rect=None):

    sys.path.append("../prj.core")
    try:
        from utils import load_png
    except Exception, e:
        print(e)
    finally:
        del sys.path[-1]

    try:
        image = load_png(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message

    part = image.subsurface(rect)

    assert(part.get_size()[0] == part.get_size()[1])  # only square images
    return pygame.surfarray.pixels3d(part)


class ColorCell(object):
    """Cell with the color of corresonding pixel in the field area."""

    def __init__(self, x, y, size, color, padding=1):
        super(ColorCell, self).__init__()

        self.rect = pygame.Rect((x * size, y * size), (size, size))
        self.color = color
        self.padding = padding

    def draw_cell(self, surface):
        surface.fill(
            self.color, self.rect.inflate(-self.padding, -self.padding))


class FieldGrid(object):
    """FieldGrid describing loading image"""

    def __init__(self, pxarray):
        super(FieldGrid, self).__init__()
        self.data = []
        self.step = 800 / len(pxarray[0])
        self.pxarray = pxarray
        self.field = pygame.Surface((800, 800))

        width, height = self.field.get_size()

        for x in xrange(len(pxarray[0])):
            self.data.append([])
            for y in xrange(len(pxarray[0])):
                self.data[x].append(None)

    def image_to_FieldGrid(self):

        palette = []
        temp_set = set()
        HEIGHT = WIDTH = len(self.pxarray[0])

        for row in xrange(HEIGHT):
            for column in xrange(WIDTH):
                color = pygame.Color(int(self.pxarray[row][column][0]),
                                     int(self.pxarray[row][column][1]),
                                     int(self.pxarray[row][column][2]))
                temp_set.add((int(self.pxarray[row][column][0]),
                              int(self.pxarray[row][column][1]),
                              int(self.pxarray[row][column][2])))

                cell = ColorCell(row, column, self.step, color)
                self.data[row][column] = cell

        temp_list = list(temp_set)
        for r, g, b in temp_list:
            palette.append(pygame.Color(r, g, b))
        return self.pxarray, palette

    def draw_field(self, padding=1):

        width, height = self.field.get_size()
        for x, row in enumerate(self.data):
            for y, column in enumerate(row):
                try:
                    column.padding = padding
                    column.draw_cell(self.field)
                except Exception as e:
                    print(e)

    def get_idx(self, pos):
        """Return cell of field grid for given position."""

        row, column = (int(math.ceil(pos[0] / self.step)),
                       int(math.ceil(pos[1] / self.step)))
        print(row, column)
        return self.data[row][column]


class ToolsGrid(object):
    """Grid for tools area."""

    def __init__(self, step=20):
        super(ToolsGrid, self).__init__()
        self.data = []

        self.tools = pygame.Surface((475, 600))
        self.tools.fill(pygame.Color("grey"))
        self.step = step
        self.width, self.height = self.tools.get_size()

        for x in xrange(20):
            self.data.append([])
            for y in xrange(23):
                self.data[x].append(0)

        self.step = step

    def insert_palette(self, palette):
        """Save given platte."""
        for x, row in enumerate(self.data):
            for y, column in enumerate(row):
                if len(palette) > 0:
                    self.data[x][y] = ColorCell(y, x, self.step, palette.pop())
                else:
                    column = 0

    def draw_tools(self, padding=1):
        """Draw palette."""
        width, height = self.tools.get_size()

        for x, row in enumerate(self.data):
            for y, column in enumerate(row):
                if column != 0:
                    # print(column.rect)
                    column.padding = padding
                    column.draw_cell(self.tools)

    def get_idx(self, pos):
        """Return cell of tools grid for given position."""
        
        row, column = (int(math.ceil((pos[0] - 805)/ self.step)),
                       int(math.ceil(pos[1] / self.step)))
        
        if self.data[column][row] != 0:
            return self.data[column][row]


def main(image_name, target_rect):
    size = width, height = 1280, 800
    FPS = 10
    screen = pygame.display.set_mode(size, 0)
    clock = pygame.time.Clock()

    pxarray = getPixelArray(image_name, target_rect)

    # main area with image
    grid = FieldGrid(pxarray)
    tools = ToolsGrid()


    tumbnails = pygame.Surface((480, 195))  # thumbnails
    tumbnails.fill(pygame.Color("grey"))

    image, image_palette = grid.image_to_FieldGrid()
    tools.insert_palette(image_palette)

    te = pygame.surfarray.make_surface(image)
    tumbnails.blit(te, (10, 10))

    tools.draw_tools()
    grid.draw_field()

    done = False
    field_cell = None

    while not done:  # main loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 0 <= pos[0] <= 800 and 0 <= pos[1] <= 800:  # in the field area
                    field_cell = grid.get_idx(pos)
                    print(field_cell.color)
                    # target_cell.color = pygame.Color(255, 255, 255)
                    # target_cell.draw_cell(grid.field)
                elif 805 <= pos[0] <= 1280 and 0 <= pos[1] <= 600:
                    tools_cell = tools.get_idx(pos)
                    if tools_cell:
                        print(tools_cell.color)
            elif event.type == pygame.QUIT:
                done = True

        screen.blit(grid.field, (0, 0))
        screen.blit(tools.tools, (805, 0))
        screen.blit(tumbnails, (805, 605))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser(description='image viewer')
    p.add_argument('-i', '--image', required=True,
                   help="name of image in data/images dir (only .png)")
    p.add_argument('-l', '--left', default=0, type=int,
                   required=False, help="left corner of the rect taken out of the picture")
    p.add_argument('-t', '--top', default=0, type=int,
                   required=False, help="top corner of the rect taken out of the picture")
    p.add_argument('-w', '--width', default=32, type=int,
                   required=True, help="width of the rect taken out of the picture")
    p.add_argument('-he', '--height', default=32, type=int,
                   required=True, help="height of the rect taken out of the picture")
    args = p.parse_args()

    target_rect = pygame.Rect(args.left, args.top, args.width, args.height)

    main(args.image, target_rect)
