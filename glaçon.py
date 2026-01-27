import pygame
from fruit import Fruit

class Glaçon(Fruit):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/images/glaçon.png"), (80, 80))
    
    