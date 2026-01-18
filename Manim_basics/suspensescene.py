from manim import *
import numpy as np

class SuspenseScene(MovingCameraScene): 
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        blood_red = "#8B0000"
        
        # PHASE 1: "DATA IS WRONG" - 0:00-0:02 (2.0s total)
        big_text = Text("DATA IS WRONG", font_size=84, color=blood_red, weight=BOLD)
        big_text.center()
        self.play(Write(big_text), run_time=0.2)
        
        # TV Static glitch (1.3s)
        glitch_patterns = [
            (RIGHT*0.12 + UP*0.08, 1.05), (LEFT*0.15 + DOWN*0.10, 0.95),
            (RIGHT*0.08 + UP*0.12, 1.02), (LEFT*0.10 + DOWN*0.06, 0.98),
            (RIGHT*0.05, 1.08), (LEFT*0.07 + UP*0.09, 0.97),
            (DOWN*0.11, 1.03), (RIGHT*0.09 + LEFT*0.03, 0.99)
        ]
        
        for shift_vec, scale_val in glitch_patterns:
            glitch_text = big_text.copy().shift(shift_vec).scale(scale_val).set_opacity(0.6)
            self.add(glitch_text)
            self.play(
                glitch_text.animate.scale(0.1).set_opacity(0),
                big_text.animate.shift(RIGHT*0.02 + UP*0.01),
                run_time=0.1625
            )
            self.remove(glitch_text)
            big_text.shift(LEFT*0.02 + DOWN*0.01)
        
        self.play(FadeOut(big_text), run_time=0.5)
        
        # PHASE 2: "SYSTEM DOWN" - 0:02-0:04:00 (2.0s total)
        system_text = Text("SYSTEM DOWN", font_size=84, color=blood_red, weight=BOLD)
        system_text.center()
        self.play(ReplacementTransform(big_text, system_text), run_time=0.3)
        self.wait(1.4)  # Adjusted to hit exactly 4.0s total
        
        self.remove(system_text)
        
        # SPLIT SCREEN RECTANGLES - PERFECT VERTICAL SPLIT (NO OVERLAP)
        left_screen = Rectangle(width=6.0, height=8.0, color="#1a1a2e", fill_opacity=0.95)
        left_screen.shift(LEFT*3.8)
        
        right_screen = Rectangle(width=6.0, height=8.0, color="#16213e", fill_opacity=0.95)
        right_screen.shift(RIGHT * 3.8)
        
        # LEFT PHOTOREALISTIC DATABASE
        left_db_base = Rectangle(width=0.65, height=1.1, color="#4A90E2", fill_opacity=0.9)
        left_db_highlight = Rectangle(width=0.65, height=0.3, color="#7AB8F5", fill_opacity=1.0).align_to(left_db_base, UP)
        left_db_shadow = Rectangle(width=0.65, height=0.15, color="#2E5F99", fill_opacity=0.8).align_to(left_db_base, DOWN)
        left_db_top = Ellipse(width=0.7, height=0.35, color="#5AA0F2", fill_opacity=0.95)
        left_db_top_highlight = Circle(radius=0.12, color="#FFFFFF", fill_opacity=0.4).shift(UP*0.05 + RIGHT*0.15)
        left_db_shadow_side = Rectangle(width=0.12, height=1.1, color="#1E4066", fill_opacity=0.6).next_to(left_db_base, LEFT, buff=0)
        
        left_db_icon = VGroup(left_db_base, left_db_highlight, left_db_shadow, 
                             left_db_top, left_db_top_highlight, left_db_shadow_side)
        left_db_icon.shift(LEFT*3.8 + UP*0.8).scale(0.75)
        
        # RIGHT PHOTOREALISTIC DATABASE
        right_db_base = Rectangle(width=0.65, height=1.1, color="#4A90E2", fill_opacity=0.9)
        right_db_highlight = Rectangle(width=0.65, height=0.3, color="#7AB8F5", fill_opacity=1.0).align_to(right_db_base, UP)
        right_db_shadow = Rectangle(width=0.65, height=0.15, color="#2E5F99", fill_opacity=0.8).align_to(right_db_base, DOWN)
        right_db_top = Ellipse(width=0.7, height=0.35, color="#5AA0F2", fill_opacity=0.95)
        right_db_top_highlight = Circle(radius=0.12, color="#FFFFFF", fill_opacity=0.4).shift(UP*0.05 + LEFT*0.15)
        right_db_shadow_side = Rectangle(width=0.12, height=1.1, color="#1E4066", fill_opacity=0.6).next_to(right_db_base, RIGHT, buff=0)
        
        right_db_icon = VGroup(right_db_base, right_db_highlight, right_db_shadow, 
                              right_db_top, right_db_top_highlight, right_db_shadow_side)
        right_db_icon.shift(RIGHT*3.8 + UP*0.8).scale(0.75)
        
        # LEFT & RIGHT BALANCES
        left_balance = Text("Balance: ₹100", font_size=35, color=WHITE, weight=BOLD).shift(LEFT*3.8 + DOWN*0.4)
        right_balance = Text("Balance: ₹80", font_size=35, color=WHITE, weight=BOLD).shift(RIGHT*3.8 + DOWN*0.4)

                # ===== ADD PHOTOREALISTIC LIGHTNING HERE =====
        def create_photorealistic_lightning(start, end):
            points = [
                start,
                start + 0.15*RIGHT + 0.25*UP,
                start + 0.1*LEFT + 0.4*UP, 
                start + 0.2*RIGHT + 0.6*UP,
                end + 0.1*LEFT + 0.1*DOWN,
                end
            ]
            branch1 = [points[2], points[2] + 0.3*UP + 0.2*RIGHT, points[2] + 0.1*RIGHT]
            branch2 = [points[3], points[3] + 0.25*UP + 0.3*LEFT, points[3] + 0.15*LEFT]
            
            lightning = VMobject()
            lightning.set_points_smoothly(points + branch1 + branch2)
            lightning.set_stroke([20,16,18,14,12,20], 
                                color=[WHITE, YELLOW_D, ORANGE, YELLOW_C, RED_C, WHITE])
            lightning.set_fill(opacity=0)
            return lightning

        # 3 centered database nodes + network (add these too)
        node1 = left_db_icon.copy().scale(0.5).shift(LEFT*0.8 + UP*0.4)
        node2 = left_db_icon.copy().scale(0.5).move_to(ORIGIN)
        node3 = left_db_icon.copy().scale(0.5).shift(RIGHT*0.8 + DOWN*0.4)
        net_line1 = Line(node1.get_center(), node2.get_center(), color=GREEN, stroke_width=8)
        net_line2 = Line(node2.get_center(), node3.get_center(), color=GREEN, stroke_width=8)
        net_line3 = Line(node1.get_center(), node3.get_center(), color=GREEN, stroke_width=6)
        network_group = VGroup(node1, node2, node3, net_line1, net_line2, net_line3)

        lightning1 = create_photorealistic_lightning(node1.get_center(), node2.get_center())
        lightning2 = create_photorealistic_lightning(node2.get_center(), node3.get_center())
        lightning3 = create_photorealistic_lightning(node1.get_center(), node3.get_center())
        lightnings = VGroup(lightning1, lightning2, lightning3)
        
      # 3 database nodes PERFECTLY CENTERED (tight triangle formation)
        node1 = left_db_icon.copy().scale(0.5).shift(LEFT*-4 + UP*0)   # Top-left
        node2 = left_db_icon.copy().scale(0.5).move_to(LEFT*1 + UP*0)            # Exact center
        node3 = left_db_icon.copy().scale(0.5).shift(RIGHT*5 + DOWN*0.8) # Bottom-right

        # Green network lines connecting all 3
        net_line1 = Line(node1.get_center(), node2.get_center(), color=GREEN, stroke_width=3)
        net_line2 = Line(node2.get_center(), node3.get_center(), color=GREEN, stroke_width=3)
        net_line3 = Line(node1.get_center(), node3.get_center(), color=GREEN, stroke_width=3)

        # DEFINE network_group HERE - includes ALL nodes + lines
        network_group = VGroup(node1, node2, node3, net_line1, net_line2, net_line3)

        # 00:04:00-00:06:00 → SPLIT SCREENS + DATABASES + BALANCES ALL TOGETHER (2.0s)
        self.play(
            FadeIn(left_screen),
            FadeIn(right_screen),
            FadeIn(left_db_icon),
            FadeIn(right_db_icon),
            FadeIn(left_balance),
            FadeIn(right_balance),
            run_time=2.0
        )

                # 00:06:01-00:07:00 → ZOOM IN + SPLIT SCREENS DISAPPEAR (1s)
        self.play(
            self.camera.frame.animate.scale(0.4).move_to(ORIGIN),  # Zoom starts
            FadeOut(left_screen, target_position=ORIGIN),
            FadeOut(right_screen, target_position=ORIGIN),
            FadeOut(left_db_icon, target_position=ORIGIN),
            FadeOut(right_db_icon, target_position=ORIGIN),
            FadeOut(left_balance, target_position=ORIGIN),
            FadeOut(right_balance, target_position=ORIGIN),
            run_time=1.0  # Ends at 00:07:00
        )

        # 00:06:45-00:07:45 → NODES + NETWORK APPEAR (overlaps zoom)
        self.play(
            FadeIn(node1, node2, node3, net_line1, net_line2, net_line3),
            run_time=1.0,
            rate_func=there_and_back  # Starts mid-zoom at 00:06:45
        )

        # Nodes stay visible till 00:08:00
        self.wait(1.0)


                # AFTER your network fade-in, replace the lightning section:

        # ===== ADD LIGHTNING ZAP HERE =====
        # 1. INTENSE ELECTRICAL BUILDUP (0.2s)
        self.play(network_group.animate.set_color(RED_C), run_time=0.1)

        # 2. MULTIPLE FLASHES + PHOTOREALISTIC LIGHTNING (0.4s)
        for i in range(3):
            self.play(Flash(ORIGIN, flash_radius=5, color=WHITE), run_time=0.1)
            self.play(FadeIn(lightnings, scale=1.2), run_time=0.1)
            self.play(lightnings.animate.scale(0.8).set_opacity(0.3), run_time=0.1)

        # 3. NODES EXPLODE APART (1s)
        self.play(
            node1.animate.shift(LEFT*3 + UP*2),
            node2.animate.shift(UP*1.5),
            node3.animate.shift(RIGHT*3 + DOWN*2),
            lightnings.animate.set_opacity(0),
            run_time=1.0
        )

        # 4. Final destruction
        self.play(FadeOut(network_group), FadeOut(lightnings), run_time=0.5)