import pygame
import movement
import logic, menu
from datetime import datetime, timedelta
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Découpeur de fruits")

screen = pygame.display.set_mode((1080, 720))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

slash_effects = []

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

#======== Animation du coup =========#

def add_slash(coord_x, coord_y):
    slash_effects.append({
        'x': coord_x,
        'y': coord_y,
        'start_time': datetime.now(),
    })

def draw_slashes(screen):
    current_time = datetime.now()
    if len(slash_effects) >= 2:
        # Parcourir à l'envers pour pouvoir supprimer en toute sécurité
        for i in range(len(slash_effects) - 2, -1, -1):  # -2 car on accède à i+1
            elapsed = (current_time - slash_effects[i]['start_time']).total_seconds()
            if elapsed < 0.2:
                # Dessiner le slash avec une opacité qui diminue
                pygame.draw.line(screen, (200, 200, 200), 
                                 (slash_effects[i]['x'], slash_effects[i]['y']), 
                                 (slash_effects[i+1]['x'], slash_effects[i+1]['y']), 
                                 5)
            else:
                slash_effects.pop(i)


def game():
    # Initialiser / Réinitialiser le jeu
    game_vars = reset_game()
    game_running = True
    mouse_press = False
    list_mouse_coord = []
    time_slash = datetime.now()
    
    # Boucle de jeu
    while game_running:
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
                    return True  # Retourne True pour quitter complètement
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Dessine l'état actuel du jeu avant d'ouvrir le menu pause
                        screen.blit(background, (0, 0))
                        for obj in game_vars['list_object']:
                            screen.blit(obj.image, (obj.coord_x, obj.coord_y))
                            screen.blit(font.render(obj.touche.upper(), 1, (0, 0, 0)),(obj.coord_x + 20, obj.coord_y - 30))
                        pygame.display.flip()        
                        # Appeler le menu pause
                        pause_result = menu.menu(screen, "pause", "jeu", game_vars["list_object"])
                        if pause_result:  # Si True, quitter le programme
                            return True
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

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mouse_press == False :
                    mouse_press = True
                    time_slash = datetime.now()
                    # ajouter le btn pause
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 or datetime.now() >= time_slash + timedelta(seconds=0.8):
                    mouse_press = False

                # Vérifier si les coordonnées de la souris correspondent à un objet
                if mouse_press:
                    list_mouse_coord.append(pygame.mouse.get_pos())
                    mouse_x, mouse_y = pygame.mouse.get_pos()  # Décomposer le tuple
    
                    for i in range(len(game_vars['list_object']) - 1, -1, -1):
                        object = game_vars['list_object'][i]
        
                        # Vérifier si la souris est dans la zone de l'objet
                        if (object.coord_x <= mouse_x <= object.coord_x + object.size and 
                            object.coord_y <= mouse_y <= object.coord_y + object.size):
            
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
                                game_vars['coord_boom'] = (object.coord_x - (object.size/2 + 100/2),object.coord_y - (object.size/2 + 100/2))
                            break
            
            # animation du coup 
            for coord in list_mouse_coord:
                add_slash(coord[0], coord[1])

            
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
                    return True

        #affichage pause et score
        #txt_score=font.render(str(score(5,12)), True, (255,255,255)) #valeur de test dans score()
        pygame.draw.rect(screen, (0,255,0), (10,10,50,50))
        txt_pause=font.render("⏸", True, (255,255,255)) 
        screen.blit(txt_pause,(25,15))
        
        draw_slashes(screen)
        pygame.display.flip()
        list_mouse_coord = []
    
    return False  # Retourne False pour retourner au menu

# Boucle principale
running = True

while running:
    # Afficher le menu principal
    menu_result = menu.menu(screen, "menu", "menu")
    
    if menu_result:  # Si menu retourne True, on doit quitter
        running = False
        break
    
    # Lancer le jeu
    quit_game = game()
    
    if quit_game:  # Si game() retourne True, quitter complètement
        running = False

pygame.quit()