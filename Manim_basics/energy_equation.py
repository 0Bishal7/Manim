from manim import *
import numpy as np
import random

class EnergyExplainer(Scene):
    def construct(self):
        # --- BACKGROUND GRADIENT ---
        self.camera.background_color = "#1B1B2F"  # dark blue-purple background

        # --- TITLE / HOOK (0-5s) ---
        title = Text(
            "Light as Waves",
            font_size=60,
            gradient=(BLUE, PURPLE)
        ).to_edge(UP)
        self.play(FadeIn(title, shift=UP*0.5), run_time=1.5)

        # --- SINGLE HAND-DRAWN-LIKE WAVE ---
        def hand_drawn_wave(time):
            def wave_func(x):
                return 0.4*np.sin(4*x + 3*time) + 0.05*np.sin(20*x + 5*time)
            return FunctionGraph(
                wave_func,
                x_range=[-4, 4],
                color=BLUE,
                stroke_width=4
            ).shift(DOWN*1.5)
        
        wave = always_redraw(lambda: hand_drawn_wave(self.time))
        self.play(Create(wave), run_time=2)

        # --- PHOTON DOT RIDING WAVE ---
        photon = Dot(point=np.array([-4, -1.5, 0]), color=YELLOW)
        self.add(photon)

        def update_photon(dot):
            x = -4 + 8 * self.time / 4  # 4s travel
            y = 0.4*np.sin(4*x + 3*self.time) + 0.05*np.sin(20*x + 5*self.time) - 1.5
            dot.move_to([x, y, 0])
        photon.add_updater(update_photon)
        self.wait(4)  # photon moves along wave

        # --- EQUATION INTRODUCTION (5-15s) ---
        equation = MathTex("E", "=", "h", "\\nu", font_size=90).shift(UP*1.5)
        self.play(Write(equation, run_time=2))
        self.wait(1)

        # --- SYMBOL LABELS ---
        E_label = MathTex(r"\text{Energy}", font_size=40).next_to(equation[0], DOWN, buff=0.8)
        h_label = MathTex(r"\text{Planck's constant}", font_size=40).next_to(equation[2], DOWN, buff=0.8)
        nu_label = MathTex(r"\text{Frequency }(\nu)", font_size=40).next_to(equation[3], DOWN, buff=0.8)
        self.play(FadeIn(E_label), FadeIn(h_label), FadeIn(nu_label), lag_ratio=0.2, run_time=1.5)
        self.wait(0.5)

        # --- FREQUENCY VS ENERGY GRAPH (15-35s) ---
        # Axes
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            tips=True,
            axis_config={"stroke_width": 2}
        ).shift(DOWN*0.5)
        # Add slight jitter to axes for hand-drawn effect
        axes.add_updater(lambda ax: ax.shift(0.01*np.random.randn()*RIGHT))

        self.play(Create(axes), run_time=2)

        # Energy line
        def energy_curve(time):
            x = np.linspace(0, 5, 100)
            y = 1*x + 0.1*np.sin(10*x + 2*time)
            points = np.array([[xi, yi, 0] for xi, yi in zip(x, y)])
            return VMobject().set_points_as_corners(points).set_color(ORANGE)
        energy_line = always_redraw(lambda: energy_curve(self.time))
        self.play(Create(energy_line), run_time=2)

        # Photon moves along energy curve
        photon_energy = Dot(color=YELLOW)
        self.add(photon_energy)
        def update_photon_energy(dot):
            t = self.time
            x = t if t <= 5 else 5
            y = x + 0.1*np.sin(10*x + 2*t)
            dot.move_to([x, y, 0])
        photon_energy.add_updater(update_photon_energy)
        self.wait(5)  # watch photon move along curve

        # --- MULTIPLE WAVES (35-50s) ---
        colors = [RED, GREEN, BLUE]
        waves = []
        photons = []
        for i, c in enumerate(colors):
            w = always_redraw(
                lambda c=c, i=i: FunctionGraph(
                    lambda x: 0.3*np.sin(4*x + 3*self.time + i) + 0.05*np.sin(15*x + 4*self.time),
                    x_range=[-4,4],
                    color=c,
                    stroke_width=3
                ).shift(DOWN*1.5 - i*0.6*UP)
            )
            waves.append(w)
            self.add(w)
            p = Dot(point=np.array([-4, -1.5 - i*0.6, 0]), color=c)
            photons.append(p)
            def updater(dot=p, i=i):
                x = -4 + 8*self.time / 4
                y = 0.3*np.sin(4*x + 3*self.time + i) + 0.05*np.sin(15*x + 4*self.time) - 1.5 - i*0.6
                dot.move_to([x, y, 0])
            p.add_updater(updater)
            self.add(p)
        self.wait(5)

        # --- WRAP-UP (50-60s) ---
        # Fade in equation again
        final_eq = MathTex("E", "=", "h", "\\nu", font_size=90, color=YELLOW).to_edge(UP)
        self.play(FadeIn(final_eq, shift=UP*0.5), run_time=2)

        # Camera zoom out
        self.play(
            self.camera.frame.animate.scale(1.2).shift(DOWN*0.5),
            run_time=2
        )
        self.wait(2)
