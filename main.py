import pygame, sys
import FieldTransform, SoftwareState, PointRef, UserInput, Utility

def main():

    screen = pygame.display.set_mode((Utility.SCREEN_SIZE + Utility.PANEL_WIDTH, Utility.SCREEN_SIZE))
    pygame.display.set_caption("Path Generation by Ansel")

    fieldTranform = FieldTransform.FieldTransform()
    userInput = UserInput.UserInput(fieldTranform, pygame.mouse, pygame.key)

    state = SoftwareState.SoftwareState()

    while True:

        userInput.getUserInput()

        if userInput.isQuit:
            pygame.quit()
            sys.exit()
        


        if state.objectDragged is not None:
            state.objectDragged.beDraggedByMouse(userInput.mousePosition)



