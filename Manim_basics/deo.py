from manim import *
import numpy as np

class CAPColdOpen(Scene):
    def construct(self):

        # -------------------------------
        # 00:00 – 00:02  COLD OPEN (SHOCK)
        # -------------------------------
        shock_text = Text("DATA IS WRONG", color=RED, font_size=96, weight=BOLD)

        self.play(FadeIn(shock_text, scale=1.2), run_time=0.2)
        self.play(Wiggle(shock_text, scale_value=1.1), run_time=0.8)
        self.wait(0.4)
        self.play(FadeOut(shock_text), run_time=0.3)

        # -------------------------------
        # 00:02 – 00:04  CONTRAST
        # -------------------------------
        down_text = Text("SYSTEM DOWN", color=RED, font_size=84, weight=BOLD)

        spinner = Circle(radius=0.25, color=WHITE).shift(DOWN * 1.2)
        spinner_dot = Dot(color=WHITE).move_to(spinner.point_at_angle(0))
        spinner_group = VGroup(spinner, spinner_dot)

        self.play(FadeIn(down_text), Create(spinner_group), run_time=0.4)
        self.play(Rotate(spinner_group, angle=TAU), run_time=0.8, rate_func=linear)
        self.play(spinner_dot.animate.set_opacity(0.2), run_time=0.2)
        self.wait(0.3)
        self.play(FadeOut(down_text), FadeOut(spinner_group))

        # -------------------------------
        # 00:04 – 00:06  REALITY SPLIT
        # -------------------------------
        left_box = Rectangle(width=5, height=3).shift(LEFT * 3)
        right_box = Rectangle(width=5, height=3).shift(RIGHT * 3)

        balance_left = Text("Balance: ₹100", font_size=42)
        balance_right = Text("Balance: ₹80", font_size=42)

        balance_left.move_to(left_box)
        balance_right.move_to(right_box)

        self.play(Create(left_box), Create(right_box), run_time=0.3)
        self.play(Write(balance_left), Write(balance_right), run_time=0.5)
        self.wait(0.7)
        self.play(FadeOut(VGroup(left_box, right_box, balance_left, balance_right)))

        # -------------------------------
        # 00:06 – 00:08  REVEAL CAUSE
        # -------------------------------
        nodes = VGroup(
            Circle(radius=0.3, color=GREEN).shift(LEFT * 3),
            Circle(radius=0.3, color=GREEN),
            Circle(radius=0.3, color=GREEN).shift(RIGHT * 3),
        )

        lines = VGroup(
            Line(nodes[0].get_center(), nodes[1].get_center(), color=GREEN),
            Line(nodes[1].get_center(), nodes[2].get_center(), color=GREEN),
        )

        self.play(FadeIn(nodes), Create(lines), run_time=0.6)
        self.wait(0.6)

        # -------------------------------
        # 00:08 – 00:10  FAILURE STRIKE
        # -------------------------------
        lightning = VMobject(color=RED)
        lightning.set_points_as_corners([
            UP * 2,
            UP * 1 + RIGHT * 0.2,
            UP * 0.5 + LEFT * 0.2,
            DOWN * 0.5 + RIGHT * 0.2,
            DOWN * 2
        ])

        lightning.move_to(lines[1])

        self.play(Create(lightning), Flash(lightning), run_time=0.4)
        self.play(
            lines[1].animate.set_color(RED),
            nodes[2].animate.shift(RIGHT * 0.3),
            run_time=0.4
        )
        self.wait(0.4)

        # -------------------------------
        # 00:10 – 00:13  THE CHOICE
        # -------------------------------
        choice_text = Text("MAKE A CHOICE", font_size=84, weight=BOLD)

        self.play(FadeIn(choice_text, scale=1.1), run_time=0.4)
        self.play(
            nodes.animate.set_opacity(0.3),
            lines.animate.set_opacity(0.3),
            run_time=0.4
        )
        self.wait(0.6)
        self.play(FadeOut(choice_text))

        # -------------------------------
        # 00:13 – 00:15  TITLE DROP
        # -------------------------------
        title = Text("CAP THEOREM", font_size=96, weight=BOLD)
        subtitle = Text(
            "Consistency  •  Availability  •  Partition Tolerance",
            font_size=36
        ).next_to(title, DOWN)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(subtitle, shift=DOWN), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(VGroup(title, subtitle, nodes, lines, lightning)))

        # -------------------------------
        # 0:15 – 0:30  PROBLEM SETUP
        # -------------------------------
        node_labels = VGroup(
            Text("Node A").shift(LEFT * 3),
            Text("Node B"),
            Text("Node C").shift(RIGHT * 3),
        )

        node_circles = VGroup(
            Circle(radius=0.3).shift(LEFT * 3),
            Circle(radius=0.3),
            Circle(radius=0.3).shift(RIGHT * 3),
        )

        links = VGroup(
            Line(node_circles[0].get_center(), node_circles[1].get_center()),
            Line(node_circles[1].get_center(), node_circles[2].get_center()),
        )

        self.play(FadeIn(node_circles), Write(node_labels), Create(links))
        self.play(Wiggle(links[1]), run_time=0.6)
        self.wait(0.6)

        # -------------------------------
        # 0:30 – 0:55  CAP LETTERS
        # -------------------------------
        c = Text("C", font_size=120)
        a = Text("A", font_size=120).shift(RIGHT * 3)
        p = Text("P", font_size=120).shift(LEFT * 3)

        triangle = Polygon(p.get_center(), c.get_center(), a.get_center())

        self.play(Write(p), Write(c), Write(a), run_time=0.6)
        self.play(Create(triangle), run_time=0.4)

        crack = Line(UP * 1.5, DOWN * 1.5, color=RED)
        self.play(Create(crack), FadeOut(triangle), run_time=0.4)
        self.wait(0.6)

        # -------------------------------
        # 0:55 – 1:20  ANALOGY
        # -------------------------------
        people = VGroup(
            Circle(radius=0.3),
            Circle(radius=0.3).shift(RIGHT * 2),
            Circle(radius=0.3).shift(LEFT * 2),
        )

        speech = RoundedRectangle(width=2.5, height=1, corner_radius=0.2)
        speech_text = Text("Hello?", font_size=28).move_to(speech)

        self.play(FadeIn(people), run_time=0.4)
        self.play(FadeIn(speech), Write(speech_text), run_time=0.4)
        self.play(people[2].animate.set_opacity(0.3), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(VGroup(people, speech, speech_text)))

        # -------------------------------
        # 1:20 – 1:45  P IS MANDATORY
        # -------------------------------
        p_big = Text("P", font_size=160, color=YELLOW)
        inevitable = Text("Network failures are inevitable", font_size=48).next_to(p_big, DOWN)

        self.play(Write(p_big), run_time=0.4)
        self.play(Indicate(p_big), Wiggle(p_big), run_time=0.6)
        self.play(FadeIn(inevitable, shift=UP), run_time=0.4)
        self.wait(0.8)

        # -------------------------------
        # 1:45 – 2:00  THE REAL CHOICE
        # -------------------------------
        c_side = Text("Consistency", font_size=64).shift(LEFT * 3)
        a_side = Text("Availability", font_size=64).shift(RIGHT * 3)

        self.play(FadeIn(c_side), FadeIn(a_side), run_time=0.4)
        self.play(
            c_side.animate.set_color(BLUE),
            a_side.animate.set_color(GREEN),
            p_big.animate.set_opacity(0.3),
            run_time=0.6
        )
        self.wait(1)
