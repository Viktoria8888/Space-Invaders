from MODULES import *


class Bullet:
    def __init__(self, surface, back_picture, coord):
        self.surface = surface
        self.back_picture = back_picture
        self.coord = coord
        self.bullet_size = (50, 50)
        self.bullet_image = pygame.image.load(
            os.path.join(img_dir, "bullet.png")).convert_alpha()
        self.bullet_image = pygame.transform.scale(
            self.bullet_image, self.bullet_size)

        self.speed = 5

    def move(self):
        x, y = self.coord
        y -= self.speed

        self.coord = (x, y)

    def draw(self):
        self.surface.blit(self.bullet_image, self.coord)
