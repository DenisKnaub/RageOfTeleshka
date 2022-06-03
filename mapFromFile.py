# Итак, для начала, желаю удачи в изучении моего кода.
# Код плохо оптимизирован, нарушает все принципы ООП
# Для разбора нужно знать вектора, сложение векторов, поворот вектора, матрицы поворота --- ГЕОМЕТРИЯ
# Итак начинаем...Улачи
#

import sys
import pygame
import enum
import numpy as np
import math
from os import path
import datetime
import pickle
import time
from datetime import date



# Стенка класс сеты, хранит начало, и длину с шириной,
# стены либо горизонтальные либо вертикальые прямоугольники
class Wall:

    x = 0
    y = 0

    width = 0
    height = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# Треш
class CRotate(enum.Enum):

    left = 1
    right = -1


#
# Класс робота тут хранится угол для поворота  его скорости теоретическая скорость практическая короче дальше объясню
#
#
#
#

class robot:
    robotStartX = 0
    robotStartY = 0
    robotWidth = 0
    robotHeight = 0
    maxRobotSpeed = 3
    maxRobotRotate = 5
    robotSpeed = 0.3 # РЎРєРѕСЂРѕСЃС‚СЊ СЂРѕР±РѕС‚Р°
    Tspeed = 0
    Aspeed = 0
    robotAngle = 0# Р’ РіСЂР°РґСѓСЃР°С…

    standartRotateAngle = 2 * math.pi / 360
    
    def _init_(self):
        self.robotStartX = 0
        self.robotStartY = 0
        self.robotWidth = 0
        self.robotHeight = 0
        self.maxRobotSpeed = 3
        self.maxRobotRotate = 5
        self.robotSpeed = 0.3 # РЎРєРѕСЂРѕСЃС‚СЊ СЂРѕР±РѕС‚Р°
        self.Tspeed = 0
        self.Aspeed = 0
        self.robotAngle = 0# Р’ РіСЂР°РґСѓСЃР°С…
        self.standartRotateAngle = 2 * math.pi / 360
        
    def restart(self):
        self.robotStartX = 0
        self.robotStartY = 0
        self.robotWidth = 0
        self.robotHeight = 0
        self.maxRobotSpeed = 3
        self.maxRobotRotate = 5
        self.robotSpeed = 0.3 # РЎРєРѕСЂРѕСЃС‚СЊ СЂРѕР±РѕС‚Р°
        self.Tspeed = 0
        self.Aspeed = 0
        self.robotAngle = 0# Р’ РіСЂР°РґСѓСЃР°С…
        self.standartRotateAngle = 2 * math.pi / 360
        
# Класс датчиков дальномеров как робот только не перемещается

class censorLeng:
    xnd = 0
    ynd = 0
    x = 1
    y = 0
    k = 0
    c = 0
    standartRotateAngle = 2 * math.pi / 360
    rotateAngle = 0
    startRotator = 0
    def __init__(self, Angle):
        self.rotateAngle = self.standartRotateAngle * Angle
        self.startRotator = self.rotateAngle
        standartVector = np.array([1, 0])
        #print("XS - ", self.mainRobot.robotStartX, "YS - ", self.mainRobot.robotStartY)
        #print("XS - ", standartVector[0], "YS - ", standartVector[1])
        MoveVector = np.array([[math.cos(self.rotateAngle), -math.sin(self.rotateAngle)],
                              [math.sin(self.rotateAngle), -math.cos(self.rotateAngle)]])
        newVector = standartVector.dot(MoveVector)
        self.x = newVector[0]
        self.y = newVector[1]
        #print("Cx - ", self.x, "Cy - ", self.y)


    #
    # Короче если поворачивается робот то вызывается эта штука потомучто при повороте робота поворачиваются с тем все датчики и их нужно переповернуть
    #
    def reRotate(self):  
        standartVector = np.array([1, 0])
        #print("XS - ", self.mainRobot.robotStartX, "YS - ", self.mainRobot.robotStartY)
        #print("XS - ", standartVector[0], "YS - ", standartVector[1])
        MoveVector = np.array([[math.cos(self.rotateAngle), -math.sin(self.rotateAngle)],
                              [math.sin(self.rotateAngle), -math.cos(self.rotateAngle)]])
        newVector = standartVector.dot(MoveVector)
        self.x = newVector[0]
        self.y = newVector[1]
        #print("Cx - ", self.x, "Cy - ", self.y)
#
# основной класс wallList хранит объекты стен
# censLenList хранит датчики
#
#
#
class mapParse:
    xMax = 0
    yMax = 0
    wallList = []
    censLengList = []
    mainRobot = robot()
    
    
    def GetRobotAngle(self):
        return self.mainRobot.robotAngle
    #Р’РѕР·РІСЂР°С‰Р°РµС‚ РґР°РЅРЅС‹Рµ РєРѕРѕСЂРґРёРЅР°С‚ РїРѕ index-Сѓ
    def GetObjectN(self, i):  
        return [self.wallList[i].x, self.wallList[i].y, self.wallList[i].width, self.wallList[i].height]

    # Р’С‹РІРѕРґ РєРѕР»РёС‡РµСЃС‚РІРѕ РѕР±СЉРµРєС‚РѕРІ
    def GetObjectCount(self):
        return len(self.wallList)

    #Р’РѕР·РІСЂР°С‚ РїРѕР·РёС†РёРё СЂРѕР±РѕС‚Р° РїРѕ X
    def GetRobotX(self):
        return self.mainRobot.robotStartX

    # РєРѕРѕСЂРґРёРЅР°С‚С‹ РїРѕР·РёС†РёРё РїРѕ Y
    def GetRobotY(self):
        return self.mainRobot.robotStartY

    # РєРѕРѕСЂРґРёРЅР°С‚С‹ РїРѕР·РёС†РёРё РїРѕ Y
    def GetRobotWidth(self):
        return self.mainRobot.robotWidth

    # РєРѕРѕСЂРґРёРЅР°С‚С‹ РїРѕР·РёС†РёРё РїРѕ Y
    def GetRobotHeight(self):
        return self.mainRobot.robotHeight

    def SetRobotX(self, newX):
        self.mainRobot.robotStartX = newX



    ### Ох основная функция туту лучше рисуй чтобы понять
    # Изначально есть 4 колеса у каждого свой вектор если аргумент 1 
    # то вектор складыается если ноль обнуляется находится среднее и по этоим штукам понимается поворачивает ли робот или нет если поворачивает 
    # 
    #
    #
    def newMove(self, L1, L2, R1, R2):
        # получение где напряжение больше
        if(L1 + L2 - R1 - R2 == 0):
            self.mainRobot.Tspeed = (L1 + L2 + R1 + R2) / 4
            #print("Tspeed - ", Tspeed)
        else:
            self.mainRobot.Tspeed = 0.3#self.mainRobot.maxRobotSpeed
        if(self.mainRobot.Tspeed > self.mainRobot.Aspeed):
            self.mainRobot.Aspeed += 0.001 * self.mainRobot.Tspeed
        if(self.mainRobot.Tspeed < self.mainRobot.Aspeed):
            self.mainRobot.Aspeed -= 0.001 * self.mainRobot.Tspeed
        # print("T speed ", self.mainRobot.Tspeed)
        # print("A speed ", self.mainRobot.Aspeed)
        # print("spead ", self.mainRobot.robotSpeed)
        # Aspeed это actual speed, и tspeed theor speed нужны чтоюы поддержвиать изменение школы
        self.mainRobot.robotSpeed = self.mainRobot.Aspeed
        L1Vector = np.array([1 * L1 * self.mainRobot.robotSpeed, -1 * L1 * self.mainRobot.robotSpeed])
        L2Vector = np.array([1 * L2 * self.mainRobot.robotSpeed, -1 * L2 * self.mainRobot.robotSpeed])
        R1Vector = np.array([1 * R1 * self.mainRobot.robotSpeed, 1  * R1 * self.mainRobot.robotSpeed])
        R2Vector = np.array([1 * R2 * self.mainRobot.robotSpeed, 1  * R2 * self.mainRobot.robotSpeed])
        standartVector = np.array([self.mainRobot.robotSpeed, 0])#L1Vector + L2Vector + R1Vector + R2Vector

        # все я устал
        self.mainRobot.robotAngle += ((L1 + L2 - R1 - R2) * self.mainRobot.standartRotateAngle * 0.5) % (2 * math.pi)
        for i in self.censLengList:
            i.rotateAngle = (i.startRotator + self.mainRobot.robotAngle)# %(2*math.pi)
            i.reRotate()
        #print("sens - Agle - ",i.rotateAngle,'x-',i.x,'y-',i.y )
        #print(standartVector, "Angle - ", self.mainRobot.robotAngle)
        #print("XS - ", self.mainRobot.robotStartX, "YS - ", self.mainRobot.robotStartY)
        #print("XS - ", standartVector[0], "YS - ", standartVector[1])
        MoveVector = np.array([[math.cos(self.mainRobot.robotAngle), -math.sin(self.mainRobot.robotAngle)],
                              [math.sin(self.mainRobot.robotAngle), -math.cos(self.mainRobot.robotAngle)]])
        newVector = standartVector.dot(MoveVector)
        #print("XN - ", newVector[0], "YN - ", newVector[1])
        self.mainRobot.robotStartX += newVector[0]
        self.mainRobot.robotStartY += newVector[1]
        if not (self.checkCollishions()):
            self.mainRobot.robotStartX -= newVector[0]
            self.mainRobot.robotStartY -= newVector[1]
            self.mainRobot.robotSpeed = 0.01
            self.mainRobot.Aspeed = 0.01
            return False
        #print("RX - ", self.mainRobot.robotStartX, "RY - ", self.mainRobot.robotStartY)
        return True
    # РєРѕРѕСЂРґРёРЅР°С‚С‹ РїРѕР·РёС†РёРё РїРѕ Y
    def SetRobotY(self, newY):
        self.mainRobot.robotStartY = newY
    

    ## Проверка того находтся робот в стене или нет
    def checkCollishions(self):
        def shit(x1, y1, x2, y2, w, h):
            if((x1 >= x2) and (x1 <= x2 + w) and
               (y1 >= y2) and (y1 <= y2 + h)):
                return True
            return False
        for i in range(len(self.wallList)):
            x1 = self.mainRobot.robotStartX
            y1 = self.mainRobot.robotStartY
            w1 = self.mainRobot.robotWidth
            h1 = self.mainRobot.robotHeight
            x2 = self.wallList[i].x 
            y2 = self.wallList[i].y
            w  = self.wallList[i].width
            h  = self.wallList[i].height
            #РџСЂРѕРІРµСЂРєР° СЂРѕР±РѕС‚Р°
            #print(self.mainRobot.robotStartX, self.mainRobot.robotStartY)
            #print("РћС‚С‡РµС‚:")
            #print("x1,     y1      - ", shit(x1,y1,x2,y2,w,h))
            #print("x1 + w1,y1      - ", shit(x1 + w1, y1,x2,y2,w,h))
            #print("x1,     y1 + h1 - ", shit(x1,y1 + h1,x2,y2,w,h))
            #print("x1 + w1,y1 + h1 - ", shit(x1 + w1,y1 + h1,x2,y2,w,h))
            ####
            #print("x2,     y2      - ", shit(x2,y2,x1,y1,w1,h1))
            #print("x2 + w, y2      - ", shit(x2 + w,y2,x1,y1,w1,h1))
            #print("x2,     y2 + h  - ", shit(x2,y2 + h,x1,y1,w1,h1))
            #print("x2 + w, y2 + h  - ", shit(x2 + w,y2 + h,x1,y1,w1,h1))
            #print("РС‚РѕРі:")
            if (shit(x1,y1,x2,y2,w,h)):
                #print("x1,y1")
                return False
            if (shit(x1 + w1, y1,x2,y2,w,h)):
                #print("x1 + w1,y1")
                return False
            if (shit(x1,y1 + h1,x2,y2,w,h)):
                #print("x1,y1 + h1")
                return False
            if (shit(x1 + w1,y1 + h1,x2,y2,w,h)):
                #print("x1 + w1,y1 + h1")
                return False
            #РџСЂРѕРІРµСЂРєР° СЃС‚РµРЅС‹
            if (shit(x2,y2,x1,y1,w1,h1)):
                #print("x2,y2")
                return False
            if (shit(x2 + w,y2,x1,y1,w1,h1)):
                #print("x2 + w,y2")
                return False
            if (shit(x2,y2 + h,x1,y1,w1,h1)):
                #print("x2,y2 + h")
                return False
            if (shit(x2 + w,y2 + h,x1,y1,w1,h1)):
                #print("x2 + w,y2")
                return False
        return True
    def addNewCensLen(self, Angle):
        a = censorLeng(Angle)
        self.censLengList.append(a)



    ### Это парсер проходим по карте svg и вытаскиваем отттуда данные 
    def CreateFrame(self, filePath):
        self.mainRobot.restart()
        self.wallList = []
        self.censLengList = []
        readText = open(filePath, "r").read()
        mainText = readText.split("\n")
        #for i in range(len(xMax)):
        #    print(i," :", xMax[i])
    
    
        #РњР°РєСЃРёРјР°Р»СЊРЅС‹Р№ X
        self.xMax = float(mainText[4].split('\"')[1])
        #print("xMax - ", self.xMax)

        #РњР°РєСЃРёРјР°Р»СЊРЅС‹Р№ Y
        self.yMax = float(mainText[5].split('\"')[1])
        #print("yMax - ", self.yMax)

        RectArray = readText.split("<rect")
        #for i in range(1, len(RectArray)):
        #    print(i, " - ", RectArray[i])
        l = 0
        for i in range(1, len(RectArray)):
            n = RectArray[i].split('\"')
            if  (n[1] == "fill:#000000"):
                l = 1
                #print(i, " -", RectArray[i])
                #print(i)
                #X - РєРІР°РґСЂР°С‚Р°
                self.mainRobot.robotStartX = float(n[9])
                #print("x -", x)
                #Y - РєРІР°РґСЂР°С‚Р°
                self.mainRobot.robotStartY = float(n[11])
                #print("y -", y)
                #Width - РєРІР°РґСЂР°С‚Р°
                self.mainRobot.robotWidth = float(n[5])
                #print("width -", width)
                #height - РєРІР°РґСЂР°С‚Р°
                self.mainRobot.robotHeight = float(n[7])
                # print("height - ", self.mainRobot.robotHeight)
                continue
 
            #X - РєРІР°РґСЂР°С‚Р°
            x = float(n[9])
            #print("x -", x)
            #Y - РєРІР°РґСЂР°С‚Р°
            y = float(n[11])
            #print("y -", y)
            #Width - РєРІР°РґСЂР°С‚Р°
            width = float(n[5])
            #print("width -", width)
            #height - РєРІР°РґСЂР°С‚Р°
            height = float(n[7])
            #print("height - ", height)
            
            self.wallList.append(Wall(x, y, width, height))
        if (l == 0):
            print("Где робот!")
            return      
            #print(self.wallList)
    def robotRotate(self, move): # 1 РЅР°РїСЂР°РІРѕ. -1 РЅР°Р»РµРІРѕ
        #self.mainRobot.background = pygame.transform.rotate(self.background, self.standartRotateAngle * move)
        self.mainRobot.robotAngle += self.mainRobot.standartRotateAngle * move
        #print("RobotAngle - ", self.mainRobot.robotAngle)
        # Чел писавший game использует эту прогу чтобы узнать врежится ли робот в стенку если двинется вперед
    def robotMove(self, move): # 1 РїРѕРµРґРµ РІРїРµСЂРµРґ 2 РїРѕРµРґРµС‚ РІРїРµСЂРµРґ СЃ Р±РѕР»СЊС€РµР№ СЃРєРѕСЂРѕСЃС‚СЊСЋ
        standartVector = np.array([self.mainRobot.robotSpeed * move, 0])
        #print("XS - ", self.mainRobot.robotStartX, "YS - ", self.mainRobot.robotStartY)
        #print("XS - ", standartVector[0], "YS - ", standartVector[1])
        MoveVector = np.array([[math.cos(self.mainRobot.robotAngle), -math.sin(self.mainRobot.robotAngle)],
                              [math.sin(self.mainRobot.robotAngle), -math.cos(self.mainRobot.robotAngle)]])
        newVector = standartVector.dot(MoveVector)
        #print("XN - ", newVector[0], "YN - ", newVector[1])
        self.mainRobot.robotStartX += newVector[0]
        self.mainRobot.robotStartY += newVector[1]
        if not (self.checkCollishions()):
            self.mainRobot.robotStartX -= newVector[0]
            self.mainRobot.robotStartY -= newVector[1]
            return False
        #print("RX - ", self.mainRobot.robotStartX, "RY - ", self.mainRobot.robotStartY)
        return True


    ####
    #
    # Если хочешь сделать эту функцию лучше, то изучи поиск точки пересечения двух прямых, превращай части стены в прямые и из всех прямых ищи пересечение с прямой
    # полученной из прямой датчика сам разберешься
    # Сейчас эта штука работает медленно, создаеься вектор и кучу раз двигается по своему направлению пока не попадет в стенку 
    #
    #
    #
    #
    #####
    def checkCensor(self, index):
        if((index < 0) or (index > len(self.censLengList))):
            return
        startX = self.mainRobot.robotStartX + self.mainRobot.robotWidth/2
        SstartX = self.mainRobot.robotStartX + self.mainRobot.robotWidth/2
        startY = self.mainRobot.robotStartY + self.mainRobot.robotHeight/2
        SstartY = self.mainRobot.robotStartY + self.mainRobot.robotHeight/2

        def shit(x1, y1, x2, y2, w, h):
                if((x1 >= x2) and (x1 <= x2 + w) and
                (y1 >= y2) and (y1 <= y2 + h)):
                    return True
                return False
        while(1):
            for i in range(len(self.wallList)):
                x1 = startX
                y1 = startY
                x2 = self.wallList[i].x 
                y2 = self.wallList[i].y
                w  = self.wallList[i].width
                h  = self.wallList[i].height

                if (shit(x1,y1,x2,y2,w,h)):
                    self.censLengList[index].xnd = x1 
                    self.censLengList[index].ynd = y1  
                    return math.sqrt(((x1 - SstartX) * (x1 - SstartX)) +  ((y1 - SstartY) * (y1 - SstartY)))
            startX += self.censLengList[index].x
            startY += self.censLengList[index].y
            # print("CX - ", startX, "CY - ", startY)
