#  Découpeur de Fruits (Fruit Slicer Game)

Un jeu de type "Fruit Ninja" développé en Python avec Pygame où le joueur doit couper des fruits en appuyant sur les bonnes touches du clavier.

##  Description

Dans ce jeu, des fruits tombent du haut de l'écran avec des lettres assignées. Le joueur doit appuyer sur la touche correspondante pour "couper" le fruit. Attention aux bombes qui mettent fin à la partie et aux glaçons qui gèlent temporairement le jeu !

##  Fonctionnalités

- **3 niveaux de difficulté** : Facile, Moyen, Difficile
- **Types d'objets** :
  -  Fruits normaux (rapportent des points)
  -  Bombes (game over si coupées)
  -  Glaçons (gèlent le jeu pendant 5 secondes)
- **Système de score** avec sauvegarde des meilleurs scores
- **Support multilingue** : Français et Anglais
- **Effets sonores** lors de l'apparition des objets
- **Système de vies** : perdez une vie si un fruit tombe sans être coupé
- **Animation** : rotation et physique réaliste des objets

##  Comment jouer

1. Lancez le jeu et choisissez votre niveau de difficulté
2. Des fruits apparaissent avec une lettre assignée
3. Appuyez sur la touche correspondante pour couper le fruit
4. Évitez de couper les bombes 
5. Les glaçons  gèlent temporairement le jeu
6. Gagnez des points : 10 pts par fruit simple, 20 pts par combo

##  Niveaux de difficulté

### Facile
- Apparition : 2.5-4 secondes
- Fruits : 85%
- Glaçons : 5%
- Bombes : 10%

### Moyen
- Apparition : 1.5-3 secondes
- Fruits : 75%
- Glaçons : 5%
- Bombes : 20%

### Difficile
- Apparition : 1-2 secondes
- Fruits : 65%
- Glaçons : 5%
- Bombes : 30%

##  Installation

### Prérequis
- Python 3.x
- Pygame

### Installation des dépendances

```bash
pip install pygame
```

### Lancer le jeu

```bash
python main.py
```

##  Structure des fichiers

```
projet/
│
├── main.py                 # Fichier principal du jeu (boucle principale)
├── logique.py             # Logique du jeu et fonctions principales
├── menu.py                # Système de menus et interface
├── mouvement_pop.py       # Gestion des mouvements et apparitions
├── sauvegarde.py          # Gestion des scores et sauvegardes
├── translation.py         # Support multilingue
├── fruit.py               # Classe Fruit de base
├── bombe.py               # Classe Bombe (hérite de Fruit)
├── glaçon.py              # Classe Glaçon (hérite de Fruit)
├── translation.txt        # Fichier de traductions FR/EN
├── scores.txt             # Sauvegarde des meilleurs scores
│
└── assets/
    ├── images/
    │   ├── pomme.png
    │   ├── banane.png
    │   ├── pasteque.png
    │   ├── fraise.png
    │   ├── citron.png
    │   ├── bombe.png
    │   ├── glaçon.png
    │   ├── boom.png
    │   ├── fond_jeu.png
    │   ├── fond_glace.png
    │   ├── game.jpg
    │   ├── fond_menu.png
    │   ├── fond_logo.png
    │   ├── btn_pause.png
    │   ├── heart.png
    │   └── logoo.png
    │
    └── sons/
        ├── pop.mp3
        ├── coupe.wav
        ├── glace.wav
        ├── boom.wav
        ├── hurt.mp3
        ├── music_menu.mp3
        ├── musique_fond.mp3
        ├── musique_fond_tunnel.wav
        └── Game_over.mp3
```

##  Ressources nécessaires

### Images requises (dans `assets/images/`)
- **Fruits** : pomme.png, banane.png, pasteque.png, fraise.png, citron.png
- **Spéciaux** : bombe.png, glaçon.png, boom.png (explosion)
- **Interface** : game.jpg, fond_jeu.png, fond_glace.png (effet gel), fond_menu.png, fond_logo.png, logoo.png, btn_pause.png, heart.png (vies)

### Sons requis (dans `assets/sons/`)
- **Effets sonores** :
  - pop.mp3 : Son d'apparition des objets
  - coupe.wav : Son de coupe des fruits
  - glace.wav : Son d'activation du glaçon
  - boom.wav : Son d'explosion de la bombe
  - hurt.mp3 : Son de perte de vie
- **Musiques** :
  - music_menu.mp3 : Musique du menu principal
  - musique_fond.mp3 : Musique du jeu (normale)
  - musique_fond_tunnel.wav : Musique du jeu (effet tunnel pendant le gel)
  - Game_over.mp3 : Musique de game over

##  Contrôles

### Mode 0 : Mode Clavier (par défaut)
- **Lettres A-Z** et caractères spéciaux **( , ; : ! ù $ * )** : Couper les fruits
- Les touches assignées sont affichées au-dessus de chaque objet

### Mode 1 : Mode Souris
- **Clic gauche maintenu** : Tracer une ligne pour couper les fruits
- Déplacez la souris sur les fruits pour les couper
- Effet visuel de slash animé

### Contrôles communs
- **ESC** : Mettre en pause / Reprendre la partie
- **Bouton Pause** (en haut à gauche) : Accéder au menu pause
- **Clic souris** : Navigation dans les menus

##  Système de score

- **1 fruit coupé** = 10 points
- **Combo** (plusieurs fruits d'affilée) = 20 points par fruit
- Les **10 meilleurs scores** sont sauvegardés dans `scores.txt`
- Format JSON pour une sauvegarde persistante

##  Mécaniques de jeu

### Système de combo
- Coupez plusieurs fruits dans une fenêtre de **0.5 secondes** pour créer un combo
- Combo de 2 fruits ou plus = **20 points par fruit** au lieu de 10
- Affichage visuel "COMBO x[nombre]!" lors de la réussite d'un combo
- Le combo se réinitialise après 0.5s sans coupe

### Physique des objets
- Vitesse initiale aléatoire vers le haut
- Accélération gravitationnelle réaliste
- Mouvement horizontal avec rebonds sur les bords
- Rotation continue pour un effet réaliste

### Système musical dynamique
- **Musique du menu** : Lecture en boucle dans les menus
- **Musique de jeu** : Change en fonction de l'état du jeu
- **Effet tunnel** : La musique change automatiquement pendant le gel (glaçon)
- **Musique de game over** : Musique spécifique lors de la défaite

### Touches assignées
- Chaque objet reçoit une touche unique non utilisée
- Les touches sont libérées quand l'objet est coupé ou tombe
- Maximum d'objets à l'écran selon la difficulté

### Système de vies
- **3 vies** au début de la partie
- Perdez une vie si un fruit (normal) tombe sans être coupé
- Les bombes et glaçons ne font pas perdre de vies s'ils tombent
- Game over à **0 vie** ou si une **bombe est coupée**

### Effets visuels
- **Animation de slash** : Effet visuel lors de la coupe en mode souris
- **Effet de gel** : Overlay visuel bleu pendant l'activation du glaçon
- **Explosion** : Animation de boom lors de la coupe d'une bombe
- **Affichage des vies** : Cœurs en haut à droite de l'écran

##  Langues supportées

- 🇫🇷 **Français**
- 🇬🇧 **Anglais**

Changez la langue dans le menu **Options**.

##  Configuration

Le fichier `translation.txt` contient les traductions au format :
```
mot_clé:traduction_français:traduction_anglais
```

Exemple :
```
Jouer:Jouer:Play
Options:Options:Options
Quitter:Quitter:Quit
```

##  Fichiers principaux

### main.py
Boucle principale du jeu et gestion globale :
- Initialisation de Pygame et du mixer audio
- Gestion de la boucle principale (menu → jeu → menu)
- Système de combo avec fenêtre temporelle (0.5s)
- Gestion de la musique dynamique (normale/tunnel)
- Animation des slashes en mode souris
- Écran de game over avec saisie du nom
- Gestion des événements clavier et souris
- Affichage du score et des vies en temps réel

### logique.py (logic.py)
Fonctions de jeu essentielles :
- Génération aléatoire des objets (fruits, bombes, glaçons)
- Détection de coupe avec gestion des touches
- Gestion des vies et conditions de défaite
- Système de difficulté configurable
- Réinitialisation du jeu

### menu.py
Interface utilisateur complète :
- Menu principal avec boutons circulaires animés
- Menu options (difficulté, langue, mode de jeu)
- Menu pause avec overlay semi-transparent
- Tableau des meilleurs scores (top 10)
- Navigation intuitive avec feedback visuel

### mouvement_pop.py (movement.py)
Gestion dynamique des objets :
- Mouvement avec physique réaliste et accélération
- Apparition temporisée selon difficulté
- Effet de gel pour les glaçons (5 secondes)
- Gestion des collisions avec les bords

### sauvegarde.py
Persistance des données :
- Chargement/sauvegarde des scores au format JSON
- Calcul du score (simple/combo)
- Système de classement automatique des meilleurs scores
- Gestion des erreurs de fichier

##  Détails techniques

### Système audio
- **Mixer Pygame** : Gestion des effets sonores simultanés
- **Transition musicale fluide** : Synchronisation entre musique normale et effet tunnel
- **Volume ajusté** : 10% pour les musiques, 55% pour l'effet tunnel

### Performance
- **60 FPS** : Boucle de jeu optimisée pour un rendu fluide
- **Fenêtre de jeu** : 1080x720 pixels
- **Timer précis** : Utilisation de `datetime` pour les délais et animations

### Architecture
- **Programmation orientée objet** : Classes pour Fruit, Bombe, Glaçon
- **Héritage** : Bombe et Glaçon héritent de Fruit
- **Modularité** : Code séparé en modules logiques distincts

## 🐛 Bugs connus

Aucun bug majeur connu. Si vous en trouvez, n'hésitez pas à les signaler !

##  Améliorations possibles

- [ ] Améliorer les effets de particules lors de la coupe
- [ ] Ajouter des effets sonores variés pour chaque type de fruit
- [ ] Implémenter un système de niveaux progressifs
- [ ] Créer un mode multijoueur local (écran partagé)
- [ ] Ajouter plus de types de fruits spéciaux (ralentisseur, multiplicateur de points, etc.)
- [ ] Implémenter un système de succès/achievements
- [ ] Créer un mode entraînement sans game over
- [ ] Ajouter des thèmes visuels déblocables
- [ ] Optimiser la détection de collision en mode souris
- [ ] Ajouter un système de replay des meilleures parties

##  Crédits

Développé avec **Pygame** - Un projet de jeu éducatif en Python
-Logann grange
-Mohamed Mahamoud
-Clément Koch
##  Licence

Projet éducatif - Libre d'utilisation et de modification

---

**Bon jeu ! **

*Amusez-vous bien à découper des fruits !*
