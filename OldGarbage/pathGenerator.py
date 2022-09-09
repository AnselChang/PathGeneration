import sys, pygame, cProfile
import SingletonState.UserInput as UserInput, OldGarbage.PathStructuresBezier as PathStructuresBezier, Utility, OldGarbage.Slider as Slider

# Handle A and S keys to zoom in and out, as well as mousewheel. Returns true if zoom has been changed
def handleZoom(m, mousewheel, currentfieldSurface, rawFieldSurface):

    previousZoom = m.zoom
    if m.getKey(pygame.K_a):
        m.zoom += 0.15 # zoom in
    elif m.getKey(pygame.K_s):
        m.zoom -= 0.15 # zoom out
    m.zoom += mousewheel * 0.1
    m.zoom = Utility.clamp(m.zoom, 1, 3) # limits to how much you can zoom in or out

    # Rescale the field surface ONLY when there is a zoom update
    if previousZoom != m.zoom:
        x,y = m.inchToPixel(m.zx, m.zy)
        m.panX += m.x - x
        m.panY += m.y - y
        m.boundFieldPan() # clamp panning to make sure it does not go out of bounds

        # Redraw the field with new zoom
        return pygame.transform.smoothscale(rawFieldSurface, [Utility.SCREEN_SIZE * m.zoom, Utility.SCREEN_SIZE * m.zoom])

    return currentfieldSurface

# If pressed E key, export to csv
def handleExporting(m, path):
    if m.getKeyPressed(pygame.K_e):
            path.export2()

# Handle the position of the sliders based on the mouse in simulation mode
def handleSliders(m, slider, path):
        slider.handleMouse()
        if slider.draggingSlider:
            m.playingSimulation = False
        path.handleRobotSliders(m, slider)

# Set the cursor sprite (hand, crosshair, etc.) based on what the mouse is hovering over
def handleCursorSprite(m, anyPoseHovered, slider):
        if m.simulating:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if slider.mouseHovering() else pygame.SYSTEM_CURSOR_WAIT)
        elif m.poseDragged is not None or m.panning:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
        elif anyPoseHovered:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            

def main():
    
    screen = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation by Ansel")

    rawFieldSurface = pygame.image.load("Images/squarefield.png")
    fieldSurface = pygame.transform.smoothscale(rawFieldSurface, (Utility.SCREEN_SIZE, Utility.SCREEN_SIZE))

    path = PathStructuresBezier.Path(0.5)
    m = UserInput.Mouse(pygame.mouse, pygame.key)

    Slider.init(m)
    slider = Slider.Slider(830, 1070, 730)

    clock = pygame.time.Clock()

    while True:

        # handle events
        keyPressed = None
        mousewheel = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                path.save()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                keyPressed = event.key
            elif event.type == pygame.MOUSEWHEEL:
                mousewheel = event.y
            elif event.type == pygame.DROPFILE:
                path.load(event.file) # load file
                
        m.tick(keyPressed) # update mouse state machine
        
        fieldSurface = handleZoom(m, mousewheel, fieldSurface, rawFieldSurface) # handle zoom controls for the field

        handleExporting(m, path)

        if m.simulating:
            handleSliders(m, slider, path)

        # Handle all the mouse interactions with the screen. It returns whether the mouse was hovering over a pose this frame
        anyPoseHovered = path.handleMouse(m, slider)

        handleCursorSprite(m, anyPoseHovered, slider)

        # Draw everything
        screen.blit(fieldSurface, (m.panX,m.panY)) # draw field
        if not m.simulating:
            path.drawPaths(screen, m)
        path.drawPoints(screen, m)
        path.drawRobot(screen, m, slider.value)


        # If nothing is selected and not currently scrolling the field, draw a dot where the mouse is hovering to indicate a potential new pose
        if not anyPoseHovered and not m.panning and not m.simulating: 
            Utility.drawCircle(screen, *m.inchToPixel(*path.getMousePosePosition(m.zx,m.zy)), Utility.GREEN, PathStructuresBezier.Pose.RADIUS * m.getPartialZoom(0.75), 100)

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

main()
