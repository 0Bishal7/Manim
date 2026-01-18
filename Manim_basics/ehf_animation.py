from manim import *
import numpy as np


class EHFAnimation(Scene):
    def construct(self):
        # Title
        title = Text("E = h f", font_size=64, color=BLUE)
        subtitle = Text("Energy of a Photon", font_size=32, color=WHITE).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Key variables
        eq = MathTex(r"E = h f", font_size=72, color=YELLOW)
        self.play(ReplacementTransform(title, eq), FadeOut(subtitle))
        self.wait(2)
  
          # Move equation up a bit
        self.play(eq.animate.shift(UP*1.0), run_time=0.8)

        # Typewriter-style explanation lines
        #typewriter_font = "Courier New"  # or another monospaced font installed on your system

        #lines = [
        #    "Energy & Frequency: The formula",
        #    "E = h/nu shows a direct relationship:",
        #    "double the frequency, double the energy.",
        #    "Planck's Law explains the particle nature of light"
        #]

        #text_mobjects = VGroup(
        #    *[
        #        Text(
        #            line,
        #            font=typewriter_font,
        #            font_size=20
        #        )
        #        for line in lines
        #    ]
        #).arrange(DOWN, aligned_edge= ORIGIN, buff=0.12)

        #text_mobjects.next_to(eq, DOWN, buff=0.6)

        # Typewriter-style: write one line after another
        #for line_text in text_mobjects:
        #    self.play(Write(line_text), run_time=1.0)
        #    self.wait(0.2)

        #self.wait(2)
        #self.play(FadeOut(text_mobjects))

              # Photoelectric effect sketch (photon hits top surface, electron ejects)


        # ---------------- Light as particles vs waves ----------------


# Two lamps on left and right

# Left lamp
        lamp_left = RoundedRectangle(
            corner_radius=0.2,
            width=0.8,
            height=1.2,
            color=PINK,
            fill_opacity=1,
        )
        lamp_left.to_edge(UP).shift(LEFT*3)

        lamp_left_head = Circle(
            radius=0.35,
            color=YELLOW,
            fill_opacity=1,
        ).next_to(lamp_left, DOWN, buff=-0.1)

        # Right lamp (copy and shift to the other side)
        lamp_right = lamp_left.copy().shift(RIGHT*6)
        lamp_right_head = lamp_left_head.copy().shift(RIGHT*6)

        # Optional labels
        label_left = Text("LIGHT SOURCE", font_size=19).next_to(lamp_left, RIGHT, buff=0.2)
        label_right = label_left.copy().shift(RIGHT*6)

        # Show both lamps
        self.play(
            FadeIn(lamp_left), FadeIn(lamp_left_head),
            FadeIn(lamp_right), FadeIn(lamp_right_head),
            Write(label_left), Write(label_right),
            run_time=1
        )


        # Frustum-shaped light beams from both lamps
# Left beam (frustum)
        left_top = lamp_left_head.get_center() + DOWN*0.1
        left_bottom_y = left_top[1] - 4  # beam length

        top_left_left  = left_top + LEFT*0.4
        top_right_left = left_top + RIGHT*0.4
        bottom_left_left  = left_top + LEFT*1.5 + (left_bottom_y - left_top[1]) * UP * 0 + DOWN*4
        bottom_right_left = left_top + RIGHT*1.5 + (left_bottom_y - left_top[1]) * UP * 0 + DOWN*4

        beam_left = Polygon(
            top_left_left,
            top_right_left,
            bottom_right_left,
            bottom_left_left,
            color=YELLOW,
            fill_opacity=0.15,
            stroke_width=0,
        )

        # Right beam (mirror of left)
        right_top = lamp_right_head.get_center() + DOWN*0.1
        right_bottom_y = right_top[1] - 4

        top_left_right  = right_top + LEFT*0.4
        top_right_right = right_top + RIGHT*0.4
        bottom_left_right  = right_top + LEFT*1.5 + DOWN*4
        bottom_right_right = right_top + RIGHT*1.5 + DOWN*4

        beam_right = Polygon(
            top_left_right,
            top_right_right,
            bottom_right_right,
            bottom_left_right,
            color=YELLOW,
            fill_opacity=0.15,
            stroke_width=0,
        )

        self.play(FadeIn(beam_left), FadeIn(beam_right), run_time=1)


        # Dimensions for barriers: cover right half of each frustum
        barrier_height = 1.3   # adjust to taste
        barrier_width_factor = 0.5  # half of beam width

        # LEFT barrier (on right half of left frustum)
        left_beam_bottom = beam_left.get_vertices()[2:]  # bottom edge approx
        left_bottom_y = min(v[1] for v in left_beam_bottom)
        left_top_y = beam_left.get_top()[1]

        left_center_x = (beam_left.get_right()[0] + beam_left.get_center()[0]) / 2
        left_barrier = Rectangle(
            width=(beam_left.get_right()[0] - beam_left.get_center()[0]) * 2 * barrier_width_factor,
            height=barrier_height,
            color=GREEN,
            fill_opacity=0.9,
        ).move_to([
            left_center_x,
            left_top_y - barrier_height/2 - 3,   # sits inside upper half of frustum
            0
        ])

        left_barrier_label = Text("BARRIER", font_size=24, color=WHITE).move_to(left_barrier.get_center())

                # Show lamps and beams
        #self.play(
        #    FadeIn(lamp_left), FadeIn(lamp_left_head),
        #    FadeIn(lamp_right), FadeIn(lamp_right_head),
        #    FadeIn(beam_left), FadeIn(beam_right),
        #    run_time=1
        #)

        # RIGHT barrier (mirror on right frustum)
        right_beam_bottom = beam_right.get_vertices()[2:]
        right_bottom_y = min(v[1] for v in right_beam_bottom)
        right_top_y = beam_right.get_top()[1]

        right_center_x = (beam_right.get_right()[0] + beam_right.get_center()[0]) / 2
        right_barrier = Rectangle(
            width=(beam_right.get_right()[0] - beam_right.get_center()[0]) * 2 * barrier_width_factor,
            height=barrier_height,
            color=GREEN,
            fill_opacity=0.9,
        ).move_to([
            right_center_x,
            right_top_y - barrier_height/2 - 3,
            0
        ])

        right_barrier_label = Text("BARRIER", font_size=24, color=WHITE).move_to(right_barrier.get_center())

        # Show barriers on top of beams
        self.play(
            FadeIn(left_barrier), FadeIn(right_barrier),
            Write(left_barrier_label), Write(right_barrier_label),
            run_time=1
        )

        # Show barriers BEFORE particles
        #self.play(
        #    FadeIn(left_barrier), FadeIn(right_barrier),
        #    Write(left_barrier_label), Write(right_barrier_label),
        #    run_time=1
        #)
        self.wait(0.5)  # small pause so students can see the barriers

               # ---------- PARTICLE FLOW FROM LEFT LAMP: diverging from mouth ----------

        particle_dots = VGroup()
        animations = []

        # Geometry
        beam_verts = beam_left.get_vertices()  # [top-left, top-right, bottom-right, bottom-left]
        top_left, top_right, bottom_right, bottom_left = beam_verts

        lamp_mouth = lamp_left_head.get_center()

        # y of the frustum base
        base_y = min(bottom_left[1], bottom_right[1])

        barrier_top_y   = left_barrier.get_top()[1]
        barrier_left_x  = left_barrier.get_left()[0]
        barrier_right_x = left_barrier.get_right()[0]

        # pick several TARGET points along the base of the frustum
        x_targets = np.linspace(bottom_left[0] + 0.05, bottom_right[0] - 0.05, 9)

        for x in x_targets:
            # full path from lamp mouth to base point (diverging)
            full_end = np.array([x, base_y, 0.0])

            # if this ray passes under the barrier, cut it at barrier top
            if barrier_left_x <= x <= barrier_right_x:
                cut_y = barrier_top_y
                ray_dir = full_end - lamp_mouth
                if ray_dir[1] != 0:
                    t_cut = (cut_y - lamp_mouth[1]) / ray_dir[1]
                    t_cut = max(0.0, min(1.0, t_cut))
                    end_pos = lamp_mouth + t_cut * ray_dir
                else:
                    end_pos = full_end
            else:
                end_pos = full_end

            start_pos = lamp_mouth

            # create several dots along that ray, all starting at the mouth
            n_dots = 6
            for t in np.linspace(0.1, 1.0, n_dots):
                dot_start = start_pos
                dot_end   = start_pos + t * (end_pos - start_pos)

                dot = Dot(dot_start, radius=0.05, color=YELLOW)
                particle_dots.add(dot)
                animations.append(dot.animate.move_to(dot_end))

        self.add(particle_dots)
        self.play(LaggedStart(*animations, lag_ratio=0.03, run_time=2))

        # ------------ WAVEFRONTS FROM RIGHT LAMP ------------

        wave_group = VGroup()

        source = lamp_right_head.get_center()

        # Frustum geometry
        v0, v1, v2, v3 = beam_right.get_vertices()
        frustum_left_x  = min(v0[0], v3[0])
        frustum_right_x = max(v1[0], v2[0])
        base_y          = min(v2[1], v3[1])

        # Barrier geometry
        b_left_x  = right_barrier.get_left()[0]
        b_right_x = right_barrier.get_right()[0]
        b_top_y   = right_barrier.get_top()[1]
        b_bottom_y = right_barrier.get_bottom()[1]

        # Parameters controlling look
        n_waves      = 10          # how many semicircular fronts
        max_radius   = abs(base_y - source[1]) * 1.2
        wave_spacing = max_radius / n_waves

        for k in range(1, n_waves + 1):
            R = k * wave_spacing

            # sample a semicircle centred at source, opening downward
            theta_vals = np.linspace(-0.65*np.pi, -0.35*np.pi, 120)  # tweak to match frustum angle
            pts = []
            for theta in theta_vals:
                x = source[0] + R * np.cos(theta)
                y = source[1] + R * np.sin(theta)
                p = np.array([x, y, 0])

                # clip to frustum
                if x < frustum_left_x or x > frustum_right_x or y < base_y:
                    continue

                # cut out the barrier region (waves stop there, do NOT go around)
                if b_left_x <= x <= b_right_x and b_bottom_y <= y <= b_top_y:
                    continue

                pts.append(p)

            if len(pts) < 2:
                continue

            wave = VMobject(stroke_color=YELLOW_C, stroke_width=6, stroke_opacity=0.9)
            wave.set_points_as_corners(pts)
            wave_group.add(wave)

        # animate wavefronts appearing one after another from lamp
        for i, wave in enumerate(wave_group):
            wave.set_opacity(0)
            self.add(wave)
            self.play(wave.animate.set_opacity(1), run_time=0.15)
        self.wait(1.5)

        # ---- END OF LIGHT AS PARTICLES VS WAVES SECTION ----
        light_scene = VGroup(
            lamp_left, lamp_left_head, lamp_right, lamp_right_head,
            label_left, label_right,
            beam_left, beam_right,
            left_barrier, right_barrier,
            left_barrier_label, right_barrier_label,
            particle_dots, wave_group
        )

        self.play(FadeOut(light_scene), run_time=1.2)
        self.wait(0.5)






        # Metal block (like your image)
        metal = Rectangle(
            width=5,
            height=1.5,
            color=PURPLE,
            stroke_width=4,
            fill_opacity=0.1,
        ).shift(DOWN*0.5)

        # Electrons inside metal
        electron_dots = VGroup(
            *[
                Dot(color=ORANGE, radius=0.07).move_to(
                    metal.get_center()
                    + RIGHT * x
                    + UP * y
                )
                for x, y in [
                    (-1.8, 0.3), (-1.2, -0.2), (-0.6, 0.1),
                    (0.0, -0.3), (0.6, 0.2), (1.2, -0.1), (1.8, 0.25)
                ]
            ]
        )

        metal_label = Text("Metal", font_size=28, color=WHITE).next_to(metal, DOWN)

        self.play(FadeOut(eq), Create(metal), FadeIn(electron_dots), Write(metal_label))
        self.wait(1)

        # Choose one surface electron that will be emitted
        surface_electron = Dot(color=ORANGE, radius=0.09).move_to(
            metal.get_top() + LEFT*0.5 + DOWN*0.05
        )
        self.play(FadeIn(surface_electron), run_time=0.3)

        # Photon coming straight down from above onto top surface
        photon_path_start = surface_electron.get_center() + UP*2.5
        photon_path_end   = surface_electron.get_center() + UP*0.15

        # A wavy photon centered on this straight-down path
        def photon_curve(t):
            # t in [0, 1]
            x = photon_path_start[0] + 0.0                      # vertical path only
            y = photon_path_start[1] + (photon_path_end[1] - photon_path_start[1]) * t
            y += 0.2 * np.sin(10 * t * TAU)                     # small wiggle, no penetration
            return np.array([x, y, 0])

        photon = ParametricFunction(
            photon_curve,
            t_range=[0, 1, 0.02],
            color=YELLOW,
            stroke_width=6,
        )

        photon_label = Text("Photon", font_size=24, color=YELLOW).next_to(
            photon_path_start, LEFT
        )

        self.play(Create(photon), Write(photon_label), run_time=1.5)
        self.wait(0.3)

        # Photon shrinks/disappears exactly at the top surface
        self.play(
            photon.animate.scale(0.2).move_to(photon_path_end),
            run_time=0.4,
        )
        self.play(FadeOut(photon), FadeOut(photon_label), run_time=0.2)

        # Electron ejection: same point, moves out above surface
        emitted_electron = surface_electron.copy().set_color(ORANGE)
        emitted_path = emitted_electron.get_center() + UP*2 + RIGHT*0.7

        emitted_label = Text("Emitted electron", font_size=24, color=ORANGE).next_to(
            emitted_path, RIGHT
        )

        self.play(
            emitted_electron.animate.move_to(emitted_path),
            run_time=1.2,
            rate_func=smooth,
        )
        self.play(Write(emitted_label), run_time=0.5)
        self.wait(0.5)

        # Optional: fade the whole photoelectric illustration before moving on
        self.play(
            FadeOut(VGroup(
                metal, electron_dots, metal_label,
                surface_electron, emitted_electron, emitted_label
            )),
            run_time=0.8,
        )


        # Define variables with colors
       # Create variables with proper spacing
        e_tex = MathTex(r"E", color=RED, font_size=48)
        h_tex = MathTex(r"h", color=GREEN, font_size=48)
        f_tex = MathTex(r"f", color=BLUE, font_size=48)

        vars_group = VGroup(e_tex, h_tex, f_tex).arrange(RIGHT, buff=1.5)
 
        labels = VGroup(
                Text("Energy", color=RED, font_size=15).next_to(vars_group[0], DOWN, buff=0.5),
                Text("Planck's Constant", color=GREEN, font_size=15).next_to(vars_group[1], DOWN, buff=0.5),
                Text("Frequency", color=BLUE, font_size=15).next_to(vars_group[2], DOWN, buff=0.5)
                )

        
        self.play(
          TransformFromCopy(e_tex, vars_group[0]), 
          TransformFromCopy(h_tex, vars_group[1]), 
          TransformFromCopy(f_tex, vars_group[2]))
        self.play(Write(labels))
        self.wait(1.5)
        # Graph setup - E vs f linear relationship
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE},
            tips=False
        ).shift(DOWN*0.5)
        
        # Replace the broken axes label section with this:
        x_label = MathTex(r"f", color=BLUE, font_size=36).next_to(axes.x_axis.get_end(), RIGHT, buff=0.1)
        y_label = MathTex(r"E", color=RED, font_size=36).next_to(axes.y_axis.get_end(), UP, buff=0.1)
        h_label = Text("E = h f", font_size=32, color=YELLOW).next_to(axes, UR, buff=0.2)

        self.play(
            FadeOut(VGroup(*vars_group, *labels)),
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(h_label)
        )

        # Animate h value (slope)
        h_text = MathTex(r"h = 6.626 \times 10^{-34}", font_size=28, color=GREEN).to_edge(UL)
        
        # Fixed slope line (h=1 for visualization)
        line = axes.plot(lambda x: x, color=YELLOW, stroke_width=6)
        self.play(Write(h_text), Create(line))
        
        # Animate frequency points
        dots = VGroup()
        for f in [2, 4, 6, 8]:
            dot = Dot(axes.coords_to_point(f, f), color=BLUE, radius=0.08)
            energy_text = MathTex(rf"E = {f}", color=RED, font_size=24).next_to(dot, RIGHT)
            dots.add(dot)
            self.play(Create(dot), Write(energy_text), run_time=0.5)
            self.wait(0.3)

        # Higher f → Higher E label. 
        photon_label = Text("Higher f → Higher E", font_size=24, color=WHITE).next_to(axes, UP, buff=0.5)
        self.play(Write(photon_label), run_time=2)
        self.wait(1)

        # Final equation with graph
        final_eq = MathTex(r"E = h f", font_size=96, color=YELLOW).to_edge(UP)
        self.play(Transform(h_label, final_eq))
        self.wait(2)

        all_objects = Group(*self.mobjects)
        self.play(FadeOut(all_objects), run_time=1)
        #self.play(
         #  FadeOut(VGroup(axes, line, dots, photon_label, h_text, final_eq, energy_text, x_label, y_label)),  # No photon_wave
          # run_time=1
        #)
        
        # Closing message
        conclusion = Text("Photon Energy ∝ Frequency", font_size=48, color=BLUE)
        end = Text("Higher Frequency → Higher Photon Energy", font_size=36)
        
        end.next_to(conclusion, DOWN, buff=0.3)  # adjust buff for spacing

        self.play(Write(conclusion))
        
        self.play(Write(end))
        self.wait(2)
        self.play(FadeOut(conclusion), run_time=1)
        
        self.play(FadeOut(end), run_time=1)


               # After: self.play(FadeOut(conclusion), run_time=1)

        # ---------------- Light as particles vs waves ----------------


# Two lamps on left and right

# Left lamp


        # Final thank-you message
        thanks = Text("Thank you for watching :)", font_size=40, color=YELLOW)
        thanks.to_edge(DOWN)  # or .move_to(ORIGIN) if you prefer centered

        self.play(Write(thanks), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(thanks), run_time=1)
        