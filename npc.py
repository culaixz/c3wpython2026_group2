import pygame

class SilhouetteNPC:
    def __init__(self, x, y):
        # Grid Box Sizing Layout
        self.frame_w = 32
        self.frame_h = 32
        self.scale_factor = 3.0  # Scales up to 96x96 to match player size

        # Animation Clock Tracking Setup
        self.current_frame = 0
        self.animation_cooldown = 320  # Matches the slow breathing speed of the player
        self.last_update = pygame.time.get_ticks()

        # Loads and slices the 4 breathing frames from the front-facing row (Row 0)
        self.frames = self._slice_npc_frames()

        # Position and Hit-Box Footprint Configurations (Used by Interactables/Map Person)
        self.rect = pygame.Rect(x, y, int(self.frame_w * self.scale_factor), int(self.frame_h * self.scale_factor))

    def _slice_npc_frames(self):
        try:
            sheet = pygame.image.load("idleholder_sheet.png").convert_alpha()
        except pygame.error:
            # Safe code color backup box if image fails to load
            placeholder = pygame.Surface((self.frame_w * 4, self.frame_h), pygame.SRCALPHA)
            sheet = placeholder

        sliced_frames = []
        new_size = (int(self.frame_w * self.scale_factor), int(self.frame_h * self.scale_factor))

        # Crops all 4 columns from Row 0 (Facing Down/Front)
        for col_index in range(4):
            x = col_index * self.frame_w
            y = 0 * self.frame_h  # Index 0 is the front-facing row
            rect = pygame.Rect(x, y, self.frame_w, self.frame_h)

            frame_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
            frame_surface.blit(sheet, (0, 0), rect)
            frame_surface.set_colorkey((0, 0, 0))  # Strips black backdrops

            # Scales up to crisp pixel art size
            frame_surface = pygame.transform.scale(frame_surface, new_size)

            # Floods the sprite with a cold, pale ghostly blue mask
            frame_surface.fill((200, 220, 240), special_flags=pygame.BLEND_RGB_MULT)
            
            # Applies master transparency fade (100 out of 255 makes it see-through)
            frame_surface.set_alpha(100)

            sliced_frames.append(frame_surface)

        return sliced_frames

    def update(self):
        now = pygame.time.get_ticks()
        
        if now - self.last_update >= self.animation_cooldown:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= 4:
                self.current_frame = 0

    def draw(self, screen):
        active_sprite = self.frames[self.current_frame]

        # Draws a faint copy slightly offset to create double vision
        echo_image = active_sprite.copy()
        echo_image.set_alpha(35)  # Makes the echo extra faint
        screen.blit(echo_image, (self.rect.x + 5, self.rect.y + 2))

        # Draws main ghost body layer on top
        screen.blit(active_sprite, self.rect)


# =====================================================================
# STANDALONE SOLO TESTING ENVIRONMENT BLOCK
# =====================================================================
if __name__ == "__main__":
    import sys
    pygame.init()
    
    # Sets up a private standalone screen canvas
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Animated Ghost NPC Solo Test Environment")
    clock = pygame.time.Clock()
    
    # Spawns a group of static, breathing ghost silhouettes across the screen coordinates
    npc_list = [
        SilhouetteNPC(150, 150),  # Top-left ghost
        SilhouetteNPC(580, 120),  # Top-right ghost
        SilhouetteNPC(352, 400)   # Bottom-center ghost
    ]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Updates the internal animation timers for every single ghost NPC
        for npc in npc_list:
            npc.update()
            
        # Graphics Rendering Layer
        screen.fill((50, 60, 75))  # Clears screen with slate backdrop
        
        # Draws all the animated ghost copies into the background
        for npc in npc_list:
            npc.draw(screen)
            
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()
