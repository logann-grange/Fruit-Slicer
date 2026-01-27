import random
import pygame

list_image = ["assets/images/pomme.png", "assets/images/banane.png"]
list_touche=["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",",",";",":","!","ù","$","*"]

class Fruit:
    def __init__(self, font):
        self.size = 90
        self.image_origin = pygame.transform.scale(pygame.image.load(list_image[random.randint(0,len(list_image)-1)]), (self.size, self.size))
        self.image = self.image_origin
        self.image
        self.coord_x = random.randint(0, 1000-self.size) #à modifier selon la taille x de l'écran et du fruit en gardant un format (0, 1000-taille_fruit)
        self.coord_y = 750 #à modifier par la taille y max de l'écran
        self.speed_y = -50 #50
        self.speed_x = random.uniform(-10, 10)
        self.speed_change_y = random.uniform(1.5, 2.7) #1.5 2.7
        self.angle = 0
        self.angle_direction = random.uniform(-3, 3)
        self.touche = list_touche[random.randint(0, len(list_touche)-1)]
        self.image_touche = font.render(self.touche, 1, (0, 0, 0))
    
    def acceleration(self):
        self.speed_y += self.speed_change_y
        if self.coord_x < 0 or self.coord_x > 1000-self.size :
            self.speed_x = -self.speed_x*0.7
    
    def movement(self):
        self.coord_y += self.speed_y
        self.coord_x += self.speed_x
    
    # def rotate(self):
    #     self.image = pygame.transform.rotate(self.image, 5)
    
    def rotate(self):
        self.angle += self.angle_direction
        self.angle %= 360  # Garde l'angle entre 0 et 360
        
        # Rotation à partir de l'original
        self.image = pygame.transform.rotate(self.image_origin, self.angle)
