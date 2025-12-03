from manim import *

class TestSquare(Scene):
    def construct(self):
        self.play(Create(Square()))
        self.wait(1)
