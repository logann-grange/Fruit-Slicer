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
                fruit.rotate()
        time = datetime.now()
    return list_object, time

#======= Apparition des objets ========#
def pop(list_object, time) :
    # timer entre chaque apparition
    if datetime.now() >= time + timedelta(seconds=random.uniform(1.5, 4)) and not freeze:
        random_num = random.randint(0, 100)
        if random_num > 90  and random_num <= 100:
            list_object.append(Bombe(font))
        elif random_num > 80 and random_num <= 90:
            list_object.append(Glaçon(font))
        elif random_num >= 0 and random_num < 80 :
            list_object.append(Fruit(font))
        
        time = datetime.now()
        time = datetime.now()
    return list_object, time

def freezer(freeze, time) :
    if freeze :
        screen.blit(background_freeze, (0, 0))
    if freeze and datetime.now() >= time + timedelta(seconds=5) :
        freeze = False
        time = None
    return freeze, time


pygame.init()

screen = pygame.display.set_mode((1000, 750))
font = pygame.font.Font(None, 40)
list_object = [Fruit(font)]
time_move = datetime.now()
time_pop = time_move
time_freeze = None
background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1000, 750))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1000, 750))
background_freeze.set_alpha(60)
running = True
freeze = False
touche = ""

while running :
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, 1000, 750))
    screen.blit(background, (0, 0))
    
    list_object, time_move = move(list_object, time_move)
    list_object, time_pop = pop(list_object, time_pop)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            print(event.unicode)
            if event.unicode == object.touche:
                touche = event.unicode

    # Supprimer les objets hors écran
    for i in range(len(list_object) - 1, -1, -1):
        object = list_object[i]
        if object.coord_y > 750:
            list_object.pop(i)
        elif object.touche == touche :
            list_object.pop(i)
            if isinstance(object, Glaçon) :
                freeze = True
                time_freeze = datetime.now()
                
        else:
            screen.blit(object.image, (object.coord_x, object.coord_y))
            screen.blit(font.render(object.touche.upper(), 1, (0, 0, 0)), (object.coord_x + 20, object.coord_y -10))

    freeze, time_freeze = freezer(freeze, time_freeze)

    pygame.display.flip()    