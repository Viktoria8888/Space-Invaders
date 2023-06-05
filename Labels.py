from MODULES import *
class Label:
    def __init__(self, text, font_size, font_color, pos):
        self.font_obj = pygame.font.Font("resources/Foldit-Regular.ttf", font_size)
        self.font_color = font_color
        self.pos = pos
        self.text = text
        self.text_obj = self.font_obj.render(self.text, True, self.font_color)

    def update_text(self, new_text):
        self.text = new_text
        self.text_obj = self.font_obj.render(self.text, True, self.font_color)

    def draw(self, surface):
        surface.blit(self.text_obj, self.pos)
