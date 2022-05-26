import pygame, sys, math
from pygame.locals import *
from enum import Enum
import MouseHandler

BLACK = (0,0,0)
GREEN = (50,205,50)

SCREEN_SIZE = 600
SCREEN_DIMS = (SCREEN_SIZE, SCREEN_SIZE)

screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

fieldSurface = pygame.transform.smoothscale(pygame.image.load("Images/squarefield.png"), SCREEN_DIMS)

def distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

def drawCircle(screen, x, y, color, radius, alpha = 255):
    if alpha == 255:
        pygame.draw.circle(screen, color, (x,y), radius)
    else:
        surface = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
        screen.blit(surface, (x - radius, y - radius))



path = Path()
m = MouseHandler.Mouse(pygame.mouse)

while True:

    m.tick()
    anyPosePressed = path.handleMouse(m)
    if not anyPosePressed and m.pressed:
        path.addPose(m.x, m.y, 0)

    screen.blit(fieldSurface, (0,0))
    drawCircle(screen, m.x, m.y, GREEN, Pose.RADIUS, 100)
    path.draw(screen)


    
    pygame.display.update()

    pygame.time.wait(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


