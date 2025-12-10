from manim import *
import numpy as np

# ---------------------------
# Helper: smooth pseudo-noise
# ---------------------------
def smooth_noise(x, t, freqs=(3.0, 7.0, 13.0), amps=(0.03, 0.015, 0.007)):
    """
    Smooth pseudo-noise using a sum of sines with different frequencies and amplitudes.
    This yields a hand-drawn jitter that is deterministic and smooth in time.
    """
    total = 0.0
    for f, a in zip(freqs, amps):
        total += a * np.sin(f * x + 1.5 * f * t)
    return total

# ---------------------------
# Main Scene (Moving camera)
# ---------------------------
class EnergyExplainer(MovingCameraScene):
    def construct(self):
        # --- Background: soft gradient-like fill (v0.19 safe) ---
        bg = FullScreenRectangle().set_fill(color=[BLUE, PURPLE], opacity=1)
        self.add(bg)

        # Keep a small margin so title doesn't collide with content
        title = Text("Light as Waves", font_size=64, weight=BOLD).to_edge(UP)
        self.play(FadeIn(title, shift=UP * 0.5), run_time=1.2)

        # -------------------------
        # 0–5 sec: Hook — single wiggly wave + photon
        # -------------------------
        # Hand-drawn wave: base sine + smooth_noise
        def wave_func(x):
            return 0.45 * np.sin(3.6 * x)  # base shape; time component added in always_redraw

        wave = always_redraw(lambda:
            FunctionGraph(
                lambda x: 0.45 * np.sin(3.6 * x + 2.8 * self.time) + smooth_noise(x, self.time),
                x_range=[-6, 6], stroke_width=4
            ).shift(DOWN * 1.5)
        )
        # Photon riding the wave: we will update its (x, y) based on time
        photon = Dot(radius=0.09, color=YELLOW)
        # initial position
        photon.move_to(np.array([-5.5, wave_func(-5.5) - 1.5, 0]))
        self.add(wave, photon)

        # Photon updater: move smoothly across x in ~4.5s
        def photon_updater(mob):
            # travel from x=-5.5 to x=5.5 in 4.5s (map scene time segment)
            # We'll use a local time window: when started, we run it for 4.5s
            # Use the global self.time but scale so the motion takes ~4.5s from now
            # To keep exact storyboard timings we animate explicitly below instead of relying purely on updater
            pass
        photon.add_updater(lambda m: m.move_to(
            np.array([
                -5.5 + 11.0 * min(self.time / 4.5, 1.0),
                0.45 * np.sin(3.6 * (-5.5 + 11.0 * min(self.time / 4.5, 1.0)) + 2.8 * self.time)
                + smooth_noise(-5.5 + 11.0 * min(self.time / 4.5, 1.0), self.time) - 1.5,
                0
            ])
        ))

        # Let the photon travel across the wave for ~4.5s (0–5s slot)
        self.play(FadeIn(wave), run_time=0.7)
        self.play(MoveAlongPath(photon, Line(start=LEFT * 5.5 + DOWN * 1.5, end=RIGHT * 5.5 + DOWN * 1.5),
                                run_time=4.5, rate_func=linear),  # visual motion sync, updater keeps vertical alignment
                  run_time=4.5)
        # small pause to end the hook
        self.wait(0.5)

        # -------------------------
        # 5–15 sec: Equation introduction with handwriting feel
        # -------------------------
        # Use MathTex split so we can animate symbols stroke-by-stroke (approx)
        eq = MathTex("E", "=", "h", r"\nu", font_size=110).shift(UP * 1.3)
        # Handwriting effect: write each submobject with a short stagger
        self.play(Write(eq[0], run_time=0.6), run_time=0.6)
        self.play(Write(eq[1], run_time=0.3), run_time=0.3)
        self.play(Write(eq[2], run_time=0.6), run_time=0.6)
        self.play(Write(eq[3], run_time=0.6), run_time=0.6)
        self.wait(0.4)

        # Labels beneath equation (arranged to avoid overlap)
        E_label = Tex("Energy", font_size=32).next_to(eq[0], DOWN, buff=0.6)
        h_label = Tex("Planck's constant", font_size=28).next_to(eq[2], DOWN, buff=0.6)
        # nu_label = Tex("Frequency (\\nu)", font_size=28).next_to(eq[3], DOWN, buff=0.6)
        nu_label = Tex(r"Frequency ($\nu$)", font_size=28).next_to(eq[3], DOWN, buff=0.6)

        self.play(FadeIn(E_label), FadeIn(h_label), FadeIn(nu_label), run_time=1.2)
        self.wait(0.5)

        # Photon path follows slightly wavy irregular curve (simulate with a separate wiggly track)
        # We'll animate a glowing circle that expands as 'energy increases' while moving
        glow = Circle(radius=0.14, color=YELLOW, fill_opacity=0.7).move_to(photon.get_center())
        glow.set_gloss(0.8)
        self.add(glow)

        # updater for glow to follow photon and grow with a faux energy function
        def glow_updater(mob):
            pos = photon.get_center()
            # energy proxy: higher x -> more energy
            energy = 1.0 + 0.6 * ((pos[0] + 5.5) / 11.0)  # from 1.0 -> 1.6
            mob.move_to(pos)
            mob.set_width(0.18 * energy)
            mob.set_fill(opacity=0.5 + 0.3 * ((pos[0] + 5.5) / 11.0))
        glow.add_updater(glow_updater)

        # Let the glow update visually while photon finishes
        self.wait(0.1)

        # keep eq and labels visible until 15s mark (we've already used ~5s)
        # small pause
        self.wait(4.5)  # progress timeline so total ~15s

        # -------------------------
        # 15–35 sec: Frequency vs Energy graph (sketchy)
        # -------------------------
        # create sketchy axes (add small smooth perturbation)
        axes = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], tips=True).shift(DOWN * 0.6)
        # jittered axes lines: we will overlay a hand-drawn looking border with a low-opacity wiggle
        def jittered_axis_graph():
            # Create a slightly sketchy x axis by using a polyline with smooth_noise on y
            xs = np.linspace(0, 10, 200)
            pts = [axes.c2p(x, 0.0 + 0.05 * np.sin(4 * x + 2.0 * self.time)) for x in xs]
            jitter_x = VMobject()
            jitter_x.set_points_as_corners(pts)
            jitter_x.set_stroke(GREY, 1.0, opacity=0.6)
            return jitter_x

        sketch_x = always_redraw(jittered_axis_graph)
        self.play(Create(axes), run_time=1.5)
        self.play(FadeIn(sketch_x), run_time=0.8)

        # energy vs frequency curve: base linear with time-varying smooth noise
        def energy_curve_func(x):
            # base linear positive slope
            return 0.9 * x + 0.25 * np.sin(2.5 * x + 1.5 * self.time) + 0.15 * np.sin(8 * x + 0.8 * self.time)

        energy_curve = always_redraw(lambda:
                                     axes.plot(lambda x: energy_curve_func(x),
                                               x_range=[0, 10],
                                               color=ORANGE, stroke_width=3)
                                     )
        self.play(Create(energy_curve), run_time=2.5)

        # photon riding the graph from left to right in ~8s window
        photon_graph = Dot(color=YELLOW, radius=0.09)
        photon_graph.move_to(axes.c2p(0, energy_curve_func(0)))
        self.add(photon_graph)

        # updater for photon on graph: move from x=0 to x=9.2 in 8s (so ~t mapping)
        start_time_for_graph = self.time
        def photon_graph_updater(mob):
            elapsed = self.time - start_time_for_graph
            progress = min(max(elapsed / 8.0, 0.0), 1.0)  # 8s travel
            x = 9.2 * progress
            y = energy_curve_func(x)
            mob.move_to(axes.c2p(x, y))
        photon_graph.add_updater(photon_graph_updater)

        # animate for 8s
        self.play(UpdateFromAlphaFunc(photon_graph, lambda m, a: None), run_time=8)  # rely on updater
        self.wait(0.5)

        # -------------------------
        # 35–50 sec: Real-World Example — multiple colored wiggly waves + photons hopping
        # -------------------------
        waves = VGroup()
        wave_colors = [RED, GREEN, BLUE]
        wave_vertical_shifts = [0.0, -0.6, -1.2]  # to avoid overlap

        for i, color in enumerate(wave_colors):
            def make_wave(i=i, color=color):
                return always_redraw(lambda:
                    FunctionGraph(
                        lambda x: 0.35 * np.sin(3.2 * x + 2.0 * self.time + i * 0.9)
                                  + 0.06 * np.sin(12.0 * x + 1.6 * self.time + i),
                        x_range=[-6, 6],
                        stroke_width=3,
                        color=color
                    ).shift(DOWN * (1.2 + i * 0.8))
                )
            w = make_wave()
            waves.add(w)
            self.add(w)

        # photons hopping along these waves — stagger their starts to avoid overlap
        hopping_photons = VGroup()
        for i, w in enumerate(waves):
            p = Dot(radius=0.08, color=wave_colors[i]).move_to([-5.5, 0, 0])
            # position initially near start of its wave
            p.move_to(np.array([-5.5, 0.35 * np.sin(3.2 * -5.5 + i * 0.9) - (1.2 + i * 0.8), 0]))
            hopping_photons.add(p)
            # updater: hop across in ~4.5s but offset each by i*0.6s
            start_t = self.time + i * 0.6
            def make_updater(offset=start_t, idx=i):
                def updater(mob):
                    elapsed = self.time - offset
                    if elapsed < 0:
                        # not started yet
                        return
                    progress = min(max(elapsed / 4.5, 0.0), 1.0)
                    x = -5.5 + 11.0 * progress
                    y = 0.35 * np.sin(3.2 * x + 2.0 * self.time + idx * 0.9) + 0.06 * np.sin(12.0 * x + 1.6 * self.time + idx) - (1.2 + idx * 0.8)
                    mob.move_to([x, y, 0])
                return updater
            p.add_updater(make_updater())
            self.add(p)

        # Let the hopping animation run ~5s
        self.play(UpdateFromAlphaFunc(hopping_photons, lambda m, a: None), run_time=5.0)
        self.wait(0.5)

        # Background soft transition: fade tint stronger to indicate energy color shift
        tint_rect = FullScreenRectangle().set_fill(color=[PURPLE, ORANGE], opacity=0.12)
        self.play(FadeIn(tint_rect), run_time=1.0)
        self.wait(0.5)

        # -------------------------
        # 50–60 sec: Wrap-up — zoom out, all photons glow, equation fades in
        # -------------------------
        # Make all photons glow with a subtle halo (use Circles with low opacity and updaters)
        halos = VGroup()
        all_photons = VGroup(photon, photon_graph, *hopping_photons, glow)
        for p in all_photons:
            halo = Circle(radius=0.22, color=YELLOW, fill_opacity=0.18)
            halo.move_to(p.get_center())
            def make_halo_updater(h=halo, src=p):
                return lambda m: m.move_to(src.get_center())
            halo.add_updater(make_halo_updater())
            halos.add(halo)
            self.add(halo)

        # Final eq gently fades in with "hand-drawn" stroke (we'll write it again but faint)
        final_eq = MathTex("E", "=", "h", r"\nu", font_size=120, color=WHITE).set_opacity(0.0).to_edge(UP)
        self.add(final_eq)
        # fade and stroke-draw effect: reveal with increasing opacity
        self.play(final_eq.animate.set_opacity(1.0), run_time=1.4)

        # Camera: zoom out smoothly to show all content
        frame = self.camera.frame  # MovingCameraScene has .frame
        # scale out (zoom out) and slight upward pan to give a cinematic finish
        self.play(frame.animate.scale(1.25).shift(UP * 0.2), run_time=2.0, rate_func=smooth)
        self.wait(0.8)

        # final hold
        self.wait(1.0)
