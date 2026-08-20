mport pygame
import players

pygame.init()

#Creating the screen of course! Without it there would be.. well.. no screen and no game.

WIDTH = 800
LENGTH = 600

screen = pygame.display.set_mode((WIDTH, LENGTH))

#Since the background is just one image and not like different sprites for the boxes and what not, they need rectangles for collision boxes.
class Collision:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)

#Different collision boxes
Cllbox1 = Collision("box1", 600, 56, 150, 131)
Cllbox2 = Collision("box2", 401, 320, 99, 225)
Cllbox3 = Collision("metalbox3", 150, 0, 75, 243)
Cllbox4 = Collision("metal4", 576, 358, 73, 241) 
Cllbox5 = Collision("collisionbox5", 0, 0, 25, 599) 
Cllbox6 = Collision("Hitbox6", 0, 0, 799, 10)
Cllbox7 = Collision("Hitbox7", 775, 0, 25, 599) 
Cllbox8 = Collision("Collisionbox8", 5, 595, 795, 599)
Cllbox9 = Collision("Collisionbox9", 325, 57, 75, 55)
Cllbox10 = Collision("Collisionbox10", 300, 75, 125, 20)
Cllbox11 = Collision("Collisionbox11", 350, 38, 24, 92)
Cllbox12 = Collision("Collisionbox12", 75, 414, 75, 96)
Cllbox13 = Collision("Collisionbox13", 125, 450, 75, 93)
Cllbox14 = Collision("Collisionbox14", 50, 432, 124, 57)
Cllbox15 = Collision("Collisionbox15", 124, 468, 100, 55)




maze_walls = [Cllbox1, Cllbox2, Cllbox3, Cllbox4, Cllbox5, Cllbox6, Cllbox7, Cllbox8, Cllbox9, Cllbox10, Cllbox11, Cllbox12, Cllbox13, Cllbox14, Cllbox15]

try:
    Background = pygame.image.load("NewestBGS.png")
    
    maze_walls.append(pygame.Rect(200, 400, 150, 20)) 
    maze_walls.append(pygame.Rect(500, 300, 100, 20))

except pygame.error:
    Background = None  

    maze_walls.clear()
   
    Othermap_collision = pygame.Rect(0, 500, 800, 100)
    maze_walls.append(Othermap_collision)

try:
    Background = pygame.image.load("NewestBGS.png").convert_alpha()
except pygame.error:
    Background = None
Background = pygame.transform.scale(Background, (WIDTH, LENGTH))

#main run loop
running = True

while running:
    
 for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False 

#These allow the collision boxes to actually work.
 walk_sheet.rect.y = walk_y
 idle_sheet.rect.y = idle_y


 for item in maze_walls:
      if walk_sheet.rect.colliderect(item.rect):
           walk_sheet.rect.y = walk_y
           

 for item in maze_walls:
       if idle_sheet.rect.colliderect(item.rect):
            idle_sheet.rect.y = idle_y
            

 walk_sheet.rect.x = walk_x
 idle_sheet.rect.x = idle_x

 for item in maze_walls:
      if walk_sheet.rect.colliderect(item.rect):
           walk_sheet.rect.x = walk_x
           

 for item in maze_walls:
        if idle_sheet.rect.colliderect(item.rect):
                idle_sheet.rect.x = idle_x
                
        

#If the player doesnt have the background, they can have a screen with a darkgreen floor and a navy blue kinda background
 if Background is not None:
        screen.blit(Background, (0, 0))
 else:
        screen.fill((25, 25, 112))

 if Background is None:
    
        pygame.draw.rect(screen, (34, 139, 34), (0, 500, 800, 100))

#Wait do I even need this..? Uh.... I wont remove it cuz it works 
 pygame.display.flip()
