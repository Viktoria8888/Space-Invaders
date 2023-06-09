
import pygame
class FireBar:
    def __init__(self, surface, x, y, width, height, fill_color, empty_color):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.level = 1.0  # Initial level (100%)

    def update(self, dt):
        # Adjust the level based on the time passed (dt)
        fill_amount = dt / 3000  # Adjust the rate of decrease/increase here
        self.level = max(0, self.level - fill_amount)  # Decrease the level over time
        # Alternatively, you can increase the level by changing the sign of fill_amount
        # self.level = min(1, self.level + fill_amount)  # Increase the level over time

    def draw(self):
        fill_height = int(self.height * self.level)
        empty_height = self.height - fill_height
        fill_rect = pygame.Rect(self.x, self.y + empty_height, self.width, fill_height)
        empty_rect = pygame.Rect(self.x, self.y, self.width, empty_height)
        pygame.draw.rect(self.surface, self.fill_color, fill_rect)
        pygame.draw.rect(self.surface, self.empty_color, empty_rect)
