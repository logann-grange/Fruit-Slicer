import pygame
from fruit import Fruit
from glaçon import Glaçon
from bombe import Bombe
from datetime import datetime, timedelta
import random

#======= Mouvement des objets ========#
def move(list_object, time, freeze, list_used) :
    # timer entre chaque mouvement
    if datetime.now() >= time + timedelta(seconds=0.05):
        for fruit in list_object:
            if not freeze :
                fruit.movement()
                fruit.acceleration()
                fruit.rotate()
        time = datetime.now()
    return list_object, time, list_used

#======= Apparition des objets ========#
def pop(list_object, time, freeze, list_used, difficulty='Moyen'):
    object = None
    match difficulty:
        case "Facile":
            if datetime.now() >= time + timedelta(seconds=random.uniform(2.5, 4)) and not freeze:
                random_num = random.randint(0, 100)
                object = None
                if random_num > 90 and random_num <= 100: # Bombe 10%
                    object = Bombe()
                elif random_num > 85 and random_num <= 90: #Glaçon 5%
                    object = Glaçon()
                elif random_num >= 0 and random_num <= 85: # Fruit 85% 
                    object = Fruit()
        case "Moyen":
            if datetime.now() >= time + timedelta(seconds=random.uniform(1.5, 3)) and not freeze:
                random_num = random.randint(0, 100)
                object = None
                if random_num > 80 and random_num <= 100: # Bombe 20%
                    object = Bombe()
                elif random_num > 75 and random_num <= 80: #Glaçon 5%
                    object = Glaçon()
                elif random_num >= 0 and random_num <= 75: # Fruit 75% 
                    object = Fruit()
        case "Difficile":
            if datetime.now() >= time + timedelta(seconds=random.uniform(1, 2)) and not freeze:
                random_num = random.randint(0, 100)
                object = None
                if random_num > 70 and random_num <= 100: # Bombe 30%
                    object = Bombe()
                elif random_num > 65 and random_num <= 70: #Glaçon 5%
                    object = Glaçon()
                elif random_num >= 0 and random_num <= 65: # Fruit 65% 
                    object = Fruit()              
        # Vérifier que object a bien été créé
    if object is not None:
        object.assign_key(list_used)
        list_object.append(object)
        list_used.append(object.touche)
        
        time = datetime.now()
        pygame.mixer.Sound("assets/sons/pop.mp3").play()
        
    return list_object, time, list_used

def freezer(freeze, time, screen, background_freeze) :
    if freeze :
        screen.blit(background_freeze, (0, 0))
    if freeze and datetime.now() >= time + timedelta(seconds=5) :
        freeze = False
        time = None
    return freeze, time