from MODULES import *
from Ship import *
from Labels import Label
from Button import Button
from Enemy import Enemy
from PopUpWindow import PopupWindow
from Explosion import Explosion

class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game Launcher")
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.image.load("resources/menu_background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create a label
        self.hello_label = Label("Choose the game", 100, (255, 226, 254), (WINDOW_WIDTH/3 - 70,  WINDOW_HEIGHT/3 - 90))

        # Create buttons for each game option
        self.button1 = Button(self.surface, "Space invaders", 100, "white" ,WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50)
        self.button2 = Button(self.surface, "Settings", 100, "white" , WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80)


        self.selected_game = None  # Initialize selected game to None
        self.popup_visible = False  # Flag to control popup visibility



    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                    if self.button1.is_hovered():
                        self.selected_game = "Space invaders"
                        running = False
                    elif self.button2.is_hovered():
                        self.selected_game = "Settings"
                        running = False

            # Draw the menu
            self.surface.blit(self.background, (0, 0))
            self.hello_label.draw(self.surface)
            self.button1.draw()
            self.button2.draw()
            pygame.display.flip()

        # Start the selected game
        if self.selected_game == "Space invaders":
            game = Game1(self.surface, self)
            game.run()
        elif self.selected_game == "Settings":
            game = Settings()
            game.run()

        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()  # Exit the program



class Game1:
    def __init__(self, surface, menu):
        # Game screen setup
        self.menu = menu
        self.running = True
        self.surface = surface
        self.background = pygame.image.load("resources/background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Score label
        self.score_label = Label("SCORE", 50, (0, 150, 250), (22, 0))
        self.score_number_label = Label("0", 50, (150, 150, 250), (160, 0))
        self.score = 0

        # Ship setup
        self.user_movement_allowed = True
        self.ship = Ship(self.surface, self.background)

        # Lives
        self.heart_image = pygame.image.load("resources/heart.png").convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))
        self.lives = 0
        self.heart_spacing = 60

        # Enemies setup
        self.enemy_timer = pygame.time.get_ticks()
        self.enemies = []
        self.enemies_stopped = False

        # Popup window setup (to restore lives)
        self.popup = PopupWindow(self.menu,self)

        # Explosion settup
        self.explosion_anim = []
        for i in range(5):
            filename = "regularExplosion0{}.png".format(i)
            img = pygame.image.load("resources/explosions/{0}".format(filename)).convert_alpha()

            img_lg = pygame.transform.scale(img, (350, 350))
            # I wanted to extend the time of my animation of the
            # explosion and couldn't come up with an idea
            # other than adding the frame multiple times
            # I know that this is a stupid solution
            # but it works :)
            for _ in range(25):
                self.explosion_anim.append(img_lg)
        self.explosion = Explosion(self.explosion_anim)

    def spawn_enemy(self):
        if not self.enemies_stopped:
            new_enemy = Enemy(self.surface, self.background)
            self.enemies.append(new_enemy)

    def pause_game(self):
        self.enemies_stopped = True
        self.user_movement_allowed = False
        for enemy in self.enemies:
            enemy.stop_moving()
        self.popup.show()
         # Show the popup window

    def draw_lives(self):
        for i in range(self.lives):
            x = WINDOW_WIDTH - 185 + self.heart_spacing * i
            y = 7
            self.surface.blit(self.heart_image, (x, y))


    def collision_logic(self):
        # Traversing the list of bullet objects and enemy objects then
        # checking one by one if the Euclidean distance is less than
        # some tolerance
        for enemy in self.enemies:
            for bullet in self.ship.bullets:
                if math.dist(bullet.coord, enemy.coord) < enemy.my_size[0] - 30:
                        self.enemies.remove(enemy)
                        if bullet in self.ship.bullets:
                            self.ship.bullets.remove(bullet)

                        # Updating the score
                        self.score += 1
                        self.score_number_label.update_text(str(self.score))
            # Collision with the enemy
            if math.dist(self.ship.coord, enemy.coord) < enemy.my_size[0] - 30:
                    if self.lives > 0:
                        self.lives -= 1
                        self.enemies.remove(enemy)


    def run(self):
        while self.running:
            # Spawning the enemy every 2000 sec
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.enemy_timer
            if elapsed_time >= 2000:
                self.spawn_enemy()
                self.enemy_timer = current_time

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menu.selected_game = None
                        self.running = False
                        self.menu.run()
                    elif event.key == pygame.K_LEFT and self.user_movement_allowed:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_RIGHT and self.user_movement_allowed:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_SPACE and self.user_movement_allowed:
                        self.ship.fire_bullet()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                elif event.type == pygame.QUIT:
                    self.running = False

            # Ship on the screen
            self.surface.blit(self.background, (0, 0))
            self.ship.update()
            self.ship.draw()

            # Displaying lives
            self.draw_lives()

            # Rendering moving objects
            for enemy in self.enemies:
                enemy.move()
                enemy.draw()

            for bullet in self.ship.bullets:
                bullet.move()
                bullet.draw()

            self.score_label.draw(self.surface)
            self.score_number_label.draw(self.surface)

            # Checking if the player lost
            if self.lives == 0:
                if self.explosion.update():
                    self.surface.blit(self.explosion_anim[40],(self.ship.coord[0]-80, self.ship.coord[1]-50))
                else:
                    explosion_x = self.ship.coord[0] + 100
                    explosion_y = self.ship.coord[1] + 100
                    self.explosion.draw(self.surface, explosion_x, explosion_y)
                    # Pausing the game in case if the user chooses an option to
                    # restore the lives
                    self.pause_game()

            if self.enemies_stopped:
                self.popup.draw(self.surface)

            self.collision_logic()
            pygame.display.flip()



class Settings:
    def run(self):
        print("hello")

game = Menu()
game.run()
input()
