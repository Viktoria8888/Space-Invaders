
from MODULES import *
from Solutions import *


class AlgebraProblem:
    def __init__(self, menu, play_state):
        self.menu = menu
        self.play_state = play_state

        self.range_problems = [x for x in range(1, 9) if x != 5 and x != 6]
        # Keep track of the last three problems
        self.last_three = [None, None, None]
        self.reset()

    # Random.choice would sometimes choose the same problem
    # 3 times in a row, so this class method would make
    # sure this would not happen
    def fairly_chosen(self):
        self.number_chosen = None
        while self.number_chosen is None or self.number_chosen in self.last_three:
            potential_number = random.choice(self.range_problems)
            self.number_chosen = potential_number
        # Update last_three list
        self.last_three.pop(0)
        self.last_three.append(self.number_chosen)
        return self.number_chosen

    # The AlgebraProblem class can be used more than
    # once while the program is running.
    # Screen initialization was moved to separed
    # method reset() but not to __init__ in order to
    # avoid situations when the state of this screen
    # stayed the same even after the current screen
    # was switched (e.g, "Space Invader" -> "Menu"
    # and then "Menu"->"Play with algebra")

    def reset(self):

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Chosing what algebra task to display
        # Decided to exclude 5th and 6th problem because the solution displayed would be not quite readable
        # random.choice([x for x in range(1, 8) if x != 5 and x!= 6])
        self.number_task = self.fairly_chosen()
        self.picture = pygame.image.load(os.path.join(
            math_dir, "Problem{0}.png".format(self.number_task))).convert()
        # self.picture = pygame.transform.scale(self.picture, (WINDOW_WIDTH, WINDOW_HEIGHT/3))
        # Create a label
        self.hello_label = Label("Problem № {0}".format(self.number_task),
                                 60, (255, 226, 254), (WINDOW_WIDTH/2 - 110,
                                                       25))
        self.show_image = False
        # Show the solution button
        self.show_sol_b = True
        self.button_sol = Button(self.surface, "Show the solution", 60, (193, 254, 255),
                                 WINDOW_WIDTH/2, WINDOW_HEIGHT / 2)

        self.button1 = Button(self.surface, "Correct", 60, "white",
                              WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT - 80)
        self.button2 = Button(self.surface, "Wrong", 60, "white",
                              WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT - 80)
        self.label_playes_lost = Label("Work on your algebra more then!",
                                       60, (255, 226, 254), (400,
                                                             WINDOW_HEIGHT / 2))
        self.label_playes_won = Label("Nice job!",
                                      100, (255, 226, 254), (WINDOW_WIDTH/2 - 150,
                                                             WINDOW_HEIGHT / 2 - 150))

        self.clear_everything = False
        self.answer_showed = False
        self.correct = None
        self.solution_label1 = Label("", 50, "black", (WINDOW_WIDTH/3 + 30,
                                                       WINDOW_HEIGHT / 2-40))
        self.solution_label2 = Label("", 50, "black", (WINDOW_WIDTH/3+30,
                                                       WINDOW_HEIGHT / 2))
        self.solution_label3 = Label("", 50, "black", (WINDOW_WIDTH/3+30,
                                                       WINDOW_HEIGHT / 2+40))
        if self.play_state:
            self.comeback_to_game = Button(self.surface, "Resume game", 40, "white",
                                           100, WINDOW_HEIGHT - 40)
        else:
            self.comeback_to_game = Button(self.surface, "Another problem", 40, "white",
                                           120, WINDOW_HEIGHT - 40)

        self.show_task = True

        self.selected_game = None

    def show_sol(self):
        num = self.number_task
        if num == 1:
            sol = solve_1()
            self.solution_label1.update_text("Image: " + sol["image"])
            # self.solution_label2.update_text("Kernel: " + sol["kernel"] )
        elif num == 2:
            sol = solve_2()
            self.solution_label1.update_text("dim(S+T): " + str(sol[0]))
            self.solution_label2.update_text("dim(S ^ T): " + str(sol[1]))

        elif num == 3:
            sol = solve_3()  # the list with booleans
            sol2 = " ".join(["Yes" if i else "No" for i in sol])
            self.solution_label1.update_text("Result: " + sol2)

        elif num == 4:
            sol = solve_4()
            sol2 = " ".join([str(i) for i in sol])
            self.solution_label1.update_text("It is invertable for" + sol2)
        elif num == 7:
            # Will also show the picture
            self.show_image = True
            self.answer_showed = True
            self.show_task = False

        elif num == 8:
            sol = solve_8()
            self.solution_label1.update_text(
                " ".join([str(i) for i in sol[0]]))
            self.solution_label2.update_text(
                " ".join([str(i) for i in sol[1]]))
            self.solution_label3.update_text(
                " ".join([str(i) for i in sol[2]]))

    def run(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    self.selected_game = None

                    return False
                    pygame.quit()  # Quit the pygame module
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:

                    if self.button_sol.is_hovered():  # Show solution button is clicked
                        self.show_sol_b = False
                        self.answer_showed = True

                        self.show_sol()

                    elif self.button1.is_hovered():
                        self.clear_everything = True
                        self.correct = True

                    elif self.button2.is_hovered():
                        self.clear_everything = True
                        self.menu.run()
                        running = False

                    elif self.comeback_to_game.is_hovered():
                        self.reset()
                        if self.play_state:
                            return True

            # Scren
            self.surface.fill((255, 255, 255))

            if not self.clear_everything:
                self.hello_label.draw(self.surface)
                # This picture was displayed incorrectly
                if self.show_sol_b:
                    self.button_sol.draw()
                if self.answer_showed:
                    self.solution_label1.draw(self.surface)
                    self.solution_label2.draw(self.surface)
                    self.solution_label3.draw(self.surface)
                    self.button1.draw()
                    self.button2.draw()
                # There was some problem with displaying problem 7
                # that is why the distinct clause is created for it
                if self.number_task == 7:
                    self.surface.blit(self.picture, (-10,  100))
                self.surface.blit(self.picture, (50,  100))
            # Created the flag for displaying the image solution
            if self.show_image:
                img = pygame.image.load(os.path.join(
                    math_dir, "sol7.png")).convert()

                self.surface.blit(img, (100, 20))

            # To make sure that everything disappears
            # and the text with the responce to the user's
            # answer pops up
            if self.correct is not None:
                if self.correct:
                    self.show_image = False
                    self.label_playes_won.draw(self.surface)
                    self.comeback_to_game.draw()
                else:
                    self.label_playes_lost.draw(self.surface)

            pygame.display.flip()

        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()
