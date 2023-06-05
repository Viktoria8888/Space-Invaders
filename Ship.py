from MODULES import *
from Bullet import Bullet
class Ship:
    def __init__(self, surface, back_picture):
        self.parent_screen = surface
        self.back_picture = back_picture
        self.my_size = (140,140)
        image = pygame.image.load("resources/ship1.png").convert_alpha()
        self.block = pygame.transform.scale(image, self.my_size)

        self.coord = [WINDOW_WIDTH/2,WINDOW_HEIGHT-150]


        self.moving_left = False
        self.moving_right = False

        # Ready - 0 You can't see the bullet on the screen.
        # Fire  - 1 The bullet is currently moving
        self.bullets = []
        self.bullet_state = False


    def update(self):
        if self.moving_left:
            self.move_left()
        elif self.moving_right:
            self.move_right()



    def move_left(self):
        self.coord = AddVectors(self.coord, DIRECTIONS["LEFT"])
        self.draw()

    def move_right(self):
        self.coord = AddVectors(self.coord, DIRECTIONS["RIGHT"])
        self.draw()

    def move_up(self):
        self.coord = AddVectors(self.coord, DIRECTIONS["UP"])
        self.draw()

    def move_down(self):
        self.coord = AddVectors(self.coord, DIRECTIONS["DOWN"])
        self.draw()

    def fire_bullet(self):
        x = self.coord[0] + self.my_size[0] / 2 - 25
        y = self.coord[1] - self.my_size[1] / 2
        bullet = Bullet(self.parent_screen, self.back_picture, (x, y))
        self.bullets.append(bullet)


    def draw(self):
        self.parent_screen.blit(self.back_picture, (0, 0))
        if self.coord[0] + self.my_size[0]/2 < 0:
            self.coord[0] = WINDOW_WIDTH - self.my_size[0]

        elif self.coord[1] < 0:
              self.coord[1] = WINDOW_HEIGHT - self.my_size[1]

        elif self.coord[0] > WINDOW_WIDTH:
              self.coord[0] =  0

        elif self.coord[1] > WINDOW_HEIGHT:
            self.coord[1] = 0

        self.parent_screen.blit(self.block, (self.coord[0], self.coord[1]))






