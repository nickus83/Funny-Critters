# -*- coding: utf-8 -*-
import os
import os.path as osp
import math
import pygame
from pygame.locals import *


def load_image(name, colorkey=None):

    fullname = osp.join('..', 'prj.data', 'images', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message

    image = image.convert()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image


def load_sound(name):

    class NoneSound:

        def play(self): pass

    if not pygame.mixer:
        return NoneSound()

    fullname = osp.join('..', 'prj.data', name)

    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message

    return sound


def load_png(name, colorkey=None):

    fullname = osp.join('..', 'prj.data', 'images', name)

    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message

    image = image.convert_alpha()

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    return image


def import_images():
    forest_source = load_png("forest.png")
    animals_source = load_png("animals1.png")
    wolf_source = load_png("wolf.png")

    return [dict(background_tile=forest_source.subsurface(0, 0, 32, 32),
                 hubble2=forest_source.subsurface(32, 0, 32, 32),
                 hubble1=forest_source.subsurface(64, 0, 32, 32),
                 hubble5=forest_source.subsurface(96, 0, 32, 32),
                 stump1=forest_source.subsurface(128, 0, 32, 32),
                 rocks3=forest_source.subsurface(160, 0, 32, 32),
                 bush_flower1=forest_source.subsurface(192, 0, 32, 32),
                 bush_flower2=forest_source.subsurface(224, 0, 32, 32),

                 hubble3=forest_source.subsurface(32, 32, 32, 32),
                 hubble_flower=forest_source.subsurface(64, 32, 32, 32),
                 hubble6=forest_source.subsurface(96, 32, 32, 32),
                 stump2=forest_source.subsurface(128, 32, 32, 32),
                 rocks2=forest_source.subsurface(160, 32, 32, 32),
                 bush1=forest_source.subsurface(192, 32, 32, 32),
                 bush2=forest_source.subsurface(224, 32, 32, 32),

                 nenuphar1=forest_source.subsurface(0, 64, 32, 32),
                 nenuphar2=forest_source.subsurface(32, 64, 32, 32),
                 sprout1=forest_source.subsurface(64, 64, 32, 32),
                 sprout2=forest_source.subsurface(96, 64, 32, 32),
                 mushroums=forest_source.subsurface(128, 64, 32, 32),
                 rocks1=forest_source.subsurface(160, 64, 32, 32),
                 wood1=forest_source.subsurface(192, 64, 32, 32),
                 wood2=forest_source.subsurface(224, 64, 32, 32),

                 ),
            dict(grass1=forest_source.subsurface(96, 96, 32, 32),
                 grass3=forest_source.subsurface(96, 128, 64, 64),
                 grass2=forest_source.subsurface(128, 96, 32, 32),
                 grass4=forest_source.subsurface(0, 96, 96, 96),
                 ),
            dict(
                pig_down1=animals_source.subsurface(0, 0, 48, 48),
                pig_down0=animals_source.subsurface(48, 0, 48, 48),
                pig_down2=animals_source.subsurface(96, 0, 48, 48),
                pig_left1=animals_source.subsurface(0, 48, 48, 48),
                pig_left0=animals_source.subsurface(48, 48, 48, 48),
                pig_left2=animals_source.subsurface(96, 48, 48, 48),
                pig_right1=animals_source.subsurface(0, 96, 48, 48),
                pig_right0=animals_source.subsurface(48, 96, 48, 48),
                pig_right2=animals_source.subsurface(96, 96, 48, 48),
                pig_up1=animals_source.subsurface(0, 144, 48, 48),
                pig_up0=animals_source.subsurface(48, 144, 48, 48),
                pig_up2=animals_source.subsurface(96, 144, 48, 48),

                goat_down1=animals_source.subsurface(144, 0, 48, 48),
                goat_down0=animals_source.subsurface(192, 0, 48, 48),
                goat_down2=animals_source.subsurface(240, 0, 48, 48),
                goat_right1=animals_source.subsurface(144, 48, 48, 48),
                goat_right0=animals_source.subsurface(192, 48, 48, 48),
                goat_right2=animals_source.subsurface(240, 48, 48, 48),
                goat_left1=animals_source.subsurface(144, 96, 48, 48),
                goat_left0=animals_source.subsurface(192, 96, 48, 48),
                goat_left2=animals_source.subsurface(240, 96, 48, 48),
                goat_up1=animals_source.subsurface(144, 144, 48, 48),
                goat_up0=animals_source.subsurface(192, 144, 48, 48),
                goat_up2=animals_source.subsurface(240, 144, 48, 48),

                Sheep_down1=animals_source.subsurface(288, 0, 48, 48),
                Sheep_down0=animals_source.subsurface(336, 0, 48, 48),
                Sheep_down2=animals_source.subsurface(384, 0, 48, 48),
                Sheep_left1=animals_source.subsurface(288, 48, 48, 48),
                Sheep_left0=animals_source.subsurface(336, 48, 48, 48),
                Sheep_left2=animals_source.subsurface(384, 48, 48, 48),
                Sheep_right1=animals_source.subsurface(288, 96, 48, 48),
                Sheep_right0=animals_source.subsurface(336, 96, 48, 48),
                Sheep_right2=animals_source.subsurface(384, 96, 48, 48),
                Sheep_up1=animals_source.subsurface(288, 144, 48, 48),
                Sheep_up0=animals_source.subsurface(336, 144, 48, 48),
                Sheep_up2=animals_source.subsurface(384, 144, 48, 48),

                Wolf_down1=wolf_source.subsurface(0, 0, 64, 64),
                Wolf_down0=wolf_source.subsurface(64, 0, 64, 64),
                Wolf_down2=wolf_source.subsurface(128, 0, 64, 64),
                Wolf_left1=wolf_source.subsurface(0, 64, 64, 32),
                Wolf_left0=wolf_source.subsurface(64, 64, 64, 32),
                Wolf_left2=wolf_source.subsurface(128, 64, 64, 32),
                Wolf_right1=wolf_source.subsurface(0, 114, 64, 32),
                Wolf_right0=wolf_source.subsurface(64, 114, 64, 32),
                Wolf_right2=wolf_source.subsurface(128, 114, 64, 32),
                Wolf_up1=wolf_source.subsurface(0, 154, 64, 38),
                Wolf_up0=wolf_source.subsurface(64, 154, 64, 38),
                Wolf_up2=wolf_source.subsurface(128, 154, 64, 38),
    )]

def round_32(x, base=32):
    """Round x to base. Default 32."""
    if x == 0:
        return 0
    else:
        return int(math.ceil(float(x) / base)) - 1