#!/usr/bin/env python
from MODULES import *
from Ship import *
from FireBar import FireBar
from Enemy import Enemy
from PopUpWindow import PopupWindow
from Explosion import Explosion
from SolveProblem import AlgebraProblem

# Created "Menu" "Game" and "Algebra" classes
# in one file to avoid circular importing in the future

# ChatGpt taught me how to hadle different screens
# The key is just to have a class with run() and
# while loop in it.
# Even though it is better not to have
# while loops in pop-up windows
# because the program will crash  (two while loops at the same time :)


class Menu:
    def __init__(self):
        # Initializing modules.
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Game Launcher")

        # Music background
        self.menu_music = os.path.join(img_dir, "menu_music.mp3")
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.play(-1)

        # Screen
        self.surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.background = pygame.image.load(
            os.path.join(img_dir, "menu_background.jpg")).convert()
        self.background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create a label
        self.hello_label = Label(
            "Choose the game", 100, (255, 226, 254), (WINDOW_WIDTH/3 - 70,  WINDOW_HEIGHT/3 - 90))

        # Create buttons for each game option
        self.button1 = Button(self.surface, "Space invaders",
                              100, "white", WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50)
        self.button2 = Button(self.surface, "Play with algebra",
                              100, "white", WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80)

        self.selected_game = None  # Initialize selected game to None
        self.popup_visible = False  # Flag to control popup visibility

    def run(self):
        pygame.mixer.music.load(self.menu_music)  # Load your music file.
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    pygame.quit()  # Quit the pygame module
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    # Check if a button was clicked
                    if self.button1.is_hovered():
                        self.selected_game = "Space invaders"

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
            game = Algebra(self.surface, self)
            pygame.mixer.music.stop()  # stop menu music
            game.run()

        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()  # Exit the program


class Game1:
    def __init__(self, surface, menu):
        self.game1_music = os.path.join(img_dir, "music.mp3")
        self.blaster_music = os.path.join(img_dir, "blaster.wav")
        self.ship_explode = os.path.join(img_dir, "ship_explode.wav")
        self.music_player_won = os.path.join(img_dir, "player-congrats.wav")
        self.enemy_punch = os.path.join(img_dir, "enemy_punch.wav")

        # Game screen setup

        self.menu = menu
        self.running = True
        self.surface = surface
        self.background = pygame.image.load(
            os.path.join(img_dir, "background.jpg")).convert()
        self.background = pygame.transform.scale(
            self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Score label
        self.score_label = Label("SCORE", 50, (0, 150, 250), (22, 0))
        self.score_number_label = Label("0", 50, (150, 150, 250), (160, 0))
        self.score = 0

        # Ship setup
        self.user_movement_allowed = True
        self.ship = Ship(self.surface, self.background)

        # Lives/winning
        self.heart_image = pygame.image.load(
            os.path.join(img_dir, "heart.png")).convert_alpha()
        self.heart_image = pygame.transform.scale(self.heart_image, (40, 40))
        self.lives = 3
        self.heart_spacing = 60

        self.player_lost = True

        # Enemies setup
        self.enemy_timer = pygame.time.get_ticks()
        self.enemies = []
        self.enemies_stopped = False
        self.spawn_time = 1300
        # Popup window setup (to restore lives)
        self.popup = PopupWindow(self.menu, self)

        # Firebar settup
        self.fire_bar = FireBar(self.surface, 20, 60,
                                20, 200, (0, 255, 0), (255, 0, 0), 10, 6000)

        # Explosion settup
        self.explosion_anim = []
        for i in range(5):
            filename = "regularExplosion0{}.png".format(i)
            img = pygame.image.load(os.path.join(
                img_dir, "explosions/{0}".format(filename))).convert_alpha()

            img_lg = pygame.transform.scale(img, (350, 350))
            # To extend the time of my animation of the
            # explosion the frame multiple times would be
            # added to the frame list
            for _ in range(25):  # "_" in Python means that we are not goint to use
                # the variable in the iteration
                self.explosion_anim.append(img_lg)
        self.explosion = Explosion(self.explosion_anim)

    def spawn_enemy(self):
        if not self.enemies_stopped:
            new_enemy = Enemy(self.surface, self.background)
            self.enemies.append(new_enemy)

    def remove_all_enemies_below(self):
        for i in self.enemies:
            if i.coord[1] < WINDOW_HEIGHT / 2:
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
        # so that there were no collision again with the ship
        self.remove_all_enemies_below()
        self.explosion.reset()
        self.music()

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

    def collision_logic(self):
        # Traversing the list of bullet objects and enemy objects then
        # checking one by one if the Euclidean distance is less than
        # some tolerance
        for enemy in self.enemies:
            for bullet in self.ship.bullets:
                if math.dist(bullet.coord, enemy.coord) < enemy.my_size[0] - 30:
                    print("Bullet-Enemy collision detected!")  # Debug print
                    self.enemies.remove(enemy)
                    if bullet in self.ship.bullets:
                        self.ship.bullets.remove(bullet)
                    self.score += 1
                    self.score_number_label.update_text(str(self.score))
                    if self.score == 10:
                        self.spawn_time -= 200
                    if self.score == 15:
                        self.spawn_time -= 200
                    if self.score == 25:
                        self.spawn_time -= 200

                    if self.score == 42:
                        self.player_lost = False
                        m3 = pygame.mixer.Sound(self.music_player_won)
                        m3.set_volume(1)
                        m3.play()
            if math.dist(self.ship.coord, enemy.coord) < enemy.my_size[0] - 30:
                if self.lives > 0:
                    self.lives -= 1
                    # Enemy-ship collision sound
                    m4 = pygame.mixer.Sound(self.enemy_punch)
                    m4.play()
                    m4.set_volume(0.5)
                    self.enemies.remove(enemy)

    def music(self):
        pygame.mixer.music.load(self.game1_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

    def run(self):
        # Music background
        self.music()
        while self.running:

            # Collision checking
            self.collision_logic()

            # Spawning the enemy every 1300 sec
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.enemy_timer

            if elapsed_time >= self.spawn_time:
                self.spawn_enemy()
                self.enemy_timer = current_time

            # Keys
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

                            # Load your music file.
                            m = pygame.mixer.Sound(self.blaster_music)
                            m.set_volume(0.1)
                            m.play()

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

            # Ship and fire bar on the screen
            self.surface.blit(self.background, (0, 0))
            self.fire_bar.update()
            self.ship.update()
            self.ship.draw()
            self.fire_bar.draw()

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
                    m2 = pygame.mixer.Sound(self.ship_explode)
                    m2.set_volume(0.2)
                    m2.play()
                    # Pausing the game in case if the user chooses an option to
                    # restore the lives
            # If the player won then call popup window with congratualations
            if self.player_lost == False:
                self.pause_game()
                self.popup.draw_player_won(self.surface)

            if self.player_lost == True:
                self.popup.draw_player_lost(self.surface)

            pygame.display.flip()


class Algebra:
    def __init__(self, surface, menu) -> None:
        self.surface = surface
        self.menu = menu

    def run(self):
        AlgebraProblem(self.menu, False).run()


game = Menu()
game.run()

# Other questions to ChatGpt that helped me to fix bugs:
# "Why blaster.mp3 doesn't work with pygame.mixer.Sound()?"
# "Why on earth does the bullet disapper after the very moment is was fired?????"
# "Is there a way to omit storing bullets and enemies in a list. Is there some pygame
# feature?"
# "Can you help me to fix my fire bar?"
# And so on...
