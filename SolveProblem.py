from Labels import Label
from MODULES import *
from Math.Solutions import solve_problem
def random_problem():
    number_task = random.randint(1, 8)
    picture = "Math/problems/Problem{0}".format(number_task)

class AlgebraProblem:
    def __init__(self):

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Chosing what algebra task to display
        # There is some problem with problem 6
        self.number_task = random.randint(1,8)
        self.picture =  pygame.image.load("Math/problems/Problem{0}.png".format(self.number_task))
        #self.picture = pygame.transform.scale(self.picture, (WINDOW_WIDTH, WINDOW_HEIGHT/3))
        # Create a label
        self.hello_label = Label("Problem № {0}".format(self.number_task),
                                  60, (255, 226, 254), (WINDOW_WIDTH/2 -110,
                                                          25))

        # Show the solution button
        self.show_sol_b = True
        self.button_sol = Button(self.surface, "Show the solution", 60, (193,254,255) ,
                              WINDOW_WIDTH/2 , WINDOW_HEIGHT /2)

        self.button1 = Button(self.surface, "Correct", 60, "white" ,
                              WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT - 80)
        self.button2 = Button(self.surface, "Wrong", 60, "white" ,
                               WINDOW_WIDTH/2 +100, WINDOW_HEIGHT - 80)
        self.label_playes_lost = Label("Work on your algebra more then!",
                                  60, (255, 226, 254), (WINDOW_WIDTH/2 -110,
                                                          WINDOW_HEIGHT /2))
        self.label_playes_won = Label("Nice job!",
                                  60, (255, 226, 254), (WINDOW_WIDTH/2 -110,
                                                          WINDOW_HEIGHT /2))
        self.clear_everything = False
        self.answer_showed = False
        self.correct = None

        self.selected_game = None



    def run(self):
        running = True
        while running:

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:

                    if self.button_sol.is_hovered():
                        self.show_sol_b = False
                        self.answer_showed = True

                    elif self.button1.is_hovered():
                        self.clear_everything = True
                        self.correct = True

                    elif self.button2.is_hovered():
                        self.clear_everything = True
                        self.correct = False


            self.surface.fill((255,255,255))

            if not self.clear_everything:
                self.hello_label.draw(self.surface)
                # This picture was displayed incorrectly
                if self.number_task == 7:
                    self.surface.blit(self.picture,(-10,  100))
                self.surface.blit(self.picture,(0,  100))
                if self.show_sol_b:
                    self.button_sol.draw()
                if self.answer_showed:
                    self.button1.draw()
                    self.button2.draw()
            # To make sure that everything disappears
            # and the text with the responce to the user's
            # answer pops up
            elif self.correct is not None:
                if self.correct:
                    self.label_playes_won.draw(self.surface)
                else:
                    self.label_playes_lost.draw(self.surface)

            pygame.display.flip()

        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()

