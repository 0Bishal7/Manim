
# from manim import *
# import numpy as np

# # Combined 2-minute video: each segment duration sums to 120s
# class CombinedVideo(Scene):
#     def construct(self):
#         # ----------------------
#         # 1) Matrix label (8s)
#         # ----------------------
#         matrix_txt = Text("A = [[1, 2], [2, 1]]").to_edge(UL).scale(0.8).add_background_rectangle()
#         self.play(FadeIn(matrix_txt), run_time=1.2)
#         self.wait(6.8)  # overall ~8s including animation
#         self.play(matrix_txt.animate.to_edge(UL), run_time=0.2)

#         # ----------------------
#         # 2) Determinant (6s)
#         # ----------------------
#         det_val = np.round(np.linalg.det(np.array([[1, 2], [2, 1]])), 3)
#         det_txt = Text(f"det(A) = {det_val}").scale(0.9)
#         self.play(Write(det_txt), run_time=1.0)
#         self.wait(5.0)
#         self.play(FadeOut(det_txt), run_time=0.5)

#         # ----------------------
#         # 3) Unit square (8s)
#         # ----------------------
#         unit_sq = Square(side_length=1.0).set_fill(BLUE_E, opacity=0.5)
#         unit_sq.move_to(ORIGIN)
#         unit_label = Text("Unit square").scale(0.6).next_to(unit_sq, UP, buff=0.2)
#         self.play(DrawBorderThenFill(unit_sq), Write(unit_label), run_time=1.2)
#         self.wait(6.8)
#         self.play(FadeOut(unit_label), run_time=0.4)

#         # ----------------------
#         # 4) Apply matrix to square (16s)
#         # ----------------------
#         A = np.array([[1, 2], [2, 1]])
#         # create transformable polygon (unit square)
#         # use unit_sq vertices for consistency
#         verts = unit_sq.get_vertices()
#         # Polygon expects points in correct order; ensure we pass them
#         square = Polygon(*verts, fill_opacity=0.6, fill_color=BLUE_D)
#         square.move_to(ORIGIN)
#         square.set_z_index(0)
#         self.add(square)
#         # compute transformed points (apply A to each vertex)
#         pts = [np.array([v[0], v[1]]) for v in verts]
#         transformed = [np.array([*(A.dot(p)), 0.0]) for p in pts]
#         target_polygon = Polygon(*transformed, fill_opacity=0.6, fill_color=BLUE_D)

#         # animate morph to the transformed polygon
#         self.play(Transform(square, target_polygon), run_time=4.0)

#         # -----------------------------------------
#         # Instead of camera.frame (which is variant),
#         # scale the transformed polygon to mimic zoom
#         # -----------------------------------------
#         self.play(square.animate.scale(1.6), run_time=1.0)  # zoom-in effect
#         self.wait(11.0)  # pause to inspect transform (~16s total including anims)
#         self.play(square.animate.scale(1/1.6), run_time=0.6)  # zoom-out: restore original visual scale

#         self.play(FadeOut(square), run_time=0.6)

#         # ----------------------
#         # 5) Transform vector and shapes (12s)
#         # ----------------------
#         vect = Arrow(ORIGIN, np.array([1, -2, 0]), buff=0).set_color(PURPLE_B)
#         v_label = Text("v = (1, -2)").scale(0.6).next_to(vect.get_end(), RIGHT, buff=0.1).set_color(PURPLE_B)
#         rect = Rectangle(height=1.6, width=0.9, fill_opacity=0.6).shift(UP * 2 + LEFT * 2)
#         circ = Circle(radius=0.9, fill_opacity=0.6).shift(DOWN * 2 + RIGHT * 1)
#         self.play(GrowFromCenter(vect), Write(v_label), DrawBorderThenFill(rect), Create(circ), run_time=2.0)
#         self.wait(1.0)

#         # simulate transform by scaling/rotating these shapes (visual proxy for ApplyMatrix)
#         # Note: apply_matrix exists on mobjects; using it visually here is fine
#         self.play(
#             vect.animate.shift(RIGHT * 1.5 + UP * 0.4).scale(1.0).rotate(0.2),
#             rect.animate.apply_matrix(np.array([[1, 2],[2,1]])).shift(LEFT*0.2),
#             circ.animate.apply_matrix(np.array([[1, 2],[2,1]])).shift(RIGHT*0.4),
#             run_time=3.2
#         )
#         self.wait(6.8)  # completes ~12s block
#         self.play(FadeOut(vect), FadeOut(v_label), FadeOut(rect), FadeOut(circ), run_time=0.8)

#         # ----------------------
#         # 6) Plane reveal (6s)
#         # ----------------------
#         plane = NumberPlane()
#         # do NOT call plane.add_coordinates() to stay LaTeX-free
#         self.play(Create(plane), run_time=1.0)
#         self.wait(5.0)
#         self.play(FadeOut(plane), run_time=0.6)

#         # ----------------------
#         # 7) Vector v1 (9s)
#         # ----------------------
#         v1 = Arrow(ORIGIN, LEFT * 3 + DOWN * 2, buff=0).set_color(YELLOW)
#         v1_label = Text("v").scale(0.6).next_to(v1.get_end(), RIGHT, buff=0.1).set_color(YELLOW)
#         self.play(GrowFromCenter(v1), Write(v1_label), run_time=1.2)
#         self.wait(7.8)
#         self.play(FadeOut(v1), FadeOut(v1_label), run_time=0.6)

#         # ----------------------
#         # 8) Vector v2 (9s)
#         # ----------------------
#         v2 = Arrow(ORIGIN, RIGHT * 2 + UP * 2, buff=0).set_color(GREEN)
#         v2_label = Text("w").scale(0.6).next_to(v2.get_end(), UP, buff=0.1).set_color(GREEN)
#         self.play(GrowFromCenter(v2), Write(v2_label), run_time=1.2)
#         self.wait(7.8)
#         self.play(FadeOut(v2), FadeOut(v2_label), run_time=0.6)

#         # ----------------------
#         # 9) Vector sum (10s)
#         # ----------------------
#         plane2 = NumberPlane()
#         self.add(plane2)
#         p_origin = plane2.coords_to_point(0, 0)
#         p_v_plus_w = plane2.coords_to_point(1, 3)
#         sum_arrow = Arrow(p_origin, p_v_plus_w, buff=0).set_color(GREEN)
#         sum_label = Text("v + w").scale(0.6).next_to(sum_arrow.get_end(), LEFT, buff=0.1).set_color(GREEN)
#         self.play(Create(sum_arrow), Write(sum_label), run_time=1.6)
#         self.wait(8.4)
#         self.play(FadeOut(sum_arrow), FadeOut(sum_label), FadeOut(plane2), run_time=0.6)

#         # ----------------------
#         # 10) Code block (8s)
#         # ----------------------
#         # 10) Code block (8s) — minimal args for maximum compatibility
#         # 10) Code block fallback (8s) — no external file required
#         code = Text("See: Tute3Vectors.py").to_edge(UL).scale(0.7).add_background_rectangle()
#         self.play(Write(code), run_time=1.6)
#         self.wait(6.0)
#         self.play(FadeOut(code, shift=UP*0.4), run_time=0.6)

        

#         # code = Code(
#         #     "Tute3Vectors.py",
#         #     language="python",
#         #     background="window",
#         #     insert_line_no=True,
#         #     font="Monospace",
#         #     tab_width=4,
#         # ).set_width(8).to_edge(UL)

#         # code = Code(
#         #     "Tute3Vectors.py",
#         #     style="monokai",
#         #     language="python",
#         #     background="window",
#         #     insert_line_no=True,
#         #     font="Monospace",
#         # ).set_width(8).to_edge(UL)
#         self.play(Write(code), run_time=1.6)
#         self.wait(6.0)
#         self.play(FadeOut(code, shift=UP*0.4), run_time=0.6)

#         # ----------------------
#         # 11) Rectangle (8s)
#         # ----------------------
#         r = Rectangle(height=1.6, width=0.9, fill_opacity=0.6)
#         r_label = Text("Rectangle").scale(0.7).next_to(r, UP, buff=0.2)
#         self.play(DrawBorderThenFill(r), Write(r_label), run_time=1.2)
#         self.wait(6.2)
#         self.play(FadeOut(r), FadeOut(r_label), run_time=0.6)

#         # ----------------------
#         # 12) Circle (8s)
#         # ----------------------
#         c = Circle(radius=0.9, fill_opacity=0.6)
#         c_label = Text("Circle").scale(0.7).next_to(c, DOWN, buff=0.2)
#         self.play(Create(c), Write(c_label), run_time=1.2)
#         self.wait(6.2)
#         self.play(FadeOut(c), FadeOut(c_label), run_time=0.6)

#         # ----------------------
#         # 13) Summary & outro (12s)
#         # ----------------------
#         summary_box = RoundedRectangle(height=2.2, width=7.0, corner_radius=0.2, stroke_color=WHITE)
#         summary_lines = VGroup(
#             Text("What we saw:", weight=BOLD).scale(0.7),
#             Text("- Matrix transforms shapes and vectors").scale(0.6),
#             Text("- Determinant = area scaling factor").scale(0.6),
#             Text("- Vector addition via tip-to-tail").scale(0.6),
#         ).arrange(DOWN, aligned_edge=LEFT)
#         summary_group = VGroup(summary_box, summary_lines).arrange(UP, buff=0.5)
#         summary_group.move_to(ORIGIN)
#         self.play(DrawBorderThenFill(summary_box), FadeIn(summary_lines, shift=UP*0.3), run_time=1.4)
#         self.wait(10.6)

#         # End with a short fade-out
#         self.play(FadeOut(summary_group), run_time=1.0)
#         self.wait(0.6)
from manim_imports_ext import *
from _2025.laplace.shm import ShowFamilyOfComplexSolutions


S_COLOR = YELLOW
T_COLOR = BLUE


def get_exp_graph_icon(s, t_range=(0, 7), y_max=4, pos_real_scalar=0.1, neg_real_scalar=0.2, width=1, height=1):
    axes = Axes(
        t_range,
        (-y_max, y_max),
        width=width,
        height=height,
        axis_config=dict(tick_size=0.035, stroke_width=1)
    )
    scalar = pos_real_scalar if s.real > 0 else neg_real_scalar
    new_s = complex(s.real * scalar, s.imag)
    graph = axes.get_graph(lambda t: np.exp(new_s * t).real)
    graph.set_stroke(YELLOW, 2)
    rect = SurroundingRectangle(axes)
    rect.set_fill(BLACK, 1)
    rect.set_stroke(WHITE, 1)
    return VGroup(rect, axes, graph)


class IntroduceEulersFormula(InteractiveScene):
    def construct(self):
        # Add plane
        plane = ComplexPlane(
            (-2, 2), (-2, 2),
            width=6, height=6,
        )
        plane.background_lines.set_stroke(BLUE, 1)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.5)
        plane.to_edge(LEFT)

        plane.add_coordinate_labels([1, -1])
        i_labels = VGroup(
            Tex(R"i", font_size=36).next_to(plane.n2p(1j), UL, SMALL_BUFF),
            Tex(R"-i", font_size=36).next_to(plane.n2p(-1j), DL, SMALL_BUFF),
        )
        plane.add(i_labels)

        self.add(plane)

        # Show pi
        pi_color = RED
        arc = Arc(0, PI, radius=plane.x_axis.get_unit_size(), arc_center=plane.n2p(0))
        arc.set_stroke(pi_color, 5)
        t_tracker = ValueTracker(0)
        t_dec = DecimalNumber(0)
        t_dec.set_color(pi_color)
        t_dec.add_updater(lambda m: m.set_value(t_tracker.get_value()))
        t_dec.add_updater(lambda m: m.move_to(plane.n2p(1.3 * np.exp(0.9 * t_tracker.get_value() * 1j))))

        pi = Tex(R"\pi", font_size=72)
        pi.set_color(pi_color)
        pi.set_backstroke(BLACK, 3)

        self.play(
            ShowCreation(arc),
            t_tracker.animate.set_value(PI),
            VFadeIn(t_dec, time_span=(0, 1)),
            run_time=2
        )
        pi.move_to(t_dec, DR)
        self.play(
            FadeOut(t_dec),
            FadeIn(pi),
            run_time=0.5
        )

        # Write formula
        formula = Tex(R"e^{\pi i} = -1", font_size=90, t2c={R"\pi": RED, "i": BLUE})
        formula.set_x(FRAME_WIDTH / 4).to_edge(UP)
        cliche = Text("Cliché?", font_size=72)
        cliche.next_to(formula, DOWN, LARGE_BUFF)

        randy = Randolph(height=2)
        randy.next_to(plane, RIGHT, LARGE_BUFF, aligned_edge=DOWN)
        randy.body.set_backstroke(BLACK)

        self.play(LaggedStart(
            TransformFromCopy(pi, formula[R"\pi"][0]),
            FadeTransform(i_labels[0].copy(), formula["i"][0]),
            Write(formula["="][0]),
            TransformFromCopy(plane.coordinate_labels[1], formula["-1"][0]),
            Write(formula["e"][0]),
            lag_ratio=0.2,
            run_time=3
        ))
        self.wait()

        self.play(
            LaggedStart(
                *(
                    # TransformFromCopy(formula[c1][0], cliche[c2][0])
                    FadeTransform(formula[c1][0].copy(), cliche[c2][0])
                    for c1, c2 in zip(
                        ["e", "1", "i", "e", R"\pi", "e", "1"],
                        "Cliché?",
                    )
                ),
                lag_ratio=0.1,
                run_time=3
            ),
            VFadeIn(randy),
            randy.says("This again?", mode="sassy", bubble_direction=LEFT)
        )
        self.play(Blink(randy))
        self.add(cliche)

        # Show many thumbnails
        plane_group = VGroup(plane, arc, pi)
        plane_group.set_z_index(-1)
        thumbnails = Group(
            Group(ImageMobject(f"https://img.youtube.com/vi/{slug}/maxresdefault.jpg"))
            for slug in [
                "-dhHrg-KbJ0",  # Mathologer
                "f8CXG7dS-D0",  # Welch Labs
                "ZxYOEwM6Wbk",  # 3b1b
                "LE2uwd9V5vw",  # Khan Academy
                "CRj-sbi2i2I",  # Numberphile
                "v0YEaeIClKY",  # Other 3b1b
                "sKtloBAuP74",
                "IUTGFQpKaPU",  # Po shen lo
            ]
        )
        thumbnails.set_width(4)
        thumbnails.arrange(DOWN, buff=-0.8)
        thumbnails[4:].align_to(thumbnails, UP).shift(0.5 * DOWN)
        thumbnails.to_corner(UL)
        for n, tn in enumerate(thumbnails):
            tn.add_to_back(SurroundingRectangle(tn, buff=0).set_stroke(WHITE, 1))
            tn.shift(0.4 * n * RIGHT)

        self.play(
            FadeOut(randy.bubble, time_span=(0, 1)),
            randy.change("raise_left_hand", thumbnails).set_anim_args(time_span=(0, 1)),
            plane_group.animate.set_width(3.5).next_to(formula, DOWN, MED_LARGE_BUFF).set_anim_args(time_span=(0, 2)),
            FadeOut(cliche, 3 * RIGHT, lag_ratio=-0.02, time_span=(0.5, 2.0)),
            LaggedStartMap(FadeIn, thumbnails, shift=UP, lag_ratio=0.5),
            run_time=3
        )

        # Fail to explain
        thumbnails.generate_target()
        for tn, vect in zip(thumbnails.target, compass_directions(len(thumbnails))):
            vect[0] *= 1.5
            tn.set_height(1.75)
            tn.move_to(3 * vect)

        formula.generate_target()
        q_marks = Tex(R"???", font_size=90)
        VGroup(formula.target, q_marks).arrange(DOWN, buff=MED_LARGE_BUFF).center()

        self.play(
            MoveToTarget(thumbnails, lag_ratio=0.01, run_time=2),
            FadeOut(randy, DOWN),
            FadeOut(plane_group, DOWN),
            MoveToTarget(formula),
            Write(q_marks)
        )
        self.wait()
        self.play(LaggedStartMap(FadeOut, thumbnails, shift=DOWN, lag_ratio=0.5, run_time=4))
        self.wait()

        # Show constant meanings
        e_copy = formula["e"][0].copy()

        circle = Circle(radius=1)
        circle.to_edge(UP, buff=LARGE_BUFF)
        circle.set_stroke(WHITE, 1)
        arc = circle.copy().pointwise_become_partial(circle, 0, 0.5)
        arc.set_stroke(pi_color, 5)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_stroke(WHITE, 1)
        radius_label = Tex(R"1", font_size=24)
        radius_label.next_to(radius, DOWN, SMALL_BUFF)
        pi_label = Tex(R"\pi").set_color(pi_color)
        pi_label.next_to(circle, UP, buff=SMALL_BUFF)
        circle_group = VGroup(circle, arc, radius_label, radius, pi_label)

        i_eq = Tex(R"i^2 = -1", t2c={"i": BLUE}, font_size=90)
        i_eq.move_to(circle).set_x(5)

        self.play(
            formula.animate.shift(DOWN),
            FadeOut(e_copy, 3 * UP + 5 * LEFT),
            FadeOut(q_marks, DOWN)
        )
        self.play(
            TransformFromCopy(formula[R"\pi"][0], pi_label),
            LaggedStartMap(FadeIn, VGroup(circle, radius, radius_label)),
            ShowCreation(arc),
        )
        self.play(
            FadeTransform(formula["i"][0].copy(), i_eq["i"][0]),
            Write(i_eq[1:], time_span=(0.75, 1.75)),
        )
        self.wait()

        # Question marks over i
        i_rect = SurroundingRectangle(formula["i"], buff=0.05)
        i_rect.set_stroke(YELLOW, 2)
        q_marks = Tex(R"???", font_size=24)
        q_marks.match_color(i_rect)
        q_marks.next_to(i_rect, UP, SMALL_BUFF)

        self.play(
            ShowCreation(i_rect),
            FadeIn(q_marks, 0.25 * UP, lag_ratio=0.25)
        )
        self.wait()

        # Who cares (To overlay)
        frame = self.frame
        back_rect = FullScreenRectangle()
        back_rect.fix_in_frame()
        back_rect.set_z_index(-1),

        self.play(
            LaggedStartMap(FadeOut, VGroup(circle_group, i_eq, VGroup(i_rect, q_marks))),
            FadeOut(circle_group),
            frame.animate.set_y(-3.5),
            FadeIn(back_rect),
            formula.animate.set_fill(WHITE),
            run_time=2
        )
        self.wait()


class ExpGraph(InteractiveScene):
    def construct(self):
        # Set up graph
        axes = Axes((-1, 4), (0, 20), width=10, height=6)
        axes.to_edge(RIGHT)
        x_axis_label = Tex("t")
        x_axis_label.next_to(axes.x_axis.get_right(), UL, MED_SMALL_BUFF)
        axes.add(x_axis_label)

        graph = axes.get_graph(np.exp)
        graph.set_stroke(BLUE, 3)

        title = Tex(R"\frac{d}{dt} e^t = e^t", t2c={"t": GREY_B}, font_size=60)
        title.to_edge(UP)
        title.match_x(axes.c2p(1.5, 0))

        self.add(axes)
        self.add(graph)
        self.add(title)

        # Add height tracker
        t_tracker = ValueTracker(1)
        get_t = t_tracker.get_value
        v_line = always_redraw(
            lambda: axes.get_v_line_to_graph(get_t(), graph, line_func=Line).set_stroke(RED, 3)
        )
        height_label = Tex(R"e^t", font_size=42)
        height_label.always.next_to(v_line, RIGHT, SMALL_BUFF)
        height_label_height = height_label.get_height()
        height_label.add_updater(lambda m: m.set_height(
            min(height_label_height, 0.7 * v_line.get_height())
        ))

        self.play(
            ShowCreation(v_line, suspend_mobject_updating=True),
            FadeIn(height_label, UP, suspend_mobject_updating=True),
        )
        self.wait()

        # Add tangent line
        tangent_line = always_redraw(
            lambda: axes.get_tangent_line(get_t(), graph, length=10).set_stroke(BLUE_A, 1)
        )
        unit_size = axes.x_axis.get_unit_size()
        unit_line = Line(axes.c2p(0, 0), axes.c2p(1, 0))
        unit_line.add_updater(lambda m: m.move_to(v_line.get_end(), LEFT))
        unit_line.set_stroke(WHITE, 2)
        unit_label = Integer(1, font_size=24)
        unit_label.add_updater(lambda m: m.next_to(unit_line.pfp(0.6), UP, 0.5 * SMALL_BUFF))
        tan_v_line = always_redraw(
            lambda: v_line.copy().shift(v_line.get_vector() + unit_size * RIGHT)
        )

        deriv_label = Tex(R"\frac{d}{dt} e^t = e^t", font_size=42)
        deriv_label[R"\frac{d}{dt}"].scale(0.75, about_edge=RIGHT)
        deriv_label_height = deriv_label.get_height()
        deriv_label.add_updater(lambda m: m.set_height(
            min(deriv_label_height, 0.8 * v_line.get_height())
        ))
        deriv_label.always.next_to(tan_v_line, RIGHT, SMALL_BUFF)

        self.play(ShowCreation(tangent_line, suspend_mobject_updating=True))
        self.play(
            VFadeIn(unit_line),
            VFadeIn(unit_label),
            VFadeIn(tan_v_line, suspend_mobject_updating=True),
            TransformFromCopy(title, deriv_label),
        )
        self.play(
            ReplacementTransform(v_line.copy().clear_updaters(), tan_v_line, path_arc=45 * DEG),
            FadeTransform(height_label.copy(), deriv_label["e^t"][1], path_arc=45 * DEG, remover=True),
        )
        self.wait()

        # Move it around
        for t in [2.35, 0, 1, 2]:
            self.play(t_tracker.animate.set_value(t), run_time=5)


class DefiningPropertyOfExp(InteractiveScene):
    def construct(self):
        # Key property
        tex_kw = dict(t2c={"{t}": GREY_B, "x": BLUE})
        equation = Tex(R"\frac{d}{d{t}} e^{t} = e^{t}", font_size=90, **tex_kw)

        exp_parts = equation["e^{t}"]
        ddt = equation[R"\frac{d}{d{t}}"]

        self.play(Write(exp_parts[0]))
        self.wait()
        self.play(FadeIn(ddt, scale=2))
        self.play(
            Write(equation["="]),
            TransformFromCopy(*exp_parts, path_arc=PI / 2),
        )
        self.wait()

        # Differential Equation
        ode = Tex(R"x'(t) = x(t)", font_size=72, **tex_kw)
        ode.move_to(equation).to_edge(UP)
        ode_label = Text("Differential\nEquation", font_size=36)
        ode_label.next_to(ode, LEFT, LARGE_BUFF, aligned_edge=DOWN)

        self.play(
            FadeTransform(equation.copy(), ode),
            FadeIn(ode_label)
        )
        self.wait()

        # Initial condition
        frame = self.frame
        abs_ic = Tex(R"x(0) = 1", font_size=72, **tex_kw)
        exp_ic = Tex(R"e^{0} = 1", font_size=90, t2c={"0": GREY_B})
        abs_ic.next_to(ode, RIGHT, buff=2.0)
        exp_ic.match_x(abs_ic).match_y(equation).shift(0.1 * UP)
        ic_label = Text("Initial\nCondition", font_size=36)
        ic_label.next_to(abs_ic, RIGHT, buff=0.75)

        self.play(
            FadeIn(abs_ic, RIGHT),
            FadeIn(exp_ic, RIGHT),
            frame.animate.set_x(2),
            Write(ic_label)
        )
        self.wait()

        # Scroll down
        self.play(frame.animate.set_y(-2.5), run_time=2)
        self.wait()
