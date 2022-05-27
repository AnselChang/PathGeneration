import sys, pygame
import MouseHandler, PathStructures, Utility

SCREEN_SIZE = 600
SCREEN_DIMS = (SCREEN_SIZE, SCREEN_SIZE)

screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption("Path Generation by Ansel")

fieldSurface = pygame.transform.smoothscale(pygame.image.load("Images/squarefield.png"), SCREEN_DIMS)



path = PathStructures.Path()
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
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    # Draw everything
    path.draw(screen)
    path.drawPoints(screen, 5)
    if not anyPoseHovered: # Draw hovering pose if nothing selected
        Utility.drawCircle(screen, *path.getMousePosePosition(m.x,m.y), Utility.GREEN, PathStructures.Pose.RADIUS, 100)
    
    pygame.display.update()

    pygame.time.wait(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


