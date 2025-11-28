from manim import *

class LongSquareScene(Scene):
    def construct(self):
        # Create a square
        square = Square(side_length=2, color=BLUE)
        
        # Show square (2 seconds)
        self.play(Create(square), run_time=2)
        self.wait(1)

        # Rotate square (3 seconds)
        self.play(Rotate(square, angle=PI), run_time=3)

        # Change color (2 seconds)
        self.play(square.animate.set_color(RED), run_time=2)

        # Move square around (3 seconds)
        self.play(square.animate.shift(RIGHT*2 + UP*1), run_time=3)

        # Add text BELOW the square (small size)
        text = Text("Square Animation Complete", font_size=28)
