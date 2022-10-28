import pygame_menu
import pickle

def widgetPreset(widget):
        widget._background_color = (16, 51, 83)
        widget.set_border(1, (54, 211, 233))
        return widget

def framePreset(frame, widget):
    frame = frame.pack(widget,
                        align=pygame_menu.locals.ALIGN_CENTER,
                        vertical_position=pygame_menu.locals.POSITION_CENTER,
                        margin=(0, 10)
                        )
    return frame

def getScoreMenu(screen_width, screen_height):

    # def framePreset(frame, widget):
    #     frame = frame.pack(widget,
    #                        align=pygame_menu.locals.ALIGN_CENTER,
    #                        vertical_position=pygame_menu.locals.POSITION_CENTER,
    #                        margin=(0, 10)
    #                        )
    #     return frame

    # def widgetPreset(widget):
    #     widget._background_color = (16, 51, 83)
    #     widget.set_border(1, (54, 211, 233))
    #     return widget


    background_image = pygame_menu.BaseImage(
        image_path="images/Menu.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
    )

    # Make beauty here
    mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
    mytheme.title_background_color = (1, 1, 1)
    mytheme.background_color = background_image
    mytheme.title_font = pygame_menu.font.FONT_FIRACODE_BOLD
    mytheme.widget_font = pygame_menu.font.FONT_OPEN_SANS_BOLD
    mytheme.widget_font_color = (1, 1, 1)

    menu = pygame_menu.Menu('User manual', screen_width, screen_height, theme=mytheme)
    
    HELP = 'ЗАПУСК ЭМУЛЯЦИИ\n' \
             'Нажать на кнопку "Start" в главном меню\n' \
                 'СОЗДАНИЕ КАРТЫ\n' \
                     'Карта создается в графическом редакторе Inkscape размером 800*600. \n' \
                         'Робот обязательно рисуется черного цвета в виде квадрата! \n' \
                             'По контуру рисуются стены в виде прямоугольников, отличающихся по цвету от робота. \n' \
                                'ДОБАВЛЕНИЕ КАРТЫ В ПРОГРАММУ\n' \
                                    'Чтобы добавить карту, необходимо загрузить ее svg файл в папку map.\n' \
                                        'Открыть svg код карты, в самый низу или чуть выше удалить фрагмент строки.\n' \
                                            'с ним почему-то карта не рисуется.\n' \
                                             'Пример: <rect style="fill:#000000;stroke-width:0.523844">, после удаления <rect style="fill:#000000 >. \n'\
                                                 'Сделать это нужно лишь в одной строке, где имеется этот фрагмент\n'\
                                                    'УДАЛЕНИЕ КАРТЫ\n' \
                                                        'Чтобы удалить карту, необходимо удалить svg и png файл из папки map\n' \
                                                            'ВЫБОР КАРТЫ\n' \
                                                                'Зайти в меню карты, выбрать нужную карту и нажать кнопку "Сохранить"\n' \
                                                                    '(Если нужно будет выбрать первую отобразившуюся карту при загрузке меню.\n' \
                                                                        'Пролисните до следующей и вернитесь к первой и нажмите кнопку "Сохранить")\n' \
                                                                            'СОХРАНЁННАЯ КАРТА\n' \
                                                                                'Путь выбранной карты, будет внесён в файл settings.txt \n' \
                                                                                    'ПОРТ ПОДКЛЮЧЕНИЯ\n' \
                                                                                        'Если будет ошибка:  \n' \
                                                                                            '[WinError 10048] Обычно разрешается только одно использование адреса сокета (протокол/сетевой адрес/порт)\n' \
                                                                                                'Необходимо поменять порт подключения он находится в файле port.txt \n' \
       
                                                           
    menu.add.label(HELP, max_char=-1, font_size=18, selectable=True, font_color = (255,255,255))
    


    framy = menu.add.frame_v(width=screen_width * 0.6, height=screen_height * 0.6)
    
    framePreset(framy, widgetPreset(menu.add.button('Назад', pygame_menu.events.BACK)))

    return menu
