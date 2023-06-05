from MODULES import *


class Explosion:
    def __init__(self, frames):
        self.frames = frames  # List of explosion frames
        self.frame_index = 0  # Current frame index
        self.image = self.frames[self.frame_index]  # Current frame surface
          # Position of the explosion

    def update(self):
        # Update the explosion animation
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            # Animation ended
            return True  # Return True to indicate the explosion is finished
        else:
            self.image = self.frames[self.frame_index]
            return False

    def draw(self, surface,x,y):
        self.rect = self.image.get_rect(center=(x, y))
        # Draw the explosion on the given surface
        surface.blit(self.image, self.rect)
