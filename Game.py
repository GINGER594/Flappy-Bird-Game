import pygame, random

class Game:
    def __init__(self, font):
        #defining font
        self.font = font
        #defining screen
        self.scrn = pygame.display.get_surface()

        #defining player size and images (flapping up and flapping down)
        self.playerSize = 20
        self.playerImg1 = pygame.image.load("bird1.png")
        self.playerImg1 = pygame.transform.scale(self.playerImg1, (self.playerSize + 15, self.playerSize + 7))
        self.playerImg2 = pygame.image.load("bird2.png")
        self.playerImg2 = pygame.transform.scale(self.playerImg2, (self.playerSize + 15, self.playerSize + 7))

        #setting default image to flap down and setting flap counter to 0
        self.currentPlayerImg = self.playerImg1
        self.flapCounter = 0
        #player rotate variables
        self.playerAngle = 0
        self.rotateSpeed = 3
        self.minPlayerAngle = -35
        self.maxPlayerAngle = 35

        #setting max velocity (downwards) and gravity
        self.maxVel = -7
        self.gravity = 1

        #setting pipe dimensions and speed, then loading pipe image
        self.pipeWidth = 50
        self.gapSize = 125
        self.pipeSpeed = 3
        self.pipeImg = pygame.image.load("pipe.png")

        #loading floor image
        self.floorImg = pygame.image.load("floor.png")
        self.floorImg = pygame.transform.scale(self.floorImg, (self.scrn.get_width() * 2, 25))
        self.floorX = 0

        #loading background image, setting its staring x coord to 0 and setting its scroll speed to 1
        self.bgImg = pygame.image.load("bgimg.png")
        self.bgImg = pygame.transform.scale(self.bgImg, (self.scrn.get_width() * 2, self.scrn.get_height()))
        self.bgX = 0
        self.bgSpeed = 1

        #running self.Reset() method
        self.Reset()

    def Reset(self):
        #setting player pos to default position
        self.playerPos = pygame.Vector2((self.scrn.get_width() / 3) - (self.playerSize / 2), (self.scrn.get_height() / 2) - (self.playerSize / 2))
        self.playerAngle = 0

        #setting score, counter, and player velocity to 0
        self.score = 0
        self.counter = 0
        self.vel = 0

        #clearing the pipes and scoreBoxes lists
        self.pipes = []
        self.scoreBoxes = []

    def Update(self, gamestate):
        #awaiting player input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamestate = "quit"
            #jumping (increases player velocity, sets image to flapping up and sets flap counter to 10)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w):
                self.vel = 11
                self.currentPlayerImg = self.playerImg2
                self.flapCounter = 12

        #decrements flap counter to that the image defaults after a few milliseconds and rotating player
        if self.flapCounter > 0:
            self.flapCounter -= 1
            #rotating player upward if flapcounter > 0
            if self.playerAngle < self.maxPlayerAngle:
                self.playerAngle += self.rotateSpeed
        else:
            #rotating them downward otherwise
            if self.playerAngle > self.minPlayerAngle:
                self.playerAngle -= self.rotateSpeed

        #setting default player image and flap counter is 0
        if self.flapCounter == 0:
            self.currentPlayerImg = self.playerImg1
                
        #accelerating downward
        if self.vel > self.maxVel:
            self.vel -= self.gravity

        #moving the player vertically
        self.playerPos.y -= self.vel

        #stopping the player from flying ontop of the screen
        if self.playerPos.y <= 0:
            self.playerPos.y = 0

        #stopping the player from falling off the screen
        if self.playerPos.y >= self.scrn.get_height() - self.floorImg.get_height() - self.playerSize:
            self.playerPos.y = self.scrn.get_height() - self.floorImg.get_height() - self.playerSize
            gamestate = "over"

        #updating player rect
        player = pygame.Rect(self.playerPos.x, self.playerPos.y, self.playerSize, self.playerSize)

        #generating pipes
        if len(self.pipes) == 0:
            height = random.randint(0, self.scrn.get_height() - self.gapSize)
            self.pipes.append({"pipe": pygame.Rect(self.scrn.get_width() + self.pipeWidth, 0, self.pipeWidth, height), "height": height})
            self.pipes.append({"pipe": pygame.Rect(self.scrn.get_width() + self.pipeWidth, height + self.gapSize, self.pipeWidth, self.scrn.get_height() - height - self.gapSize), "height": height})
            self.scoreBoxes.append(pygame.Rect(self.scrn.get_width() + self.pipeWidth, height, self.pipeWidth, self.gapSize))

        #moving pipes
        for x, pipe in enumerate(self.pipes):
            pipe["pipe"].x -= self.pipeSpeed
            #checking for player collision
            if player.colliderect(pipe["pipe"]):
                gamestate = "over"
            #removing pipes from the list if they go off screen
            if pipe["pipe"].x <= -self.pipeWidth:
                self.pipes.pop(x)

        #moving score boxes
        for x, scoreBox in enumerate(self.scoreBoxes):
            scoreBox.x -= self.pipeSpeed
            #checking for player collision and incremented score if true, then removing the scoreBox from scoreBoxes
            if player.colliderect(scoreBox):
                self.score += 1
                self.scoreBoxes.pop(x)

        #moving floor
        if self.floorX < self.scrn.get_width() - self.floorImg.get_width():
            #loopijng floor
            self.floorX = 0
        else:
            #scrolling floor
            self.floorX -= self.pipeSpeed

        #moving background
        if self.bgX < self.scrn.get_width() - self.bgImg.get_width():
            #looping background
            self.bgX = 0
        else:
            #scrolling the background
            self.bgX -= self.bgSpeed

        #draw statements
        #drawing background
        self.scrn.blit(self.bgImg, (self.bgX, 0))
        #drawing player
        self.scrn.blit(pygame.transform.rotate(self.currentPlayerImg, self.playerAngle), (player.x - (self.playerSize / 2), player.y - (self.playerSize / 2)))
        #drawing pipes
        for x, pipe in enumerate(self.pipes):
            if x % 2 == 0:
                pipeImg = pygame.transform.scale(self.pipeImg, (self.pipeWidth, pipe["height"]))
                pipeImg = pygame.transform.rotate(pipeImg, 180)
                self.scrn.blit(pipeImg, pipe["pipe"])
            else:
                pipeImg = pygame.transform.scale(self.pipeImg, (self.pipeWidth, self.scrn.get_height() - self.gapSize - pipe["height"]))
                self.scrn.blit(pipeImg, pipe["pipe"])
        #drawing floor
        self.scrn.blit(self.floorImg, (self.floorX, self.scrn.get_height() - self.floorImg.get_height()))
        #drawing score text
        scoreText = self.font.render(str(self.score), False, "white")
        self.scrn.blit(scoreText, (5, 5))
        pygame.display.update()
        #incrementing game counter
        self.counter += 1
        return gamestate, self.score