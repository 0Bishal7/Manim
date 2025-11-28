from manim import *

class MathBasics(Scene):
    def construct(self):
        # TITLE (3 seconds)
        title = Text("Basic Math: Addition & Subtraction", font_size=40)
        self.play(FadeIn(title), run_time=2)
        self.wait(1)
        self.play(FadeOut(title))

        # ADDITION (10 seconds)
        addition_title = Text("Addition", font_size=36, color=YELLOW)
        addition_title.to_edge(UP)
        self.play(Write(addition_title), run_time=2)

        add_eq = MathTex("3", "+", "4", "=", "7").scale(1.5)
        self.play(Write(add_eq), run_time=3)
        self.wait(1)

        add_expl = Text("We add numbers to get a bigger number.", font_size=28)
        add_expl.next_to(add_eq, DOWN, buff=0.5)
        self.play(FadeIn(add_expl), run_time=2)
        self.wait(1.5)

        self.play(FadeOut(add_eq), FadeOut(add_expl), FadeOut(addition_title))

        # SUBTRACTION (10 seconds)
        sub_title = Text("Subtraction", font_size=36, color=BLUE)
        sub_title.to_edge(UP)
        self.play(Write(sub_title), run_time=2)

        sub_eq = MathTex("9", "-", "5", "=", "4").scale(1.5)
        self.play(Write(sub_eq), run_time=3)
        self.wait(1)

        sub_expl = Text("We subtract to find what is left.", font_size=28)
        sub_expl.next_to(sub_eq, DOWN, buff=0.5)
        self.play(FadeIn(sub_expl), run_time=2)
        self.wait(1.5)

        self.play(FadeOut(sub_eq), FadeOut(sub_expl), FadeOut(sub_title))

        # END SCREEN (5 seconds)
        end_text = Text("Math is Easy! Keep Practicing ❤️", font_size=32)
        self.play(FadeIn(end_text), run_time=2)
        self.wait(3)
