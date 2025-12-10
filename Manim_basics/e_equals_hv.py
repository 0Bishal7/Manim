from manim import *

class PhotonEnergyScene(Scene):
    def construct(self):
        title = Text("E = hν", font_size=80)
        self.play(Write(title))
        self.wait(1)

        # Explanation text
        explanation = Text(
            "Energy of a photon is proportional to frequency",
            font_size=32
        ).next_to(title, DOWN)
        self.play(FadeIn(explanation))
        self.wait(2)

        # Show the variables
        eq1 = MathTex("E = h \\times \\nu", font_size=70).shift(UP*2)
        h_text = Text("h = Planck's constant", font_size=32).next_to(eq1, DOWN)
        freq_text = Text("ν = frequency of the wave", font_size=32).next_to(h_text, DOWN)

        self.play(Transform(title, eq1))
        self.play(FadeIn(h_text), FadeIn(freq_text))
        self.wait(2)

        # Animation: increasing frequency waves
        low_wave = FunctionGraph(lambda x: 0.5*np.sin(2*x)).shift(LEFT*3)
        high_wave = FunctionGraph(lambda x: 0.5*np.sin(6*x)).shift(RIGHT*3)
        low_label = Text("Low ν → Low E", font_size=30).next_to(low_wave, DOWN)
        high_label = Text("High ν → High E", font_size=30).next_to(high_wave, DOWN)

        self.play(Create(low_wave), FadeIn(low_label))
        self.wait(1)
        self.play(Create(high_wave), FadeIn(high_label))
        self.wait(2)

        # Photon energy rise animation
        arrow = Arrow(start=LEFT, end=RIGHT).shift(DOWN*2)
        energy_text = Text("Energy increases with frequency", font_size=32)
        energy_text.next_to(arrow, DOWN)

        self.play(GrowArrow(arrow))
        self.play(FadeIn(energy_text))
        self.wait(2)

        # Glow effect for photons
        photon_low = Dot(point=LEFT*3, radius=0.15, color=BLUE)
        photon_high = Dot(point=RIGHT*3, radius=0.15, color=YELLOW)

        self.play(FadeIn(photon_low))
        self.wait(0.5)
        self.play(FadeIn(photon_high))
        self.wait(0.5)

        self.play(
            photon_low.animate.scale(0.8),
            photon_high.animate.scale(2)
        )
        self.wait(2)

        final_text = Text("Higher frequency → Higher energy", font_size=40).to_edge(DOWN)
        self.play(FadeIn(final_text))
        self.wait(3)
