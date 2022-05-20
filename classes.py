import random
import math
import numpy as np
from enum import Enum


class objectOnMap:
    def __init__(self, xpos, ypos, isAlive, idObj):
        self.xpos = xpos
        self.ypos = ypos
        self.isAlive = isAlive
        self.idObj = idObj

    def give_info(self):
        return (self.xpos, self.ypos, self.idObj)

    def calculate_vector(self):
        return

    def objectMove(self, xvec, yvec):
        self.xpos += xvec
        self.ypos += yvec

def calc_wektor_from_a_to_b(x_1, x_2, y_1, y_2):
    return x_1 - x_2, y_1 - y_2




def spawnObjects(object_on_map, liczba_owiec, init_pos_limit):
    for x in range(liczba_owiec):
        object_on_map.append(objectOnMap(giveRandomXY(init_pos_limit), giveRandomXY(init_pos_limit), 1, x))
        print("owca nr",x,"pozycja x y to ",object_on_map[x].xpos,object_on_map[x].ypos)
    return 1


def spawnWolf(object_on_map, liczba_owiec):
    object_on_map.append(objectOnMap(0.0, 0.0, 1, liczba_owiec))


def giveRandomXY(init_pos_limit):
    return random.uniform(-init_pos_limit, init_pos_limit)


def giveRandomDir(self):
    cho = random.randint(1, 4)
    if cho == 1:
        return 0, -self
    if cho == 2:
        return 0, self
    if cho == 3:
        return -self, 0
    if cho == 4:
        return self, 0
def calcDistance(obj1,obj2):
    if not obj1.isAlive or not obj2.isAlive:
        return np.inf
    return math.sqrt((obj2.xpos - obj1.xpos) ** 2 + (obj2.ypos - obj2.ypos) ** 2)

def moving_through_object(x, y, distance, angle_degrees):
    new_x = x + distance * math.cos(angle_degrees * math.pi / 180)
    new_y = y + distance * math.sin(angle_degrees * math.pi / 180)
    #print("newx  ",new_x,"newy  ",new_y)
    return new_x, new_y

def movenew(x0,x1,y0,y1,dt):

    # print("dddddddddddddd",d)
    # t = dt / d
    # xt = ((1 - t) * x0 + t * x1)
    # yt = ((1 - t) * y0 + t * y1)
    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) **2)
    xt=x0-((dt*(x0-x1))/d)
    yt = y0 - ((dt * (y0 - y1)) / d)
    return xt , yt
def calculating_degree(x1, y1, x2, y2):
    return math.degrees(math.atan2(y2-y1, x1 - x2))
def calcAlive(object_on_map):
    # ilosc = 0
    # for i in range(object_on_map.size - 1):
    #     if (object_on_map[i].isAlive == 1):
    #         ilosc = ilosc + 1
    # return ilosc
    return len([x for x in object_on_map if x.isAlive]) - 1
