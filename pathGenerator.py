import sys, pygame
import MouseHandler, PathStructures, Utility

screen = pygame.display.set_mode(Utility.SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

rawFieldSurface = pygame.image.load("Images/squarefield.png")
IMAGE_SIZE = 812
fieldSurface = pygame.transform.smoothscale(rawFieldSurface, Utility.SCREEN_DIMS)

path = PathStructures.Path(5)
m = MouseHandler.Mouse(pygame.mouse, pygame.key)

while True:

    m.tick()

    zx,zy =m.zx, m.zy
    z = m.zoom
    if m.getKey(pygame.K_a):
        m.zoom = min(3, m.zoom + 0.15) # zoom in
    elif m.getKey(pygame.K_s):
        m.zoom = max(1, m.zoom - 0.15) # zoom out
        
    # Rescale the field surface ONLY when there is a zoom update
    if z != m.zoom:
        x,y = m.inchToPixel(zx, zy)
        m.panX += m.x - x
        m.panY += m.y - y
        m.boundFieldPan()
        # slightly inefficient but oh well
        fieldSurface = pygame.transform.smoothscale(rawFieldSurface, [Utility.SCREEN_SIZE * m.zoom, Utility.SCREEN_SIZE * m.zoom])

    # draw field
    screen.blit(fieldSurface, (m.panX,m.panY))
    
    anyPoseHovered = path.handleMouse(m)    

    if m.poseDragged is not None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif anyPoseHovered:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


    # Draw everything
    path.drawPaths(screen, m)
    path.drawPoints(screen, m)
    
    p = m.poseSelectHeading # Draw guide line for heading
    if p is not None and p.theta is not None: 
        Utility.drawThinLine(screen, Utility.PURPLE, *m.inchToPixel(p.x, p.y), m.x, m.y)

    if not anyPoseHovered: # Draw hovering pose if nothing selected
        Utility.drawCircle(screen, *m.inchToPixel(*path.getMousePosePosition(m.zx,m.zy)), Utility.GREEN, PathStructures.Pose.RADIUS * m.getPartialZoom(1.25), 100)
    
    pygame.display.update()

    pygame.time.wait(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


