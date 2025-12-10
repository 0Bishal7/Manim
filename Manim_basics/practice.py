# laplace_style_scene.py
# Manim Community Edition (manimce) script
# Produces a ~60 second animation inspired by 3Blue1Brown's "Why Laplace transforms are so useful"
#
# Usage (example):
# manim -pql laplace_style_scene.py LaplaceOneMinute
#
from manim import *
import numpy as np

# --- Configuration: tweak these to adjust total duration/feel ---
GRAPH_RUN = 12         # secs for initial graph build & morph
CAMERA_MOVE = 4        # secs for camera pan/zoom
EQ_ANIMATE = 10        # secs for equations / transitions
SPLANE_BUILD = 12      # secs to show s-plane and poles
FORCE_DEMO = 12        # secs to show forced oscillator idea
WRAP_UP = 8            # secs to finalize / fade out

TOTAL = GRAPH_RUN + CAMERA_MOVE + EQ_ANIMATE + SPLANE_BUILD + FORCE_DEMO + WRAP_UP

# A pleasing color palette (different from the video to keep it original)
PALETTE = {
    "background": "#0b0c10",
    "axis": "#9aa7b0",
    "func": BLUE_A,
    "transformed": YELLOW_C,
    "highlight": TEAL,
    "pole": RED_B,
    "text": LIGHT_GRAY,
}

class LaplaceOneMinute(Scene):
    def construct(self):
        self.camera.background_color = PALETTE["background"]

        title = Text("Why transforms help", font_size=56).to_edge(UP)
        subtitle = Text("Turning hard differential problems into algebra", font_size=28).next_to(title, DOWN)
        self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=UP), run_time=1.4)
        self.wait(0.6)

        # -----------------------
        # 1) Draw a function w/ moving dot (graph morphing)
        # -----------------------
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-3, 3, 1],
            tips=False,
            axis_config={"include_numbers": False, "stroke_color": PALETTE["axis"]},
            x_length=10,
            y_length=4
        ).to_edge(DOWN).shift(LEFT*0.5)

        # base function: a damped sinusoid (a typical physics signal)
        def damped_sin(x, decay=0.2, freq=1.0, phase=0):
            return np.exp(-decay * x) * np.sin(freq * x + phase)

        graph = axes.plot(lambda x: damped_sin(x, decay=0.25, freq=2.0), x_range=[0, 10], color=PALETTE["func"])
        graph_label = MathTex("f(t) = e^{-0.25t}\\sin(2t)", font_size=36).next_to(axes, LEFT+UP*0.5)

        dot = Dot(color=PALETTE["highlight"]).move_to(axes.c2p(0, 0))

        self.play(Create(axes, run_time=1.6), Create(graph, run_time=2.0), FadeIn(graph_label, shift=LEFT))
        self.play(GrowFromCenter(dot), run_time=0.6)

        # animate dot traveling and the graph subtly changing (morph)
        def update_dot(mob, dt):
            t = self.time
            x = (t % 8)  # loop motion across domain
            y = damped_sin(x, decay=0.25, freq=2.0)
            mob.move_to(axes.c2p(x, y))

        dot.add_updater(update_dot)
        # gentle morph: change the frequency and amplitude over time to show "parameter change"
        for decay, freq in [(0.25, 2.0), (0.5, 1.5), (0.12, 3.0)]:
            new_graph = axes.plot(lambda x, d=decay, f=freq: damped_sin(x, decay=d, freq=f), x_range=[0,10])
            self.play(Transform(graph, new_graph), run_time=GRAPH_RUN/3)
        self.wait(0.5)

        # -----------------------
        # 2) Camera swoop & highlight "hard ODE"
        # -----------------------
        self.play(self.camera.frame.animate.scale(0.8).shift(RIGHT*2), run_time=CAMERA_MOVE)
        ode = MathTex(r"\text{Solve } \; \; y'' + 0.5 y' + 2 y = f(t)", font_size=36).next_to(axes, UP*1.5+RIGHT*1.5)
        self.play(FadeIn(ode, shift=UP), run_time=1.0)
        self.wait(0.4)

        hint = Text("Differential equation → messy to solve directly", font_size=24).next_to(ode, DOWN)
        self.play(Write(hint), run_time=1.2)
        self.wait(0.6)

        # subtle emphasis on derivatives
        derivs = MathTex(r"\mathrm{d} / \mathrm{d}t", font_size=28).next_to(hint, DOWN)
        self.play(Indicate(ode, scale_factor=1.05), FadeIn(derivs, shift=DOWN), run_time=1.0)
        self.wait(0.6)

        # -----------------------
        # 3) Show idea of transform (arrow + algebraic simplification)
        # -----------------------
        self.play(self.camera.frame.animate.shift(LEFT*1.5).scale(0.9), run_time=1.0)
        trans_box = Rectangle(height=3, width=6, stroke_width=2).set_fill(opacity=0).move_to(RIGHT*1.5+UP*0.5)
        trans_label = Text("Laplace Transform", font_size=30).move_to(trans_box.get_top() + DOWN*0.5)
        self.play(Create(trans_box), FadeIn(trans_label, shift=UP), run_time=0.8)

        # Show transform action: differential to algebraic
        lhs = MathTex(r"\mathcal{L}\{y'(t)\} = sY(s) - y(0)").scale(0.8).next_to(trans_box.get_center(), LEFT*1.1+DOWN*0.1)
        rhs = MathTex(r"\mathcal{L}\{y''(t)\} = s^2 Y(s) - s y(0) - y'(0)").scale(0.8).next_to(lhs, DOWN)
        self.play(Write(lhs, run_time=1.2), Write(rhs, run_time=1.2))
        self.wait(0.6)

        eq_before = MathTex(r"s^2 Y(s) - s y(0) - y'(0) + 0.5(sY(s)-y(0)) + 2Y(s) = F(s)",
                            font_size=28).next_to(trans_box.get_center(), RIGHT*0.5)
        self.play(Write(eq_before, run_time=1.6))
        self.wait(0.6)

        eq_after = MathTex(r"Y(s)\big(s^2 + 0.5 s + 2\big) - (\cdots)= F(s)", font_size=28).next_to(eq_before, DOWN)
        self.play(Transform(eq_before, eq_after), run_time=1.0)
        self.wait(0.4)

        simpl = MathTex(r"Y(s) = \dfrac{F(s) + (\text{ICs})}{s^2 + 0.5s + 2}", font_size=32).next_to(trans_box.get_bottom(), DOWN)
        self.play(Write(simpl, run_time=1.2))
        self.wait(0.6)

        # -----------------------
        # 4) s-plane (complex plane) with poles visualization
        # -----------------------
        # move camera to new area
        self.play(self.camera.frame.animate.shift(RIGHT*1.5+UP*0.8).scale(1.05), run_time=1.0)
        splane = ComplexPlane(real_range=[-6, 6, 1], imag_range=[-4, 4, 1],
                             axis_config={"stroke_color": PALETTE["axis"]}, background_line_style={"stroke_opacity": 0.15}).scale(1.0)
        splane_title = Text("s-plane (poles & zeros)", font_size=28).next_to(splane, UP*3.1)
        self.play(Create(splane, run_time=1.2), FadeIn(splane_title, shift=UP), run_time=1.2)

        # compute roots of denominator s^2 + 0.5 s + 2
        coeffs = [1, 0.5, 2]
        roots = np.roots(coeffs)
        poles = VGroup()
        for r in roots:
            pole = Dot(splane.n2p(complex(r.real, r.imag)), radius=0.12, color=PALETTE["pole"])
            cross = Cross(pole, stroke_width=3).scale(0.6)
            pole_group = VGroup(pole, cross)
            poles.add(pole_group)

        self.play(LaggedStartMap(FadeIn, poles, shift=UP), run_time=2.0)
        pole_labels = VGroup(*[
            MathTex(f"{root.real:.2f}{'+' if root.imag>=0 else '-'}{abs(root.imag):.2f}i", font_size=20).next_to(p, RIGHT*0.4+UP*0.05)
            for root, p in zip(roots, poles)
        ])
        for lbl in pole_labels:
            self.play(FadeIn(lbl), run_time=0.3)

        expl = Text("Poles near the imaginary axis → resonant/long lasting response", font_size=20).next_to(splane, DOWN*2.6)
        self.play(Write(expl), run_time=1.0)
        self.wait(0.8)

        # animate how input frequency F(s) interacts with poles (a simplified depiction)
        freq_dot = Dot(color=PALETTE["transformed"]).move_to(splane.n2p(2.0, 1.0))
        freq_label = Text("F(s) (input frequency)", font_size=18).next_to(freq_dot, RIGHT)
        self.play(GrowFromCenter(freq_dot), FadeIn(freq_label, shift=RIGHT), run_time=1.0)
        # pulse effect toward nearest pole
        self.play(freq_dot.animate.scale(1.4), run_time=0.6)
        self.play(freq_dot.animate.move_to(poles[0][0].get_center()).scale(0.6), run_time=1.2)
        self.wait(0.5)

        # -----------------------
        # 5) Quick "forced oscillator" demonstration (overlay)
        # -----------------------
        # return camera near original axes and overlay a small oscillator schematic
        self.play(self.camera.frame.animate.shift(LEFT*2.5+DOWN*0.2).scale(0.8), run_time=1.2)

        # small oscillator schematic
        box = RoundedRectangle(corner_radius=0.2, height=2.6, width=4.6).to_corner(DL).set_fill(opacity=0)
        mass = Circle(radius=0.25).move_to(box.get_center()+RIGHT*1.2)
        spring = Line(box.get_center()+LEFT*0.8, mass.get_center(), stroke_width=6)
        force_arrow = Arrow(start=mass.get_center()+UP*0.6, end=mass.get_center()+UP*0.2).set_stroke(width=3)
        force_label = MathTex("f(t)", font_size=24).next_to(force_arrow, UP)

        self.play(Create(box), Create(spring), Create(mass), Create(force_arrow), Write(force_label), run_time=1.4)
        self.play(mass.animate.shift(RIGHT*0.2), mass.animate.shift(LEFT*0.2), rate_func=there_and_back, run_time=1.2)
        self.wait(0.6)

        # connect the oscillator to s-plane idea (arrow)
        arrow = Arrow(start=mass.get_center()+UP*0.4, end=splane.get_center()+RIGHT*0.5, buff=0.2)
        self.play(Create(arrow), run_time=1.0)
        note = Text("Use Laplace → algebraic transfer function → study poles", font_size=20).next_to(arrow, UP*0.2)
        self.play(Write(note), run_time=1.0)
        self.wait(0.8)

        # -----------------------
        # 6) Wrap up: suggest the power of transforms, fade out
        # -----------------------
        wrap = VGroup(
            Text("Takeaway:", font_size=36).to_edge(UP).shift(LEFT*3),
            Text("Transforms let us turn calculus (derivatives) into algebra (polynomials in s).", font_size=22).next_to(axes, UP*3.2)
        )
        self.play(FadeIn(wrap, shift=UP), run_time=1.2)

        self.play(FadeOut(VGroup(axes, graph_label, dot, ode, hint, derivs, trans_box, lhs, rhs, eq_after, simpl,
                                 splane_title, poles, pole_labels, expl, freq_dot, freq_label, box, spring, mass, force_arrow,
                                 force_label, arrow, note)),
                       shift=DOWN, run_time=1.8)
        self.wait(0.6)

        end_text = Text("Want the Manim code for this? I can customize timing, colors, or make it longer.", font_size=20)
        self.play(Write(end_text), run_time=1.2)
        self.wait(1.0)
