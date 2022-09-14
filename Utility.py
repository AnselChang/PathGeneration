import pygame, math, pygame.gfxdraw

pygame.font.init()

SCREEN_SIZE = 800
PANEL_WIDTH = 300
PIXELS_TO_FIELD_CORNER = 19
FIELD_SIZE_IN_PIXELS = 766
FIELD_SIZE_IN_INCHES = 144

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
  
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

