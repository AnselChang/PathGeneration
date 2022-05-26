class Mouse:
    def __init__(self, mouse):
        self.mouse = mouse
        self.prevPressed = False
        
        self.pressing = False
        self.pressed = False
        self.released = False
        self.x = -1
        self.y = -1

        self.poseDragged  = None
        

    def tick(self):

        self.prevPressed = self.pressing
        self.pressing = self.mouse.get_pressed()[0]
        
        self.x, self.y = self.mouse.get_pos()
        self.pressed = self.pressing and not self.prevPressed
        self.released = not self.pressing and self.prevPressed


        

    
