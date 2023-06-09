from MODULES import *
from Ship import *
from FireBar import FireBar
from Enemy import Enemy
from PopUpWindow import PopupWindow
from Explosion import Explosion
from SolveProblem import AlgebraProblem
class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module.

        pygame.display.set_caption("Game Launcher")
        self.menu_music = os.path.join(img_dir,"menu_music.mp3")
        self.game1_music = os.path.join(img_dir,"music.mp3")

        pygame.mixer.music.load(self.menu_music)  # Load your music file.
        pygame.mixer.music.play(-1)

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.image.load(os.path.join(img_dir,"menu_background.jpg")).convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create a label
        self.hello_label = Label("Choose the game", 100, (255, 226, 254), (WINDOW_WIDTH/3 - 70,  WINDOW_HEIGHT/3 - 90))

        # Create buttons for each game option
        self.button1 = Button(self.surface, "Space invaders", 100, "white" ,WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50)
        self.button2 = Button(self.surface, "Play with algebra", 100, "white" , WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80)


        self.selected_game = None  # Initialize selected game to None
        self.popup_visible = False  # Flag to control popup visibility



    def run(self):
        pygame.mixer.music.load(self.menu_music)  # Load your music file.
        pygame.mixer.music.play(-1)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                    if self.button1.is_hovered():
                        self.selected_game = "Space invaders"
                        pygame.mixer.music.load(self.game1_music)
                        pygame.mixer.music.play(-1)
                        running = False
                    elif self.button2.is_hovered():
                        self.selected_game = "Play with algebra"
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
        elif self.selected_game == "Play with algebra":
             # to resolve circular importfrom PopUpWindow import PopupWindow
            game = Algebra(self.surface,self)
            pygame.mixer.music.stop()
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
        self.background = pygame.image.load(os.path.join(img_dir,"background.jpg")).convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Score label
        self.score_label = Label("SCORE", 50, (0, 150, 250), (22, 0))
        self.score_number_label = Label("0", 50, (150, 150, 250), (160, 0))
        self.score = 0

        # Ship setup
        self.user_movement_allowed = True
        self.ship = Ship(self.surface, self.background)

        # Lives/winning
        self.heart_image = pygame.image.load(os.path.join(img_dir,"heart.png")).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))
        self.lives = 3
        self.heart_spacing = 60

        self.player_lost = True

        # Enemies setup
        self.enemy_timer = pygame.time.get_ticks()
        self.enemies = []
        self.enemies_stopped = False
        self.spawn_time = 1500
        # Popup window setup (to restore lives)
        self.popup = PopupWindow(self.menu,self)

        # Firebar settup
        self.fire_bar = FireBar(self.surface, 20, 60, 20, 200, (0, 255, 0), (255, 0, 0), 10, 6000)


        # Explosion settup
        self.explosion_anim = []
        for i in range(5):
            filename = "regularExplosion0{}.png".format(i)
            img = pygame.image.load(os.path.join(img_dir,"explosions/{0}".format(filename))).convert_alpha()

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
    def remove_all_enemies_below(self):
        for i in self.enemies:
            if i.coord[1] < WINDOW_HEIGHT /2:
                self.enemies.remove(i)

    def pause_game(self):


        self.enemies_stopped = True
        self.user_movement_allowed = False
        for enemy in self.enemies:
            enemy.stop_moving()
        self.popup.show()  # Show the popup window
        pygame.mixer.music.stop()


    def resume_game(self):
        self.enemies_stopped = False
        self.user_movement_allowed = True
        for enemy in self.enemies:
            enemy.start_moving()
        self.lives = 3
        self.remove_all_enemies_below() # so that there were no collision again with the ship
        self.explosion.reset()

    def reset_game(self):
        self.enemies_stopped = False
        self.user_movement_allowed = True
        self.enemy = []
        self.lives = 3
        self.explosion.reset()

    def draw_lives(self):
        for i in range(self.lives):
            x = WINDOW_WIDTH - 185 + self.heart_spacing * i
            y = 7
            self.surface.blit(self.heart_image, (x, y))


    def collision_logic1(self):
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
    def collision_logic(self):
        for enemy in self.enemies:
            for bullet in self.ship.bullets:
                if math.dist(bullet.coord, enemy.coord) < enemy.my_size[0] - 30:
                    print("Bullet-Enemy collision detected!")  # Debug print
                    self.enemies.remove(enemy)
                    if bullet in self.ship.bullets:
                        self.ship.bullets.remove(bullet)
                    self.score += 1
                    self.score_number_label.update_text(str(self.score))
                    if self.score == 10 :
                        self.spawn_time -=200
                    if self.score == 15:
                        self.spawn_time -=200
                    if self.score == 25:
                        self.spawn_time -=200

                    if self.score == 10:
                        self.player_lost = False


            if math.dist(self.ship.coord, enemy.coord) < enemy.my_size[0] - 30:
                print("Ship-Enemy collision detected!")  # Debug print
                if self.lives > 0:
                    self.lives -= 1
                    self.enemies.remove(enemy)


    def run(self):
        while self.running:
            # Collision checking
            self.collision_logic()

            # Spawning the enemy every 2000 sec
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.enemy_timer

            if elapsed_time >= self.spawn_time:
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
                        if self.fire_bar.allow_fire():
                            self.ship.fire_bullet()

                        self.fire_bar.fire_bullet()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()  # Quit the pygame module
                    sys.exit()

            # Ship on the screen
            self.surface.blit(self.background, (0, 0))
            self.fire_bar.update()
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
                self.pause_game()
                if (not self.explosion.update()):
                    explosion_x = self.ship.coord[0] + 100
                    explosion_y = self.ship.coord[1] + 100
                    self.explosion.draw(self.surface, explosion_x, explosion_y)
                    # Pausing the game in case if the user chooses an option to
                    # restore the lives


            if self.player_lost == False:
                print("You won")
                self.pause_game()
                self.popup.draw_player_won(self.surface)

            if self.player_lost == True:
                self.popup.draw_player_lost(self.surface)

            self.fire_bar.draw()
            pygame.display.flip()



class Algebra: # Creating this class here to avoid circular importing in the future
    def __init__(self,surface, menu) -> None:
        self.surface = surface
        self.menu = menu
    def run(self):
        AlgebraProblem(self.menu, False).run()


game = Menu()
game.run()

