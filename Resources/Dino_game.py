import pygame
import time
import random
from pygame.sprite import Sprite

def Buttonify(Picture, coords, surface):
    image = pygame.image.load(Picture)
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    return (image,imagerect)

class Obj(Sprite):
    objs = {}

    def __init__(self, name, x, y, path=None, ord_num=0):
        Sprite.__init__(self)
        self.name = name
        self.x = x
        self.y = y

        if path is not None:
            self.image = pygame.image.load('Textures/' + path)
            self.width, self.height = self.image.get_rect().size
        else:
            self.image = None
            self.width, self.height = 0, 0

        self.visible = True

        self.ord = ord_num

        Obj.objs[self.name] = self

    def __del__(self):

        del Obj.objs[self.name]
        self.kill()

    def collides(self, other):
        if sliding == True:
            return self.x <= other.x + other.width and self.y <= other.y + other.height/2 and\
               self.x + self.width >= other.x and self.y + self.height >= other.y
        else:
            return self.x <= other.x + other.width and self.y <= other.y + other.height and \
                   self.x + self.width >= other.x and self.y + self.height >= other.y
    def onCollision(self, other):
        pass

    def update(self):
        for other in Obj.objs.values():
            if self.collides(other):
                self.onCollision(other)

        if self.visible and self.image is not None:

            if self.name == 'dino' and sliding == True:
                gamepad.blit(pygame.transform.scale(self.image, (96,120//2)), (self.x, self.y+60))
            else:
                if 'rudolf' not in self.name and 'ground' not in self.name:

                    gamepad.blit(self.image, (self.x, self.y))


class Snow(Obj):
    def __init__(self,x,y,name):
        Obj.__init__(self, name, x, y, 'snow.png',4)

    def downSnow(self):
        self.y += random.randrange(1,7)
        if self.y > 400:
            self.y = -600

class Ground(Obj):
    def __init__(self, x, y, name):
        Obj.__init__(self, name, x, y, 'Whiteland.png',2)


    def moveGround(self, score):
        self.x -= 3 + score/1000
        if self.x < -1400:
            self.x = 1300
        gamepad.blit(self.image, (self.x, self.y))

class Obstacle(Obj):
    def __init__(self, x, y, name):
        Obj.__init__(self, name, x , y , 'Rudolf.png',3)

    def moving(self, score):
        self.x -= 8 + score/500
        if self.x < -1400:
            self.kill()
        gamepad.blit(self.image, (self.x, self.y))


class Dino(Obj):

    def __init__(self, x, y):
        Obj.__init__(self, 'dino', x, y, 'dino.png',1)
        self.gravity = 1000
        self.velocity = 0
        self.jump_power = 750

        self.isJump = False

    def jump(self):
        if self.isJump == False:
            self.velocity = -self.jump_power
            self.isJump = True

    def onCollision(self, other):
        if 'ground' == other.name:
            if sliding == False:
                self.y = 280
            else:
                self.y = 300
            self.velocity = 0
            self.isJump = False

        if 'rudolf' in other.name:
            global GameOver
            if GameOver == False:
                GameOver = True

    def update(self):
        self.velocity += self.gravity * delta_time
        self.y += self.velocity * delta_time
        Obj.update(self)


WHITE = (255, 255, 255)
pad_size = (1024, 512)

delta_time = 0

def runGame(grounds,snows,moon):
    global gamepad, clock
    global delta_time
    global end , sliding
    global GameOver

    crashed = False
    prev_time = time.time()
    check_time = time.time()
    snowCount = 0
    score = 0
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 102, 204)
    BLACK = (0, 0, 0)

    font =  pygame.font.SysFont("Font/notosanscjkkr",40)
    text = font.render('score: %06d' % score, True, BLACK, WHITE)
    textRectObj = text.get_rect()
    textRectObj.center = (750, 50)



    start_time = time.time()

    Obs = []

    retry = False
    while not crashed and end == False:

        if time.time() - start_time <2:
            GameOver = False

        if GameOver == False:

            delta_time = time.time() - prev_time
            prev_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        Obj.objs['dino'].jump()
                    if event.key == pygame.K_DOWN:
                        sliding = True
                    if event.key == pygame.K_r:
                        initGame()

                    if event.key == pygame.K_ESCAPE:
                        end = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        sliding = False


            gamepad.fill(BLUE)
            text = font.render('score: %06d' % score, True, BLACK, WHITE)

            gamepad.blit(text, textRectObj)
            gamepad.blit(pygame.transform.scale(moon, (900//6, 640//6)), (220, 20))


            for ground in grounds:
                ground.moveGround(score)

            for obj in Obj.objs.values():
                obj.update()

            for i in range(6):
                gamepad.blit(pygame.transform.scale(snows[:][snowCount % 20],(200,350)), (200*i, 0))

            for obs in Obs:
                obs.moving(score)

            snowCount += 1
            score += 1

            if time.time() -check_time > 3:
                check_time = time.time()
                y = random.randrange(0,4)

                Obs += [Obstacle(1200,280-y*80,'rudolf%d' % score)]
                print(Obs)
        else:
            moon1 = pygame.image.load('Textures/Btn.png')
            moon2 = pygame.image.load('Textures/Btn.png')
            gamepad.blit(moon1, (200, 200))
            gamepad.blit(moon2, (700, 200))

            font_result = pygame.font.SysFont("Font/notosanscjkkr", 60)
            text_result = font_result.render('Result: %06d' % int(score-1), True, BLACK, WHITE)

            gamepad.blit(text_result, (400,100))



            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse = pygame.mouse.get_pos()

                    if mouse[0] > 200 and mouse[0] < 400 and mouse[1] > 200 and mouse[1] < 333:
                        print(mouse)

                        GameOver = False
                        for i in range(len(Obs[:])):
                            Obs.pop(0)
                        Obj.objs.clear()
                        print(Obs)
                        initGame()

                    elif mouse[0] > 700 and mouse[0] < 900 and mouse[1] > 200 and mouse[1] < 333:
                        print(mouse)
                        GameOver = False

                        end = True

        pygame.display.update()
        clock.tick(60)



def initGame():
    global gamepad, clock, GameOver

    pygame.init()

    gamepad = pygame.display.set_mode(pad_size)
    pygame.display.set_caption('PyFlying')

    #bg = Obj('Bg', 0, 0, 'Background.jpg', 0)
    moon = pygame.image.load('Textures/Moon.png')
    #bg_group = pygame.sprite.RenderPlain(bg)
    #bg.__del__()

    Image = Buttonify('Textures/Moon.png', (300,100), gamepad)

    snows = []
    for i in range(20):
        snows.append(pygame.image.load('Textures/snow_%s.png' % str(i+1)))

    ground_1 = Ground(0, 275,'ground_1')
    ground_2 = Ground(917, 275,'ground_2')
    ground_3 = Ground(917*2, 275,'ground_3')

    #obs = Obstacle(400, 150, 'rudolf')

    grounds = [ground_1,ground_2,ground_3]
    #Obj.objs.pop(bg.name)
    ground = Obj('ground', 0, 400, 'Whiteland.png', 0)

    ground.visible = False

    dino = Dino(pad_size[0] * 0.02,-100)

    Obj.objs = dict(sorted(Obj.objs.items(), key=lambda x: x[1].ord))



    clock = pygame.time.Clock()
    GameOver = False
    runGame(grounds,snows,moon)

end = False
GameOver = False
sliding = False
while end == False:
    initGame()

pygame.quit()