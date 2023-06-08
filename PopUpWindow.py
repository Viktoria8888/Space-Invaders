from MODULES import *
from SolveProblem import AlgebraProblem
class PopupWindow:
    def __init__(self, menu, game):
        self.menu = menu
        self.game = game
        self.width = 500
        self.height = 300
        self.x = (WINDOW_WIDTH - self.width) // 2
        self.y = (WINDOW_HEIGHT - self.height) // 2
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_alpha(200)
        self.visible = False
        self.new_window = AlgebraProblem()

    def show(self):
        self.visible = True


    def hide(self):
        self.visible = False

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))

            label1_text = "YOU'VE LOST!"
            label2_text = "Now, you would have to solve an algebra problem :)"
            label3_text = "If you want to restore your lives*"

            label1 = Label(label1_text, 50, "black", (self.x + 150, self.y + self.height // 2 - 65 - 30))
            label3 = Label(label2_text, 28, "black", (self.x + 10, self.y + self.height // 2 - 65 + 30))
            label2 = Label(label3_text, 24, "black", (self.x + 110, self.y + self.height // 2 - 65 + 70))

            label1.draw(surface)
            label2.draw(surface)
            label3.draw(surface)

            button1 = Button(surface, "Yes", 50, (199, 255, 252), self.x + self.width // 4, self.y + self.height // 2 + 90,
                             width=140, height=80)
            button2 = Button(surface, "No", 50, (255, 205, 199), self.x + self.width // 4 * 3,
                             self.y + self.height // 2 + 90, width=140, height=80)

            button1.draw()
            button2.draw()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.type == QUIT:
                        self.hide()
                        self.running = False

                    elif button1.is_hovered():
                        self.hide()  # Hide the current popup window
                        self.new_window.run()


                    elif button2.is_hovered():
                        self.menu.selected_game = None
                        self.hide()
                        self.running = False
                        self.menu.run()

                if event.type == QUIT:
                    self.hide()
                    self.running = False
                    self.game.running = False

