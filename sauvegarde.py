import json

def score(points,nb_coupe):
    points+= nb_coupe*10
    return points
    
def charger_scores(score_file="score.txt"):
    try:
        with open(score_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            f.seek(0)
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []    

def sauvegarder_score(highscores, score_file="score.txt"):
    with open(score_file, "w", encoding="utf-8") as f:
        json.dump(highscores, f, ensure_ascii=False, indent=4)

#ajout d'un score dans la liste des highscores
def ajouter_score(nom_joueur, points,highscores):
    nouveau_score = {"Nom": nom_joueur, "Score": points}
    highscores.append(nouveau_score)
    highscores.sort(key=lambda x: x["Score"], reverse=True)
    sauvegarder_score(highscores)
