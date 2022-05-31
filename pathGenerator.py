import sys, pygame
import MouseHandler, PathStructures, Utility, Slider

screen = pygame.display.set_mode(Utility.SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

rawFieldSurface = pygame.image.load("Images/squarefield.png")
IMAGE_SIZE = 812
fieldSurface = pygame.transform.smoothscale(rawFieldSurface, Utility.SCREEN_DIMS)

path = PathStructures.Path(1)
m = MouseHandler.Mouse(pygame.mouse, pygame.key)

Slider.init(m)
slider = Slider.Slider()

clock = pygame.time.Clock()

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

    slider.handleMouse()
    anyPoseHovered = path.handleMouse(m, slider)    
        
    if m.simulating:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if slider.mouseHovering() else pygame.SYSTEM_CURSOR_WAIT)
    elif m.poseDragged is not None or m.scrolling:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif anyPoseHovered:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    # Draw everything
    screen.blit(fieldSurface, (m.panX,m.panY)) # draw field
    if not m.simulating:
        path.drawPaths(screen, m)
    path.drawPoints(screen, m)
    path.drawRobot(screen, m, slider.pointIndex)
    
    p = m.poseSelectHeading # Draw guide line for heading
    if p is not None and p.theta is not None: 
        Utility.drawThinLine(screen, Utility.PURPLE, *m.inchToPixel(p.x, p.y), m.x, m.y)

    if not anyPoseHovered and not m.scrolling and not m.simulating: # Draw hovering pose if nothing selected and not scrolling field
        Utility.drawCircle(screen, *m.inchToPixel(*path.getMousePosePosition(m.zx,m.zy)), Utility.GREEN, PathStructures.Pose.RADIUS * m.getPartialZoom(0.75), 100)

    # Draw fps counter
    Utility.drawText(screen, Utility.getFont(30), "FPS: {}".format(round(clock.get_fps())), Utility.BLACK, 30, 30, 0)

    slider.draw(screen)
    slider.incrementPossibly(m)
    
    pygame.display.update()

    clock.tick(50) # limit to a 50 fps, or 20 ms per loop iteration

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


