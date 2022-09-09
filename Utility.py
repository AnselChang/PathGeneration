from email.mime import image
import pygame, math, pygame.gfxdraw

pygame.font.init()

SCREEN_SIZE = 800
PANEL_WIDTH = 300
PIXELS_TO_FIELD_CORNER = 19
FIELD_SIZE_IN_PIXELS = 766
FIELD_SIZE_IN_INCHES = 144

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

# Return an image given a filename
def getImage(filename: str, imageScale: float = 1) -> pygame.Surface:
    unscaledImage = pygame.image.load(filename).convert_alpha()
    if imageScale == 1:
        return unscaledImage
    else:
        dimensions = ( int(unscaledImage.get_width() * imageScale), int(unscaledImage.get_height() * imageScale) )
        return pygame.transform.smoothscale(unscaledImage, dimensions)

# Amount from 0 (nothing) to 1 (transparent)
def getLighterImage(image: pygame.Surface, lightenPercent: float) -> pygame.Surface:

    newImage = image.copy()
    newImage.set_alpha(lightenPercent * 255)

    return newImage

def scaleTuple(nums: tuple, scalar: float):
    return [i * scalar for i in nums]

def divideTuple(nums: tuple, scalar: float):
    return [i / scalar for i in nums]

def addTuples(tupleA: tuple, tupleB: tuple):
    assert len(tupleA) == len(tupleB)
    return [a+b for a,b in zip(tupleA, tupleB)]

def subtractTuples(tupleA: tuple, tupleB: tuple):
    assert len(tupleA) == len(tupleB)
    return [a-b for a,b in zip(tupleA, tupleB)]

def pixelsToInches(pixels):
    return (pixels / SCREEN_SIZE) * 144

def pixelsToTiles(pixels):
    return (pixels / SCREEN_SIZE) * 6

def clamp(value: float, minBound: float, maxBound: float) -> float:
    return max(minBound, min(maxBound, value))

def clamp2D(point: tuple, minX: float, minY: float, maxX: float, maxY: float) -> tuple:
    return clamp(point[0], minX, maxX), clamp(point[1], minY, maxY)

def hypo(s1, s2):
    return math.sqrt(s1*s1 + s2*s2)

def distanceTuple(vector: tuple):
    return hypo(*vector)

def distance(x1,y1,x2,y2):
    return hypo(y2-y1, x2-x1)

def distanceTuples(vector1: tuple, vector2: tuple):
    return distance(*vector1, *vector2)

# Distance between point (x0, y0) and line (x1, y1,),(x2,y2)
def distanceTwoPoints(x0, y0, x1, y1, x2, y2):
    return abs((x2-x1)*(y1-y0)- (x1-x0)*(y2-y1)) / distance(x1, y1, x2, y2)

def vector(x0, y0, theta, magnitude):
    return [x0 + magnitude*math.cos(theta), y0 + magnitude*math.sin(theta)]

def pointTouchingLine(mouseX: int, mouseY: int, x1: int, y1: int, x2: int, y2: int, lineHitboxThickness: int):

    if x1 == x2 and y1 == y2:
        return False
    
    if distanceTwoPoints(mouseX,mouseY, x1, y1, x2, y2) <=  lineHitboxThickness:
        dist = distance(x1, y1, x2, y2)
        if distance(mouseX, mouseY, x1, y1) < dist and distance(mouseX, mouseY, x2, y2) < dist:
            return True
    return False

# Vector projection algorithm
def pointOnLineClosestToPoint(pointX: int, pointY: int, firstX: int, firstY: int, secondX: int, secondY: int) -> tuple:
    ax = pointX - firstX
    ay = pointY - firstY
    bx = secondX - firstX
    by = secondY - firstY

    scalar = (ax * bx + ay * by) / (bx * bx + by * by)
    return [firstX + scalar * bx, firstY + scalar * by]

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

# align = 0 -> align left/top
# align = 0.5 -> align mid
# align = 1 -> align right/bottom
def drawText(surface: pygame.Surface, font: pygame.font, string: str, color: tuple, x: int, y: int, alignX: float = 0.5, alignY: float = 0.5):
    text = font.render(string, True, color)
    surface.blit(text, [x - text.get_width()*alignX, y - text.get_height()*alignY])

def drawThinLine(screen: pygame.Surface, color: tuple, x1: int, y1: int, x2: int, y2: int):
    pygame.draw.aaline(screen, color, (x1,y1), (x2,y2))

def drawCircle(screen: pygame.Surface, x: int, y: int, color: tuple, radius: int, alpha: int = 255):
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

def drawLine(screen: pygame.Surface, color: tuple, x1: int, y1: int, x2: int, y2: int, thickness: int = 1):

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
