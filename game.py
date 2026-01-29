import pygame
import movement
import logic, menu
from datetime import datetime, timedelta
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon

logo_pause=pygame.image.load("assets/images/pause.png")
logo_pause=pygame.transform.scale(logo_pause,(25,25))

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Découpeur de fruits")

screen = pygame.display.set_mode((1080, 720))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1080, 720))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1080, 720))
img_boom = pygame.transform.scale(pygame.image.load("assets/images/boom.png"), (300, 300))
background_freeze.set_alpha(60)

pygame.mixer.music.load("assets/sons/musique_fond.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

def print_boom(boom, coord_boom):
    if boom:
        screen.blit(img_boom, coord_boom)
        pygame.mixer.Sound("assets/sons/boom.wav").play()

# Réinitialise les variables du jeu
def reset_game():
    return {
        'list_object': [],
        'time_move': datetime.now(),
        'time_pop': datetime.now(),
        'time_freeze': None,
        'freeze': False,
        'stop': False,
        'list_used': [],
        'life': 3,
        'boom': False,
        'defeat': False,
        'coord_boom': None
    }

running = True

while running:
    # Afficher le menu principal
    menu_result = menu.menu(screen, "menu", "menu")
    
    if menu_result:  # Si menu retourne True, on doit quitter
        running = False
        break
    
    # Initialiser / Réinitialiser le jeu
    game_vars = reset_game()
    game_running = True
    
    # Boucle de jeu
    while game_running and running:
        clock.tick(60)
        
        if not game_vars['stop']:
            screen.blit(background, (0, 0))
            game_vars['list_object'], game_vars['time_move'] = movement.move(
                game_vars['list_object'], game_vars['time_move'], game_vars['freeze']
            )
            game_vars['list_object'], game_vars['time_pop'], game_vars['list_used'] = movement.pop(
                game_vars['list_object'], game_vars['time_pop'], game_vars['freeze'], game_vars['list_used']
            )
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Dessiner l'état actuel du jeu avant d'ouvrir le menu pause
                        screen.blit(background, (0, 0))
                        for obj in game_vars['list_object']:
                            screen.blit(obj.image, (obj.coord_x, obj.coord_y))
                            screen.blit(
                                font.render(obj.touche.upper(), 1, (0, 0, 0)),
                                (obj.coord_x + 20, obj.coord_y - 30)
                            )
                        pygame.display.flip()
                        
                        # Appeler le menu pause
                        pause_result = menu.menu(screen, "pause", "jeu")
                        if pause_result:  # Si True, quitter le programme
                            running = False
                            game_running = False
                        # Si False, continuer le jeu
                        continue

                    # Vérifier si la touche correspond à un objet
                    for i in range(len(game_vars['list_object']) - 1, -1, -1):
                        object = game_vars['list_object'][i]
                        if event.unicode.lower() == object.touche.lower():
                            pygame.mixer.Sound("assets/sons/coupe.wav").play()
                            # Retirer la touche de list_used
                            if object.touche in game_vars['list_used']:
                                game_vars['list_used'].remove(object.touche)
                            
                            game_vars['list_object'].pop(i)
                            
                            if isinstance(object, Glaçon):
                                game_vars['freeze'] = True
                                game_vars['time_freeze'] = datetime.now()
                                pygame.mixer.Sound("assets/sons/glace.wav").play()
                            
                            if isinstance(object, Bombe):
                                game_vars['boom'] = True
                                game_vars['coord_boom'] = (
                                    object.coord_x - (object.size/2 + 100/2),
                                    object.coord_y - (object.size/2 + 100/2)
                                )
                            break
            
            # Supprimer les objets hors écran
            for i in range(len(game_vars['list_object']) - 1, -1, -1):
                object = game_vars['list_object'][i]
                
                if object.coord_y > 720:
                    if isinstance(object, Fruit) and not isinstance(object, Bombe) and not isinstance(object, Glaçon):
                        game_vars['life'] = logic.strike(object, game_vars['life'])
                        print(game_vars['life'])
                    # Retirer la touche de list_used quand l'objet sort
                    if object.touche in game_vars['list_used']:
                        game_vars['list_used'].remove(object.touche)
                    game_vars['list_object'].pop(i)
                else:
                    screen.blit(object.image, (object.coord_x, object.coord_y))
                    screen.blit(
                        font.render(object.touche.upper(), 1, (0, 0, 0)),
                        (object.coord_x + 20, object.coord_y - 30)
                    )
            
            game_vars['freeze'], game_vars['time_freeze'] = movement.freezer(
                game_vars['freeze'], game_vars['time_freeze'], screen, background_freeze
            )
            
            if logic.defaite(game_vars['life'], game_vars['boom']):  # vérifie si la partie est perdue
                game_vars['life'] = 0
                game_vars['stop'] = True
                game_running = False  # Sortir de la boucle de jeu pour retourner au menu
            
            print_boom(game_vars['boom'], game_vars['coord_boom'])
        
        else:
            # Gérer les événements même quand le jeu est en pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False

        #affichage pause et score
        #txt_score=font.render(str(score(5,12)), True, (255,255,255)) #valeur de test dans score()
        pygame.draw.rect(screen, (0,255,0), (10,10,50,50))
        screen.blit(logo_pause,(20,20))
        
        pygame.display.flip()

pygame.quit()