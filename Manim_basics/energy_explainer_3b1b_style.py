# energy_explainer_3b1b_style.py
from manim import *
import numpy as np

# ---------------------------
# Helpers
# ---------------------------
def smooth_noise(x, t, freqs=(2.5, 5.5, 11.0), amps=(0.04, 0.02, 0.01)):
    """Deterministic smoothly-varying 'hand-draw' jitter as sum of sines."""
    s = 0.0
    for f, a in zip(freqs, amps):
        s += a * np.sin(f * x + 1.9 * f * t)
    return s

def hand_drawn_wave(x, t, amp=0.35, freq=3.2, phase=0.0):
    return amp * np.sin(freq * x + 2.2 * t + phase) + smooth_noise(x, t)

# small utility - make a subtle halo
def make_halo(point, radius=0.18, color=YELLOW, opacity=0.14):
    c = Circle(radius=radius).move_to(point)
    c.set_fill(color, opacity=opacity)
    c.set_stroke(width=0)
    return c

# ---------------------------
# Main Scene
# ---------------------------
class EnergyExplainer(MovingCameraScene):
    def construct(self):
        # ---------- Background (soft two-color fill) ----------
        self.camera.background_color = "#0b1223"  # dark navy
        bg = FullScreenRectangle().set_fill(color=[BLUE, PURPLE], opacity=1)
        self.add(bg)

        # ---------- Title (0s) ----------
        title = Text("Light as Waves", font_size=64, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title, shift=UP * 0.5), run_time=1.0)

        # ---------------------
        # 0–5 sec: Hook — single hand-drawn wave + photon
        # ---------------------
        wave = always_redraw(lambda:
            FunctionGraph(
                lambda x: hand_drawn_wave(x, self.time, amp=0.45, freq=3.6),
                x_range=[-6, 6],
                stroke_width=4,
            ).shift(DOWN * 1.4)
        )
        photon = Dot(radius=0.10, color=YELLOW).move_to([-5.8, hand_drawn_wave(-5.8, 0) - 1.4, 0])
        photon_halo = make_halo(photon.get_center(), radius=0.22)

        # ensure halo follows photon
        photon_halo.add_updater(lambda m: m.move_to(photon.get_center()))

        self.add(wave, photon, photon_halo)
        # Move photon along x (we use MoveAlongPath for smooth horizontal motion; vertical tracked by updater)
        photon.add_updater(lambda m: m.move_to(
            np.array([m.get_center()[0], hand_drawn_wave(m.get_center()[0], self.time) - 1.4, 0])
        ))
        # Animate photon moving left->right in ~4.8s for hook
        self.play(photon.animate.shift(RIGHT * 11.6), run_time=4.8, rate_func=linear)
        self.wait(0.2)

        # ---------------------
        # 5–15 sec: Equation Introduction (handwriting effect)
        # ---------------------
        eq = MathTex("E", "=", "h", r"\nu", font_size=112).shift(UP * 1.3)
        # handwriting: Write each token with slight stagger
        self.play(Write(eq[0], run_time=0.6))
        self.play(Write(eq[1], run_time=0.25))
        self.play(Write(eq[2], run_time=0.6))
        self.play(Write(eq[3], run_time=0.6))
        self.wait(0.25)

        # labels below (use math mode for nu)
        E_label = Tex("Energy", font_size=34).next_to(eq[0], DOWN, buff=0.6)
        h_label = Tex("Planck's constant", font_size=28).next_to(eq[2], DOWN, buff=0.6)
        nu_label = Tex(r"Frequency ($\nu$)", font_size=28).next_to(eq[3], DOWN, buff=0.6)
        self.play(FadeIn(E_label), FadeIn(h_label), FadeIn(nu_label), run_time=1.2)

        # Photon glow expands as energy increases — create a glow whose width depends on x position
        glow = Circle(radius=0.14, color=YELLOW, fill_opacity=0.5).move_to(photon.get_center())
        def glow_update(m):
            pos = photon.get_center()
            # energy proxy (normalized x from -5.8..+5.8)
            norm = (pos[0] + 5.8) / (11.6)
            size = 0.14 + 0.12 * norm  # grows with x
            m.move_to(pos)
            m.set_width(size)
            m.set_fill(opacity=0.4 + 0.3 * norm)
        glow.add_updater(glow_update)
        self.add(glow)
        self.wait(4.0)  # continue storyline so total ~15s

        # ---------------------
        # 15–35 sec: Frequency vs Energy (sketchy graph)
        # ---------------------
        # Move camera slightly to focus on bottom area where graph will be
        frame = self.camera.frame
        self.play(frame.animate.shift(DOWN * 0.5), run_time=1.2, rate_func=smooth)

        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=9,
            y_length=5,
            tips=True,
        ).to_edge(DOWN)
        axes.shift(RIGHT * 0.5)

        # sketchy (hand-drawn) outline of axes: a jagged polyline overlay
        def sketch_x():
            xs = np.linspace(0, 10, 200)
            pts = [axes.c2p(x, 0.0 + 0.03 * np.sin(4 * x + 1.4 * self.time)) for x in xs]
            m = VMobject()
            m.set_points_as_corners(pts)
            m.set_stroke(GREY_A, 1.2, opacity=0.6)
            return m

        sketch_x_overlay = always_redraw(sketch_x)

        self.play(Create(axes), run_time=1.5)
        self.play(FadeIn(sketch_x_overlay), run_time=0.6)

        # energy curve (smoothly grows; hand-drawn jitter incorporated)
        def energy_func(x):
            return 0.85 * x + 0.25 * np.sin(2.0 * x + 0.9 * self.time) + 0.12 * np.sin(7.0 * x + 0.6 * self.time)

        energy_curve = always_redraw(lambda:
            axes.plot(lambda x: energy_func(x), x_range=[0, 10], stroke_width=3.5, color=ORANGE)
        )
        self.play(Create(energy_curve), run_time=2.2)

        # photon rides the curve from left to right (8s)
        photon_graph = Dot(color=YELLOW, radius=0.09)
        photon_graph.move_to(axes.c2p(0, energy_func(0)))
        photon_graph.add_updater(lambda m: m.move_to(axes.c2p(
            min(9.5, max(0.0, (self.time - (self.time)) * 0)), energy_func(0)
        )))  # dummy until we animate using ValueTracker

        # Instead use ValueTracker to control x along curve, so updater is smooth
        x_tracker = ValueTracker(0.0)
        def photon_graph_updater(m):
            x = x_tracker.get_value()
            y = energy_func(x)
            m.move_to(axes.c2p(x, y))
        photon_graph.add_updater(photon_graph_updater)
        self.add(photon_graph)

        # Advance tracker from 0 to 9.2 over 8 seconds
        self.play(x_tracker.animate.set_value(9.2), run_time=8.0, rate_func=smooth)
        self.wait(0.4)

        # ---------------------
        # 35–50 sec: Real-World Example — multiple colored hand-drawn waves + hopping photons
        # ---------------------
        # Add three colored waves at different vertical positions
        wave_group = VGroup()
        colors = [RED, GREEN, BLUE]
        verticals = [0.6, 0.0, -0.6]  # relative shifts
        for i, c in enumerate(colors):
            wave_i = always_redraw(lambda i=i, c=c:
                FunctionGraph(
                    lambda x: hand_drawn_wave(x, self.time + i * 0.4, amp=0.32, freq=3.0, phase=i),
                    x_range=[-6, 6],
                    stroke_width=3,
                    color=c
                ).shift(DOWN * (0.6 + i * 0.6))
            )
            wave_group.add(wave_i)
            self.add(wave_i)

        # create hopping photons (staggered start)
        hopping_photons = VGroup()
        hop_trackers = []
        for i in range(3):
            pt = Dot(radius=0.085, color=colors[i])
            # place at start
            x0 = -5.5
            y0 = hand_drawn_wave(x0, self.time + i * 0.2, amp=0.32, freq=3.0, phase=i) - (0.6 + i * 0.6)
            pt.move_to([x0, y0, 0])
            hopping_photons.add(pt)
            self.add(pt)
            vt = ValueTracker(0.0)
            hop_trackers.append(vt)
            def make_updater(pt=pt, idx=i, tracker=vt):
                def updater(m):
                    prog = tracker.get_value()
                    x = -5.5 + 11.0 * prog
                    y = hand_drawn_wave(x, self.time + idx * 0.4, amp=0.32, freq=3.0, phase=idx) - (0.6 + idx * 0.6)
                    m.move_to([x, y, 0])
                return updater
            pt.add_updater(make_updater())

        # Animate hopping photons sequentially with small offsets
        self.play(
            hop_trackers[0].animate.set_value(1.0),
            run_time=4.5, rate_func=linear
        )
        self.play(
            hop_trackers[1].animate.set_value(1.0),
            hop_trackers[2].animate.set_value(1.0),
            run_time=4.5, rate_func=linear
        )
        self.wait(0.4)

        # Soft background tint transition indicating energy/mood change
        tint = FullScreenRectangle().set_fill(color=[PURPLE, ORANGE], opacity=0.12)
        self.play(FadeIn(tint), run_time=1.0)
        self.wait(0.3)

        # ---------------------
        # 50–60 sec: Wrap-Up — zoom out; final E = h nu appears gently
        # ---------------------
        # Create halos for all photons
        all_photons = VGroup(photon, photon_graph, *hopping_photons)
        halos = VGroup()
        for p in all_photons:
            h = make_halo(p.get_center(), radius=0.22, color=YELLOW, opacity=0.12)
            h.add_updater(lambda m, src=p: m.move_to(src.get_center()))
            halos.add(h)
            self.add(h)

        # Final equation (hand-drawn stroke reveal)
        final_eq = MathTex("E", "=", "h", r"\nu", font_size=140).to_edge(UP)
        final_eq.set_color(WHITE)
        # start faint and reveal
        final_eq.set_opacity(0.0)
        self.add(final_eq)
        self.play(final_eq.animate.set_opacity(1.0), run_time=1.6)

        # Camera cinematic zoom-out (frame is a Mobject in MovingCameraScene)
        self.play(frame.animate.scale(1.22).shift(UP * 0.25), run_time=2.0, rate_func=smooth)
        self.wait(0.8)

        # final hold
        self.wait(1.0)
