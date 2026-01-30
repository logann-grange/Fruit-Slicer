import pygame
import movement
import logic, menu, sauvegarde
from datetime import datetime, timedelta
import time
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Découpeur de fruits")

COMBO_WINDOW = 0.5  # Fenêtre de 500ms pour le combo
combo_count = 0  # Le nombre de fruits du dernier combo

screen = pygame.display.set_mode((1080, 720))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

slash_effects = []
mode = 0
game_vars = {}
difficulty = "Moyen"

background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1080, 720))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1080, 720))
img_boom = pygame.transform.scale(pygame.image.load("assets/images/boom.png"), (300, 300))
background_freeze.set_alpha(60)

heart1, heart2, heart3 = pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50)), pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50)), pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50))
hearts = [heart1, heart2, heart3]

# Variables pour gérer la musique pendant le jeu
music_state = "normal"  # "normal" ou "tunnel"
music_start_time = 0

# Charger la musique du menu
pygame.mixer.music.load("assets/sons/music_menu.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# pygame.mixer.music.load("assets/sons/musique_fond.mp3")
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.1)

def switch_music(freeze):
    global music_state, music_start_time
    
    if freeze and music_state == "normal":
        # Passer à la version tunnel
        current_time = pygame.time.get_ticks()
        music_pos = (current_time - music_start_time) / 1000.0
        
        pygame.mixer.music.load("assets/sons/musique_fond_tunnel.wav")
        pygame.mixer.music.play(-1, start=music_pos)
        pygame.mixer.music.set_volume(0.55)
        music_state = "tunnel"
        music_start_time = current_time - (music_pos * 1000)
        
    elif not freeze and music_state == "tunnel":
        # Revenir à la version normale
        current_time = pygame.time.get_ticks()
        music_pos = (current_time - music_start_time) / 1000.0
        
        pygame.mixer.music.load("assets/sons/musique_fond.mp3")
        pygame.mixer.music.play(-1, start=music_pos)
        pygame.mixer.music.set_volume(0.1)
        music_state = "normal"
        music_start_time = current_time - (music_pos * 1000)

def print_defaite(point, list_object=None):
    nom_joueur = ""
    saisie_terminee = False
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/sons/Game_over.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)


    
    while not saisie_terminee:
        screen.blit(background, (0, 0))
        if list_object != None:
            for obj in list_object:
                screen.blit(obj.image, (obj.coord_x, obj.coord_y))
                screen.blit(font.render(obj.touche.upper(), 1, (0, 0, 0)), (obj.coord_x + 20, obj.coord_y - 30))
        txt_defaite = font.render("Vous avez perdu !", True, (255, 0, 0))
        screen.blit(txt_defaite, (350, 200))
        screen.blit(font.render(f"Score final : {point}", True, (255, 255, 255)), (400, 280))
        
        # Afficher le texte de demande de nom
        txt_prompt = font.render("Entrez votre nom :", True, (255, 255, 255))
        screen.blit(txt_prompt, (380, 350))
        
        # Afficher le nom en cours de saisie avec un curseur
        txt_nom = font.render(nom_joueur + "|", True, (255, 255, 0))
        screen.blit(txt_nom, (540 - txt_nom.get_width() // 2, 400))
        
        # Instructions
        txt_instruction = font.render("(Appuyez sur ENTREE pour valider)", True, (150, 150, 150))
        screen.blit(txt_instruction, (280, 480))
        
        pygame.display.flip()
        
        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Joueur"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    saisie_terminee = True
                elif event.key == pygame.K_BACKSPACE:
                    nom_joueur = nom_joueur[:-1]
                elif event.unicode.isprintable() and len(nom_joueur) < 15:
                    nom_joueur += event.unicode
        
        clock.tick(30)
    
    return nom_joueur if nom_joueur else "Joueur"


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
        'coord_boom': None,
        'point' : 0,
        'combo_display_time' : None,
        'fruits_cuts' : 0,
        'score_saved' : False,
        'last_cut_time' : None,
        'combo_fruits': [],  # Liste temporaire pour stocker les fruits du combo en cours
    }

#======== Animation du coup =========#

def add_slash(coord_x, coord_y):
    slash_effects.append({
        'x': coord_x,
        'y': coord_y,
        'start_time': datetime.now(),
    })

def draw_slashes(screen, mode):
    current_time = datetime.now()
    # if mode == 0 :
    #     pygame.draw.line(screen, (200, 200, 200), (slash_effects[i]['x'], slash_effects[i]['y']), (slash_effects[i+1]['x'], slash_effects[i+1]['y']), 5)

    if mode == 1 :
        if len(slash_effects) >= 2:
            # Parcour à l'envers pour pouvoir supprimer sans erreur
            for i in range(len(slash_effects) - 2, -1, -1):  # -2 car on accède à i+1
                elapsed = (current_time - slash_effects[i]['start_time']).total_seconds()
                if elapsed < 0.2:
                    # Dessiner le slash avec une opacité qui diminue
                    pygame.draw.line(screen, (200, 200, 200), (slash_effects[i]['x'], slash_effects[i]['y']), (slash_effects[i+1]['x'], slash_effects[i+1]['y']), 5)
                else:
                    slash_effects.pop(i)



def game():
    # Initialiser / Réinitialiser le jeu
    global mode, combo_count, game_vars, difficulty
    game_vars = reset_game()
    game_running = True
    mouse_press = False
    list_mouse_coord = []
    time_slash = datetime.now()
    prev_freeze = game_vars['freeze']
    
    # Boucle de jeu
    while game_running:
        clock.tick(60)
        
        if not game_vars['stop']:
            screen.blit(background, (0, 0))
            game_vars['list_object'], game_vars['time_move'],game_vars['list_used']  = movement.move(game_vars['list_object'], game_vars['time_move'], game_vars['freeze'], game_vars['list_used'])
            #apparition
            game_vars['list_object'], game_vars['time_pop'], game_vars['list_used'] = movement.pop(game_vars['list_object'], game_vars['time_pop'], game_vars['freeze'],game_vars['list_used'],difficulty)

            # affichage des vies
            for i in range(game_vars['life']):
                            screen.blit(hearts[i], (900 + i*60, 10))
            # affichage du score
            score_text = font.render(f"Score: {game_vars['point']}", 1, (0, 0, 0))
            score_rect = score_text.get_rect(center=(540, 30))
            screen.blit(score_text, score_rect)
            
            # Afficher le combo s'il est actif
            if game_vars["combo_display_time"] is not None:
                elapsed = pygame.time.get_ticks() - game_vars["combo_display_time"]
                if elapsed < 1000:  # Afficher pendant 1 seconde
                    combo_font = pygame.font.SysFont('Arial', 60, bold=True)
                    combo_text = combo_font.render(f"COMBO x{combo_count}!", 1, (255, 215, 0))
                    combo_rect = combo_text.get_rect(center=(540, 360))
                    screen.blit(combo_text, combo_rect)
                else:
                    game_vars["combo_display_time"] = None

            # Vérifier si le délai du combo est dépassé (en dehors de la boucle d'événements)
            current_time = time.time()
            if game_vars['last_cut_time'] and (current_time - game_vars['last_cut_time']) > COMBO_WINDOW:
                # Le combo est terminé, calculer le score
                if game_vars['fruits_cuts'] >= 2:
                    # C'est un combo!
                    game_vars["point"] = sauvegarde.score(game_vars["point"], game_vars["fruits_cuts"])
                    combo_count = game_vars["fruits_cuts"]
                    game_vars['combo_display_time'] = pygame.time.get_ticks()
                elif game_vars['fruits_cuts'] == 1:
                    # Un seul fruit, pas de combo
                    game_vars["point"] = sauvegarde.score(game_vars["point"], 1)
                
                # Réinitialiser le compteur de fruits
                game_vars["fruits_cuts"] = 0
                game_vars['last_cut_time'] = None

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
                            if mode == 0 :
                                screen.blit(font.render(obj.touche.upper(), 1, (0, 0, 0)),(obj.coord_x + 20, obj.coord_y - 30))
                        pygame.display.flip()        
                        # Appeler le menu pause
                        pause_result, mode, difficulty = menu.menu(screen, "pause", "jeu", difficulty, game_vars["list_object"])
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
                                # Ne compter que les fruits normaux, pas les glaçons ni les bombes
                                if not isinstance(object, Glaçon) and not isinstance(object, Bombe):
                                    game_vars['fruits_cuts'] += 1
                                    game_vars['last_cut_time'] = time.time()
                            
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

                if mode == 1 :
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
                            if (object.coord_x <= mouse_x <= object.coord_x + object.size and object.coord_y <= mouse_y <= object.coord_y + object.size):
            
                                pygame.mixer.Sound("assets/sons/coupe.wav").play()
            
                                # Retirer la touche de list_used
                                if object.touche in game_vars['list_used']:
                                    game_vars['list_used'].remove(object.touche)
                                    # Ne compter que les fruits normaux, pas les glaçons ni les bombes
                                    if not isinstance(object, Glaçon) and not isinstance(object, Bombe):
                                        game_vars['fruits_cuts'] += 1
                                        game_vars['last_cut_time'] = time.time()
            
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
                        pygame.mixer.Sound("assets/sons/hurt.mp3").play()
                        print(game_vars['life'])
                    # Retirer la touche de list_used quand l'objet sort
                    if object.touche in game_vars['list_used']:
                        game_vars['list_used'].remove(object.touche)
                    game_vars['list_object'].pop(i)
                else:
                    screen.blit(object.image, (object.coord_x, object.coord_y))
                    if mode == 0 :
                        screen.blit(font.render(object.touche.upper(), 1, (0, 0, 0)),(object.coord_x + 20, object.coord_y - 30))
            
            game_vars['freeze'], game_vars['time_freeze'] = movement.freezer(
                game_vars['freeze'], game_vars['time_freeze'], screen, background_freeze
            )
            
            # Changer la musique si l'état freeze a changé
            if prev_freeze != game_vars['freeze']:
                switch_music(game_vars['freeze'])
                prev_freeze = game_vars['freeze']

            if logic.defaite(game_vars['life'], game_vars['boom']) and not game_vars['score_saved']:  # vérifie si la partie est perdue
                print_boom(game_vars['boom'], game_vars['coord_boom'])
                game_vars['life'] = 0
                game_vars['stop'] = True
                nom_joueur = print_defaite(game_vars['point'], list_object=game_vars['list_object'])
                charger_score = sauvegarde.charger_scores()
                sauvegarde.ajouter_score(nom_joueur,game_vars["point"], charger_score) 
                game_vars['score_saved'] = True
                game_running = False  # Sortir de la boucle de jeu pour retourner au menu
                # Recharger la musique du menu
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/sons/music_menu.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            
            print_boom(game_vars['boom'], game_vars['coord_boom'])
        
        else:
            # Gérer les événements même quand le jeu est en pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

        #affichage pause
        #txt_score=font.render(str(score(5,12)), True, (255,255,255)) #valeur de test dans score()
        pygame.draw.rect(screen, (0,255,0), (10,10,50,50))
        txt_pause=font.render("⏸", True, (255,255,255)) 
        screen.blit(txt_pause,(25,15))

        draw_slashes(screen, mode)
        pygame.display.flip()
        list_mouse_coord = []
    
    return False  # Retourne False pour retourner au menu

# Boucle principale
running = True

while running:
    # Afficher le menu principal
    menu_result, mode, difficulty = menu.menu(screen, "menu", "menu", difficulty)
    
    if menu_result:  # Si menu retourne True, on doit quitter
        running = False
        break
    
    # Arrêter la musique du menu et lancer celle du jeu
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/sons/musique_fond.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    music_state = "normal"
    music_start_time = pygame.time.get_ticks()

    # Lancer le jeu
    quit_game = game()
    
    if quit_game:  # Si game() retourne True, quitter complètement
        running = False

pygame.quit()