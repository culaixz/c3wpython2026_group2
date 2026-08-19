import pygame

color = (0, 0, 0)
hovercolor = (179, 217, 217)
backgroundcolor = (255, 255, 255)

def draw_button(text_str, font, x, y, mouse_pos):
    text = font.render(text_str, True, color)
    rect = text.get_rect(center=(x, y))

    hovered = rect.collidepoint(mouse_pos)
    hoveringcolor = hovercolor if hovered else color

    text = font.render(text_str, True, hoveringcolor)
    return text, rect


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.Font(None, 60)
        self.currentstate = "inmenu"

        self.continueon = pygame.Rect(0, 0, 0, 0)
        self.settingsopened = pygame.Rect(0, 0, 0, 0)
        self.back_rect = pygame.Rect(0, 0, 0, 0)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.currentstate == "inmenu":
                if self.continueon.collidepoint(event.pos):
                    self.currentstate = "start"
                elif self.settingsopened.collidepoint(event.pos):
                    self.currentstate = "settings"
            elif self.currentstate == "settings":
                if self.back_rect.collidepoint(event.pos):
                    self.currentstate = "inmenu"

    def draw(self, screen, mouse_pos):
        screen.fill(backgroundcolor)

        if self.currentstate == "inmenu":
            titlepage = self.font.render("Untitled " \
            "Archery Game", True, color)
            titleclick = titlepage.get_rect(center=(self.width // 2, 100))
            screen.blit(titlepage, titleclick)

            continuepage, self.continueon = draw_button("Start", self.font, self.width // 2, 400, mouse_pos)
            settingpage, self.settingsopened = draw_button("Settings", self.font, self.width // 2, 500, mouse_pos)

            screen.blit(continuepage, self.continueon)
            screen.blit(settingpage, self.settingsopened)

        elif self.currentstate == "settings":
            text_surf = self.font.render("Settings", True, color)
            text_rect = text_surf.get_rect(center=(self.width // 2, 100))
            screen.blit(text_surf, text_rect)

            back_surf, self.back_rect = draw_button("Back", self.font, self.width // 2, 450, mouse_pos)
            screen.blit(back_surf, self.back_rect)