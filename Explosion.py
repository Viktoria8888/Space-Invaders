from MODULES import *


class Explosion:
    def __init__(self, frames):
        self.frames = frames  # List of explosion frames
        self.frame_index = 0  # Current frame index
        self.image = self.frames[self.frame_index]  # Current frame surface

    def update(self):
        self.frame_index += 1
        if self.frame_index >= len(self.frames):
            # Animation ended
            return True  # to indicate the explosion is finished
        else:
            self.image = self.frames[self.frame_index]
            return False

    def draw(self, surface, x, y):
        self.rect = self.image.get_rect(center=(x, y))
        # Draw the explosion on the given surface
        surface.blit(self.image, self.rect)

    # Missed that part (ChatGpt added)
    # "Why the explosion isn't displayed after the user restores lives?"
    def reset(self):
        # Reset the explosion animation
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
