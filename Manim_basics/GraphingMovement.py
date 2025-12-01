from manim import *
import numpy as np


class SquareScene(LinearTransformationScene):
    """A scene that shows the unit square and applies a 2x2 matrix to it."""

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            **kwargs,
        )

    def construct(self):
        # Matrix to apply
        A = np.array([[1, 2], [2, 1]])

        # Label for the matrix
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}").to_edge(UL).add_background_rectangle()

        # Unit square provided by LinearTransformationScene
        unit_square = self.get_unit_square()

        # Determinant text, always redraw to stay on the square
        det_text = always_redraw(
            lambda: MathTex(f"\\det(A) = {np.round(np.linalg.det(A), 2)}").scale(0.6).move_to(unit_square.get_center())
        )

        # A sample vector that will transform with ApplyMatrix
        vect = self.get_vector([1, -2], color=PURPLE_B)

        # Extra shapes that transform
        rect1 = Rectangle(height=1.6, width=0.9, fill_opacity=0.5).shift(UP * 2 + LEFT * 2)
        circ1 = Circle(radius=0.9, fill_opacity=0.5).shift(DOWN * 2 + RIGHT * 1)

        # Register transformable objects
        self.add_transformable_mobject(vect, unit_square, rect1, circ1)

        # Add background labels
        self.add_background_mobject(matrix_tex, det_text)

        # Animate application of matrix A
        self.play(ApplyMatrix(A, run_time=2))
        self.wait(1)


class Matrix(LinearTransformationScene):
    """Simpler matrix demo scene (keeps the old 'Matrix' name)."""

    def __init__(self, **kwargs):
        super().__init__(
            show_coordinates=True,
            leave_ghost_vectors=True,
            show_basis_vectors=True,
            **kwargs,
        )

    def construct(self):
        A = np.array([[1, 2], [2, 1]])
        matrix_tex = MathTex(r"A = \begin{bmatrix} 1 & 2 \\ 2 & 1 \end{bmatrix}").to_edge(UL).add_background_rectangle()
        unit_square = self.get_unit_square()
        self.add_transformable_mobject(unit_square)
        self.add_background_mobject(matrix_tex)
        self.play(ApplyMatrix(A, run_time=1.5))
        self.wait(0.8)


class Vectors(Scene):
    """A vector demonstration. Shows a code snippet and some vectors."""

    def construct(self):
        # If you want a Code block, use a valid style string (no Code.styles_list)
        code = (
            Code(
                "Tute3Vectors.py",
                style="monokai",
                background="window",
                language="python",
                insert_line_no=True,
                tab_width=2,
                line_spacing=0.3,
                scale_factor=0.55,
                font="Monospace",
            )
            .set_width(6)
            .to_edge(UL, buff=0)
        )

        # Plane and coordinates
        plane = NumberPlane()
        plane.add_coordinates()

        self.play(Create(plane), run_time=1.2)
        self.play(Write(code), run_time=3)
        self.wait(0.4)

        # Add vectors (use Arrow for compatibility)
        v1 = Arrow(start=ORIGIN, end=LEFT * 3 + DOWN * 2, buff=0).set_color(YELLOW)
        v1_label = MathTex(r"\vec v").next_to(v1.get_end(), RIGHT, buff=0.1).set_color(YELLOW)
        self.play(GrowFromCenter(v1), Write(v1_label), run_time=1)

        basis = VGroup(
            Arrow(ORIGIN, RIGHT, buff=0).set_color(BLUE),
            Arrow(ORIGIN, UP, buff=0).set_color(BLUE),
        )
        self.add(basis)
        self.wait(0.4)

        v2 = Arrow(start=ORIGIN, end=RIGHT * 2 + UP * 2, buff=0).set_color(GREEN)
        v2_label = MathTex(r"\vec w").next_to(v2.get_end(), UP, buff=0.1).set_color(GREEN)
        self.play(GrowFromCenter(v2), Write(v2_label), run_time=1)
        self.wait(0.6)

        self.play(FadeOut(code, shift=UP * 0.5), run_time=0.6)
        self.wait(0.8)


class Tute1(Scene):
    """A tutorial showing vector addition on a plane."""

    def construct(self):
        plane = NumberPlane(x_range=[-5, 5, 1], y_range=[-4, 4, 1], x_length=10, y_length=7)
        plane.add_coordinates()
        plane.shift(RIGHT * 2)
        self.add(plane)

        # Coordinates in the plane
        p_origin = plane.coords_to_point(0, 0)
        p_v = plane.coords_to_point(3, 2)
        p_w = plane.coords_to_point(-2, 1)
        p_v_plus_w = plane.coords_to_point(1, 3)

        # Arrows
        v = Arrow(p_origin, p_v, buff=0).set_color(YELLOW)
        v_label = MathTex(r"\vec v").next_to(v.get_end(), RIGHT, buff=0.1).set_color(YELLOW)

        w = Arrow(p_origin, p_w, buff=0).set_color(RED)
        w_label = MathTex(r"\vec w").next_to(w.get_end(), LEFT, buff=0.1).set_color(RED)

        v_to_vplusw = Arrow(p_v, p_v_plus_w, buff=0).set_color(RED)

        sum_arrow = Arrow(p_origin, p_v_plus_w, buff=0).set_color(GREEN)
        sum_label = MathTex(r"\vec v + \vec w").next_to(sum_arrow.get_end(), LEFT, buff=0.1).set_color(GREEN)

        # Animate
        self.play(Create(v), Write(v_label), run_time=1)
        self.wait(0.2)
        self.play(Create(w), Write(w_label), run_time=1)
        self.wait(0.2)
        self.play(Transform(w.copy(), v_to_vplusw), w_label.animate.next_to(v_to_vplusw, UP, buff=0.1), run_time=1.2)
        self.wait(0.2)
        self.play(Create(sum_arrow), Write(sum_label), run_time=1.4)
        self.wait(0.6)

        # Small boxed summary
        box = RoundedRectangle(height=1.5, width=1.5, corner_radius=0.1, stroke_color=PINK).to_edge(DL)
        group = VGroup(plane, v, v_label, w, w_label, v_to_vplusw, sum_arrow, sum_label)
        self.add(box)
        self.play(group.animate.move_to(box.get_center()).set(width=1.2), run_time=1.2)
        self.wait(1)
