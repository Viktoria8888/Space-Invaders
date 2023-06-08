from Labels import Label
from MODULES import *
def random_problem():
    number_task = random.randint(1, 8)
    picture = "Math/problems/Problem{0}".format(number_task)

class AlgebraProblem:
    def __init__(self):

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Chosing what algebra tast to display
        self.number_task = random.randint(1, 8)
        self.picture =  pygame.image.load("Math/problems/Problem{0}.png".format(self.number_task))
        #self.picture = pygame.transform.scale(self.picture, (WINDOW_WIDTH, WINDOW_HEIGHT))
        # Create a label
        self.hello_label = Label("Problem № {0}".format(self.number_task),
                                  60, (255, 226, 254), (WINDOW_WIDTH/2 -100,
                                                          25))

        # Create buttons for each game option
        self.button1 = Button(self.surface, "Correct", 60, "white" ,
                              WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50)
        self.button2 = Button(self.surface, "Wrong", 60, "white" ,
                               WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80)

        self.selected_game = None  # Initialize selected game to None
        self.popup_visible = False  # Flag to control popup visibility

    def display_correctly(self):
        m = self.number_task
        if m==1:
            pass




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
            self.surface.fill((255,255,255))
            self.hello_label.draw(self.surface)
            self.button1.draw()
            self.button2.draw()
            self.surface.blit(self.picture,(100,  200))
            pygame.display.flip()



        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()  # Exit the program
