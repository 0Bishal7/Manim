from manim import *
import numpy as np

class EHFAdvanced(Scene):
    def construct(self):

        # -----------------------------
        # 1. Title
        # -----------------------------
        title = Text("E = h f", font_size=72, color=YELLOW)
        subtitle = Text("Energy of a Photon", font_size=32)
        subtitle.next_to(title, DOWN)

        self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=DOWN))
        self.wait(1)
        self.play(FadeOut(subtitle))

        # -----------------------------
        # 2. Classical wave animation
        # -----------------------------
        wave_axis = NumberLine(
            x_range=[-4, 4],
            length=8,
            include_numbers=False
        ).shift(DOWN*2)

        def sine_wave(freq=1, amp=0.5):
            return FunctionGraph(
                lambda x: amp*np.sin(freq*x),
                x_range=[-4, 4],
                color=BLUE,
                stroke_width=4
            ).shift(DOWN*2)

        wave_low = sine_wave(freq=2)
        wave_high = sine_wave(freq=6)

        label_low = Text("Low Frequency → Low Energy", font_size=28, color=BLUE).to_edge(DOWN)
        label_high = Text("Higher Frequency → Higher Energy", font_size=28, color=RED).to_edge(DOWN)

        self.play(Create(wave_axis), Create(wave_low), Write(label_low))
        self.wait(1)

        # Morph low frequency → high frequency
        self.play(
            Transform(wave_low, wave_high),
            Transform(label_low, label_high),
            run_time=2
        )
        self.wait(1)

        self.play(FadeOut(VGroup(wave_low, wave_axis, label_low)))

        # -----------------------------
        # 3. Photon wave packet
        # -----------------------------
        def photon_packet(freq=3):
            return ParametricFunction(
                lambda t: np.array([
                    t,
                    0.4*np.sin(freq * t) * np.exp(-((t)**2)),
                    0
                ]),
                t_range=[-3, 3],
                color=YELLOW,
                stroke_width=6
            )

        packet_low = photon_packet(freq=3)
        packet_high = photon_packet(freq=10)

        packet_label = Text("Photon = Wave Packet", font_size=28).to_edge(UP)

        self.play(FadeIn(packet_label))
        self.play(Create(packet_low))
        self.wait(1)

        # Frequency increases smoothly → photon energy rises
        self.play(Transform(packet_low, packet_high), run_time=2)
        self.wait(1)
        self.play(FadeOut(VGroup(packet_low, packet_label)))

        # -----------------------------
        # 4. Quantization steps
        # -----------------------------
        steps = VGroup()
        for i in range(5):
            rect = Rectangle(
                width=1.2,
                height=0.4 * (i+1),
                color=BLUE,
                fill_opacity=0.2
            ).shift(RIGHT*3 + UP*(i*0.3))
            steps.add(rect)

        step_label = Text("Energy comes in packets of hf", font_size=28).to_edge(UP)

        self.play(Write(step_label))
        self.play(LaggedStart(*[Create(r) for r in steps], lag_ratio=0.2))
        self.wait(1)
        self.play(FadeOut(steps), FadeOut(step_label))

        # -----------------------------
        # 5. Photoelectric effect with threshold frequency
        # -----------------------------
        metal = Rectangle(width=5, height=1.4, color=PURPLE, fill_opacity=0.1)
        metal.shift(DOWN*1.5)

        electron = Dot(color=ORANGE).next_to(metal, UP + LEFT*1.0)
        metal_label = Text("Metal", font_size=24).next_to(metal, DOWN)

        self.play(Create(metal), FadeIn(electron), Write(metal_label))

        # Photon wave (LOW frequency – fails to eject electron)
        bad_photon = photon_packet(freq=3).shift(UP*2)
        bad_label = Text("f < f₀ → No Ejection", font_size=24, color=RED).to_edge(UP)

        self.play(Create(bad_photon), Write(bad_label))
        self.wait(1)

        self.play(FadeOut(bad_photon), FadeOut(bad_label))

        # HIGH frequency photon (success)
        good_photon = photon_packet(freq=12).shift(UP*2)
        good_label = Text("f > f₀ → Electron Ejected", font_size=24, color=GREEN).to_edge(UP)

        self.play(Create(good_photon), Write(good_label))
        self.wait(0.5)

        ejected = electron.copy()
        self.play(
            ejected.animate.shift(UP*2 + RIGHT*1.5),
            run_time=1.5,
            rate_func=smooth
        )
        self.wait(1)

        self.play(FadeOut(VGroup(metal, electron, ejected, metal_label, good_photon, good_label)))

        # -----------------------------
        # 6. E = h f graph
        # -----------------------------
        axes = Axes(
            x_range=[0, 10],
            y_range=[0, 10],
            x_length=6,
            y_length=4,
            axis_config={"color": WHITE}
        )

        x_lab = MathTex("f", color=BLUE).next_to(axes.x_axis.get_end(), RIGHT)
        y_lab = MathTex("E", color=RED).next_to(axes.y_axis.get_end(), UP)

        line = axes.plot(lambda x: x, color=YELLOW, stroke_width=6)

        self.play(Create(axes), Write(x_lab), Write(y_lab))
        self.wait(0.3)
        self.play(Create(line), run_time=1.5)

        eq = MathTex("E = h f", font_size=72, color=YELLOW).to_edge(UP)
        self.play(Write(eq))
        self.wait(2)

        # -----------------------------
        # Ending
        # -----------------------------
        end = Text("Higher Frequency → Higher Photon Energy", font_size=36)
        self.play(FadeOut(axes), FadeOut(line), FadeOut(eq), FadeIn(end))
        self.wait(2)
        self.play(FadeOut(end))
