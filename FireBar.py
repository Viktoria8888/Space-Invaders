# Author: Wiktoria Kaszpruk (Viktoriia Kashpruk)
import pygame

class FireBar:
    def __init__(self, surface, x, y, width, height, fill_color, empty_color, bullet_limit, time_threshold):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.empty_color = empty_color
        self.bullet_limit = bullet_limit
        self.time_threshold = time_threshold
        self.bullets_fired = 0
        self.bullet_timer = pygame.time.get_ticks()
        self.level = 1.0  # Initial fill level
        self.fire_allowed = True

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.bullet_timer

        # If the elapsed time exceeds the time threshold, reset the bullet count and timer
        if elapsed_time >= self.time_threshold:
            self.bullets_fired = 0
            self.bullet_timer = current_time

        # Calculate the fill level based on the remaining bullet limit
        remaining_bullets = self.bullet_limit - self.bullets_fired
        self.level = remaining_bullets / self.bullet_limit

        # Check if firing is allowed based on the bullet limit
        self.fire_allowed = self.bullets_fired < self.bullet_limit

    def fire_bullet(self):
        if self.fire_allowed:
            self.bullets_fired += 1

    def draw(self):
        fill_height = int(self.height * self.level)
        empty_height = self.height - fill_height
        fill_rect = pygame.Rect(self.x, self.y + empty_height, self.width, fill_height)
        empty_rect = pygame.Rect(self.x, self.y, self.width, empty_height)
        pygame.draw.rect(self.surface, self.fill_color, fill_rect)
        pygame.draw.rect(self.surface, self.empty_color, empty_rect)

    def allow_fire(self):
        return self.fire_allowed
