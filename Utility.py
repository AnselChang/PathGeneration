import pygame, math, pygame.gfxdraw

GREEN = (50,205,50)
LINEGREY = (100, 100, 100)
LINEDARKGREY = (75, 75, 75)

def distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

def distanceTwoPoints(x0, y0, x1, y1, x2, y2):
    return abs((x2-x1)*(y1-y0)- (x1-x0)*(y2-y1)) / distance(x1, y1, x2, y2)

def pointTouchingLine(x, y, x1, y1, x2, y2, lineThickness):
    if distanceTwoPoints(x,y, x1, y1, x2, y2) <=  lineThickness:
        dist = distance(x1, y1, x2, y2)
        if distance(x, y, x1, y1) < dist and distance(x, y, x2, y2) < dist:
            return True
    return False

# Vector projection algorithm
def pointOnLineClosestToPoint(x, y, x1, y1, x2, y2):
    ax = x - x1
    ay = y - y1
    bx = x2 - x1
    by = y2 - y1

    scalar = (ax * bx + ay * by) / (bx * bx + by * by)
    return [x1 + scalar * bx, y1 + scalar * by]
    

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
