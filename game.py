import pygame
import movement
import logic
from datetime import datetime, timedelta
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon
import sauvegarde
import time

pygame.init()

screen = pygame.display.set_mode((1000, 750))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

list_object = []
time_move = datetime.now()
time_pop = time_move
time_freeze = None
background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1000, 750))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1000, 750))
img_boom = pygame.transform.scale(pygame.image.load("assets/images/bombe.png"), (300, 300))
background_freeze.set_alpha(60)
running = True
freeze = False
stop = False
list_used = []
life = 3
boom = False
defeat = False
coord_boom = None
fruits_cuts=0
point=0
score_saved = False
last_cut_time = None
COMBO_WINDOW = 0.5  # Fenêtre de 500ms pour le combo

def print_boom(boom, coord_boom) :
    if boom :
        screen.blit(img_boom, coord_boom)

while running:
    #clock.tick(60)
    
    screen.blit(background, (0, 0))
    
    list_object, time_move = movement.move(list_object, time_move, freeze)
    list_object, time_pop, list_used = movement.pop(list_object, time_pop, freeze, list_used)
    print_boom(boom, coord_boom)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            current_time = time.time()
            
            # Réinitialiser le combo si trop de temps s'est écoulé
            if last_cut_time and (current_time - last_cut_time) > COMBO_WINDOW:
                fruits_cuts = 0
            
            # Vérifier si la touche correspond à un objet
            for i in range(len(list_object) - 1, -1, -1):
                object = list_object[i]
                if event.unicode.lower() == object.touche.lower():
                    # Retirer la touche de list_used si elle y est
                    if object.touche in list_used:
                        list_used.remove(object.touche)
                        fruits_cuts += 1
                        last_cut_time = current_time
                        list_object.pop(i)
                        
                    if isinstance(object, Glaçon):
                        freeze = True
                        time_freeze = datetime.now()

                    if isinstance(object, Bombe):
                        boom = True
                        coord_boom = (object.coord_x-(object.size/2 + 100/2), object.coord_y-(object.size/2 + 100/2))
                    break
            
            # Vérifier le combo après 500ms de pause ou 2+ fruits
            if fruits_cuts >= 2:
                bonus = fruits_cuts * 50
                point += sauvegarde.score(0, fruits_cuts) + bonus
                print(f"Combo x{fruits_cuts}! +{sauvegarde.score(0, fruits_cuts) + bonus} points")
                fruits_cuts = 0
                last_cut_time = None      
        
    # Supprimer les objets hors écran et afficher
    for i in range(len(list_object) - 1, -1, -1):
        object = list_object[i]
        
        if object.coord_y > 750 and object is Fruit:
            print(life)
            # Retirer la touche de list_used quand l'objet sort
            if object.touche in list_used:
                list_used.remove(object.touche)
            list_object.pop(i)
        else:
            screen.blit(object.image, (object.coord_x, object.coord_y))
            screen.blit(font.render(object.touche.upper(), 1, (0, 0, 0)), (object.coord_x + 20, object.coord_y - 30))

    freeze, time_freeze = movement.freezer(freeze, time_freeze, screen, background_freeze)

    if logic.defaite(life, boom) and not score_saved: #vérifie si la partie est perdue
        life = 0
        #pygame.quit() # à modifier par une fenêtre de défaite
        charger_score=sauvegarde.charger_scores()
        sauvegarde.ajouter_score("Joueur1",point,charger_score)
        score_saved = True
        running = False  # Arrête la boucle après avoir sauvegardé
    pygame.display.flip()

pygame.quit()
