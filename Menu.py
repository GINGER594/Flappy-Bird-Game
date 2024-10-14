import pygame

class Menu:
    def __init__(self, font):
        #defining font
        self.font = font
        #defining screen
        self.scrn = pygame.display.get_surface()
        #defining menu text
        self.menuText = font.render("PRESS ENTER", False, "white")

    def Update(self, gamestate):
        #checking for inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = "quit"
            #checking for player pressing enter (or backslash so that you can start a new game without taking your hand off the arrow keys/spacebar)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_BACKSLASH):
                gamestate = "game"
        
        #displaying menu
        self.scrn.fill("black")
        self.scrn.blit(self.menuText, ((self.scrn.get_width() / 2) - (self.menuText.get_width() / 2), (self.scrn.get_height() / 2) - (self.menuText.get_height() / 2)))
        pygame.display.update()
        return gamestate