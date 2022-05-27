import sys, pygame
import MouseHandler, PathStructures, Utility

screen = pygame.display.set_mode(Utility.SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

fieldSurface = pygame.transform.smoothscale(pygame.image.load("Images/squarefield.png"), Utility.SCREEN_DIMS)

path = PathStructures.Path(10)
m = MouseHandler.Mouse(pygame.mouse, pygame.key)

while True:

    screen.blit(fieldSurface, (0,0)) # draw field
    m.tick()
    
    anyPoseHovered = path.handleMouse(m)
    

    if m.poseDragged is not None:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
    elif anyPoseHovered:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)


    # Draw everything
    path.drawPaths(screen)
    path.drawPoints(screen)
    
    p = m.poseSelectHeading # Draw guide line for heading
    if p is not None and p.theta is not None: 
        Utility.drawThinLine(screen, Utility.PURPLE, p.x, p.y, m.x, m.y)
        
    if not anyPoseHovered: # Draw hovering pose if nothing selected
        Utility.drawCircle(screen, *path.getMousePosePosition(m.x,m.y), Utility.GREEN, PathStructures.Pose.RADIUS, 100)
    
    pygame.display.update()

    pygame.time.wait(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


