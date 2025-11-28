from manim import *

class SquareScene(Scene):
    def construct(self):
        # Create a square
        square = Square()
        
        # Show the square on screen
        self.play(Create(square))
        
        # Wait for 1 second
        self.wait(1)
