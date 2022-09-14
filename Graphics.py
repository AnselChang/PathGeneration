import pygame, math, Utility, colors, colorsys


"""
A class that cycles through each hue gradually through next(), which returns a color
"""
class ColorCycle:
    def __init__(self, rate: float = 0.05, brightness: float = 0.5):
        self.rate = rate
        self.brightness: float = 0.5

        self.hue: float = 0

    def _hsv2rgb(self, h,s,v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

    # Return the next color
    def next(self) -> tuple:
        self.hue += self.rate
        return self._hsv2rgb(self.hue, self.brightness, self.brightness)



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

# Draw filled polygon given list of points
def drawPolygon(screen: pygame.Surface, color: tuple, points: list[tuple]):

    pygame.gfxdraw.filled_polygon(screen, points, color)
    pygame.gfxdraw.aapolygon(screen, points, color)


def drawLine(screen: pygame.Surface, color: tuple, x1: int, y1: int, x2: int, y2: int, thickness: int = 1):

    thickness = round(thickness)

    from math import cos, sin

    X0 = [x1,y1]
    X1 = [x2,y2]

    center_L1 = [(x1+x2) / 2, (y1+y2) / 2 ]
    length = Utility.distance(x1, y1, x2, y2)
    angle = math.atan2(X0[1] - X1[1], X0[0] - X1[0])
    
    UL = (center_L1[0] + (length/2.) * cos(angle) - (thickness/2.) * sin(angle), center_L1[1] + (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
    UR = (center_L1[0] - (length/2.) * cos(angle) - (thickness/2.) * sin(angle), center_L1[1] + (thickness/2.) * cos(angle) - (length/2.) * sin(angle))
    BL = (center_L1[0] + (length/2.) * cos(angle) + (thickness/2.) * sin(angle), center_L1[1] - (thickness/2.) * cos(angle) + (length/2.) * sin(angle))
    BR = (center_L1[0] - (length/2.) * cos(angle) + (thickness/2.) * sin(angle), center_L1[1] - (thickness/2.) * cos(angle) - (length/2.) * sin(angle))

    pygame.gfxdraw.aapolygon(screen, (UL, UR, BR, BL), color)
    pygame.gfxdraw.filled_polygon(screen, (UL, UR, BR, BL), color)

def drawVector(screen, x1, y1, x2, y2, zoom = 1):

    drawLine(screen, colors.VECTORCOLOR, x1, y1, x2, y2, 3 * zoom)
    theta = math.atan2(y2-y1, x2-x1)
    drawPolarTriangle(screen, colors.VECTORCOLOR, x2, y2, theta, 5 * zoom, 2, 1.6)



# Round the edges of the thick line
def drawRoundedLine(screen, color, x1, y1, x2, y2, thickness):
    drawLine(screen, color, x1, y1, x2, y2, thickness)
    drawCircle(screen, x1, y1, color, thickness/2)
    drawCircle(screen, x2, y2, color, thickness/2)
