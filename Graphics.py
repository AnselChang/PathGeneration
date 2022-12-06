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


FONT_PATH = 'Corbel.ttf'
FONT20 = pygame.font.Font(FONT_PATH, 20)
FONT25 = pygame.font.Font(FONT_PATH, 25)
FONT30 = pygame.font.Font(FONT_PATH, 30)
FONT40 = pygame.font.Font(FONT_PATH, 40)

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

def drawSurface(surface: pygame.Surface, drawnSurface: pygame.Surface, cx: int, cy: int, angle: float):
    drawnSurface = pygame.transform.rotate(drawnSurface, angle)
    r = drawnSurface.get_rect()
    rect = drawnSurface.get_rect(center = (cx + r.width/2, cy + r.height/2))
    surface.blit(drawnSurface, (rect.x, rect.y))

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

def drawVector(screen: pygame.Surface, x1: int, y1: int, magnitude: float, heading: float):

    x2 = int(x1 + magnitude * math.cos(heading))
    y2 = int(y1 + magnitude * math.sin(heading))

    drawLine(screen, colors.VECTORCOLOR, x1, y1, x2, y2, 3)
    drawPolarTriangle(screen, colors.VECTORCOLOR, x2, y2, heading, 5, 2, 1.6)



# Round the edges of the thick line
def drawRoundedLine(screen, color, x1, y1, x2, y2, thickness):
    drawLine(screen, color, x1, y1, x2, y2, thickness)
    drawCircle(screen, x1, y1, color, thickness/2)
    drawCircle(screen, x2, y2, color, thickness/2)


# Draw anti-aliased filled rounded rectangle
def drawRoundedRectangle(surface: pygame.Surface, rect: list[int], color: tuple, rad: int =20, border=0, inside=(0,0,0)):
    """
    Draw an antialiased rounded rect on the target surface.  Alpha is not
    supported in this implementation but other than that usage is identical to
    round_rect.
    """
    rect: pygame.Rect = pygame.Rect(rect)
    _aa_render_region(surface, rect, color, rad)
    if border:
        rect.inflate_ip(-2*border, -2*border)
        _aa_render_region(surface, rect, inside, rad)

# helper function for drawRoundedRectangle()
def _aa_render_region(image, rect: pygame.Rect, color, rad):
    corners = rect.inflate(-2*rad-1, -2*rad-1)
    for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
        x, y = getattr(corners, attribute)
        pygame.gfxdraw.aacircle(image, x, y, rad, color)
        pygame.gfxdraw.filled_circle(image, x, y, rad, color)
    image.fill(color, rect.inflate(-2*rad,0))
    image.fill(color, rect.inflate(0,-2*rad))