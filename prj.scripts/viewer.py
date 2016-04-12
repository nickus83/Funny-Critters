# -*- coding: utf-8 -*-
import os
import os.path as osp
import math
import numpy as np
import pygame
import random
from pygame.locals import *


path = r"C:\Users\utkin\Documents\GitHub\Funny-Critters\prj.data\images\animal_test.png"
# path = r"C:\Users\utkin\Documents\GitHub\Funny-Critters\prj.data\images\test.png"


def getPixelArray(filename):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    assert(image.get_size()[0] == image.get_size()[1])
    return pygame.surfarray.pixels3d(image)


def make_grid((width, height), step=80):
    grid = []
    for x in xrange(width / step):
        grid.append([])
        for y in xrange(height / step):
            grid[x].append(pygame.Color("grey"))
    return grid


def draw_field(field, grid, step=80, padding=1):

    width, height = field.get_size()

    for x in xrange(width / step):
        for y in xrange(height / step):
            field.fill(grid[x][y], (x * step + padding,
                                    y * step + padding,
                                    step - padding,
                                    step - padding))


def image_to_grid(grid, pxarray):

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
            grid[row][column] = color

    temp_list = list(temp_set)
    for r, g, b in temp_list:
        palette.append(pygame.Color(r, g, b))
    return pxarray, palette


def draw_tools(tools, grid, step=20, padding=1):
    width, height = tools.get_size()

    for row in xrange(len(grid)):
        for column in xrange(len(grid[row])):
            tools.fill(grid[row][column], (column * step + padding,
                                           row * step + padding,
                                           step - padding,
                                           step - padding))


def main():
    size = width, height = 1280, 800
    FPS = 10
    screen = pygame.display.set_mode(size, 0)
    clock = pygame.time.Clock()

    pxarray = getPixelArray(path)  # only square images apply

    field = pygame.Surface((800, 800))  # main area with image
    grid_step = 800 / len(pxarray[0])
    # grid_step = 20
    grid = make_grid(field.get_size(), grid_step)

    tools = pygame.Surface((475, 600))  # color palette and buttons
    tools.fill(pygame.Color("grey"))
    tools_grid = []

    tumbnails = pygame.Surface((480, 195))  # thumbnails
    tumbnails.fill(pygame.Color("grey"))

    image, image_palette = image_to_grid(grid, pxarray)
    # import pdb; pdb.set_trace()
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

    draw_field(field, grid, grid_step)

    done = False

    while not done:  # main loop
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
            elif event.type == pygame.QUIT:
                done = True

        screen.blit(field, (0, 0))
        screen.blit(tools, (805, 0))
        screen.blit(tumbnails, (805, 605))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
