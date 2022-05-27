import pygame, math
pygame.init()

SCREEN_SIZE = 600
SCREEN_DIMS = (SCREEN_SIZE, SCREEN_SIZE)

screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

def distance(x1,y1,x2,y2):
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )

def hypo(s1, s2):
    return math.sqrt(s1*s1 + s2 * s2)


# Return position at t, 0 < t < 1
def getSplinePoint(t, p1, p2, p3, p4):
    tt = t * t
    ttt = tt * t

    q1 = -ttt+ 2 * tt - t
    q2 =  3 * ttt - 5* tt + 2
    q3 = -3 * ttt + 4 * tt + t
    q4 = ttt - tt

    tx = 0.5 * (p1[0] * q1 + p2[0] * q2 + p3[0] * q3 + p4[0] * q4)
    ty = 0.5 * (p1[1] * q1 + p2[1] * q2 + p3[1] * q3 + p4[1] * q4)

    return [tx, ty]

# Return position at t, 0 < t < 1
def getSplineGradient(t, p1, p2, p3, p4):
    tt = t * t
    ttt = tt * t

    q1 = -3 * tt + 4 * t - 1
    q2 =  9 * tt - 10 * t
    q3 = -9 * tt + 8 * t + 1
    q4 = 3 * tt - 2 * t

    tx = 0.5 * (p1[0] * q1 + p2[0] * q2 + p3[0] * q3 + p4[0] * q4)
    ty = 0.5 * (p1[1] * q1 + p2[1] * q2 + p3[1] * q3 + p4[1] * q4)

    return [tx, ty]

points = [[200,300], [200,500], [400,400], [500,100]]
P1, P2, P3, P4  = points

screen.fill([255,255,255])

SPEED = 10
s = 0
while s < 1:
    x,y = getSplinePoint(s, P1, P2, P3, P4)
    pygame.draw.circle(screen, [0,0,0], [x,y], 1)

    dxds,dyds = getSplineGradient(s, P1, P2, P3, P4)
    dsdt = SPEED / hypo(dxds, dyds)
    s += dsdt

x2,y2 = getSplinePoint(1, P1, P2, P3, P4)
print(SPEED - distance(x,y,x2,y2))

for p in points:
    pygame.draw.circle(screen, [255,0,0], p, 4)

while True:
    pygame.display.update()
    pygame.time.wait(20)
    e = pygame.event.get()
    
