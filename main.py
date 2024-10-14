import pygame, Menu, Game, GameOverMenu

#initializing pygame
pygame.init()

#defining screen and setting caption
scrn = pygame.display.set_mode((270, 400))
pygame.display.set_caption("Flappy Bird");
pygame.display.set_icon(pygame.image.load("icon.png"))

clock = pygame.time.Clock()

#defining font
font = pygame.font.SysFont("PressStart2P", 20)

#defining menu, game and game over menu objects
menu = Menu.Menu(font)
game = Game.Game(font)
gameovermenu = GameOverMenu.GameOverMenu(font)

#setting gamestate to start with the main menu
gamestate = "menu"

#loop
run = True
while gamestate != "quit":
    
    #running the main menu
    if gamestate == "menu":
        gamestate = menu.Update(gamestate)
        if gamestate == "game":
            game.Reset()

    #running the game
    if gamestate == "game":
        gamestate, score = game.Update(gamestate)

    #running the game over menu
    if gamestate == "over":
        gamestate = gameovermenu.Update(gamestate, score)
        if gamestate == "game":
            game.Reset()

    #capping the framerate at 60
    clock.tick(60)
pygame.quit()