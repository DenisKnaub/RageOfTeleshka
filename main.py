# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:34:25 2022

@author: dKnau
"""

# База основного окна
import pygame
import pygame_menu
import random
import os
import source.mainMenu as mainMenu
import source.helpMenu as helpMenu
import source.mapMenu as mapMenu
import source.game as game

# Настройки окна
screen_width = 800
screen_height = 600
FPS = 60

# Инициализация игры
pygame.init()

# Окно по центру экрана
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Размер окна и FPS
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

mapMenu = mapMenu.getShipMenu(screen_width, screen_height)
helpMenu = helpMenu.getScoreMenu(screen_width, screen_height)
mainMenu = mainMenu.getMainMenu(screen_width, screen_height, [mapMenu, helpMenu])

mainMenu.mainloop(screen)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if mainMenu.is_enabled():
        mainMenu.update(events)
        mainMenu.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)