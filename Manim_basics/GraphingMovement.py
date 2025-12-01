
from manim import *
import numpy as np

# Combined 2-minute video: each segment duration sums to 120s
class CombinedVideo(Scene):
    def construct(self):
        # ----------------------
        # 1) Matrix label (8s)
        # ----------------------
        matrix_txt = Text("A = [[1, 2], [2, 1]]").to_edge(UL).scale(0.8).add_background_rectangle()
        self.play(FadeIn(matrix_txt), run_time=1.2)
        self.wait(6.8)  # overall ~8s including animation
        self.play(matrix_txt.animate.to_edge(UL), run_time=0.2)

        # ----------------------
        # 2) Determinant (6s)
        # ----------------------
        det_val = np.round(np.linalg.det(np.array([[1, 2], [2, 1]])), 3)
        det_txt = Text(f"det(A) = {det_val}").scale(0.9)
        self.play(Write(det_txt), run_time=1.0)
        self.wait(5.0)
        self.play(FadeOut(det_txt), run_time=0.5)

        # ----------------------
        # 3) Unit square (8s)
        # ----------------------
        unit_sq = Square(side_length=1.0).set_fill(BLUE_E, opacity=0.5)
        unit_sq.move_to(ORIGIN)
        unit_label = Text("Unit square").scale(0.6).next_to(unit_sq, UP, buff=0.2)
        self.play(DrawBorderThenFill(unit_sq), Write(unit_label), run_time=1.2)
        self.wait(6.8)
        self.play(FadeOut(unit_label), run_time=0.4)

        # ----------------------
        # 4) Apply matrix to square (16s)
        # ----------------------
        A = np.array([[1, 2], [2, 1]])
        # create transformable polygon (unit square)
        # use unit_sq vertices for consistency
        verts = unit_sq.get_vertices()
        # Polygon expects points in correct order; ensure we pass them
        square = Polygon(*verts, fill_opacity=0.6, fill_color=BLUE_D)
        square.move_to(ORIGIN)
        square.set_z_index(0)
        self.add(square)
        # compute transformed points (apply A to each vertex)
        pts = [np.array([v[0], v[1]]) for v in verts]
        transformed = [np.array([*(A.dot(p)), 0.0]) for p in pts]
        target_polygon = Polygon(*transformed, fill_opacity=0.6, fill_color=BLUE_D)

        # animate morph to the transformed polygon
        self.play(Transform(square, target_polygon), run_time=4.0)

        # -----------------------------------------
        # Instead of camera.frame (which is variant),
        # scale the transformed polygon to mimic zoom
        # -----------------------------------------
        self.play(square.animate.scale(1.6), run_time=1.0)  # zoom-in effect
        self.wait(11.0)  # pause to inspect transform (~16s total including anims)
        self.play(square.animate.scale(1/1.6), run_time=0.6)  # zoom-out: restore original visual scale

        self.play(FadeOut(square), run_time=0.6)

        # ----------------------
        # 5) Transform vector and shapes (12s)
        # ----------------------
        vect = Arrow(ORIGIN, np.array([1, -2, 0]), buff=0).set_color(PURPLE_B)
        v_label = Text("v = (1, -2)").scale(0.6).next_to(vect.get_end(), RIGHT, buff=0.1).set_color(PURPLE_B)
        rect = Rectangle(height=1.6, width=0.9, fill_opacity=0.6).shift(UP * 2 + LEFT * 2)
        circ = Circle(radius=0.9, fill_opacity=0.6).shift(DOWN * 2 + RIGHT * 1)
        self.play(GrowFromCenter(vect), Write(v_label), DrawBorderThenFill(rect), Create(circ), run_time=2.0)
        self.wait(1.0)

        # simulate transform by scaling/rotating these shapes (visual proxy for ApplyMatrix)
        # Note: apply_matrix exists on mobjects; using it visually here is fine
        self.play(
            vect.animate.shift(RIGHT * 1.5 + UP * 0.4).scale(1.0).rotate(0.2),
            rect.animate.apply_matrix(np.array([[1, 2],[2,1]])).shift(LEFT*0.2),
            circ.animate.apply_matrix(np.array([[1, 2],[2,1]])).shift(RIGHT*0.4),
            run_time=3.2
        )
        self.wait(6.8)  # completes ~12s block
        self.play(FadeOut(vect), FadeOut(v_label), FadeOut(rect), FadeOut(circ), run_time=0.8)

        # ----------------------
        # 6) Plane reveal (6s)
        # ----------------------
        plane = NumberPlane()
        # do NOT call plane.add_coordinates() to stay LaTeX-free
        self.play(Create(plane), run_time=1.0)
        self.wait(5.0)
        self.play(FadeOut(plane), run_time=0.6)

        # ----------------------
        # 7) Vector v1 (9s)
        # ----------------------
        v1 = Arrow(ORIGIN, LEFT * 3 + DOWN * 2, buff=0).set_color(YELLOW)
        v1_label = Text("v").scale(0.6).next_to(v1.get_end(), RIGHT, buff=0.1).set_color(YELLOW)
        self.play(GrowFromCenter(v1), Write(v1_label), run_time=1.2)
        self.wait(7.8)
        self.play(FadeOut(v1), FadeOut(v1_label), run_time=0.6)

        # ----------------------
        # 8) Vector v2 (9s)
        # ----------------------
        v2 = Arrow(ORIGIN, RIGHT * 2 + UP * 2, buff=0).set_color(GREEN)
        v2_label = Text("w").scale(0.6).next_to(v2.get_end(), UP, buff=0.1).set_color(GREEN)
        self.play(GrowFromCenter(v2), Write(v2_label), run_time=1.2)
        self.wait(7.8)
        self.play(FadeOut(v2), FadeOut(v2_label), run_time=0.6)

        # ----------------------
        # 9) Vector sum (10s)
        # ----------------------
        plane2 = NumberPlane()
        self.add(plane2)
        p_origin = plane2.coords_to_point(0, 0)
        p_v_plus_w = plane2.coords_to_point(1, 3)
        sum_arrow = Arrow(p_origin, p_v_plus_w, buff=0).set_color(GREEN)
        sum_label = Text("v + w").scale(0.6).next_to(sum_arrow.get_end(), LEFT, buff=0.1).set_color(GREEN)
        self.play(Create(sum_arrow), Write(sum_label), run_time=1.6)
        self.wait(8.4)
        self.play(FadeOut(sum_arrow), FadeOut(sum_label), FadeOut(plane2), run_time=0.6)

        # ----------------------
        # 10) Code block (8s)
        # ----------------------
        # 10) Code block (8s) — minimal args for maximum compatibility
        # 10) Code block fallback (8s) — no external file required
        code = Text("See: Tute3Vectors.py").to_edge(UL).scale(0.7).add_background_rectangle()
        self.play(Write(code), run_time=1.6)
        self.wait(6.0)
        self.play(FadeOut(code, shift=UP*0.4), run_time=0.6)

        

        # code = Code(
        #     "Tute3Vectors.py",
        #     language="python",
        #     background="window",
        #     insert_line_no=True,
        #     font="Monospace",
        #     tab_width=4,
        # ).set_width(8).to_edge(UL)

        # code = Code(
        #     "Tute3Vectors.py",
        #     style="monokai",
        #     language="python",
        #     background="window",
        #     insert_line_no=True,
        #     font="Monospace",
        # ).set_width(8).to_edge(UL)
        self.play(Write(code), run_time=1.6)
        self.wait(6.0)
        self.play(FadeOut(code, shift=UP*0.4), run_time=0.6)

        # ----------------------
        # 11) Rectangle (8s)
        # ----------------------
        r = Rectangle(height=1.6, width=0.9, fill_opacity=0.6)
        r_label = Text("Rectangle").scale(0.7).next_to(r, UP, buff=0.2)
        self.play(DrawBorderThenFill(r), Write(r_label), run_time=1.2)
        self.wait(6.2)
        self.play(FadeOut(r), FadeOut(r_label), run_time=0.6)

        # ----------------------
        # 12) Circle (8s)
        # ----------------------
        c = Circle(radius=0.9, fill_opacity=0.6)
        c_label = Text("Circle").scale(0.7).next_to(c, DOWN, buff=0.2)
        self.play(Create(c), Write(c_label), run_time=1.2)
        self.wait(6.2)
        self.play(FadeOut(c), FadeOut(c_label), run_time=0.6)

        # ----------------------
        # 13) Summary & outro (12s)
        # ----------------------
        summary_box = RoundedRectangle(height=2.2, width=7.0, corner_radius=0.2, stroke_color=WHITE)
        summary_lines = VGroup(
            Text("What we saw:", weight=BOLD).scale(0.7),
            Text("- Matrix transforms shapes and vectors").scale(0.6),
            Text("- Determinant = area scaling factor").scale(0.6),
            Text("- Vector addition via tip-to-tail").scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT)
        summary_group = VGroup(summary_box, summary_lines).arrange(UP, buff=0.5)
        summary_group.move_to(ORIGIN)
        self.play(DrawBorderThenFill(summary_box), FadeIn(summary_lines, shift=UP*0.3), run_time=1.4)
        self.wait(10.6)

        # End with a short fade-out
        self.play(FadeOut(summary_group), run_time=1.0)
        self.wait(0.6)
