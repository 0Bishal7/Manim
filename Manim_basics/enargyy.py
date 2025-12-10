from manim import *
import math
import random


class HandDrawnWaveScene(Scene):
    def construct(self):
        self.camera.background_color = "#050816"

        # --------------------------------------------------
        # 0–5 s: Hook – light as waves
        # --------------------------------------------------
        background = Rectangle(
            width=16,
            height=9,
            fill_color=BLUE_E,
            fill_opacity=0.7,
            stroke_width=0,
        ).set_z_index(-10)
        self.add(background)

        main_wave = self.get_handdrawn_wave(
            x_min=-7,
            x_max=7,
            amp=1.0,
            k=2 * PI / 6,
            roughness=0.12,
            color=interpolate_color(BLUE_D, PURPLE_D, 0.4),
            stroke_width=4,
        )

        photon = Dot(radius=0.12, color=YELLOW_B)
        glow = self.get_glow(photon, color=YELLOW, radius_scale=2.8, opacity=0.35)
        self.add(main_wave, glow, photon)

        def hook_motion_updater(mob, alpha):
            x = interpolate(-7, 7, alpha)
            y = self.sample_wave_y(main_wave, x)
            mob.move_to([x, y, 0])

        self.play(
            UpdateFromAlphaFunc(photon, hook_motion_updater),
            run_time=3.0,
            rate_func=linear,
        )
        self.wait(0.5)

        # --------------------------------------------------
        # 5–15 s: Equation introduction, wiggly photon path
        # --------------------------------------------------
        eq_tex = MathTex("E", "=", "h", r"\nu")
        eq_tex.scale(1.6)
        eq_tex.to_corner(UR).shift(0.3 * LEFT + 0.2 * DOWN)
        eq_tex.set_color_by_tex_to_color_map(
            {"E": YELLOW, "h": GREEN_B, r"\nu": RED_B}
        )
        self.play(Write(eq_tex, run_time=3.0, rate_func=smooth))

        wiggly_path = self.get_handdrawn_wave(
            x_min=-5,
            x_max=5,
            amp=0.6,
            k=2 * PI / 4,
            roughness=0.15,
            color=GRAY_D,
            stroke_width=2,
        ).shift(1.8 * DOWN)

        self.play(
            Transform(main_wave, wiggly_path),
            run_time=1.8,
            rate_func=smooth,
        )

        def photon_wiggly_updater(mob, alpha):
            point = wiggly_path.point_from_proportion(alpha)
            mob.move_to(point)
            energy_scale = 1.0 + 0.8 * alpha
            mob.set(width=0.18 * energy_scale)

        def glow_wiggly_updater(mob, alpha):
            new_glow = self.get_glow(
                photon,
                color=YELLOW,
                radius_scale=3.0,
                opacity=0.4,
            )
            mob.become(new_glow)

        self.play(
            UpdateFromAlphaFunc(photon, photon_wiggly_updater),
            UpdateFromAlphaFunc(glow, glow_wiggly_updater),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(0.5)

        # --------------------------------------------------
        # 15–35 s: Frequency vs Energy graph
        # --------------------------------------------------
        axes = self.get_handdrawn_axes()
        label_freq = Tex("Frequency").scale(0.6).next_to(axes.x_axis, RIGHT, buff=0.3)
        label_energy = Tex("Energy").scale(0.6).next_to(axes.y_axis, UP, buff=0.3)

        self.play(
            FadeOut(wiggly_path),
            main_wave.animate.fade(0.4),
            FadeIn(axes),
            FadeIn(label_freq),
            FadeIn(label_energy),
            run_time=1.8,
        )

        graph = self.get_handdrawn_curve(
            func=lambda x: 0.3 * x + 0.3 * math.sin(2 * x),
            x_min=0,
            x_max=4.5,
            color=YELLOW_C,
            stroke_width=4,
        )
        graph.shift(axes.get_origin())
        self.play(Create(graph, run_time=3.0, rate_func=smooth))

        graph_photon = Dot(radius=0.12, color=YELLOW_B)
        graph_glow = self.get_glow(graph_photon, color=YELLOW, radius_scale=2.6, opacity=0.35)
        self.add(graph_glow, graph_photon)

        def graph_photon_updater(mob, alpha):
            p = graph.point_from_proportion(alpha)
            mob.move_to(p)
            energy_scale = 1.0 + 0.7 * alpha
            mob.set(width=0.18 * energy_scale)

        def graph_glow_updater(mob, alpha):
            new_glow = self.get_glow(
                graph_photon,
                color=YELLOW,
                radius_scale=3.0,
                opacity=0.4,
            )
            mob.become(new_glow)

        dynamic_wave = self.get_handdrawn_wave(
            x_min=-7,
            x_max=7,
            amp=0.5,
            k=2 * PI / 6,
            roughness=0.1,
            color=BLUE_D,
            stroke_width=3,
        ).shift(2.3 * DOWN)
        self.play(FadeIn(dynamic_wave, shift=0.2 * UP), run_time=1.0)

        offset_tracker = ValueTracker(0.0)

        def dynamic_wave_updater(mob):
            dx = 0.2 * math.sin(2 * PI * offset_tracker.get_value())
            center = mob.get_center()
            mob.move_to([dx, center[1], 0])

        dynamic_wave.add_updater(dynamic_wave_updater)

        self.play(
            UpdateFromAlphaFunc(graph_photon, graph_photon_updater),
            UpdateFromAlphaFunc(graph_glow, graph_glow_updater),
            offset_tracker.animate.set_value(3.0),
            run_time=6.0,
            rate_func=smooth,
        )

        dynamic_wave.remove_updater(dynamic_wave_updater)
        self.wait(0.5)

        # --------------------------------------------------
        # 35–50 s: Real-world RGB example
        # --------------------------------------------------
        colors = [RED_B, GREEN_B, BLUE_B]
        offsets = [1.0, 0.0, -1.0]
        waves_rgb = VGroup()
        photons_rgb = VGroup()
        glows_rgb = VGroup()

        for col, off in zip(colors, offsets):
            w = self.get_handdrawn_wave(
                x_min=-7,
                x_max=7,
                amp=0.6,
                k=2 * PI / 5,
                roughness=0.14,
                color=col,
                stroke_width=4,
            ).shift(off * UP + 1.5 * DOWN)
            waves_rgb.add(w)

            p = Dot(radius=0.12, color=col)
            g = self.get_glow(p, color=col, radius_scale=2.8, opacity=0.35)
            photons_rgb.add(p)
            glows_rgb.add(g)

        self.play(
            FadeOut(graph_photon),
            FadeOut(graph_glow),
            FadeOut(graph),
            FadeOut(axes),
            FadeOut(label_freq),
            FadeOut(label_energy),
            FadeIn(waves_rgb, lag_ratio=0.15),
            run_time=2.0,
        )
        for p, g in zip(photons_rgb, glows_rgb):
            self.add(g, p)

        def make_hopping_updater(wave, phase_shift):
            def updater(mob, alpha):
                x = interpolate(-7, 7, alpha)
                y_base = self.sample_wave_y(wave, x)
                hop = 0.25 * math.sin(6 * PI * (alpha + phase_shift))
                mob.move_to([x, y_base + hop, 0])
            return updater

        rgb_animations = []
        for idx, (w, p, g, c) in enumerate(zip(waves_rgb, photons_rgb, glows_rgb, colors)):
            rgb_animations.append(
                UpdateFromAlphaFunc(p, make_hopping_updater(w, idx * 0.15))
            )

            def make_glow_func(photon, col):
                def glow_func(mob, alpha):
                    if col == BLUE_B:
                        factor = 1.2
                    elif col == GREEN_B:
                        factor = 1.0
                    else:
                        factor = 0.8
                    new_glow = self.get_glow(
                        photon,
                        color=col,
                        radius_scale=3.0 * factor,
                        opacity=0.25 + 0.15 * factor,
                    )
                    mob.become(new_glow)
                return glow_func

            rgb_animations.append(
                UpdateFromAlphaFunc(g, make_glow_func(p, c))
            )

        # No background_color.animate here anymore
        self.play(
            *rgb_animations,
            run_time=7.0,
            rate_func=smooth,
        )

        # --------------------------------------------------
        # 50–60 s: Wrap-up, zoom out, final equation
        # --------------------------------------------------
        all_elements = VGroup(
            background,
            main_wave,
            dynamic_wave,
            waves_rgb,
            photons_rgb,
            glows_rgb,
        )

        self.play(
            all_elements.animate.scale(0.85).shift(0.3 * DOWN),
            run_time=2.0,
        )

        final_eq = MathTex("E", "=", "h", r"\nu")
        final_eq.scale(2.0)
        final_eq.set_color_by_tex_to_color_map(
            {"E": YELLOW, "h": GREEN_B, r"\nu": RED_B}
        )
        final_eq.move_to(2.6 * UP)

        self.play(
            LaggedStart(
                *[Write(part, run_time=2.0, rate_func=smooth) for part in final_eq],
                lag_ratio=0.2,
            )
        )

        all_photons = VGroup(photon, *photons_rgb)
        self.play(
            *[p.animate.set(width=0.25).set_color(YELLOW_B) for p in all_photons],
            run_time=3.0,
        )

        self.wait(2.0)
        self.play(FadeOut(VGroup(all_elements, final_eq, all_photons)), run_time=2.0)

    # ------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------
    def get_handdrawn_wave(
        self,
        x_min=-7,
        x_max=7,
        amp=1.0,
        k=2 * PI / 6,
        roughness=0.1,
        color=BLUE_D,
        stroke_width=3,
    ):
        points = []
        n_samples = 400
        for i in range(n_samples + 1):
            x = interpolate(x_min, x_max, i / n_samples)
            y = amp * math.sin(k * x)
            jitter_y = roughness * (random.random() - 0.5)
            jitter_x = roughness * 0.4 * (random.random() - 0.5)
            points.append([x + jitter_x, y + jitter_y, 0])

        wave = VMobject(stroke_color=color, stroke_width=stroke_width)
        wave.set_points_smoothly(points)
        return wave

    def sample_wave_y(self, wave: VMobject, x_target: float) -> float:
        points = wave.get_points()
        best = min(points, key=lambda p: abs(p[0] - x_target))
        return best[1]

    def get_glow(self, anchor_mobject, color=YELLOW, radius_scale=3.0, opacity=0.35):
        r = anchor_mobject.width * radius_scale
        glow = Circle(
            radius=r,
            stroke_width=0,
            fill_color=color,
            fill_opacity=opacity,
        )
        glow.move_to(anchor_mobject.get_center())
        glow.set_z_index(anchor_mobject.get_z_index() - 1)
        return glow

    def get_handdrawn_axes(self):
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=5.5,
            y_length=3.2,
            tips=False,
            axis_config={
                "stroke_width": 3,
                "stroke_color": GREY_B,
            },
        ).move_to(ORIGIN + 1.3 * LEFT)

        for axis in [axes.x_axis, axes.y_axis]:
            pts = axis.get_points()
            jittered = []
            for p in pts:
                jittered.append(
                    [
                        p[0] + 0.03 * (random.random() - 0.5),
                        p[1] + 0.03 * (random.random() - 0.5),
                        0,
                    ]
                )
            rough_axis = VMobject(
                stroke_color=axis.get_color(),
                stroke_width=axis.get_stroke_width(),
            )
            rough_axis.set_points_smoothly(jittered)
            self.add(rough_axis)
            axis.set_opacity(0)
        return axes

    def get_handdrawn_curve(
        self,
        func,
        x_min=0,
        x_max=4,
        color=YELLOW,
        stroke_width=4,
        samples=200,
    ):
        pts = []
        for i in range(samples + 1):
            x = interpolate(x_min, x_max, i / samples)
            y = func(x)
            jitter = 0.05 * (random.random() - 0.5)
            pts.append([x, y + jitter, 0])

        curve = VMobject(
            stroke_color=color,
            stroke_width=stroke_width,
        )
        curve.set_points_smoothly(pts)
        return curve
