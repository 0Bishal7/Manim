from manim import *
import numpy as np

class DataWrongScene(Scene):
    def construct(self):
        # Create big red text centered
        text = Text("DATA IS WRONG", color=RED, font_size=35)
        
        # Instant pop in with glitch
        self.play(FadeIn(text, scale=0.1), run_time=0.2)
        self.play(text.animate.scale(1.5), run_time=0.2)
        
        # Continuous static effect for rest of time
        def static_effect(mob, dt):
            mob.shift(RIGHT * 0.03 * np.sin(30 * self.time) * dt)
            mob.shift(UP * 0.02 * np.cos(40 * self.time) * dt)
            mob.rotate(0.05 * np.sin(25 * self.time) * dt)
        
        text.add_updater(static_effect)
        
        # Stay exactly 2 seconds total (1.6s static)
        self.wait(1.6)


         # PART 2: 00:00:02-00:00:03 - Switch to SYSTEM DOWN
        text.clear_updaters()
        system_text = Text("SYSTEM DOWN", color=RED, font_size=48)
        self.play(FadeOut(text), run_time=0.1)
        self.play(FadeIn(system_text), run_time=0.1)
        self.wait(0.7)  # SYSTEM DOWN stays visible till exactly 00:00:03:00

         # PART 3: 00:00:03-00:00:03:30 - Screen goes dark and stays
        self.play(FadeOut(system_text), run_time=0.3)  # 3-3.3s
        self.wait(0.10)  # Scene ends, screen stays black

  # PART 4: 00:00:03:30-00:00:04:00 - Video buffering spinner#         
        circle = Circle(color=BLUE, stroke_width=15).set_stroke(BLUE, 15, opacity=0.8)
        arc = Arc(radius=1, start_angle=0, angle=TAU*0.75, stroke_width=15, color=BLUE)
        arc.set_stroke(BLUE, 15, opacity=0.8)
        
        self.play(FadeIn(circle), run_time=0.2)
        self.play(Rotate(arc, angle=TAU, about_point=ORIGIN, run_time=0.6))


        self.play(FadeOut(circle), FadeOut(arc), run_time=0.2)  # 4:00
        self.wait(0.8)  # Wait to 5:00

        # Split screen rectangles
        left_rect = Rectangle(width=7, height=8, color=WHITE, stroke_width=2).to_edge(LEFT)
        right_rect = Rectangle(width=7, height=8, color=WHITE, stroke_width=2).to_edge(RIGHT)
        self.play(FadeIn(left_rect), FadeIn(right_rect), run_time=0.5)

                # EXACT FLATICON DATABASE ICON RECREATION
        left_db = VGroup(
            # Main cylinder body
            Rectangle(width=1.2, height=1.8, color=BLUE).set_stroke(WHITE, 6).set_fill(BLUE, opacity=0.6),
            # Top shine
            Ellipse(width=0.8, height=0.3, color=WHITE).set_fill(WHITE, opacity=0.4).move_to(UP*0.8),
            # Side shine  
            Rectangle(width=0.3, height=1.0, color=WHITE).set_fill(WHITE, opacity=0.3).move_to(RIGHT*0.55)
        ).move_to(LEFT*2)
        left_db.move_to(left_rect.get_center())  # ← HERE

        right_db = left_db.copy().move_to(RIGHT*2)
        right_db.move_to(right_rect.get_center())



        left_balance = Text("BALANCE: ₹100", font_size=32).next_to(left_db, DOWN, buff=0.5)
        right_balance = Text("BALANCE: ₹80", font_size=32).next_to(right_db, DOWN, buff=0.5)

        self.play(FadeIn(left_db), FadeIn(left_balance), FadeIn(right_db), FadeIn(right_balance))

        # ZOOM OUT + FADE OUT entire screen
        screen_group = VGroup(left_rect, right_rect, left_db, right_db, left_balance, right_balance)
        self.play(
            screen_group.animate.scale(0.3).shift(UP*2),
            FadeOut(screen_group),
            run_time=1.0
        )

        # Three database icons connected by network lines
        # Three database icons at equilateral triangle vertices (radius 2.0)
        # Perfect equilateral triangle vertices (radius 1.8, 120° apart)
        r = 1.8
        db1 = left_db.copy().scale(0.6).move_to(UP*r)
        db2 = left_db.copy().scale(0.6).move_to(UP*r*np.cos(2*PI/3) + RIGHT*r*np.sin(2*PI/3))
        db3 = left_db.copy().scale(0.6).move_to(UP*r*np.cos(4*PI/3) + RIGHT*r*np.sin(4*PI/3))

        line1 = Line(db1.get_center(), db2.get_center(), stroke_width=3, color=GREEN)
        line2 = Line(db2.get_center(), db3.get_center(), stroke_width=3, color=GREEN)
        line3 = Line(db3.get_center(), db1.get_center(), stroke_width=3, color=GREEN)

        self.play(
            FadeIn(db1), FadeIn(db2), FadeIn(db3),
            FadeIn(line1), FadeIn(line2), FadeIn(line3),
            run_time=0.8
        )
        self.wait(0.3)  # 8:00


        def lightning_bolt_above(line_obj):
            # Midpoint of the network line
            mid = line_obj.get_center()

            # Small upward offset so bolt sits ABOVE the line
            offset = UP * 0.35

            # Compact, blocky lightning icon (illustration-like)
            points = [
                ORIGIN,
                DOWN*0.25 + RIGHT*0.12,
                DOWN*0.55 - RIGHT*0.15,
                DOWN*0.85 + RIGHT*0.10,
                DOWN*1.10
            ]

            bolt = VMobject()
            bolt.set_points_as_corners(points)
            bolt.set_stroke(color=RED, width=10, opacity=1)

            # Keep it compact
            bolt.scale(0.6)

            # Place above the line
            bolt.move_to(mid + offset)

            return bolt





        # --- Create lightning bolts (compact, above lines) ---
        bolt1 = lightning_bolt_above(line1)
        bolt2 = lightning_bolt_above(line2)
        bolt3 = lightning_bolt_above(line3)

        # --- Unit direction vectors for equilateral triangle (120° apart) ---
        dir1 = UP
        dir2 = np.array([np.cos(2*PI/3), np.sin(2*PI/3), 0])
        dir3 = np.array([np.cos(4*PI/3), np.sin(4*PI/3), 0])

        spread = 1.6  # distance databases move outward

        # --- Lightning strikes ---
        self.play(
            FadeIn(bolt1),
            FadeIn(bolt2),
            FadeIn(bolt3),
            run_time=0.15
        )

        # --- Network breaks + databases move along triangle vertices ---
        self.play(
            FadeOut(line1),
            FadeOut(line2),
            FadeOut(line3),

            db1.animate.shift(dir1 * spread),
            db2.animate.shift(dir2 * spread),
            db3.animate.shift(dir3 * spread),

            run_time=0.6,
            rate_func=rush_from
        )

        # --- Lightning disappears ---
        self.play(
            FadeOut(bolt1),
            FadeOut(bolt2),
            FadeOut(bolt3),
            run_time=0.15
        )

        # --- Impact flash ---
        flash = Rectangle(
            width=16,
            height=9,
            fill_color=WHITE,
            fill_opacity=0.9,
            stroke_width=0
        )

        self.play(FadeIn(flash), run_time=0.1)
        self.play(FadeOut(flash), run_time=0.3)

        # 10:00-13:00 - "MAKE A CHOICE" with dimmed database icons
        make_choice = Text("MAKE A CHOICE", font_size=72, color=RED).move_to(UP*0.5)

        # Dim databases but keep visible in background
        db1.set_fill(opacity=0.3).set_stroke(opacity=0.4)
        db2.set_fill(opacity=0.3).set_stroke(opacity=0.4) 
        db3.set_fill(opacity=0.3).set_stroke(opacity=0.4)

        self.play(FadeIn(make_choice), run_time=0.3)
        self.play(make_choice.animate.scale(1.1), run_time=0.2)
        self.wait(2.5)


            # Clear screen first  
        self.play(
            FadeOut(make_choice, shift=UP*0.5), 
            FadeOut(db1, db2, db3, shift=DOWN*0.3),
            run_time=0.3
        )

        # 15:00-17:00 - SIMULTANEOUS: CAP slams + subtitles fade
        cap_title = Text("CAP THEOREM", font_size=84, color=YELLOW).move_to(UP*1.8)
        subtitles = Text("Consistency • Availability • Partition Tolerance", 
                        font_size=36, color=WHITE).move_to(DOWN*0.5)

        # DIFFERENT animations at SAME time
        self.play(
            cap_title.animate.shift(DOWN*1.5),           # CAP THEOREM SLAMS
            FadeIn(subtitles),                           # Subtitles FADE IN
            run_time=0.4
        )

        self.wait(1.6)  # Hold total 2 seconds
        self.play(cap_title.animate.scale(1.03), subtitles.animate.scale(1.02), run_time=0.1)




        # === 15-30s: NODES + TICKING CLOCK (CENTERED) ===
        self.play(FadeOut(cap_title), FadeOut(subtitles), run_time=0.3)

        # Three nodes in equilateral triangle
        r = 2.2
        nodeA = Circle(radius=0.4, color=BLUE, fill_opacity=0.7).move_to(UP*r)
        nodeB = Circle(radius=0.4, color=BLUE, fill_opacity=0.7).move_to(UP*r*np.cos(2*PI/3) + RIGHT*r*np.sin(2*PI/3))
        nodeC = Circle(radius=0.4, color=BLUE, fill_opacity=0.7).move_to(UP*r*np.cos(4*PI/3) + RIGHT*r*np.sin(4*PI/3))

        nodeA_label = Text("node A", font_size=28).next_to(nodeA, UP)
        nodeB_label = Text("node B", font_size=28).next_to(nodeB, DOWN)
        nodeC_label = Text("node C", font_size=28).next_to(nodeC, DOWN)

        net_lines = VGroup(
            Line(nodeA.get_center(), nodeB.get_center(), color=GREEN, stroke_width=4),
            Line(nodeB.get_center(), nodeC.get_center(), color=GREEN, stroke_width=4),
            Line(nodeC.get_center(), nodeA.get_center(), color=GREEN, stroke_width=4)
        )

        # TICKING CLOCK - CENTERED IN TRIANGLE
        clock_center = ORIGIN  # Exact triangle center
        clock_face = Circle(radius=0.25, color=WHITE, stroke_width=3).move_to(clock_center)
        clock_hand = Line(clock_center, clock_center + RIGHT*0.18, color=BLACK, stroke_width=4)

        def tick_clock(mob, dt):
            angle = -self.time * 2 * PI / 9  # Full circle every 9s
            end_point = clock_center + 0.18 * np.array([np.cos(angle), np.sin(angle), 0])
            mob.become(Line(clock_center, end_point))

        clock_hand.add_updater(tick_clock)

        # 15-16s: Everything appears
        self.play(
            FadeIn(nodeA, nodeB, nodeC),
            Write(nodeA_label), Write(nodeB_label), Write(nodeC_label),
            FadeIn(net_lines), 
            FadeIn(clock_face), FadeIn(clock_hand),
            run_time=1.0
        )

        self.wait(9.0)  # 16-25s: Stable + ticking

                    
                            
                            
        # 25s: SPLIT EACH LINE FROM ITS EXACT MIDPOINT
        for line in net_lines:
            mid = line.get_start() + (line.get_end() - line.get_start()) * 0.5  # EXACT midpoint
            
            # Replace line with TWO HALF-LINES (clear split visible)
            left_half = Line(line.get_start(), mid * 0.98, color=GREEN, stroke_width=4)
            right_half = Line(mid * 1.02, line.get_end(), color=GREEN, stroke_width=4)
            
            # Animate split
            self.play(
                FadeOut(line),
                FadeIn(left_half, right_half),
                run_time=0.3
            )

        # Arrows pointing at each split midpoint
        # Arrows pointing EXACTLY at each split midpoint
        mid1 = net_lines[0].get_start() + (net_lines[0].get_end() - net_lines[0].get_start()) * 0.5
        mid2 = net_lines[1].get_start() + (net_lines[1].get_end() - net_lines[1].get_start()) * 0.5  
        mid3 = net_lines[2].get_start() + (net_lines[2].get_end() - net_lines[2].get_start()) * 0.5

        arrow1 = Arrow(mid1 + UP*0.6, mid1 + UP*0.2, color=RED, stroke_width=10)
        arrow2 = Arrow(mid2 + UP*0.6, mid2 + UP*0.2, color=RED, stroke_width=10)
        arrow3 = Arrow(mid3 + UP*0.6, mid3 + UP*0.2, color=RED, stroke_width=10)

        self.play(FadeIn(arrow1, arrow2, arrow3), run_time=0.3)
        self.wait(4.0)

# Cleanup clock
        clock_hand.clear_updaters()





        split_lines = []  # Track all split lines created in the loop
        for line in net_lines:
            mid = line.get_start() + (line.get_end() - line.get_start()) * 0.5
            left_half = Line(line.get_start(), mid * 0.98, color=GREEN, stroke_width=4)
            right_half = Line(mid * 1.02, line.get_end(), color=GREEN, stroke_width=4)
            split_lines.extend([left_half, right_half])  # Add new split lines to list

        # Now create the everything VGroup with split_lines instead of net_lines
        everything = VGroup(
            nodeA, nodeB, nodeC, 
            nodeA_label, nodeB_label, nodeC_label, 
            clock_face, clock_hand, 
            arrow1, arrow2, arrow3,
            *split_lines  # Unpack all split lines
        )
        self.play(FadeOut(everything), run_time=0.1) 
        
        
        # LARGE LETTERS horizontally aligned
        C_letter = Text("C", font_size=140, color=RED).move_to(LEFT*3.5)
        A_letter = Text("A", font_size=140, color=YELLOW).move_to(ORIGIN)
        P_letter = Text("P", font_size=140, color=BLUE).move_to(RIGHT*3.5)

        # ONE BY ONE fade in
        self.play(FadeIn(C_letter), run_time=0.4)
        self.wait(0.3)
        self.play(FadeIn(A_letter), run_time=0.4)
        self.wait(0.3) 
        self.play(FadeIn(P_letter), run_time=0.4)
        self.wait(12.6)  # Hold till 45s
