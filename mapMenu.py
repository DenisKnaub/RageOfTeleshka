import pygame_menu
import pygame
import pickle
import glob
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
import mainMenu as mainMenu

def loadMap(): # считываем все svg карты
    for filename in glob.glob('map\*.svg'):
        drawing = svg2rlg(filename)
        image_path = renderPM.drawToFile(drawing, str(filename[:-3]) + 'png', fmt='PNG') # сохраняем в png

def sizePNG(): # считываем все png картинки и меняем на нужный размер
    for filename in glob.glob('map\*.png'):
        img = Image.open(filename)
        width, height = img.size
        if width != 100 and height != 75:
            new_image = img.resize((100, 75))
            new_image.save(filename)

def loadPNG(pngMap): # загружаем автоматически все картинки для отображения в меню Карт
    i = 1 # номер эелемента картинки
    for filename in glob.glob('map\*.png'): 
        pngMap.append((filename[4:] ,filename[:3] + "/" +  filename[4:])) # заносим все картинки в массив
        i+=1
    return pngMap

def framePreset(frame, widget):
    frame = frame.pack(widget,
                        align=pygame_menu.locals.ALIGN_CENTER,
                        vertical_position=pygame_menu.locals.POSITION_CENTER,
                        margin=(0, 10)
                        )
    return frame

def changeShip(path, widget):
    print(path)
    global shipFile
    shipFile = path
    # im = menu.get_widget("image")
    widget.set_image(pygame_menu.baseimage.BaseImage(path))
    
def saveMap(shipFile):
    settings = shipFile
    with open('settings.txt', 'w') as f: # заносим в файл с выбранной картой
      f.write(settings)
    f.close()
    # global y
    # y+=1
    # menu.add.label(str(y) + ". " + settings[4:], max_char=-1, font_size=18, font_color = (255,255,255))
    return settings

# def saveMap():
#     settings = shipFile
#     with open('settings.txt', 'w') as f: # заносим в файл с выбранной картой
#       f.write(settings)
#     f.close()
#     global y
#     y+=1
#     menu.add.label(str(y) + ". " + settings[4:], max_char=-1, font_size=18, font_color = (255,255,255))
#     return settings

def getShipMenu(screen_width, screen_height):
    global y
    y = 1 # индекс выбранной картинки
    # это самое первое изображение в меню карт, оно должно быть обьявлено так    
    pngMap = []    
    # def loadMap(): # считываем все svg карты
    #     for filename in glob.glob('map\*.svg'):
    #         drawing = svg2rlg(filename)
    #         image_path = renderPM.drawToFile(drawing, str(filename[:-3]) + 'png', fmt='PNG') # сохраняем в png
   
            
    # def sizePNG(): # считываем все png картинки и меняем на нужный размер
    #     for filename in glob.glob('map\*.png'):
    #         img = Image.open(filename)
    #         width, height = img.size
    #         if width != 100 and height != 75:
    #             new_image = img.resize((100, 75))
    #             new_image.save(filename)
                
            
    # def loadPNG(): # загружаем автоматически все картинки для отображения в меню Карт
    #     i = 1 # номер эелемента картинки
    #     for filename in glob.glob('map\*.png'): 
    #         pngMap.append((filename[4:] ,filename[:3] + "/" +  filename[4:])) # заносим все картинки в массив
    #         i+=1

    global menu
    loadMap()
    sizePNG()
    pngMap = loadPNG(pngMap)
    print(pngMap)

    shipFile1 = pngMap[0][1] # первая картинка для отображения    

    # def changeShip(value, ship):
    #     global shipFile
    #     shipFile = ship
    #     im = menu.get_widget("image")
    #     im.set_image(pygame_menu.baseimage.BaseImage(shipFile))
 
   
    
    # def framePreset(frame, widget):
    #     frame = frame.pack(widget,
    #                        align=pygame_menu.locals.ALIGN_CENTER,
    #                        vertical_position=pygame_menu.locals.POSITION_CENTER,
    #                        margin=(0, 10)
    #                        )
    #     return frame

    def widgetPreset(widget):
        widget._background_color = (16, 51, 83)
        widget.set_border(1, (54, 211, 233))
        return widget
    

    # def saveMap():
    #     settings = shipFile
    #     with open('settings.txt', 'w') as f: # заносим в файл с выбранной картой
    #       f.write(settings)
    #     f.close()
    #     global y
    #     y+=1
    #     menu.add.label(str(y) + ". " + settings[4:], max_char=-1, font_size=18, font_color = (255,255,255))
    #     return "Картинка сохранена"

    background_image = pygame_menu.BaseImage(
        image_path="images/Menu.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
    )
    
   
    # Make beauty here
    mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
    mytheme.title_background_color = (0, 0, 0)
    mytheme.background_color = background_image
    mytheme.title_font = pygame_menu.font.FONT_FIRACODE_BOLD
    mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    mytheme.widget_font_color = (54, 211, 233)

    
    menu = pygame_menu.Menu('Select a map', screen_width, screen_height, theme=mytheme)
    
    framy = menu.add.frame_v(width=screen_width * 0.6, height=screen_height * 0.6)
   
    framePreset(framy, widgetPreset(menu.add.image(shipFile1, scale=(1, 1), image_id="image" )))
    widgetImage = menu.get_widget("image")
    framePreset(framy, widgetPreset(menu.add.selector(
        "",
        pngMap,
        selector_id= 'mapMenu',
        # onchange=changeShip
        onchange = lambda value, shipPath: changeShip(value[0][1], widgetImage)             
    )))
    framePreset(framy, widgetPreset(menu.add.button('Сохранить', lambda:  saveMap(menu.get_widget('mapMenu').get_value()[0][1]))))
    framePreset(framy, widgetPreset(menu.add.button('Назад', pygame_menu.events.BACK)))
    
    file2 = open('settings.txt', 'r', encoding = "Windows-1251").read()
    menu.add.label(str(y) + ". " + file2[4:], max_char=-1, font_size=18, font_color = (255,255,255))
    
    return menu
