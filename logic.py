from random import *
from pygame import *
from random import *
from fruit import Fruit
from bombe import Bombe
from glaçon import Glaçon
import time

# class Fruit:
#     def __init__(self, x, y, speed, image,touche):
#         self.x = x
#         self.y = y
#         self.speed = speed
#         self.image = image
#         self.touche = touche
# class Glaçon(Fruit):
#     pass
# class Bombe(Fruit):
#     pass   

# Liste des touches possibles
liste_de_touche=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",",";",":","!","ù","$","*"]
liste_utilisé=[]
fruit_généré=[]

# Génère un fruit avec une touche aléatoire non utilisée
def génération_fruit(liste_de_touche,max_fruit):
    global liste_utilisé
    if len(fruit_généré)>=max_fruit:
        return
    fruit=Fruit()
    touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    while touche_aleatoire in liste_utilisé:
        touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    liste_utilisé.append(touche_aleatoire)
    fruit.touche= touche_aleatoire
    return fruit,liste_utilisé

#coupe les fruits générés en fonction des touches pressées
def couper(fruit_généré, pressed_chars):
    global liste_utilisé
    if not pressed_chars:
        return 0

    pressed = set(pressed_chars)
    removed = 0
    bombe =False
    glace=False
    # On itère sur une copie pour pouvoir retirer en place sans casser la boucle
    for f in list(fruit_généré):
        if f.touche in pressed:
            if isinstance(f, Bombe):
                bombe=True
                return bombe,glace
            elif isinstance(f, Glaçon):
                fruit_généré.remove(f)
                liste_utilisé.remove(f.touche)
                glace=True
            else:
                fruit_généré.remove(f)
                liste_utilisé.remove(f.touche)
                removed += 1    
                
    return removed,glace
# Génère une bombe avec une touche aléatoire non utilisée
def generer_bombe(liste_de_touche,max_fruit):
    global liste_utilisé
    if len(fruit_généré)>=max_fruit:
        return
    bombe=Bombe()
    touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    while touche_aleatoire in liste_utilisé:
        touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    liste_utilisé.append(touche_aleatoire)
    bombe.touche= touche_aleatoire
    return bombe

# Génère un glaçon avec une touche aléatoire non utilisée
def generer_glaçon(liste_de_touche,max_fruit):
    global liste_utilisé
    if len(fruit_généré)>=max_fruit:
        return
    glaçon=Glaçon()
    touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    while touche_aleatoire in liste_utilisé:
        touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    liste_utilisé.append(touche_aleatoire)
    glaçon.touche= touche_aleatoire
    return glaçon,liste_utilisé

 # Génère un fruit, une bombe ou un glaçon en fonction d'un nombre aléatoire
def tout_genere(liste_de_touche,max_fruit,vitesse):
    global liste_utilisé
    nb=randint(1,100)
    if nb<=70:
        fruit,liste_utilisé=génération_fruit(liste_de_touche,liste_utilisé,max_fruit)
        fruit.speed=vitesse
        time.sleep(randint(2,4)*0.1)
        return fruit,liste_utilisé
    elif nb==71 or nb==90:
        bombe,liste_utilisé=generer_bombe(liste_de_touche,liste_utilisé,max_fruit)
        bombe.speed=vitesse
        time.sleep(randint(2,4)*0.1)
        return bombe,liste_utilisé
    else:
        glacon,liste_utilisé=generer_glaçon(liste_de_touche,liste_utilisé,max_fruit)
        glacon.speed=vitesse
        time.sleep(randint(2,4)*0.1)
        return glacon,liste_utilisé
# Gestion des vies en cas de rattage 
def strike(fruit,vie:int):
    if isinstance(fruit, Fruit):
        vie-=1
    return vie

#determination de la defaite
def defaite(vie,bombe):
    if vie<=0 or bombe:
        vie = 0
        return True
    return False

#augmentation de la vitesse en fonction du score
def augmentation_vitesse(vitesse,score):
    if score %50==0:
        vitesse+=1
    return vitesse

def reset_game(fruit_généré,bombe):
    global liste_utilisé
    liste_utilisé.clear()
    fruit_généré.clear()
    bombe=False
    return liste_utilisé,fruit_généré,bombe

def choix_difficulte(nv):
    match nv:
        case 1:
            max_fruit=5
            vitesse=2
        case 2:
            max_fruit=7
            vitesse=3
        case 3:
            max_fruit=10
            vitesse=4
    return max_fruit,vitesse