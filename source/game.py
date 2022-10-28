# -*- coding: utf-8 -*-
"""
Created on Thu May  5 22:45:29 2022

@author: dKnau
"""

import pygame
import random
from os import path
import datetime
import pickle
from datetime import date
import source.mapFromFile as mapFromFile
import pygame as pg
import sys
import socket 
import os
import math

def socketConnected(port):
    ############### Подключение Сокет Сервер ##############################
    os.system("start python client.py") # запускаем клиента в отдельном окне
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет
    sock.bind(('', int(port))) # свяжем наш сокет с данными хостом и портом (9090) с помощью метода bind
    sock.listen(1) # С помощью метода listen мы запустим для данного сокета режим прослушивания, очередь
    global conn
    global cl
    conn, addr = sock.accept() # принять подключение с помощью метода accept, который возвращает кортеж с двумя элементами: новый сокет и адрес клиента    
    print ('connected:', addr)
    cl = 'Close'
    return 'connected', port, conn
    #####################################################

def downloadMap():
    # загружаем сохранённую карту
    global file
    file = open('settings.txt', 'r', encoding = "Windows-1251").read().split('.')
    file = file[0] +'.svg'
    print(file)
    return file

def closeConnected(port):
    # обновляем порт для следующего запуска    
    port1 = int(port) - 1 # удаляю по 1 чтобы был новый порт в следующий раз
    with open('port.txt', 'w') as f:
          f.write(str(port1))
    f.close()
    conn.close() # закрываем сервер
    print ('Сервер закрыт')
    return port1, "Сервер закрыт"
    
def playGame(menu, screen_width, screen_height):
    
    # ############### Подключение Сокет Сервер ##############################
    # os.system("start python client.py") # запускаем клиента в отдельном окне
    # port = open('port.txt', 'r', encoding = "utf-8").read() # из за того что каждый раз нужен новый порт и я хз как по другому сделать, будет так    
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создаем сокет
    # sock.bind(('', int(port))) # свяжем наш сокет с данными хостом и портом (9090) с помощью метода bind
    # sock.listen(1) # С помощью метода listen мы запустим для данного сокета режим прослушивания, очередь
    # conn, addr = sock.accept() # принять подключение с помощью метода accept, который возвращает кортеж с двумя элементами: новый сокет и адрес клиента    
    # print ('connected:', addr)
    # cl = 'Close'
    # return 'connected'
    # #####################################################
    
    img_dir = path.join(path.dirname(__file__), 'images')
  
    menu.disable()
    menu.full_reset()
    
    # mapFromFile.loadMap()
    # загружаем сохранённую карту
    # file = open('settings.txt', 'r', encoding = "Windows-1251").read().split('.')
    # file = file[0] +'.svg'
    # print(file)
    port = open('port.txt', 'r', encoding = "utf-8").read() # из за того что каждый раз нужен новый порт и я хз как по другому сделать, будет так    
    socketConnected(port)
    downloadMap()
    WIDTH = screen_width + 200 # 800 + 200
    HEIGHT = screen_height
    FPS = 60

    # Задаем цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLACK)
    pygame.display.set_caption("RageOfTeleshka")
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font('arial')  
    
    #вот тут карта отрисовывается 
    firstMap = mapFromFile.mapParse()
    firstMap.CreateFrame(file)
       
    index = firstMap.GetObjectCount() # получаем длину firstMap.wallList
    
    #рисуем карту
    def draw(index):
        for i in range(index):
            r = firstMap.GetObjectN(i)
            pygame.draw.rect(screen, (255, 255, 0), (r[0], r[1], r[2], r[3]))
            
    draw(index) # отрисовываем карту 
        
    pygame.display.update()
    
    # текст рисует (показания датчиков)
    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)
        

    # отрисовка робота
    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            # эта часть загружает картинку робота
            self.image = pygame.transform.scale(player_img, (firstMap.GetRobotHeight(),firstMap.GetRobotWidth()))
            self.image = pygame.transform.rotate(self.image, -90)
            self.startImage = self.image
            self.image.set_colorkey(BLACK)
            # эта часть просто рисует квадрат вместо картинки робота
            # self.image = pygame.Surface((firstMap.GetRobotWidth(), firstMap.GetRobotHeight()))
            # self.image.fill(GREEN)
            self.rect = self.image.get_rect()            
            self.radius = 20 * 1.0
            #положение робота
            self.rect.x = x * 1.0
            self.rect.y = y * 1.0
            self.speedx = 0 * 1.0
            
     
        def update(self):
            # print(math.degrees(firstMap.GetRobotAngle()))       
            self.image = pygame.transform.rotate(self.startImage, math.degrees(firstMap.GetRobotAngle()))
            self.rect.x = firstMap.GetRobotX()  
            self.rect.y = firstMap.GetRobotY() 
            

    # указываем путь до робота
    player_img = pygame.image.load(path.join("images/playerShip1_blue.png")).convert()
    
    all_sprites = pygame.sprite.Group()
    player = Player(firstMap.GetRobotX(), firstMap.GetRobotY())
    all_sprites.add(player)
    
    # добавлние датчиков (дальномер)
    # для добавления датчика, необходимо вставить строку firstMap.addNewCensLen(0) и в скобках указать угол, куда он должен смотреть
    firstMap.addNewCensLen(0) 
    firstMap.addNewCensLen(90) 
    firstMap.addNewCensLen(-90) 
    firstMap.addNewCensLen(-180) 
    firstMap.addNewCensLen(45) 
    firstMap.addNewCensLen(-45) 
    firstMap.addNewCensLen(-135) 
    firstMap.addNewCensLen(135) 
          
    # Цикл эмуляции 
    running = True
    while running:
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                screen = pygame.display.set_mode((WIDTH - 200, HEIGHT))
                conn.sendall(cl.encode()) # отсылаем сообщение о закрытии общения сокетов
                running = False # останавливаем цикл
                       
        ###################### Общение сервера с клиентом ########################
        
        # в data будем получать указания для движения, они в байтах, поэтому нужно декодировать их
        data = conn.recv(1024) # Чтобы получить данные нужно воспользоваться методом recv, который в качестве аргумента принимает количество байт для чтения.
        print('Получил server ' + str(data))
        
        if data.decode() == 'Close': # если получили сообщение закрыть, прекращаем общение
            break 
        
        if not data: # если нет данных продолжаем считывать
            continue
        
        mss = data.decode() # декодируем сообщение от клиента
        firstMap.newMove(int(mss[0]), int(mss[1]), int(mss[2]), int(mss[3])) # даём роботу команду на передвижение (Например 1111, 1100 и т.д.)
                
        # в send будем отправлять показания с датчико
        sendall = str(firstMap.robotMove(1))
        
        for e in range(len(firstMap.censLengList)): # заносим все показания с датчиков в одну строку и отправляем клиенту
            sendall = sendall + ',' + str(round(firstMap.checkCensor(e)))
            
        #print(sendall)
        conn.send(sendall.encode()) 
        #########################################################################
             
        # print(firstMap.GetRobotX(), firstMap.GetRobotY()) # координаты робота
        
        # Обновление        
        all_sprites.update()
        # Рендеринг
        screen.fill(BLACK)
        o = 40 # y для отображения     
        draw_text(screen, "Показания датчиков!", 18, 900, 10)
        # все датчики выводятся по порядку
        for q in range(len(firstMap.censLengList)):
            draw_text(screen, "Дальномер № " + str(q + 1) + ': ' + str(round(firstMap.checkCensor(q))), 18, 900, o)
            o+=30       
        draw_text(screen, "Зарядка %: ", 18, 900,  o)
        o = o + 30
        draw_text(screen, "Напряжение на колесах: ", 18, 900, o)
        o=o+30
        draw_text(screen, mss[0], 18, 880, o)
        draw_text(screen, mss[2], 18, 910, o)
        o=o+30
        draw_text(screen, mss[1], 18, 880, o)
        draw_text(screen, mss[3], 18, 910, o)
        o=o+30
        draw_text(screen, "Наличие проезда: ", 18, 880,  o)
        draw_text(screen, str(firstMap.robotMove(1)), 18, 960, o)
        all_sprites.draw(screen)
        draw(index) # чтобы после передвижения робота не было  микро роботов, нужен screen.fill(BLACK), он делает экран черным и они пропадают за ним

        # рисует для каждого дальномера луч
        for y in range(len(firstMap.censLengList)):
            # рисуем луч дальномера
            pygame.draw.line(screen, RED, 
                        [firstMap.GetRobotX()+(firstMap.GetRobotWidth()/2), firstMap.GetRobotY()+(firstMap.GetRobotHeight()/2)], # размещаем луч по середине робота 
                        [firstMap.censLengList[y].xnd, firstMap.censLengList[y].ynd], 4) # 4 - это толщина луча
        
        pygame.display.flip()

    
    # # обновляем порт для следующего запуска    
    # port1 = int(port) - 1 # удаляю по 1 чтобы был новый порт в следующий раз
    # with open('port.txt', 'w') as f:
    #       f.write(str(port1))
    # f.close()
    # conn.close() # закрываем сервер
    # print ('Сервер закрыт')
    closeConnected(port)
    menu.enable()
    menu.mainloop(screen)