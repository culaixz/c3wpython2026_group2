import pygame

WIDTH = 800
LENGTH = 600

class Collision:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

maze_walls = [
    Collision("box1", 610, 62, 120, 132),
    Collision("box2", 401, 320, 99, 215),
    Collision("metalbox3", 150, 0, 75, 243),  
    Collision("metal4", 576, 358, 73, 241),    
    Collision("collisionbox5", -60, 0, 25, 600), 
    Collision("Hitbox6", 0, -25, 799, 25),
    Collision("Hitbox7", 835, 0, 25, 600), 
    Collision("Collisionbox8", 5, 595, 795, 599),
    Collision("Collisionbox9", 335, 68, 55, 45),
    Collision("Collisionbox10", 312, 80, 101, 20),
    Collision("Collisionbox11", 350, 56, 24, 72),
    Collision("Collisionbox12", 65, 414, 85, 96),
    Collision("Collisionbox13", 100, 450, 50, 93),
    Collision("Collisionbox14", 65, 432, 85, 45),
    Collision("Collisionbox15", 100, 468, 85, 55)
]


try:
    Background = pygame.image.load("NewestBGS.png").convert_alpha()
    Background = pygame.transform.scale(Background, (WIDTH, LENGTH))
except pygame.error:
    Background = None  
