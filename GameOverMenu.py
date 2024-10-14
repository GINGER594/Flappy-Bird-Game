import pygame

class GameOverMenu:
    def __init__(self, font):
        #defining font
        self.font = font
        #defining screen
        self.scrn = pygame.display.get_surface()
        #defining game over menu text
        self.menuText = font.render("GAME OVER", False, "red")
        self.menuText2 = font.render("PRESS ENTER", False, "red")

    def Update(self, gamestate, score):
        #checking for player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = "quit"
            #checking for player pressing enter (or backslash so that you can start a new game without taking your hand off the arrow keys/spacebar)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_BACKSLASH):
                gamestate = "game"
        
        #displaying game over menu
        self.scrn.fill("black")
        self.scrn.blit(self.font.render(str(score), False, "white"), (5, 5))
        self.scrn.blit(self.menuText, ((self.scrn.get_width() / 2) - (self.menuText.get_width() / 2), (self.scrn.get_height() / 2) - (self.menuText.get_height() / 2)))
        self.scrn.blit(self.menuText2, ((self.scrn.get_width() / 2) - (self.menuText2.get_width() / 2), (self.scrn.get_height() / 2) + (self.font.get_height() / 2)))
        pygame.display.update()
        return gamestate        