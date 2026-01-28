import pygame
import movement
import logic
from datetime import datetime, timedelta
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1000, 750))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

list_object = []
time_move = datetime.now()
time_pop = time_move
time_freeze = None
background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1000, 750))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1000, 750))
img_boom = pygame.transform.scale(pygame.image.load("assets/images/boom.png"), (300, 300))
background_freeze.set_alpha(60)
running = True
freeze = False
stop = False
list_used = []
life = 3
boom = False
defeat = False
coord_boom = None

def print_boom(boom, coord_boom) :
    if boom :
        screen.blit(img_boom, coord_boom)
        pygame.mixer.Sound("assets/sons/boom.wav").play()


while running:
    #clock.tick(60)
    if not stop :
        screen.blit(background, (0, 0))
        list_object, time_move = movement.move(list_object, time_move, freeze)
        list_object, time_pop, list_used = movement.pop(list_object, time_pop, freeze, list_used)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Vérifier si la touche correspond à un objet
                for i in range(len(list_object) - 1, -1, -1):
                    object = list_object[i]
                    if event.unicode.lower() == object.touche.lower():
                        pygame.mixer.Sound("assets/sons/coupe.wav").play()
                        # Retirer la touche de list_used
                        if object.touche in list_used:
                            list_used.remove(object.touche)

                        list_object.pop(i)

                        if isinstance(object, Glaçon):
                            freeze = True
                            time_freeze = datetime.now()
                            pygame.mixer.Sound("assets/sons/glace.wav").play()

                        if isinstance(object, Bombe) :
                            boom = True
                            coord_boom = (object.coord_x-(object.size/2 + 100/2), object.coord_y-   (object.size/2 + 100/2)) # 100/2 correspond à la moitier de la taille   de img_boom
                        break

        # Supprimer les objets hors écran
        for i in range(len(list_object) - 1, -1, -1):
            object = list_object[i]

            if object.coord_y > 750:
                life = logic.strike(object, life)
                print(life)
                # Retirer la touche de list_used quand l'objet sort
                if object.touche in list_used:
                    list_used.remove(object.touche)
                list_object.pop(i)
            else:
                screen.blit(object.image, (object.coord_x, object.coord_y))
                screen.blit(font.render(object.touche.upper(), 1, (0, 0, 0)), (object.coord_x + 20, object.coord_y - 30))

        freeze, time_freeze = movement.freezer(freeze, time_freeze, screen, background_freeze)

        if logic.defaite(life, boom) : #vérifie si la partie est perdue
            life = 0
            stop = True
            #pygame.quit() # à modifier par une fenêtre de défaite
        print_boom(boom, coord_boom)


        #pygame.display.flip()
    pygame.display.flip()
pygame.quit()