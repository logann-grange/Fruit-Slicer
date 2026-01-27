import pygame
from fruit import Fruit

class Bombe(Fruit):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assets/images/bombe.png"), (90, 90))