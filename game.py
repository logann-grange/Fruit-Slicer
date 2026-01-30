import pygame
import movement
import logic, menu
from datetime import datetime, timedelta
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon
import sauvegarde
import time

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Découpeur de fruits")

point=0
score_saved = False
last_cut_time = None
COMBO_WINDOW = 0.5  # Fenêtre de 500ms pour le combo
fruits_cuts = 0
combo_display_time = None  # Pour afficher le combo pendant 1 seconde
combo_count = 0  # Le nombre de fruits du dernier combo

screen = pygame.display.set_mode((1080, 720))
font = pygame.font.SysFont('Arial', 40, bold=True)
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load('assets/images/fond_jeu.png'), (1080, 720))
background_freeze = pygame.transform.scale(pygame.image.load('assets/images/fond_glace.png'), (1080, 720))
img_boom = pygame.transform.scale(pygame.image.load("assets/images/boom.png"), (300, 300))
background_freeze.set_alpha(60)
heart1, heart2, heart3 = pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50)), pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50)), pygame.transform.scale(pygame.image.load('assets/images/heart.png'), (50, 50))
hearts = [heart1, heart2, heart3]

# Variables pour gérer la musique pendant le jeu
music_state = "normal"  # "normal" ou "tunnel"
music_start_time = 0

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

def print_defaite(list_object=None):
    nom_joueur = ""
    saisie_terminee = False
    
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

running = True

# Charger la musique du menu
pygame.mixer.music.load("assets/sons/music_menu.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

while running:
    # Afficher le menu principal
    
    menu_result, difficulty = menu.menu(screen, "menu", "menu")
    
    if menu_result:  # Si menu retourne True, on doit quitter
        running = False
        break
    
    # Initialiser / Réinitialiser le jeu
    game_vars = reset_game()
    point = 0
    score_saved = False
    game_running = True
    combo_display_time = None
    combo_count = 0
    difficulty_labels = ["Facile", "Moyen", "Difficile"]
    if isinstance(difficulty, int):
        difficulty = difficulty_labels[difficulty % len(difficulty_labels)]
    
    # Arrêter la musique du menu et lancer celle du jeu
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/sons/musique_fond.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    music_state = "normal"
    music_start_time = pygame.time.get_ticks()
    
    # Boucle de jeu
    while game_running and running:
        clock.tick(60)
        prev_freeze = game_vars['freeze']
        
        if not game_vars['stop']:
            
            screen.blit(background, (0, 0))
            game_vars['list_object'], game_vars['time_move'] = movement.move(
                game_vars['list_object'], game_vars['time_move'], game_vars['freeze']
            )
            game_vars['list_object'], game_vars['time_pop'], game_vars['list_used'] = movement.pop(
                game_vars['list_object'], game_vars['time_pop'], game_vars['freeze'], game_vars['list_used'], difficulty
            )
            for i in range(game_vars['life']):
                            screen.blit(hearts[i], (900 + i*60, 10))
            score_text = font.render(f"Score: {point}", 1, (0, 0, 0))
            score_rect = score_text.get_rect(center=(540, 30))
            screen.blit(score_text, score_rect)
            
            # Afficher le combo s'il est actif
            if combo_display_time is not None:
                elapsed = pygame.time.get_ticks() - combo_display_time
                if elapsed < 1000:  # Afficher pendant 1 seconde
                    combo_font = pygame.font.SysFont('Arial', 60, bold=True)
                    combo_text = combo_font.render(f"COMBO x{combo_count}!", 1, (255, 215, 0))
                    combo_rect = combo_text.get_rect(center=(540, 360))
                    screen.blit(combo_text, combo_rect)
                else:
                    combo_display_time = None
            
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
                        for i in range(game_vars['life']):
                            screen.blit(hearts[i], (900 + i*60, 10))
                        
                        # Appeler le menu pause
                        pause_result, difficulty = menu.menu(screen, "pause", "jeu")
                        if isinstance(difficulty, int):
                            difficulty = difficulty_labels[difficulty % len(difficulty_labels)]
                        if pause_result:  # Si True, quitter le programme
                            running = False
                            game_running = False
                        # Si False, continuer le jeu
                        continue
                    
                    current_time = time.time()
                    if last_cut_time and (current_time - last_cut_time) > COMBO_WINDOW:
                        fruits_cuts = 0
                    
                    # Vérifier si la touche correspond à un objet
                    for i in range(len(game_vars['list_object']) - 1, -1, -1):
                        object = game_vars['list_object'][i]
                        if event.unicode.lower() == object.touche.lower():
                            pygame.mixer.Sound("assets/sons/coupe.wav").play()
                            # Retirer la touche de list_used
                            if object.touche in game_vars['list_used']:
                                game_vars['list_used'].remove(object.touche)
                                fruits_cuts += 1
                                last_cut_time = current_time
                            game_vars['list_object'].pop(i)
                            
                            if isinstance(object, Glaçon):
                                game_vars['freeze'] = True
                                game_vars['time_freeze'] = datetime.now()
                                sound_glace = pygame.mixer.Sound("assets/sons/glace.wav")
                                sound_glace.set_volume(0.2)
                                sound_glace.play()
                            
                            if isinstance(object, Bombe):
                                game_vars['boom'] = True
                                game_vars['coord_boom'] = (
                                    object.coord_x - (object.size/2 + 100/2),
                                    object.coord_y - (object.size/2 + 100/2)
                                )
                            break
                # Vérifier le combo après 500ms de pause ou 2+ fruits
                    if fruits_cuts >= 2:
                        point = sauvegarde.score(point, fruits_cuts) 
                        combo_count = fruits_cuts
                        combo_display_time = pygame.time.get_ticks()
                        fruits_cuts = 0
                        last_cut_time = None
                    else:
                        point = sauvegarde.score(point, fruits_cuts)    
           
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
                    screen.blit(
                        font.render(object.touche.upper(), 1, (0, 0, 0)),
                        (object.coord_x + 20, object.coord_y - 30)
                    )
            
            game_vars['freeze'], game_vars['time_freeze'] = movement.freezer(
                game_vars['freeze'], game_vars['time_freeze'], screen, background_freeze
            )
            
            # Changer la musique si l'état freeze a changé
            if prev_freeze != game_vars['freeze']:
                switch_music(game_vars['freeze'])
            
            if logic.defaite(game_vars['life'], game_vars['boom']) and not score_saved:  # vérifie si la partie est perdue
                print_boom(game_vars['boom'], game_vars['coord_boom'])
                game_vars['life'] = 0
                game_vars['stop'] = True
                nom_joueur = print_defaite(list_object=game_vars['list_object'])
                charger_score = sauvegarde.charger_scores()
                sauvegarde.ajouter_score(nom_joueur,point, charger_score) 
                score_saved = True
                game_running = False  # Sortir de la boucle de jeu pour retourner au menu
                # Recharger la musique du menu
                pygame.mixer.music.stop()
                pygame.mixer.music.load("assets/sons/music_menu.mp3")
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)
            
        
        else:
            # Gérer les événements même quand le jeu est en pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False

        #affichage pause et score
        #txt_score=font.render(str(score(5,12)), True, (255,255,255)) #valeur de test dans score()
        pygame.draw.rect(screen, (0,255,0), (10,10,50,50))
        txt_pause=font.render("⏸", True, (255,255,255)) 
        screen.blit(txt_pause,(25,15))
        
        pygame.display.flip()

pygame.quit()