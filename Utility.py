import pygame, math, pygame.gfxdraw

pygame.font.init()

SCREEN_SIZE = 800
PANEL_WIDTH = 300

PANEL_GREY = (169, 169, 169)
BORDER_GREY = (64, 64, 64)
BLACK = (0,0,0)
ORANGE = (255, 165, 0)
BLUE = (0,0,230)
RED = (230,0,0)
PURPLE = (62, 12, 94)
GREEN = (50,205,50)
LINEGREY = (100, 100, 100)
LINEDARKGREY = (75, 75, 75)
TEXTCOLOR = (30, 30, 30)
VECTORCOLOR = (34, 185, 151)

def pixelsToInches(pixels):
    return (pixels / SCREEN_SIZE) * 144

def pixelsToTiles(pixels):
    return (pixels / SCREEN_SIZE) * 6

def clamp(value, mn, mx):
    return max(mn, min(mx, value))

def hypo(s1, s2):
    return math.sqrt(s1*s1 + s2 * s2)

def distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

# Distance between point (x0, y0) and line (x1, y1,),(x2,y2)
def distanceTwoPoints(x0, y0, x1, y1, x2, y2):
    return abs((x2-x1)*(y1-y0)- (x1-x0)*(y2-y1)) / distance(x1, y1, x2, y2)

def vector(x0, y0, theta, magnitude):
    return [x0 + magnitude*math.cos(theta), y0 + magnitude*math.sin(theta)]

def pointTouchingLine(x, y, x1, y1, x2, y2, lineThickness):

    if x1 == x2 and y1 == y2:
        return False
    
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

FONT20 = pygame.font.SysFont('Corbel', 20)
FONT30 = pygame.font.SysFont('Corbel', 30)
FONT40 = pygame.font.SysFont('Corbel', 40)

def getFont(size):
    if size < 25:
        return FONT20
    elif size < 35:
        return FONT30
    else:
        return FONT40

def drawText(surface, font, string, color, x, y, s = 0.5):
    text = font.render(string, True, color)
    surface.blit(text, [x - text.get_width()*s, y])

def drawThinLine(screen, color, x1, y1, x2, y2):
    pygame.draw.aaline(screen, color, (x1,y1), (x2,y2))

def drawCircle(screen, x, y, color, radius, alpha = 255):
    x = int(x)
    y = int(y)
    radius = int(radius)
    if alpha == 255:
        pygame.gfxdraw.aacircle(screen, x, y, radius, color)
        pygame.draw.circle(screen, color, (x,y), radius)
    else:
        surface = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
        pygame.gfxdraw.aacircle(surface, radius, radius, radius, (*color, alpha))
        pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
        screen.blit(surface, (x - radius, y - radius))

def drawTriangle(screen, color,  x1, y1, x2, y2, x3, y3):
    x1 = int(x1)
    x2 = int(x2)
    x3 = int(x3)
    y1 = int(y1)
    y2 = int(y2)
    y3 = int(y3)
    pygame.gfxdraw.aatrigon(screen, x1, y1, x2, y2, x3, y3, color)
    pygame.gfxdraw.filled_trigon(screen, x1, y1, x2, y2, x3, y3, color)

# Draws isoceles triangle given a center of rotation
# r1 is the radius from center of rotation to the closest two points
# r2 is the radius from center of rotation to the far point
def drawPolarTriangle(screen, color, x, y, theta, r1, r2Scalar, a):
    x1 = x + r1 * math.cos(theta - a)
    y1 = y + r1 * math.sin(theta - a)
    x2 = x + r1 * math.cos(theta + a)
    y2 = y + r1 * math.sin(theta + a)
    x3 = x + r2Scalar * r1 * math.cos(theta)
    y3 = y + r2Scalar * r1 * math.sin(theta)
    drawTriangle(screen, color, x1, y1, x2, y2, x3, y3)

def drawPolygon(screen, color, points, width = 1):
    width = round(width)
    pygame.gfxdraw.aapolygon(screen, points, color)
    if width > 1:
        pygame.draw.polygon(screen, color, points, width = width)

def drawLine(screen, color, x1, y1, x2, y2, thickness = 1):

    thickness = round(thickness)

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

def drawVector(screen, x1, y1, x2, y2, zoom = 1):

    drawLine(screen, VECTORCOLOR, x1, y1, x2, y2, 3 * zoom)
    theta = math.atan2(y2-y1, x2-x1)
    drawPolarTriangle(screen, VECTORCOLOR, x2, y2, theta, 5 * zoom, 2, 1.6)



# Round the edges of the thick line
def drawRoundedLine(screen, color, x1, y1, x2, y2, thickness):
    drawLine(screen, color, x1, y1, x2, y2, thickness)
    drawCircle(screen, x1, y1, color, thickness/2)
    drawCircle(screen, x2, y2, color, thickness/2)
