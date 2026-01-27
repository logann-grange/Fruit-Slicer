import pygame
from fruit import Fruit
from glaçon import Glaçon
from bombe import Bombe
from datetime import datetime, timedelta
import random

#======= Mouvement des objets ========#
def move(list_object, time) :
    # timer entre chaque mouvement
    if datetime.now() >= time + timedelta(seconds=0.05):
        for fruit in list_object:
            if not freeze :
                fruit.movement()
                fruit.acceleration()
                #fruit.rotate()
        time = datetime.now()
    return list_object, time

#======= Apparition des objets ========#
def pop(list_object, time) :
    # timer entre chaque apparition
    if datetime.now() >= time + timedelta(seconds=random.uniform(0.7, 4)) and not freeze:
        random_num = random.randint(0, 100)
        print(random_num)
        if random_num > 90  and random_num <= 100:
            list_object.append(Bombe())
        elif random_num > 80 and random_num <= 90:
            list_object.append(Glaçon())
        elif random_num >= 0 and random_num < 80 :
            list_object.append(Fruit())
        
        time = datetime.now()
        time = datetime.now()
    return list_object, time


list_object = [Fruit()]
time_move = datetime.now()
time_pop = datetime.now()
running = True
freeze = False


pygame.init()
screen = pygame.display.set_mode((1000, 750))

while running :
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 1000, 750))
    
    list_object, time_move = move(list_object, time_move)
    list_object, time_pop = pop(list_object, time_pop)
    
    # Supprimer les fruits hors écran
    for i in range(len(list_object) - 1, -1, -1):
        fruit = list_object[i]
        if fruit.coord_y > 750:
            list_object.pop(i)
        else:
            screen.blit(fruit.image, (fruit.coord_x, fruit.coord_y))
    if list_object == [] :
        list_object.append(Fruit())

    pygame.display.flip()    