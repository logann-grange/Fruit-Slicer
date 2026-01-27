import pygame
import sys
from sauvegarde import *

pygame.init()
screen=pygame.display.set_mode((1080,720))
pygame.display.set_caption("Découpeur de fruits")
clock=pygame.time.Clock()
font= pygame.font.SysFont("Arial", 42)

#variables global
MENU="menu"
JEU="jeu"
OPTION="option"
PAUSE="pause"
TABLEAU_SCORE="tableau_des_scores"
etat=MENU
ancien_etat=MENU
pos_click=None
d=1
l=0

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

            txt_btn_1 = font.render("Jouer", True, (255,255,255))
            txt_btn_2 = font.render("Options", True, (255,255,255))
            txt_btn_3 = font.render("Quitter :(", True, (255,255,255))
            txt_leaderboard = font.render ("|||", True, (255,255,255))

            pygame.draw.rect(screen,(0,255,0),(390,200,300,75))
            pygame.draw.rect(screen,(0,255,0),(390,325,300,75))
            pygame.draw.rect(screen,(255,0,0),(390,450,300,75))
            pygame.draw.rect(screen,(255,0,0),(10,10,50,50))

            if 390<=pos_souris[0]<=690:
                if 200<=pos_souris[1]<=275:
                    pygame.draw.rect(screen,(75,255,75),(390,200,300,75))
                else:
                    pygame.draw.rect(screen,(0,255,0),(390,200,300,75))

                if 325<=pos_souris[1]<=400:
                    pygame.draw.rect(screen,(75,255,75),(390,325,300,75))
                else:
                    pygame.draw.rect(screen,(0,255,0),(390,325,300,75))

                if 450<=pos_souris[1]<=525:
                    pygame.draw.rect(screen,(255,75,75),(390,450,300,75))
                else:
                    pygame.draw.rect(screen,(255,0,0),(390,450,300,75))

            elif 10<=pos_souris[0]<=60:
                if 10<=pos_souris[1]<=60:
                    pygame.draw.rect(screen,(255,75,75),(10,10,50,50))
                else:
                    pygame.draw.rect(screen,(255,0,0),(10,10,50,50))
        
            if pos_click is not None:    
                if 390<=pos_click[0]<=690:    
                    if 450<=pos_click[1]<=525:
                        running=False
                        pos_click=None
                    elif 200<=pos_click[1]<=275:
                        etat=JEU
                        pos_click=None
                    elif 325<=pos_click[1]<=400:
                        ancien_etat=etat
                        etat=OPTION
                        pos_click=None

                elif 10<=pos_click[0]<=60:
                    if 10<=pos_click[1]<=60:
                        ancien_etat=etat
                        etat=TABLEAU_SCORE
                        pos_click=None
            
            
            screen.blit(txt_btn_1 , (490,220))
            screen.blit(txt_btn_2 , (470,345))
            screen.blit(txt_btn_3 , (470,470))
            screen.blit(txt_leaderboard , (17,15))
           

        case "jeu" :

            screen.fill((0,0,0))
           
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
            
            txt_btn_1 = font.render("Niveau de difficulté", True, (255,255,255))
            txt_nv = font.render(nv_diff[d], True, (0,0,0))
            txt_l = font.render(lang[l], True, (0,0,0))
            txt_btn_3 = font.render("<", True, (255,255,255))
            txt_btn_4 = font.render(">", True, (255,255,255))
            
            pygame.draw.rect(screen, (0,255,0), (340,200,400,75))
            pygame.draw.rect(screen, (0,255,0), (255,200,75,75))
            pygame.draw.rect(screen, (0,255,0), (750,200,75,75)) 
            pygame.draw.rect(screen, (0,255,0), (390,325,300,75))
            pygame.draw.rect(screen, (0,255,0), (305,325,75,75))
            pygame.draw.rect(screen, (0,255,0), (700,325,75,75))
            pygame.draw.rect(screen, (0,255,0), (10,10,50,50)) 

            if pos_click is not None:
                if 10<=pos_click[0]<=60:
                    if 10<=pos_click[1]<=60:
                        etat=ancien_etat
                        pos_click=None
                elif 255<=pos_click[0]<=330:
                    if 200<=pos_click[1]<=275:
                        d = (d - 1) % 3
                        pos_click=None
                elif 750<=pos_click[0]<=825:
                    if 200<=pos_click[1]<=275:
                        d = (d + 1) % 3
                        pos_click=None
                elif 305<=pos_click[0]<=380:
                    if 325<=pos_click[1]<=380:
                        l = (l - 1) % 2
                        pos_click=None
                elif 700<=pos_click[0]<=775:
                    if 325<=pos_click[1]<=380:
                        l = (l + 1) % 2
                        pos_click=None

            screen.blit(txt_btn_1 , (370,150))
            screen.blit(txt_btn_3 , (25,10))
            screen.blit(txt_btn_3 , (280,215))
            screen.blit(txt_btn_3 , (330,340))
            screen.blit(txt_btn_4 , (775,215))
            screen.blit(txt_btn_4 , (725,340))
            screen.blit(txt_nv , (470,220))
            screen.blit(txt_l, (460,345))
            

        case "pause":
            screen.fill((0,0,0))
            
            txt_btn_1 = font.render("Reprendre", True, (255,255,255))
            txt_btn_2 = font.render("Options", True, (255,255,255))
            txt_btn_3 = font.render("Menu Principal", True, (255,255,255))
            
            pygame.draw.rect(screen, (0,255,0), (390,200,300,75))
            pygame.draw.rect(screen, (0,255,0), (390,325,300,75))
            pygame.draw.rect(screen, (255,0,0), (390,450,300,75))

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

            screen.blit(txt_btn_1 , (450,220))
            screen.blit(txt_btn_2 , (470,345))
            screen.blit(txt_btn_3 , (400,470))


        case "tableau_des_scores":

            screen.fill((0,0,0))
            
            txt_titre = font.render("Tableau des scores !", True, (255,255,255))
            scr= font.render(str(charger_scores()), True, (255,255,255))
            txt_fermer = font.render("X", True, (255,255,255))
            
            pygame.draw.rect(screen,(255,0,0),(10,10,1060,700))
            pygame.draw.rect(screen,(0,0,0),(10,10,50,50))

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
            
            screen.blit(txt_titre,(350,50))
            screen.blit(scr,(100,200))
            screen.blit(txt_fermer,(20,18))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()