from random import *
import json
from pygame import *


class Fruit:
    def __init__(self, x, y, speed, image,touche):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = image
        self.touche = touche
class Glaçon(Fruit):
    pass
class Bombe(Fruit):
    pass   

liste_de_touche=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",",";",":","!","ù","$","*"]
liste_utilisé=[]
fruit_généré=[]

# Génère un fruit avec une touche aléatoire non utilisée
def génération_fruit(liste_de_touche,liste_utilisé,max_fruit):
    if len(fruit_généré)>=max_fruit:
        return
    fruit=Fruit()
    touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    while touche_aleatoire in liste_utilisé:
        touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    liste_utilisé.append(touche_aleatoire)
    fruit.touche= touche_aleatoire
    return fruit,liste_utilisé

# Calcule le score en fonction du nombre de fruits coupés
def score(points,nb_coupe):
    points+= nb_coupe*10
    return points
    
#coupe les fruits générés en fonction des touches pressées
def couper(fruit_généré, liste_utilisé, pressed_chars):
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
def generer_bombe(liste_de_touche,liste_utilisé,max_fruit):
    if len(fruit_généré)>=max_fruit:
        return
    bombe=Bombe()
    touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    while touche_aleatoire in liste_utilisé:
        touche_aleatoire=liste_de_touche[randint(0,len(liste_de_touche)-1)]
    liste_utilisé.append(touche_aleatoire)
    bombe.touche= touche_aleatoire
    return bombe,liste_utilisé

# Génère un glaçon avec une touche aléatoire non utilisée
def generer_glaçon(liste_de_touche,liste_utilisé,max_fruit):
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
def tout_genere(liste_de_touche,liste_utilisé,max_fruit):
    nb=random.randint(1,100)
    if nb<=70:
        fruit,liste_utilisé=génération_fruit(liste_de_touche,liste_utilisé,max_fruit)
        time.sleep(random.randint(1,3)*0.1)
        return fruit,liste_utilisé
    elif nb==71 or nb==90:
        bombe,liste_utilisé=generer_bombe(liste_de_touche,liste_utilisé,max_fruit)
        time.sleep(random.randint(1,3)*0.1)
        return bombe,liste_utilisé
    else:
        glacon,liste_utilisé=generer_glaçon(liste_de_touche,liste_utilisé,max_fruit)
        time.sleep(random.randint(1,3)*0.1)
        return glacon,liste_utilisé
# Gestion des vies en cas de rattage 
def strike(rater,vie):
    if rater :
        vie-=1
    return vie
# Chargement des scores depuis un fichier JSON
def charger_scores(score_file="scores.txt"):
    try:
        with open(score_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            f.seek(0)
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
# sauvegarde des scores dans un fichier JSON
def sauvegarder_score(highscores, score_file="scores.txt"):
    with open(score_file, "w", encoding="utf-8") as f:
        json.dump(highscores, f, ensure_ascii=False, indent=4)
#ajout d'un score dans la liste des highscores
def ajouter_score(nom_joueur, points,highscores):
    nouveau_score = {"Nom": nom_joueur, "Score": points}
    highscores.append(nouveau_score)
    highscores.sort(key=lambda x: x["Score"], reverse=True)
    sauvegarder_score(highscores)


#determination de la defaite
def defaite(vie,bombe):
    if vie<=0 or bombe:
        return True
    return False    