import pygame
import sys
from sauvegarde import *
import translation

pygame.init()
pygame.display.set_caption("Découpeur de fruits")
clock=pygame.time.Clock()
font= pygame.font.SysFont("Arial", 42)
font_emo = pygame.font.SysFont("Arial", 60)

#variables global
l=0 #int de la langue
d=1 #int de la difficulté (0=Facile, 1=Moyen, 2=Difficile)


def print_scores_window(screen):
    global l
    highscores=charger_scores()
    font_title = pygame.font.SysFont('Rockwell', 35, bold=True)
    font_score = pygame.font.SysFont('Rockwell', 25)    
    font_small = pygame.font.SysFont('Rockwell', 18)
    
   
    txt_title = font_title.render("MEILLEURS SCORES", 1, (0, 0, 0))
    screen.blit(txt_title, (320, 150))
    
    if not highscores:
        txt_empty = font_score.render("Aucun score enregistré", 1, (100, 100, 100))
        screen.blit(txt_empty, (280, 200))
    else:
        y_pos = 200
        for i, score_entry in enumerate(highscores[:10]):
            txt_score = font_score.render(f"{i+1}. {score_entry['Nom']} - {score_entry['Score']} pts", 1, (255, 255, 255))
            screen.blit(txt_score, (270, y_pos))
            y_pos += 40
            

def menu(screen, etat, ancien_etat) :
    global l, d
    MENU="menu"
    JEU=translation.translate("jeu", l)
    OPTION="option"
    PAUSE="pause"
    TABLEAU_SCORE="tableau_des_scores"
    print_fond_pause = True
    fond_jeu = pygame.image.load("assets/images/game.jpg")
    fond_jeu = pygame.transform.scale(fond_jeu, (1080,720))
    logo = pygame.image.load("assets/images/logoo.png")
    logo = pygame.transform.scale(logo, (600,750))
    fond_menu = pygame.image.load("assets/images/fond_menu.png")
    fond_menu = pygame.transform.scale(fond_menu,(1080,720))
    fond_logo = pygame.image.load("assets/images/fond_logo.png")
    fond_logo = pygame.transform.scale(fond_logo,(420,150))
    running=True
    
    while running:
        # UNE SEULE boucle d'événements pour tout le menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True, d  # Retourner True pour quitter le programme
            if event.type == pygame.KEYDOWN:
                    if etat == PAUSE and event.key == pygame.K_ESCAPE:
                        return False, d  # Reprendre le jeu
            
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Gérer les clics selon l'état actuel du menu
                pos_click = event.pos
                
                if etat == MENU:
                    if btn_start.collidepoint(pos_click):
                        return False, d  # Lancer le jeu
                    elif btn_option.collidepoint(pos_click):
                        etat = OPTION
                    elif btn_quit.collidepoint(pos_click):
                        return True, d  # Quitter
                    elif btn_tab.collidepoint(pos_click):
                        ancien_etat = etat
                        etat = TABLEAU_SCORE
                
                elif etat == OPTION:
                    if btn_gauche1.collidepoint(pos_click):
                        d = (d - 1) % 3
                    elif btn_droite1.collidepoint(pos_click):
                        d = (d + 1) % 3
                    elif btn_gauche2.collidepoint(pos_click):
                        l = (l - 1) % 2
                    elif btn_droite2.collidepoint(pos_click):
                        l = (l + 1) % 2
                    elif btn_retour.collidepoint(pos_click):
                        etat = ancien_etat
                
                elif etat == PAUSE:
                    if btn_reprendre.collidepoint(pos_click):
                        return False, d  # Reprendre le jeu
                    elif btn_options.collidepoint(pos_click):
                        ancien_etat = PAUSE
                        etat = OPTION
                    elif btn_menu.collidepoint(pos_click):
                        etat = MENU
                
                elif etat == TABLEAU_SCORE:
                    if btn_fermer.collidepoint(pos_click):
                        etat = MENU

        pos_souris = pygame.mouse.get_pos()
        
        match etat:
            case "menu" :
                screen.fill((0,0,0))
                screen.blit(fond_menu,(0,0))

                txt_btn_1 = font.render(translation.translate("Jouer", l), True, (255,255,255))
                txt_btn_2 = font.render(translation.translate("Options", l), True, (255,255,255))
                txt_btn_3 = font.render(translation.translate("Quitter", l), True, (255,255,255))
                txt_leaderboard = font.render ("☰", True, (255,255,255))
                emo1 = font_emo.render("▶️", True,(255,255,255))
                emo2 = font_emo.render ("⚙️", True, (255,255,255))
                emo3 = font_emo.render ("❌",True,(255,255,255))

                btn_tab = pygame.draw.rect(screen,(255,0,0),(10,10,50,50), border_radius=8)

                menu_ = pygame.Surface((1080,720), pygame.SRCALPHA)
                menu_.blit(fond_logo,(350,10))
                menu_.set_alpha(250)
                screen.blit(menu_,(0,0))
                screen.blit(logo,(180,-250))
                pygame.draw.rect(screen,(0,0,0),(350,10,420,150),3,border_radius=8)

                btn_start = pygame.draw.circle(screen,(25,25,225),(200,400),105,5)
                btn_option = pygame.draw.circle(screen,(255,0,255),(540,400),105,5)            
                btn_quit = pygame.draw.circle(screen,(255,0,0),(880,400),105,5)

                screen.blit(txt_btn_1 , (200-font.size(translation.translate("Jouer", l))[0]/2,430))
                screen.blit(txt_btn_2 , (540-font.size(translation.translate("Options", l))[0]/2,430))
                screen.blit(txt_btn_3 , (880-font.size(translation.translate("Quitter", l))[0]/2,430))
                screen.blit(txt_leaderboard , (17,13))
                screen.blit(emo1, (175,360))
                screen.blit(emo2,(515,360))
                screen.blit(emo3,(855,360))

            case "option" :
                nv_diff=["Facile","Moyen","Difficile"]
                lang=["Francais","Anglais"]
            
                screen.fill((0,0,0))
                if ancien_etat==PAUSE:
                   screen.blit(fond_jeu,(0,0))
                else:
                    screen.blit(fond_menu,(0,0))
            
                txt_btn_1 = font.render(translation.translate("Niveau de difficulté", l), True, (0,0,0))
                txt_nv = font.render(translation.translate(nv_diff[d], l), True, (0,0,0))
                txt_l = font.render(translation.translate(lang[l], l), True, (0,0,0))
                txt_btn_3 = font.render("<", True, (255,255,255))
                txt_btn_4 = font.render(">", True, (255,255,255))
            
                btn_gauche1=pygame.draw.rect(screen, (75,75,75), (255,200,75,75),border_radius=8)
                btn_droite1=pygame.draw.rect(screen, (75,75,75), (750,200,75,75),border_radius=8) 
                btn_gauche2=pygame.draw.rect(screen, (75,75,75), (305,325,75,75),border_radius=8)
                btn_droite2=pygame.draw.rect(screen, (75,75,75), (700,325,75,75),border_radius=8)
                btn_retour=pygame.draw.rect(screen, (200,0,0), (10,10,50,50),border_radius=8)

                menu_ = pygame.Surface((595,300), pygame.SRCALPHA)
                pygame.draw.rect(menu_,(255,50,50),(0,0,595,300),border_radius=8)
                menu_.set_alpha(150)
                screen.blit(menu_,(240,130))

                screen.blit(txt_btn_1 , (540-font.size(translation.translate("Niveau de difficulté", l))[0]/2,150))
                screen.blit(txt_btn_3 , (20,10))
                screen.blit(txt_btn_3 , (280,215))
                screen.blit(txt_btn_3 , (330,340))
                screen.blit(txt_btn_4 , (775,215))
                screen.blit(txt_btn_4 , (725,340))
                screen.blit(txt_nv , (540-font.size(translation.translate(nv_diff[d], l))[0]/2,220))
                screen.blit(txt_l, (540-font.size(translation.translate(lang[l], l))[0]/2,345))

            case "pause":
                if print_fond_pause :
                    fond_pause = pygame.Surface((1080, 720), pygame.SRCALPHA)
                    pygame.draw.rect(fond_pause, (0, 0, 0, 128), (0, 0, 1080, 720))
                    fond_pause.set_alpha(180)
                    screen.blit(fond_pause, (0, 0))
                    print_fond_pause = False

                txt_btn_1 = font.render(translation.translate("Reprendre", l), True, (255,255,255))
                txt_btn_2 = font.render(translation.translate("Options", l), True, (255,255,255))
                txt_btn_3 = font.render(translation.translate("Menu Principal",l), True, (255,255,255))
            
                btn_reprendre = pygame.draw.rect(screen, (20,20,20), (390,200,300,75), border_radius=8)
                btn_options = pygame.draw.rect(screen, (20,20,20), (390,325,300,75), border_radius=8)
                btn_menu = pygame.draw.rect(screen, (20,20,20), (390,450,300,75), border_radius=8)

                screen.blit(txt_btn_1 , (390+(300-font.size(translation.translate("Reprendre", l))[0])/2,220))
                screen.blit(txt_btn_2 , (390+(300-font.size(translation.translate("Options", l))[0])/2,345))
                screen.blit(txt_btn_3 , (390+(300-font.size(translation.translate("Menu Principal", l))[0])/2,470))

            case "tableau_des_scores":
                screen.fill((0,0,0))
                screen.blit(fond_menu,(0,0))

                txt_titre = font.render("Tableau des scores !", True, (255,255,255))
                txt_fermer = font.render("X", True, (255,255,255))

                menu_ = pygame.Surface((595,480), pygame.SRCALPHA)
                pygame.draw.rect(menu_,(255,50,50),(0,0,595,480),border_radius=8)
                menu_.set_alpha(150)
                screen.blit(menu_,(240,130))

                print_scores_window(screen) 

                btn_fermer = pygame.draw.rect(screen,(0,0,0),(10,10,50,50))
                screen.blit(txt_titre,(350,50))

                if 10<=pos_souris[0]<=60:
                    if 10<=pos_souris[1]<=60:
                        pygame.draw.rect(screen,(75,0,0),(10,10,50,50))
                    else:
                        pygame.draw.rect(screen,(0,0,0),(10,10,50,50))
                                
                screen.blit(txt_fermer,(20,18))

        pygame.display.flip()
        clock.tick(60)

    return False, d  # Retourner False pour continuer le jeu