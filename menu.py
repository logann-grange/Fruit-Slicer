import pygame
import sys
from sauvegarde import *
import translation

pygame.init()
screen=pygame.display.set_mode((1080,720))
pygame.display.set_caption("Découpeur de fruits")
clock=pygame.time.Clock()
font= pygame.font.SysFont("Arial", 42)
font_emo = pygame.font.SysFont("Arial", 60)

#variables global
l=0 #int de la langue
MENU="menu"
JEU=translation.translate("jeu", l)
OPTION="option"
PAUSE="pause"
TABLEAU_SCORE="tableau_des_scores"
etat=MENU
ancien_etat=MENU
pos_click=None
d=1
fond_jeu = pygame.image.load("Images/game.jpg")
fond_jeu = pygame.transform.scale(fond_jeu, (1080,720))
logo = pygame.image.load("Images/logoo.png")
logo = pygame.transform.scale(logo, (600,750))
fond_menu = pygame.image.load("Images/fond_menu.png")
fond_menu = pygame.transform.scale(fond_menu,(1080,720))
fond_logo = pygame.image.load("Images/fond_logo.png")
fond_logo = pygame.transform.scale(fond_logo,(420,150))

highscores=charger_scores()

def print_scores_window(highscores):
    font_title = pygame.font.SysFont('Rockwell', 35, bold=True)
    font_score = pygame.font.SysFont('Rockwell', 25)    
    font_small = pygame.font.SysFont('Rockwell', 18)
    
    if l==0:
        txt_title = font_title.render("MEILLEURS SCORES", 1, (0, 0, 0))
        screen.blit(txt_title, (320, 150))
    else:
        txt_title = font_title.render("Best Score", 1, (0,0,0))
        screen.blit(txt_title, (320,150))

    if not highscores:
        txt_empty = font_score.render("Aucun score enregistré", 1, (100, 100, 100))
        screen.blit(txt_empty, (280, 200))
    else:
        y_pos = 200
        for i, score_entry in enumerate(highscores[:10]):
            txt_score = font_score.render(f"{i+1}. {score_entry['Nom']} - {score_entry['Score']} pts", 1, (255, 255, 255))
            screen.blit(txt_score, (270, y_pos))
            y_pos += 40
            
    

    

running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos_click=pygame.mouse.get_pos()


    pos_souris=pygame.mouse.get_pos()
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

            btn_tab=pygame.draw.rect(screen,(255,0,0),(10,10,50,50), border_radius=8)
            
            
            menu_ = pygame.Surface((1080,720), pygame.SRCALPHA)
            
            menu_.blit(fond_logo,(350,10))
            menu_.set_alpha(250)
            screen.blit(menu_,(0,0))
            screen.blit(logo,(180,-250))
            pygame.draw.rect(screen,(0,0,0),(350,10,420,150),3,border_radius=8)

            btn_start = pygame.draw.circle(screen,(25,25,225),(200,400),105,5)
            btn_option = pygame.draw.circle(screen,(255,0,255),(540,400),105,5)            
            btn_quit = pygame.draw.circle(screen,(255,0,0),(880,400),105,5)            
            
            if pos_click is not None:

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if btn_start.collidepoint(event.pos):
                            etat=JEU
                            pos_click = None
                        elif btn_option.collidepoint(event.pos):
                            etat=OPTION
                            pos_click = None
                        elif btn_quit.collidepoint(event.pos):
                            running=False
                        elif btn_tab.collidepoint(event.pos):
                            ancien_etat=etat
                            etat=TABLEAU_SCORE
                            pos_click=None
            
            
            screen.blit(txt_btn_1 , (200-font.size(translation.translate("Jouer", l))[0]/2,430))
            screen.blit(txt_btn_2 , (540-font.size(translation.translate("Options", l))[0]/2,430))
            screen.blit(txt_btn_3 , (880-font.size(translation.translate("Quitter", l))[0]/2,430))
            screen.blit(txt_leaderboard , (17,13))
            screen.blit(emo1, (175,360))
            screen.blit(emo2,(515,360))
            screen.blit(emo3,(855,360))
           

        case "jeu" :

            screen.fill((0,0,0))
            screen.blit(fond_jeu,(0,0))
           
            txt_score=font.render(str(score(5,12)), True, (255,255,255)) #valeur de test dans score()
            txt_pause=font.render("⏸", True, (255,255,255)) 
           
            pygame.draw.rect(screen, (0,255,0), (10,10,50,50))
           
            if 10<=pos_souris[0]<=60:
                if 10<=pos_souris[1]<=60:
                    pygame.draw.rect(screen, (50,255,50),(10,10,50,50))

            if pos_click is not None:
                if 10<=pos_click[0]<=60:
                    if 10<=pos_click[1]<=60:
                        etat=PAUSE
                        pos_click=None
            
            screen.blit(txt_pause,(25,15))
            screen.blit(txt_score,(500,50))


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

            if pos_click is not None:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if btn_gauche1.collidepoint(event.pos):
                            d = (d - 1) % 3
                            pos_click=None
                        elif btn_droite1.collidepoint(event.pos):
                            d = (d + 1) % 3
                            pos_click=None
                        elif btn_gauche2.collidepoint(event.pos):
                            l = (l - 1) % 2
                            pos_click=None
                        elif btn_droite2.collidepoint(event.pos):
                            l = (l + 1) % 2
                            pos_click=None
                        elif btn_retour.collidepoint(event.pos):
                            etat=ancien_etat
                            pos_click=None

            screen.blit(txt_btn_1 , (540-font.size(translation.translate("Niveau de difficulté", l))[0]/2,150))
            screen.blit(txt_btn_3 , (20,10))
            screen.blit(txt_btn_3 , (280,215))
            screen.blit(txt_btn_3 , (330,340))
            screen.blit(txt_btn_4 , (775,215))
            screen.blit(txt_btn_4 , (725,340))
            screen.blit(txt_nv , (540-font.size(translation.translate(nv_diff[d], l))[0]/2,220))
            screen.blit(txt_l, (540-font.size(translation.translate(lang[l], l))[0]/2,345))
            

        case "pause":
            screen.fill((0,0,0))
            screen.blit(fond_jeu, (0,0))
            

            txt_btn_1 = font.render(translation.translate("Reprendre", l), True, (255,255,255))
            txt_btn_2 = font.render(translation.translate("Options", l), True, (255,255,255))
            txt_btn_3 = font.render(translation.translate("Menu Principal",l), True, (255,255,255))
            
            pygame.draw.rect(screen, (20,20,20), (390,200,300,75), border_radius=8)
            pygame.draw.rect(screen, (20,20,20), (390,325,300,75), border_radius=8)
            pygame.draw.rect(screen, (20,20,20), (390,450,300,75), border_radius=8)

            if pos_click is not None:

                if 390<=pos_click[0]<=690:
                    if 200<=pos_click[1]<=275:
                        etat=JEU
                        pos_click=None
                    elif 325<=pos_click[1]<=400:
                        ancien_etat=etat
                        etat=OPTION
                        pos_click=None
                    elif 450<=pos_click[1]<=525:
                        etat=MENU  
                        pos_click=None 

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

            print_scores_window(highscores) 
            
            pygame.draw.rect(screen,(0,0,0),(10,10,50,50))
            if l==0:
                screen.blit(txt_titre,(350,50))
            else:
                txt_titre=font.render("Leaderboard",True,(255,255,255))
                screen.blit(txt_titre,(350,50))

            if 10<=pos_souris[0]<=60:
                if 10<=pos_souris[1]<=60:
                    pygame.draw.rect(screen,(75,0,0),(10,10,50,50))
                else:
                    pygame.draw.rect(screen,(0,0,0),(10,10,50,50))

            if pos_click is not None:
                if 10<=pos_click[0]<=60:
                    if 10<=pos_click[1]<=60:
                        etat=MENU
                        pos_click=None
            screen.blit(txt_fermer,(20,18))
           
            

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()