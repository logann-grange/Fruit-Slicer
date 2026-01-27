import pygame
from fruit import Fruit

class Bombe(Fruit):
    def __init__(self, font):
        super().__init__(font)
        self.image_origin = pygame.transform.scale(pygame.image.load("assets/images/bombe.png"), (100, 100))
        self.image = self.image_origin