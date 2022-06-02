import sys, pygame
import MouseHandler, PathStructuresBezier, Utility, Slider

screen = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
pygame.display.set_caption("Path Generation by Ansel")

rawFieldSurface = pygame.image.load("Images/squarefield.png")
IMAGE_SIZE = 812
fieldSurface = pygame.transform.smoothscale(rawFieldSurface, (Utility.SCREEN_SIZE, Utility.SCREEN_SIZE))

path = PathStructuresBezier.Path(0.5)
m = MouseHandler.Mouse(pygame.mouse, pygame.key)

Slider.init(m)
slider = Slider.Slider(830, 1070, 730)

clock = pygame.time.Clock()

while True:

    key = None
    mousewheel = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            key = event.key
        elif event.type == pygame.MOUSEWHEEL:
            mousewheel = event.y
    m.tick(key)

    zx,zy =m.zx, m.zy
    z = m.zoom
    if m.getKey(pygame.K_a):
        m.zoom += 0.15 # zoom in
    elif m.getKey(pygame.K_s):
        m.zoom -= 0.15 # zoom out
    m.zoom += mousewheel * 0.1
    m.zoom = Utility.clamp(m.zoom, 1, 3)
        
    # Rescale the field surface ONLY when there is a zoom update
    if z != m.zoom:
        x,y = m.inchToPixel(zx, zy)
        m.panX += m.x - x
        m.panY += m.y - y
        m.boundFieldPan()
        # slightly inefficient but oh well
        fieldSurface = pygame.transform.smoothscale(rawFieldSurface, [Utility.SCREEN_SIZE * m.zoom, Utility.SCREEN_SIZE * m.zoom])

    if m.simulating:
        slider.handleMouse()
        if slider.draggingSlider:
            m.playingSimulation = False
        path.handleRobotSliders(m, slider)

    anyPoseHovered = path.handleMouse(m, slider)    
        
    if m.simulating:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if slider.mouseHovering() else pygame.SYSTEM_CURSOR_WAIT)
    elif m.poseDragged is not None or m.panning:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif anyPoseHovered:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

    # Draw everything
    screen.blit(fieldSurface, (m.panX,m.panY)) # draw field
    if not m.simulating:
        path.drawPaths(screen, m)
    path.drawRobot(screen, m, slider.value)
    path.drawPoints(screen, m)
    
    p = m.poseSelectHeading # Draw guide line for heading
    if p is not None and p.theta is not None: 
        Utility.drawThinLine(screen, Utility.PURPLE, *m.inchToPixel(p.x, p.y), m.x, m.y)

    if not anyPoseHovered and not m.panning and not m.simulating and not m.poseSelectHeading: # Draw hovering pose if nothing selected and not scrolling field
        Utility.drawCircle(screen, *m.inchToPixel(*path.getMousePosePosition(m.zx,m.zy)), Utility.GREEN, PathStructuresBezier.Pose.RADIUS * m.getPartialZoom(0.75), 100)


    # Draw panel things

    # Draw panel background
    border = 5
    pygame.draw.rect(screen, Utility.PANEL_GREY, [Utility.SCREEN_SIZE + border, 0, Utility.PANEL_WIDTH - border, Utility.SCREEN_SIZE])
    pygame.draw.rect(screen, Utility.BORDER_GREY, [Utility.SCREEN_SIZE, 0, border, Utility.SCREEN_SIZE])

    slider.draw(screen)

    # Draw fps counter
    Utility.drawText(screen, Utility.getFont(30), "FPS: {}".format(round(clock.get_fps())), Utility.BLACK, 1000, 760, 0)
    path.drawPanel(screen, m)
    
    pygame.display.update()

    path.handlePlayback(m, slider)
    clock.tick(50) # limit to a 50 fps, or 20 ms per loop iteration


