import pygame
import tmx
import random

# Los Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Jugador_Color = AZUL

class Jugador(pygame.sprite.Sprite):
    def __init__(self, location, orientation, *groups):
        super(Jugador, self).__init__(*groups)
        Jugador_Color = AZUL
        if(Jugador_Color == AZUL):
            self.image = pygame.image.load('sprites/jugador_azul.png')
        elif(Jugador_Color == ROJO):
            self.image = pygame.image.load('sprites/jugador_rojo.png')
        elif(Jugador_Color == VERDE):
            self.image = pygame.image.load('sprites/jugador_verde.png')
        else:
            self.image = pygame.image.load('sprites/jugador.png')

        # self.image = pygame.image.load('sprites/Jugador.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))
        self.orient = orientation
        self.location = location
        self.holdTime = 0
        self.walking = False
        self.dx = 0
        self.step = 'rightFoot'
        # Set default orientation
        self.setSprite()

    def setSprite(self):
        # Resets the Jugador sprite sheet to its default position 
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
        # Walking at 8 pixels per frame in the direction the Jugador is facing 
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
        # Reset to the previous rectangle if Jugador collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'solid')) > 0:
            self.rect = lastRect
        # Drown Collision detection:
        # Reset to same place
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 'drown')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('drownreturn')[0]
            game.inicioArea(entryCell['drownreturn'])
            game.newinicioJugadors(entryCell.px, entryCell.py)
            game.Jugador.orient = 'right'
            self.orient = 'right'
            return

        # Area entry detection:
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'entry')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('entry')[0]
            game.fadeOut()
            game.inicioArea(entryCell['entry'])
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

        for x in game.listaDeCorazones:
            if x.rect == self.rect:
                x.kill()
                game.listaDeCorazones.remove(x)
                game.numeroCorazones -= 1

        if not game.comi_fruto:
            if game.fruto.rect == self.rect:
                game.fruto.kill()
                del game.fruto
                game.comi_fruto = True

        # if not game.jesus.rect == self.rect



        game.tilemap.set_focus(self.rect.x+32, self.rect.y+32)


#class Agua(pygame.sprite.Sprite):
#    def __init__(self, location, orientation, *groups):
#        super(Agua, self).__init__(*groups)
#        self.image = pygame.image.load('tiles/water.png')
#        self.imageDefault = self.image.copy()
#        self.rect = pygame.Rect(location, (32,32))
#        print(location)
        # self.setSprite()
#        self.dtcount=0

    # def update(self, dt, game):
    #     pass
        # self.dtcount += 1
        # if(dtcount % 30 == 0):
        #     self.image.scroll(64,0)

class Agua(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Agua, self).__init__(*groups)
        self.image = pygame.image.load('tiles/water.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (32,32))
        self.dtcount = -5
        self.dtnum = 1
        self.totalscrollsum = 0
        self.dtleft = True

    def update(self, dt, game):
        print(dt)
        self.dtcount +=1
        if self.dtcount == 6:
            self.dtcount = 0
            if self.dtnum == 8:
                self.image = self.imageDefault.copy()
                self.dtnum = 1

            self.image.scroll(-32,0)
            self.dtnum += 1



    # def update(self,dt,game):
    #     self.dtcount +=1
    #     if self.dtcount % 10 == 0:
    #         print(f"scrolling value {self.dtnum} for dtnum val = {self.dtnum}")
    #         self.image.scroll(-32, ,d0)
    #         self.totalscrollsum += -32*self.dtnum

    #         self.dtnum += 1
    #         if(self.dtnum == 4):
    #             self.dtnum = 0
    #             self.image.scroll(32 * 5)
    #             self.totalscrollsum += 160
    #         print(f"off by {self.totalscrollsum} from 0")

    # def update(self, dt, game):
    #     self.dtcount += 1
    #     if (self.dtcount % 5 == 0):
    #         print("hellow")
    #         self.dtnum += 1
    #         self.image.scroll(-32,0)
    #         self.totalscrollsum -= 32
    #         print(f"inner {self.totalscrollsum}")
    #         if self.totalscrollsum == -32*7:
    #             self.image.scroll(224, 0)
    #             self.totalscrollsum += 224
    #             print(f"outer {self.totalscrollsum}")

class Corazon(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Corazon, self).__init__(*groups)
        self.image = pygame.image.load('tiles/heart2.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))

class Fruto(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Fruto, self).__init__(*groups)
        self.image = pygame.image.load('tiles/fruto.png')
        self.imageDefault = self.image.copy()
        self.rect = pygame.Rect(location, (64,64))

class Jesus(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Jesus, self).__init__(*groups)
        self.image = pygame.image.load('tiles/jesus.png')
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
        # Resets the Jugador sprite sheet to its default position 
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

    def mover_al_azar(self, dt, game):
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
        # Walking at 8 pixels per frame in the direction the Jugador is facing 
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
        # Reset to the previous rectangle if Jugador collides
        # with anything in the foreground layer
        if len(game.tilemap.layers['triggers'].collide(self.rect, 'solid')) > 0:
            self.rect = lastRect
        # Area entry detection:
        elif len(game.tilemap.layers['triggers'].collide(self.rect, 
                                                        'entry')) > 0:
            entryCell = game.tilemap.layers['triggers'].find('entry')[0]
            game.fadeOut()
            game.inicioArea(entryCell['entry'])

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
        self.mover_al_azar(dt, game)

class SpriteLoop(pygame.sprite.Sprite):
    """A simple looped animated sprite.

    SpriteLoops require certain properties to be defined in the relevant
    tmx tile:

    src - the source of the image that contains the sprites
    width, height - the width and height of each section of the sprite that
        will be displayed on-pantalla during animation
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

class Juego(object):
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def fadeOut(self):
        """Animate the pantalla fading to black for entering a new area"""
        clock = pygame.time.Clock()
        blackRect = pygame.Surface(self.pantalla.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0,0,0))
        # Continuously draw a transparent black rectangle over the pantalla
        # to create a fadeout effect
        for i in range(0,5):
            clock.tick(15)
            self.pantalla.blit(blackRect, (0,0))  
            pygame.display.flip()
        clock.tick(15)
        pantalla.fill((255,255,255,50))
        pygame.display.flip()

    def inicioArea(self, mapFile):
        """Load maps and inicioialize sprite layers for each new area"""
        self.tilemap = tmx.load(mapFile, pantalla.get_size())
        self.map_ahora = mapFile
        self.Jugadors = tmx.SpriteLayer()
        self.objects = tmx.SpriteLayer()
        self.corazones = tmx.SpriteLayer()
        self.frutos = tmx.SpriteLayer()
        self.JesusLayer = tmx.SpriteLayer()
        self.aguas = tmx.SpriteLayer()
        # inicioializing other animated sprites
        try:
            for cell in self.tilemap.layers['sprites'].find('src'):
                SpriteLoop((cell.px,cell.py), cell, self.objects)
        # In case there is no sprite layer for the current map
        except KeyError:
            pass
        else:
            self.tilemap.layers.append(self.objects)

    def newinicioJugadors(self, Jugadorlocationx, Jugadorlocationy):
        
        if self.map_ahora == "agua_map.tmx":
            self.Jugador = Jugador((8*32,20*32), 'right', self.Jugadors)
            self.jesus = Jesus((12*32, 20*32), self.JesusLayer)
            self.agua = Agua((17*32, 20*32), self.aguas)
            self.agua2 = Agua((18*32, 20*32), self.aguas)
            self.agua3 = Agua((19*32, 20*32), self.aguas)
            self.agua4 = Agua((20*32, 20*32), self.aguas)
            self.tilemap.layers.append(self.JesusLayer)
            self.tilemap.layers.append(self.aguas)
        else :
            self.Jugador = Jugador((Jugadorlocationx, Jugadorlocationy), 'down', self.Jugadors)    
            self.fruto = Fruto((40*32,20*32), self.frutos)

            self.tilemap.layers.append(self.frutos)

        self.tilemap.layers.append(self.Jugadors)

        self.tilemap.set_focus(self.Jugador.rect.x+32, self.Jugador.rect.y+32)        


    def randomPopulateCorazones(self, numeroCorazones):
        TodoCorazon = []
        for i in range(0,12):
            for j in range(0,15):
                TodoCorazon.append((i,j))

        for i in range(5,8):
            for j in range(6,9):
                TodoCorazon.remove((i,j))

        #printrandom
        for i in range(0,numeroCorazones):
            index = random.randint(0,len(TodoCorazon)-1)
            hearttobelocated = TodoCorazon[index]
            self.listaDeCorazones.append(Corazon((64*hearttobelocated[1] + 256, 64*hearttobelocated[0] + 256), self.corazones))
            TodoCorazon.remove(hearttobelocated)


    def inicioJugadors(self):
        # inicioializing Jugador sprites
        startCell = self.tilemap.layers['triggers'].find('JugadorStart')[0]
        self.Jugador = Jugador((startCell.px, startCell.py),
                             startCell['JugadorStart'], self.Jugadors)
        satanStart = self.tilemap.layers['triggers'].find('satanStart')[0]
        self.satan = Satan((satanStart.px, satanStart.py), 
                             satanStart['satanStart'], self.Jugadors)

        self.numeroCorazones = 1
        self.listaDeCorazones = []

        # self.listaDeCorazones.append(Corazon((satanStart.px, satanStart.py), self.corazones))

        self.randomPopulateCorazones(self.numeroCorazones)

        self.fruto = Fruto((1280,640), self.frutos)

        # self.listaDeCorazones = []
        # # for x in range(0,self.numeroCorazones):
        # ax = Corazon((satanStart.px-256,satanStart.py-64), self.corazones)
        # ay = Corazon((satanStart.px,satanStart.py+128), self.corazones)
        # az = Corazon((satanStart.px-192,satanStart.py+192), self.corazones)
        # self.listaDeCorazones.append(ax)
        # self.listaDeCorazones.append(ay)
        # self.listaDeCorazones.append(az)

        self.tilemap.layers.append(self.corazones)
        self.tilemap.layers.append(self.Jugadors)
        self.tilemap.layers.append(self.frutos)

        self.tilemap.set_focus(self.Jugador.rect.x+32, self.Jugador.rect.y+32)

    def heartdelayremove(self):
        """Animate the pantalla fading to black for entering a new area"""
        clock = pygame.time.Clock()
        for i in range(0,len(self.listaDeCorazones)):
            dt = clock.tick(10)
            self.listaDeCorazones[i].kill()
            self.tilemap.update(dt, self)
            pantalla.fill(NEGRO)
            self.tilemap.draw(self.pantalla)
            pygame.display.update()

        clock.tick(20)
        pygame.display.flip()

    def removeHearts(self, heartdelaytime):
        print(f"heartcount is {self.numeroCorazones} and heartdelaytime is {heartdelaytime} and ")
        
        if self.numeroCorazones == 0:
            return False
        elif heartdelaytime > 5:
            x = self.listaDeCorazones[0]
            x.kill()
            self.listaDeCorazones.remove(x)
            self.numeroCorazones -= 1
        
        return True

    def drawScoreBoard(self):
        font = pygame.font.Font(None, 24)

        if self.numeroCorazones == 0:
            text = font.render(f"Corazones x {self.numeroCorazones}, puedes salir a la derecho", True, NEGRO)
        else:
            text = font.render(f"Corazones x {self.numeroCorazones}", True, NEGRO)

        text_rect = text.get_rect()
        text_x = text_rect.height*1.5
        text_y = pantalla.get_height() - text_rect.height * 1.5 
        pantalla.blit(text, [text_x, text_y])

    def drawSplashScreen(self, message):
        pantalla.fill(NEGRO)
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, AZUL)
        text_rect = text.get_rect()
        text_x = pantalla.get_width() / 2 - text_rect.width / 2
        text_y = pantalla.get_height() / 2 - text_rect.height / 2
        pantalla.blit(text, [text_x, text_y])

    def main(self):
        clock = pygame.time.Clock()
        self.inicioArea('closed_garden.tmx')
        self.inicioJugadors()
        self.juego_complete = False
        self.juego_terminado = False
        self.puerta_abierta = False
        self.comi_fruto = False
        self.en_agua_map = False

        heartdelaytime = 0
        removing_heart = False

        while 1:
            dt = clock.tick(30)

            if removing_heart:
                heartdelaytime += 1
                removing_heart = self.removeHearts(heartdelaytime)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    print(self.Jugador.location)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                    removing_heart = True

            if self.juego_terminado:
                self.drawSplashScreen("No puedes ganar sin Jesucristo")
            elif self.juego_complete:
                self.drawSplashScreen("Well Done")
            else :  
                if not self.numeroCorazones and not self.puerta_abierta:
                    myx = self.Jugador.rect.x
                    myy = self.Jugador.rect.y
                    self.inicioArea('open_garden.tmx')
                    self.newinicioJugadors(myx, myy)
                    self.puerta_abierta = True
                    del self.satan

                if (self.map_ahora == 'closed_garden.tmx' and self.Jugador.rect.colliderect(self.satan.rect)):
                    print("Satan Collision Detected")
                    self.juego_complete = True;

                if not self.en_agua_map and self.comi_fruto:
                    myx = self.Jugador.rect.x
                    myy = self.Jugador.rect.y
                    self.inicioArea('agua_map.tmx')
                    self.newinicioJugadors(myx, myy)
                    self.en_agua_map = True

                self.tilemap.update(dt, self)
                pantalla.fill(NEGRO)
                self.tilemap.draw(self.pantalla)

                self.drawScoreBoard()

            # cursurf = pygame.display.get_surface()
            # cursurf.set_clip(pygame.Rect(self.Jugador.rect.x,self.Jugador.rect.y, 640, 640))

            # pygame.display.update(cursurf.get_rect())
            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode((570, 480))
    pygame.display.set_caption("Pyllet Town")
    Juego(pantalla).main()
