#imports section
import sys

import pygame
import time

#starts pygame
pygame.init()

#var creations
Scr_Wth = 1008
Scr_Hgt = 567
screen = pygame.display.set_mode((Scr_Wth, Scr_Hgt))
Player_img = pygame.image.load('pixil-sprite(1).png').convert()
LoadingTexture = pygame.image.load('Loading(dark mode1).png').convert_alpha()
pygame.display.set_caption('Python  Platformer')

#font stuff/glob
font = pygame.font.Font(('freesansbold.ttf'), 25)
text = font.render('hi',True,(0,0,0))
screen.fill((0,0,0))
screen.blit(text,(0,0))
pygame.draw.rect(screen, (127,127,127), pygame.Rect(250,255,20,60))
screen.blit(LoadingTexture,(250,252))
pygame.display.flip()
import glob
print(glob.glob('/platformer/venv/Levels/*.txt'))
i = 2
for i in range(0,35):
    size = (510//(1/(i/35.0+0.001)))
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (127, 127, 127), pygame.Rect(250, 255, size, 60))
    screen.blit(LoadingTexture,(250,252))
    pygame.display.flip()
    i += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    time.sleep(0.1)
time.sleep(0.5)
screen.fill((0, 0, 0))
pygame.draw.rect(screen, (127, 127, 127), pygame.Rect(250, 255, 510, 60))
screen.blit(LoadingTexture,(250,252))
pygame.display.flip()
time.sleep(0.5)


Run = True
x = 0
y = 0
xv = 0
yv = 0
g = 1
avg = [0,0,0,0]
frames = 0
xchange = 0
up = False
right = False
left = False
up_allowed = True
left_allowed = True
right_allowed = True
jump_ticks = 0
jumps_left = 0
clock = pygame.time.Clock()

#important
def _count_generator(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024 * 1024)
with open(r'Levels/Level1.txt', 'rb') as fp:
    c_generator = _count_generator(fp.raw.read)
    length = sum(buffer.count(b'\n') for buffer in c_generator) + 1
fp.close()


#classes
class Player(pygame.sprite.Sprite):

    #globals
    global x
    global y
    global xv
    global yv
    global up
    global right
    global left

    def __init__(self,x,y):
        self.rect = pygame.Rect(0,0,32,32)
        self.image = Player_img
        self.rect = self.image.get_rect()
    def update(self):

        #globals
        global x
        global y
        global xv
        global yv
        global up
        global right
        global left
        global right_allowed
        global up_allowed
        global left_allowed
        global g
        global layer

        #movement
        g = 1

        if up and up_allowed:
            g = -2
        if right and right_allowed:
            xv += 1
        if left and left_allowed:
            xv -= 1


        #do collision
        up_allowed = True
        left_allowed = True
        right_allowed = True
        for i in range(0, length):
            layer = str(level[i:i + 1])
            Physics()
            if Chk_Collide(0):
                font = pygame.font.Font(('freesansbold.ttf'), 75)
                text = font.render('HEY!!!! STOP THAT!!!!!!!',True,(255,255,255))
                screen.blit(text, (75,200))
                font = pygame.font.Font(('freesansbold.ttf'), 25)
                text = font.render('No Wall Glitches Please',True,(255,255,255))
                screen.blit(text, (75,300))

        # add grav and velocity to position
        x += xv
        y += yv
        yv += g

        for i in range(0, length):
            layer = str(level[i:i + 1])
            Physics(1)
            print('test' + layer)
        print('test777')

        # check if touching edges
        if x > 974:
            x = 974
        if x < 0:
            x = 0
        if y > 533:
            y = 533
        if y < 0:
            y = 0

        #friction
        xv = xv * 0.9
        yv = yv * 0.9
        xv = round(xv, 5)
        yv = round(yv, 5)

        #update screen position
        screen.blit(Player_img, (x,y))


#level loading and player binding
levelfile = open('Levels/Level1.txt', 'r')
level = levelfile.readlines()
levelfile.close()
P = Player(x,y)


#Check for collisions
def Chk_Collide (dir=0,add=False):
    global layer, xchange, x, xv, y, yv
    if dir == 0:
        if add:
            return (
                bool(x + xv < (int(layer[14:18]) + int(layer[24:28]) - 1) and x + xv > int(layer[14:18]) - 32) and \
                bool(y + yv < (int(layer[19:23]) + int(layer[29:33]) - 1) and y + yv > int(layer[19:23]) - 32)
            )
        else:
            return (
                bool(x < (int(layer[14:18]) + int(layer[24:28]) - 1) and x > int(layer[14:18]) - 32) and \
                bool(y < (int(layer[19:23]) + int(layer[29:33]) - 1) and y > int(layer[19:23]) - 32)
            )
    elif dir == 1:
        if add:
            return (
                bool(x + xv < (int(layer[14:18]) + int(layer[24:28]) - 1) and x + xv > int(layer[14:18]) - 32)
            )
        else:
            return (
                bool(x < (int(layer[14:18]) + int(layer[24:28]) - 1) and x > int(layer[14:18]) - 32)
            )
    elif dir == 2:
        if add:
            return (
                bool(y + yv < (int(layer[19:23]) + int(layer[29:33]) - 1) and y + yv > int(layer[19:23]) - 32)
            )
        else:
            return (
                bool(y < (int(layer[19:23]) + int(layer[29:33]) - 1) and y > int(layer[19:23]) - 32)
            )
    elif dir == 3:
        return (
            bool(y + g < (int(layer[19:23]) + int(layer[29:33]) - 1) and y + g > int(layer[19:23]) - 32)
        )
    else:
        print  ('Error: Unknown Value')
        return ('Error: Unknown Value')


def Physics(Type=0):
    global g,x,y
    if Type == 0:
        if Chk_Collide(2,True) == True and Chk_Collide(1) == True:
            global yv
            yv = 0
        if Chk_Collide(1,True) == True and Chk_Collide(2) == True:
            global xv
#            global left_allowed
 #           global right_allowed
  #          if xv > 0:
   #             right_allowed = False
    #            left_allowed = True
     #       elif xv > 0:
      #          left_allowed = False
       #         right_allowed = True
            xv = 0
        if Chk_Collide(0,True):
            xv,yv = 0,0
    if Type == 1:
        if not Chk_Collide(3):
            y -= g


#while loop

slow = False

while Run:

    #draw level
    for i in range(0, length):
        global layer
        layer = str(level[i:i + 1])
        pygame.draw.rect(screen, (int(layer[2:5]), (int(layer[6:9])), (int(layer[10:13]))),
                         [(int(layer[14:18])), (int(layer[19:23])), (int(layer[24:28])), (int(layer[29:33]))], (int(layer[34])))
        if (int(layer[34])) > 0:
            pygame.draw.rect(screen, ((0), (0), (0)),
                             [(int(layer[14:18])+1), (int(layer[19:23])+1), (int(layer[24:28])-2), (int(layer[29:33])-2)], (int(0)))
        i =+ 1

    #get events
    for event in pygame.event.get():
        #check if window is closed
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
            Run = False

        #movement stuff
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if jumps_left < 3 and jump_ticks == 0:
                    jump_ticks = 1
                    up = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_SPACE:
                slow = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                up = False
                #jump_ticks = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_SPACE:
                slow = False

    if slow:
        clock.tick(30)
    #updates
    if Run:
        #jump update
        if jump_ticks:
            if jump_ticks - 15:
                jump_ticks += 1
                up = True
            else:
                jump_ticks = 0
                up = False
    #player/physics update
    P.update()
    text = font.render(str(frames),True, (255,255,255))
    screen.blit(text,(0,0))
    #screen updates
    pygame.display.flip()
    screen.fill((0, 0, 0))
    frames += 1
