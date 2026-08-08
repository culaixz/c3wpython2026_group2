import pygame

class Player:
    def __init__(self, start_x, start_y):
      # Position tracking using decimal vectors
        self.pos = pygame.math.Vector2(start_x, start_y)
        self.speed = 5
        self.is_moving = False

      # Physical box dimensions for player placeholder
        self.width = 64
        self.height = 64

      # Screen Size Configuration
        self.screen_width = 800
        self.screen_height = 600

      # Primary hit-box used by our team for boundary and object collisions
        self.rect = pygame.Rect(self.pos.x, self.pos.y,
                                self.width, self.height)

      # Color palette states
        self.color_idle = (50, 150, 250) # Blue when still
        self.color_base_moving = (100, 255, 100) # Bright Green when moving
        self.color_flash_tint = (200, 255, 200)  # Neon green flashing during movement 

    def update(self):
        keys = pygame.key.get_pressed()  # WASD / Arrow keys

      # Reset direction vector every single frame
        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x = 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y = 1

        if direction.length() > 0:
            self.is_moving = True
            direction = direction.normalize()
            self.pos += direction * self.speed
            self.rect.topleft = (self.pos.x, self.pos.y)
        else:
            self.is_moving = False

    def draw(self, screen):
        if self.is_moving:
            current_time = pygame.time.get_ticks()
          
          # Divides time into 150ms windows. Checks if even or odd to alternate colors
            if (current_time // 150) % 2 == 0:
                current_color = self.color_flash_tint
            else:
                current_color = self.color_base_moving
        else:
            current_color = self.color_idle   # Returns to blue when keys are released

        pygame.draw.rect(screen, current_color, self.rect)
