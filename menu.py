import pygame

CYAN_GLITCH = (0, 255, 240)   
TEXT_COLOR = (255, 255, 255)   
HOVER_COLOR = (255, 0, 128)    

def draw_button(text_str, font, x, y, mouse_pos):
    text_surface = font.render(text_str, True, TEXT_COLOR)
    rect = text_surface.get_rect(center=(x, y))

    hovered = rect.collidepoint(mouse_pos)
    active_color = HOVER_COLOR if hovered else TEXT_COLOR

    return text_str, rect, active_color


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.title_font = pygame.font.Font(None, 95)  
        self.button_font = pygame.font.Font(None, 65)
        self.names_font = pygame.font.Font(None, 30)
        self.currentstate = "inmenu"

        self.continueon = pygame.Rect(0, 0, 0, 0)
        self.settingsopened = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)

        try:
            self.bg_image = pygame.image.load("NewestBGS.png").convert_alpha()
            self.bg_image = pygame.transform.scale(self.bg_image, (width, height))
        except pygame.error:
            self.bg_image = None

        self.dark_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.dark_overlay.fill((15, 12, 28, 170))  

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.currentstate == "inmenu":
                if self.continueon.collidepoint(event.pos):
                    self.currentstate = "start"
                elif self.settingsopened.collidepoint(event.pos):
                    self.currentstate = "credits"  
            elif self.currentstate == "credits":   
                if self.back_rect.collidepoint(event.pos):
                    self.currentstate = "inmenu"

    def draw_glitch_text(self, screen, text_str, font, center_pos, main_color):
        cyan_surf = font.render(text_str, True, CYAN_GLITCH)
        cyan_rect = cyan_surf.get_rect(center=(center_pos[0] - 3, center_pos[1]))
        screen.blit(cyan_surf, cyan_rect)

        main_surf = font.render(text_str, True, main_color)
        main_rect = main_surf.get_rect(center=center_pos)
        screen.blit(main_surf, main_rect)

    def draw(self, screen, mouse_pos):
        import random 

        if self.bg_image is not None:
            screen.blit(self.bg_image, (0, 0))
            
            if random.random() < 0.40:
                for _ in range(random.randint(2, 5)):
                    slice_y = random.randint(0, self.height - 25)
                    slice_h = random.randint(4, 25) 
                    
                    glitch_offset_x = random.randint(-12, 12)
                    
                    slice_rect = pygame.Rect(12, slice_y, self.width - 24, slice_h)
                    bg_slice = self.bg_image.subsurface(slice_rect)
                    
                    screen.blit(bg_slice, (12 + glitch_offset_x, slice_y))
        else:
            screen.fill((20, 15, 30))

        screen.blit(self.dark_overlay, (0, 0))

        if self.currentstate == "inmenu":
            self.draw_glitch_text(screen, "Archery Arena", self.title_font, (self.width // 2, 140), TEXT_COLOR)

            start_str, self.continueon, start_color = draw_button("Start", self.button_font, self.width // 2, 290, mouse_pos)
            credits_str, self.settingsopened, credits_color = draw_button("Credits", self.button_font, self.width // 2, 390, mouse_pos)

            self.draw_glitch_text(screen, start_str, self.button_font, (self.width // 2, 290), start_color)
            self.draw_glitch_text(screen, credits_str, self.button_font, (self.width // 2, 390), credits_color)

        elif self.currentstate == "credits":  
            self.draw_glitch_text(screen, "Team:", self.title_font, (self.width // 2, 70), TEXT_COLOR)

            team_names = ["Victoria Aung", "Titianna Wells", "Riko Wells", "Dwaino Goldison"]
            start_y = 135
            spacing_gap = 42
            
            for index, name in enumerate(team_names):
                target_y = start_y + (index * spacing_gap)
                self.draw_glitch_text(screen, name, self.names_font, (self.width // 2, target_y), TEXT_COLOR)

            audio_header_y = start_y + (len(team_names) * spacing_gap) + 15
            self.draw_glitch_text(screen, "Audio Credits:", self.button_font, (self.width // 2, audio_header_y), TEXT_COLOR)

            audio_credits = ["@1ohmygon", "@637rxss", "@joshbae_", "prod.jeejee"]
            audio_start_y = audio_header_y + 45
            audio_gap = 35
            
            for index, credit in enumerate(audio_credits):
                target_y = audio_start_y + (index * audio_gap)
                self.draw_glitch_text(screen, credit, self.names_font, (self.width // 2, target_y), TEXT_COLOR)

            back_str, self.back_rect, back_color = draw_button("Back", self.button_font, self.width // 2, 550, mouse_pos)
            self.draw_glitch_text(screen, back_str, self.button_font, (self.width // 2, 550), back_color)
