# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 12:39:23 2022

@author: dKnau
"""

import pygame_menu
import source.game as game
import sys
import pygame


def getMainMenu(screen_width, screen_height, menus):
    
    screen_width = 800
    screen_height = 600
    file = open('settings.txt', 'r', encoding = "Windows-1251").read()        
    def framePreset(frame, widget):
        frame = frame.pack(widget,
                    align=pygame_menu.locals.ALIGN_CENTER,
                    vertical_position=pygame_menu.locals.POSITION_CENTER,
                    margin=(0,10)
                    )
        return frame

    def widgetPreset(widget):
        widget._background_color = (16, 51, 83)
        widget.set_border(1, (54, 211, 233))
        widget.margin=(0,10)
        widget.width = 100
        return widget
    
         
    shipMenu = menus[0]
    helpMenu = menus[1]

    background_image = pygame_menu.BaseImage(
        image_path = "images/Menu.png",
        drawing_mode = pygame_menu.baseimage.IMAGE_MODE_FILL
    )

    # Make beauty here
    mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
    mytheme.title_background_color = (0, 0, 0)
    mytheme.background_color = background_image
    mytheme.title_font = pygame_menu.font.FONT_FIRACODE_BOLD
    mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    mytheme.widget_font_color = (54, 211, 233)

    global menu
    menu = pygame_menu.Menu('RageOfTeleshka', screen_width, screen_height, theme=mytheme)

         
    menu.add.menu_link(shipMenu, "mapMenu")
    menu.add.menu_link(helpMenu, "helpMenu")

    framy = menu.add.frame_v(width=screen_width * 0.6, height=screen_height * 0.6
    )

    
    framePreset(framy, widgetPreset(menu.add.button('Start', game.playGame,
                                                    menu, screen_width, screen_height)))
    framePreset(framy, widgetPreset(menu.add.button('Map', menu.get_widget("mapMenu").open)))
    framePreset(framy, widgetPreset(menu.add.button('Help', menu.get_widget("helpMenu").open)))
    framePreset(framy, widgetPreset(menu.add.button('Exit', pygame_menu.events.EXIT)))   
    
    
        
    return menu






