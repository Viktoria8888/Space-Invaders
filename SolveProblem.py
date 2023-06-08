from Labels import Label
from MODULES import *
def random_problem():
    number_task = random.randint(1, 10)
    picture = "Math/problems/Problem{0}".format(number_task)

class AlgebraProblem:
    def __init__(self):

        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Chosing what algebra tast to display
        self.number_task = random.randint(1, 10)
        self.picture =  "Math/problems/Problem{0}".format(self.number_task)

        # Create a label
        self.hello_label = Label("Problem{0}".format(self.number_task),
                                  100, (255, 226, 254), (WINDOW_WIDTH/3 - 70,
                                                          WINDOW_HEIGHT/3 - 90))

        # Create buttons for each game option
        self.button1 = Button(self.surface, "Space invaders", 100, "white" ,
                              WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50)
        self.button2 = Button(self.surface, "Settings", 100, "white" ,
                               WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80)

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
            self.surface.fill((255,255,255))
            self.hello_label.draw(self.surface)
            self.button1.draw()
            self.button2.draw()
            pygame.display.flip()



        if self.selected_game is None:  # Check if the game was exited
            pygame.quit()  # Quit the pygame module
            sys.exit()  # Exit the program
