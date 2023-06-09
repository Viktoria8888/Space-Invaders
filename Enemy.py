from MODULES import *
class Enemy:
    def __init__(self, surface, back_picture, speed=1):
        self.surface = surface
        self.back_picture = back_picture
        self.my_size = (100, 100)
        image = pygame.image.load("resources/enemy.png").convert_alpha()
        self.block = pygame.transform.scale(image, self.my_size)

        self.coord = (0, 30)

        self.moving_left = False
        self.moving_right = False
        self.moving_down = False
        self.not_moving = False

        self.speed = speed

    def move(self):
        if self.moving_left and not self.not_moving:
            self.coord = (self.coord[0] - self.speed, self.coord[1])
        elif self.moving_right and not self.not_moving:
            self.coord = (self.coord[0] + self.speed, self.coord[1])
        if self.moving_down and not self.not_moving:
            self.coord = (self.coord[0], self.coord[1] + self.speed * 100)

        if self.coord[0] <= 0 and not self.not_moving:
            self.moving_left = False
            self.moving_right = True
            self.moving_down = True
        elif self.coord[0] >= WINDOW_WIDTH - self.my_size[0] and not self.not_moving:
            self.moving_left = True
            self.moving_right = False
            self.moving_down = True
        else:
            self.moving_down = False

    def update(self):

        if self.moving_left and not self.not_moving:
            self.move_left()
        elif self.moving_right and not self.not_moving:
            self.move_right()
        if self.moving_down and not self.not_moving:
            self.coord[1] += 90

        if self.coord[0] <= 0 and not self.not_moving:
            self.moving_left = False
            self.moving_right = True
            self.moving_down = True
        elif self.coord[0] >= WINDOW_WIDTH - self.my_size[0] and not self.not_moving:
            self.moving_left = True
            self.moving_right = False
            self.moving_down = True
        else:
            self.moving_down = False

    def draw(self):
        self.move()
        self.surface.blit(self.block, self.coord)

    def stop_moving(self):
        self.not_moving = True

    def start_moving(self):
        self.not_moving = False
