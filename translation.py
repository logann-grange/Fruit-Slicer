def translate(word, lang:int) :
    if lang > 0 :
        with open('translation.txt', 'r') as fichier:
            ligne = fichier.readline() 
            while ligne:
                if ligne.strip().split(":")[0] == word :
                    return ligne.strip().split(":")[lang]
                ligne = fichier.readline()
    else :
        return word

lang = 1 # 0=fraçais, 1=anglais
print(translate('jouer', lang))