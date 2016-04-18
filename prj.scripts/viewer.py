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

    assert(part.get_size()[0] == part.get_size()[1])
    return pygame.surfarray.pixels3d(part)


def make_FieldGrid((width, height), step=80):

    FieldGrid = []
    for x in xrange(width / step):
        FieldGrid.append([])
        for y in xrange(height / step):
            FieldGrid[x].append(pygame.Color("grey"))
    return FieldGrid


class FieldCell(object):
    """Cell with the color of corresonding pixel in the field area."""

    def __init__(self, x, y, size, color, padding=1):
        super(FieldCell, self).__init__()

        self.rect = pygame.Rect((x * size, y * size), (size, size))
        self.color = color
        self.padding = padding

    def draw_cell(self, surface):
        surface.fill(
            self.color, self.rect.inflate(-self.padding, -self.padding))


class FieldGrid(object):
    """FieldGrid describing loading image"""

    def __init__(self, (width, height), step=80):
        super(FieldGrid, self).__init__()
        self.data = []

        for x in xrange(width / step):
            self.data.append([])
            for y in xrange(height / step):
                self.data[x].append(pygame.Color("grey"))

        self.step = step

    def image_to_FieldGrid(self, pxarray):

        palette = []
        temp_set = set()
        HEIGHT = WIDTH = len(pxarray[0])

        for row in xrange(HEIGHT):
            for column in xrange(WIDTH):
                color = pygame.Color(int(pxarray[row][column][0]),
                                     int(pxarray[row][column][1]),
                                     int(pxarray[row][column][2]))
                temp_set.add((int(pxarray[row][column][0]),
                              int(pxarray[row][column][1]),
                              int(pxarray[row][column][2])))

                self.data[row][column] = FieldCell(
                    row, column, self.step, color)

        temp_list = list(temp_set)
        for r, g, b in temp_list:
            palette.append(pygame.Color(r, g, b))
        return pxarray, palette

    def draw_field(self, field, padding=1):

        width, height = field.get_size()

        for x, row in enumerate(self.data):
            for y, column in enumerate(row):
                column.padding = padding
                column.draw_cell(field)

    def get_idx(self, pos):
        """Return cell of grid for given position."""

        row, column = (int(math.ceil(pos[0] / self.step)),
                       int(math.ceil(pos[1] / self.step)))
        print(row, column)
        return self.data[row][column]


def draw_tools(tools, FieldGrid, step=20, padding=1):
    width, height = tools.get_size()

    for x, row in enumerate(FieldGrid):
        for y, column in enumerate(FieldGrid[x]):
            tools.fill(FieldGrid[x][y], (x * step + padding,
                                         y * step + padding,
                                         step - padding,
                                         step - padding))


def get_mouse_pos(x, y):
    """Returns where is mouse pinter"""


def main(image_name, target_rect):
    size = width, height = 1280, 800
    FPS = 10
    screen = pygame.display.set_mode(size, 0)
    clock = pygame.time.Clock()

    pxarray = getPixelArray(image_name,
                            target_rect)

    field = pygame.Surface((800, 800))  # main area with image
    grid_step = 800 / len(pxarray[0])

    grid = FieldGrid(field.get_size(), grid_step)
    # FieldGrid = make_FieldGrid(field.get_size(), FieldGrid_step)

    tools = pygame.Surface((475, 600))  # color palette and buttons
    tools.fill(pygame.Color("grey"))
    tools_grid = []

    tumbnails = pygame.Surface((480, 195))  # thumbnails
    tumbnails.fill(pygame.Color("grey"))

    image, image_palette = grid.image_to_FieldGrid(pxarray)

    row_tool_count = column_tool_count = 0
    tools_grid.append([])
    for color in image_palette:
        if row_tool_count <= 23:
            tools_grid[column_tool_count].append(color)
            row_tool_count += 1
        elif column_tool_count <= 29:
            tools_grid.append([])
            column_tool_count += 1
            tools_grid[column_tool_count].append(color)

    draw_tools(tools, tools_grid)

    te = pygame.surfarray.make_surface(image)
    tumbnails.blit(te, (10, 10))

    grid.draw_field(field)

    done = False

    while not done:  # main loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 0 <= pos[0] <= 800 and 0 <= pos[1] <= 800: # in the field area
                    target_cell = grid.get_idx(pos)
                elif 805 <= pos[0] <= 1280 and 0 <= pos[1] <= 600:
                    print("Tools")

            elif event.type == pygame.QUIT:
                done = True

        screen.blit(field, (0, 0))
        screen.blit(tools, (805, 0))
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
