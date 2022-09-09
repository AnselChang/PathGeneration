import Utility, pygame

"""
Classes that have a self.tooltip instance variable storing a Tooltip object will have a tooltip displayed
when the mouse is hovering over the object
"""

BACKGROUND_COLOR = [220, 220, 200]
TEXT_COLOR = [0,0,0]

class Tooltip:

    def __init__(self, *messages: str):

        self.tooltip = self.getTooltipSurface(messages)

    # Return a tooltip surface based on message parameter(s). Each parameter is a new line
    def getTooltipSurface(self, messages):

        texts = [Utility.FONT20.render(message, True, TEXT_COLOR) for message in messages]

        outsideMargin = 7 # margin between text and tooltip surface
        insideMargin = 1 # margin between lines of text
        textWidth = max([text.get_width() for text in texts])
        textHeight = texts[0].get_height()

        tooltipWidth = textWidth + 2 * outsideMargin
        tooltipHeight = len(texts) * textHeight + (len(texts)-1) * insideMargin + 2 * outsideMargin

        tooltipSurface = pygame.Surface([tooltipWidth, tooltipHeight]).convert_alpha()
        pygame.draw.rect(tooltipSurface, BACKGROUND_COLOR, [0, 0, tooltipWidth, tooltipHeight], border_radius = 10)
        pygame.draw.rect(tooltipSurface, Utility.BLACK, [0, 0, tooltipWidth, tooltipHeight], width = 3, border_radius = 10)
        
        y = outsideMargin
        for text in texts:
            tooltipSurface.blit(text, [outsideMargin, y])
            y += insideMargin + textHeight

        return tooltipSurface

    # Draw the tooltip approximately where the mouse position is
    def draw(self, screen: pygame.Surface, mousePosition: tuple):
        
        # Calculate tooltip position, preventing tooltip from going above or left of screen
        x = max(0, int(mousePosition[0] - self.tooltip.get_width()/2))
        y = max(0, int(mousePosition[1] - self.tooltip.get_height()))

        # prevent tooltip from spilling over right edge of screen
        x = min(x, Utility.SCREEN_SIZE + Utility.PANEL_WIDTH - self.tooltip.get_width())

        screen.blit(self.tooltip, (x,y))