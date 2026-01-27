import random
import pygame

list_image = ["assets/images/pomme.png", "assets/images/banane.png"]

class Fruit:
    def __init__(self):
        self.size = 70
        self.image = pygame.transform.scale(pygame.image.load(list_image[random.randint(0,1)]), (self.size, self.size))
        self.coord_x = random.randint(0, 1000-self.size) #à modifier selon la taille x de l'écran et du fruit en gardant un format (0, 1000-taille_fruit)
        self.coord_y = 750 #à modifier par la taille y max de l'écran
        self.speed_y = -50
        self.speed_x = random.uniform(-10, 10)
        self.speed_change_y = random.uniform(1.5, 2.7)
    
    def acceleration(self):
        self.speed_y += self.speed_change_y
        if self.coord_x < 0 or self.coord_x > 1000-self.size :
            self.speed_x = -self.speed_x*0.7
    
    def movement(self):
        self.coord_y += self.speed_y
        self.coord_x += self.speed_x
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.image, 5)
