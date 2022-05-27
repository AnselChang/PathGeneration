import pygame, math, pygame.gfxdraw

GREEN = (50,205,50)
LINEGREY = (100, 100, 100)

def distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

def drawCircle(screen, x, y, color, radius, alpha = 255):
    if alpha == 255:
        pygame.draw.circle(screen, color, (x,y), radius)
    else:
        surface = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
        screen.blit(surface, (x - radius, y - radius))

def drawLine(screen, color, x1, y1, x2, y2, thickness):

    from math import cos, sin

    X0 = [x1,y1]
    X1 = [x2,y2]

    center_L1 = [(x1+x2) / 2, (y1+y2) / 2 ]
    length = distance(x1, y1, x2, y2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    
    UL = (center_L1[0] + (length/2.) * cos(angle) - (thickness/2.) * sin(angle), center_L1[1] + (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
    UR = (center_L1[0] - (length/2.) * cos(angle) - (thickness/2.) * sin(angle), center_L1[1] + (thickness/2.) * cos(angle) - (length/2.) * sin(angle))
    BL = (center_L1[0] + (length/2.) * cos(angle) + (thickness/2.) * sin(angle), center_L1[1] - (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
    BR = (center_L1[0] - (length/2.) * cos(angle) + (thickness/2.) * sin(angle), center_L1[1] - (thickness/2.) * cos(angle) - (length/2.) * sin(angle))

    pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)
