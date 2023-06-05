from MODULES import *
class Button:
    def __init__(self, surface, text, font_size, color, x, y, width=None, height=None, callback=None):
        self.surface = surface
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.callback = callback

    def draw(self):
        text_surface = self.font.render(self.text, True, "black")
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x, self.y)
        pygame.draw.rect(self.surface, self.color, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), border_radius=10)
        pygame.draw.rect(self.surface, (255, 255, 255), (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20), border_radius=10, width=5)
        self.surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.is_hovered():
            if self.callback:
                self.callback()

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.width is None or self.height is None:
            text_surface = self.font.render(self.text, True, self.color)
            text_rect = text_surface.get_rect()
            self.width = text_rect.width + 20
            self.height = text_rect.height + 20
        return self.x - self.width / 2 < mouse_pos[0] < self.x + self.width / 2 and self.y - self.height / 2 < mouse_pos[1] < self.y + self.height / 2
