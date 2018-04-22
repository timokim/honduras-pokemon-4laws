import pygame
import tmx
import random

# Los Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('sprites/player.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))
        self.orient = orientation
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.setSprite()

    def setSprite(self):
        # Resets the player sprite sheet to its default position 
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -128)
        elif self.orient == 'right':
            self.image.scroll(0, -192)

    def update(self, dt, game):
        key = pygame.key.get_pressed()
        # Setting orientation and sprite based on key input: 
        if key[pygame.K_UP]:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_DOWN]:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()    
                self.holdTime += dt
        elif key[pygame.K_LEFT]:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key[pygame.K_RIGHT]:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 100:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing 
        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 8
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.dx += 8
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'solid')) > 0:
            self.rect = lastRect
        # Drown Collision detection:
        # Reset to same place
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 'drown')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('drownreturn')[0]
            game.initArea(entryCell['drownreturn'])
            game.newinitPlayers(entryCell.px, entryCell.py)
            game.player.orient = 'right'
            self.orient = 'right'
            return

        # Area entry detection:
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'entry')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('entry')[0]
            game.fadeOut()
            game.initArea(entryCell['entry'])
            self.walking=False

            return
        # Switch to the walking sprite after 32 pixels 
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or 
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()    
            self.dx = 0

        for x in game.heartlist:
            if x.rect == self.rect:
                x.kill()
                game.heartlist.remove(x)
                game.numHearts -= 1

        game.tilemap.set_focus(self.rect.x+32, self.rect.y+32)

class Heart(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Heart, self).__init__(*groups)
        self.image = pygame.image.load('tiles/heart2.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))

class Satan(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        super(Satan, self).__init__(*groups)
        self.image = pygame.image.load('sprites/satan.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))
        self.orient = orientation
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.setSprite()

    def setSprite(self):
        # Resets the player sprite sheet to its default position 
        # and scrolls it to the necessary position for the current orientation
        self.image = self.imageDefault.copy()
        if self.orient == 'up':
            self.image.scroll(0, -64)
        elif self.orient == 'down':
            self.image.scroll(0, 0)
        elif self.orient == 'left':
            self.image.scroll(0, -128)
        elif self.orient == 'right':
            self.image.scroll(0, -192)

    def random_move(self, dt, game):
        key = random.randint(1,5)
        # Setting orientation and sprite based on key input: 
        if key == 1:
            if not self.walking:
                if self.orient != 'up':
                    self.orient = 'up'
                    self.setSprite()
                self.holdTime += dt
        elif key == 2:
            if not self.walking:
                if self.orient != 'down':
                    self.orient = 'down'
                    self.setSprite()    
                self.holdTime += dt
        elif key == 3:
            if not self.walking:
                if self.orient != 'left':
                    self.orient = 'left'
                    self.setSprite()
                self.holdTime += dt
        elif key == 4:
            if not self.walking:
                if self.orient != 'right':
                    self.orient = 'right'
                    self.setSprite()
                self.holdTime += dt
        else:
            self.holdTime = 0
            self.step = 'rightFoot'
        # Walking mode enabled if a button is held for 0.1 seconds
        if self.holdTime >= 0:
            self.walking = True
        lastRect = self.rect.copy()
        # Walking at 8 pixels per frame in the direction the player is facing 
        if self.walking and self.dx < 64:
            if self.orient == 'up':
                self.rect.y -= 8
            elif self.orient == 'down':
                self.rect.y += 8
            elif self.orient == 'left':
                self.rect.x -= 8
            elif self.orient == 'right':
                self.rect.x += 8
            self.dx += 8
        # Collision detection:
        # Reset to the previous rectangle if player collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect, 'solid')) > 0:
            self.rect = lastRect
        # Area entry detection:
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'entry')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('entry')[0]
            game.fadeOut()
            game.initArea(entryCell['entry'])

            return
        # Switch to the walking sprite after 32 pixels 
        if self.dx == 32:
            # Self.step keeps track of when to flip the sprite so that
            # the character appears to be taking steps with different feet.
            if (self.orient == 'up' or 
                self.orient == 'down') and self.step == 'leftFoot':
                self.image = pygame.transform.flip(self.image, True, False)
                self.step = 'rightFoot'
            else:
                self.image.scroll(-64, 0)
                self.step = 'leftFoot'
        # After traversing 64 pixels, the walking animation is done
        if self.dx == 64:
            self.walking = False
            self.setSprite()    
            self.dx = 0

    def update(self, dt, game):
        self.random_move(dt, game)

class SpriteLoop(pygame.sprite.Sprite):
    """A simple looped animated sprite.

    SpriteLoops require certain properties to be defined in the relevant
    tmx tile:

    src - the source of the image that contains the sprites
    width, height - the width and height of each section of the sprite that
        will be displayed on-screen during animation
    mspf - milliseconds per frame, or how many milliseconds must pass to 
        advance onto the next frame in the sprite's animation 
    frames - the number individual frames that compose the animation
    """
    def __init__(self, location, cell, *groups):
        super(SpriteLoop, self).__init__(*groups)
        self.image = pygame.image.load(cell['src'])
        self.defaultImage = self.image.copy()
        self.width = int(cell['width'])
        self.height = int(cell['height'])
        self.rect = pygame.Rect(location, (self.width,self.height))
        self.frames = int(cell['frames'])
        self.frameCount = 0
        self.mspf = int(cell['mspf']) # milliseconds per frame
        self.timeCount = 0

    def update(self, dt, game):
        self.timeCount += dt
        if self.timeCount > self.mspf:
            # Advance animation to the appropriate frame
            self.image = self.defaultImage.copy()
            self.image.scroll(-1*self.width*self.frameCount, 0)
            self.timeCount = 0

            self.frameCount += 1
            if self.frameCount == self.frames:
                self.frameCount = 0

class Game(object):
    def __init__(self, screen):
        self.screen = screen

    def fadeOut(self):
        """Animate the screen fading to black for entering a new area"""
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.screen.blit(blackRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        screen.fill((255,255,255,50))
        pygame.display.flip()

    def initArea(self, mapFile):
        """Load maps and initialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, screen.get_size())
        self.players = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.hearts = tmx.SpriteLayer()
        # Initializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)

    def newinitPlayers(self, playerlocationx, playerlocationy):
        self.player = Player((playerlocationx, playerlocationy),
                             'down', self.players)
        self.tilemap.layers.append(self.players)
        self.tilemap.set_focus(self.player.rect.x+32, self.player.rect.y+32)

    def mypred(self, row, col):
        if row == 5 or row == 6 or row == 7:
            if col == 6 or col == 7 or col == 8:
                print(f"mypred: TRUE Checking for row {row} and col is {col}")
                return True
            else:
                print(f"mypred: FALSE Checking for row {row} and col is {col}")
                return False
        else :
            print(f"mypred: FALSE Checking for row {row} and col is {col}")
            return False

    def randomPopulateHearts(self, numHearts):
        allPossibleHeartLocations = []
        for i in range(0,12):
            for j in range(0,15):
                allPossibleHeartLocations.append((i,j))

        for i in range(5,8):
            for j in range(6,9):
                allPossibleHeartLocations.remove((i,j))

        #printrandom
        for i in range(0,numHearts):
            index = random.randint(0,len(allPossibleHeartLocations)-1)
            hearttobelocated = allPossibleHeartLocations[index]
            self.heartlist.append(Heart((64*hearttobelocated[1] + 1440, 64*hearttobelocated[0] + 256), self.hearts))
            allPossibleHeartLocations.remove(hearttobelocated)

        #printall
        # for places in allPossibleHeartLocations:
        #     if(not self.mypred(places[0],places[1])):
        #         self.heartlist.append(Heart((64*places[1] + 1440, 64*places[0] + 256), self.hearts))
        #         print(f"heart printed for row {places[0]} and Y is {places[1]}")

    def initPlayers(self):
        # Initializing player sprites
        startCell = self.tilemap.layers['triggers'].find('playerStart')[0]
        self.player = Player((startCell.px, startCell.py),
                             startCell['playerStart'], self.players)
        satanStart = self.tilemap.layers['triggers'].find('satanStart')[0]
        self.satan = Satan((satanStart.px, satanStart.py), 
                             satanStart['satanStart'], self.players)

        self.numHearts = 20
        self.heartlist = []
        
        self.randomPopulateHearts(self.numHearts)

        # self.heartlist = []
        # # for x in range(0,self.numHearts):
        # ax = Heart((satanStart.px-256,satanStart.py-64), self.hearts)
        # ay = Heart((satanStart.px,satanStart.py+128), self.hearts)
        # az = Heart((satanStart.px-192,satanStart.py+192), self.hearts)
        # self.heartlist.append(ax)
        # self.heartlist.append(ay)
        # self.heartlist.append(az)

        self.tilemap.layers.append(self.hearts)
        self.tilemap.layers.append(self.players)

        self.tilemap.set_focus(self.player.rect.x+32, self.player.rect.y+32)

    def heartdelayremove(self):
        """Animate the screen fading to black for entering a new area"""
        clock = pygame.time.Clock()
        for i in range(0,len(self.heartlist)):
            dt = clock.tick(10)
            print("iteration")
            print(i)
            self.heartlist[i].kill()
            self.tilemap.update(dt, self)
            screen.fill(NEGRO)
            self.tilemap.draw(self.screen)
            pygame.display.update()

        clock.tick(20)
        pygame.display.flip()

    def main(self):
        clock = pygame.time.Clock()
        self.initArea('Firstlaw.tmx')
        self.initPlayers()
        self.game_over = False
        self.havemoveddown = False

        heartdelaytime = 0
        removing_heart = False

        while 1:
            dt = clock.tick(30)

            if removing_heart:
                print(f"heartcount is {self.numHearts} and heartdelaytime is {heartdelaytime} and ")
                heartdelaytime += 1
                if self.numHearts == 0:
                    removing_heart = False
                elif heartdelaytime > 5:
                    x = self.heartlist[0]
                    x.kill()
                    self.heartlist.remove(x)
                    self.numHearts -= 1
                    heartdelaytime = 0
                    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    print(f"X is {self.player.rect.x} and Y is {self.player.rect.y}")
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print("move to new map")
                    myx = self.player.rect.x
                    myy = self.player.rect.y
                    self.initArea('open_garden.tmx')
                    self.newinitPlayers(myx, myy)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    print("TTT")
                    removing_heart = True

            if (not self.game_over) and self.player.rect.colliderect(self.satan.rect):
                print("Satan Collision Detected")
                self.game_over = True;

            if not self.game_over:
                if not self.numHearts and not self.havemoveddown:
                    self.player.rect.y += 1408
                    self.satan.rect.y += 1408
                    self.havemoveddown = True

                self.tilemap.update(dt, self)
                screen.fill(NEGRO)
                self.tilemap.draw(self.screen)

                font = pygame.font.Font(None, 24)
                if self.numHearts == 0:
                    text = font.render(f"Hearts x {self.numHearts}, you can exit through the right", True, NEGRO)
                else:
                    text = font.render(f"Hearts x {self.numHearts}", True, NEGRO)

                text_rect = text.get_rect()
                text_x = text_rect.height*1.5
                text_y = screen.get_height() - text_rect.height * 1.5 
                screen.blit(text, [text_x, text_y])

            else :
                screen.fill(NEGRO)
                font = pygame.font.Font(None, 36)
                text = font.render("No puedes ganar sin Jesucristo", True, AZUL)
                text_rect = text.get_rect()
                text_x = screen.get_width() / 2 - text_rect.width / 2
                text_y = screen.get_height() / 2 - text_rect.height / 2
                screen.blit(text, [text_x, text_y])

            # cursurf = pygame.display.get_surface()
            # cursurf.set_clip(pygame.Rect(self.player.rect.x,self.player.rect.y, 640, 640))


            # pygame.display.update(cursurf.get_rect())
            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((570, 480))
    pygame.display.set_caption("Pyllet Town")
    Game(screen).main()
