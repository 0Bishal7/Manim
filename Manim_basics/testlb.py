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

                    
                            
                            
        # 25s: SPLIT EACH LINE FROM ITS EXACT MIDPOINT - FIXED VERSION
        self.play(FadeOut(net_lines), run_time=0.3)  # Remove original lines FIRST

        # Create and store ALL split line segments in a list
        split_line_groups = []
        for i, line in enumerate(net_lines):
            mid = line.get_start() + (line.get_end() - line.get_start()) * 0.5
            
            left_half = Line(line.get_start(), mid * 0.98, color=GREEN, stroke_width=4)
            right_half = Line(mid * 1.02, line.get_end(), color=GREEN, stroke_width=4)
            
            split_line_groups.append(VGroup(left_half, right_half))

        # Animate ALL split lines appearing simultaneously  
        self.play(*[FadeIn(group) for group in split_line_groups], run_time=0.3)

        # Arrows pointing at each split midpoint
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





        # 30-45s: CLEAR SCREEN - NOW INCLUDES ALL SPLIT LINES
        everything = VGroup(
            nodeA, nodeB, nodeC, 
            nodeA_label, nodeB_label, nodeC_label, 
            clock_face, clock_hand, 
            arrow1, arrow2, arrow3,
            *[group for group in split_line_groups]  # ALL split lines
        )
        self.play(FadeOut(everything), run_time=0.8)

# Now screen is PERFECTLY CLEAN - C A P appears
        
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
        self.wait(8)  # Hold till 45s




        # === 45-55s: A RISES + C/P FORM TRIANGLE + ZIGZAG LINE ===
        self.wait(1.0)  # Brief pause after P appears

        # Define target equilateral triangle positions (radius 2.5)
        r = 2.5
        target_A = UP * r                    # A at top vertex  
        target_C = UP*r*np.cos(2*PI/3) + RIGHT*r*np.sin(2*PI/3)  # C at 120°
        target_P = UP*r*np.cos(4*PI/3) + RIGHT*r*np.sin(4*PI/3)  # P at 240°

        # 45-52s: Move to triangle vertices (4 seconds)
        self.play(
            A_letter.animate.move_to(target_A),           # A rises up
            C_letter.animate.move_to(target_C),           # C moves bottom-left
            P_letter.animate.move_to(target_P),           # P moves bottom-right
            run_time=4.0
        )



        # Move to triangle vertices (4 seconds)
        self.play(
            A_letter.animate.move_to(target_A),
            C_letter.animate.move_to(target_C), 
            P_letter.animate.move_to(target_P),
            run_time=4.0
        )

        # 1. Triangle sides first
        side_CP = Line(target_C, target_P, color=GREEN, stroke_width=8)
        side_AC = Line(target_A, target_C, color=GREEN, stroke_width=8)
        side_AP = Line(target_A, target_P, color=GREEN, stroke_width=8)


        side_CP.set_z_index(-1)
        side_AC.set_z_index(-1) 
        side_AP.set_z_index(-1)

        triangle_lines = VGroup(side_CP, side_AC, side_AP)
        self.play(Create(triangle_lines), run_time=1.0)

        # 2. THEN zigzag partition line
        mid_CP = (target_C + target_P) / 2
        zigzag_points = [
            target_A + DOWN*0.4,
            target_A + DOWN*0.8 + RIGHT*0.3,
            mid_CP + UP*0.4 + LEFT*0.2,
            mid_CP
        ]
        zigzag_line = VMobject()
        zigzag_line.set_points_as_corners(zigzag_points)
        zigzag_line.set_stroke(RED, width=4)
        self.play(Create(zigzag_line), run_time=2.0)

        self.wait(2.0)

        self.play(FadeOut(zigzag_line), run_time=1.0)


        def create_person_icon(color, scale=1.0):
            # Head circle - bottom touches body top exactly (NO overlap)
            head = Circle(radius=0.28, color=color, fill_opacity=1.0)
            
            # Body with curved top - top touches head bottom exactly  
            body_points = [
                LEFT*0.25 + UP*0.28,   # ← Top-left touches head bottom
                LEFT*0.3 + UP*0.18, 
                LEFT*0.35 + DOWN*0.02,
                LEFT*0.35 + DOWN*0.6, 
                LEFT*0.35 + DOWN*1.05,
                LEFT*0.25 + DOWN*1.1, 
                RIGHT*0.25 + DOWN*1.1,
                RIGHT*0.35 + DOWN*1.05,
                RIGHT*0.35 + DOWN*0.6, 
                RIGHT*0.35 + DOWN*0.02,
                RIGHT*0.3 + UP*0.18,
                RIGHT*0.25 + UP*0.28    # ← Top-right touches head bottom
            ]
            
            body = VMobject()
            body.set_points_as_corners(body_points)
            body.set_fill(color, opacity=1.0)
            body.set_stroke(width=0)
            
            # Position so they TOUCH at single point (UP*0.28 = head radius)
            body.next_to(head, DOWN, buff=0)  # buff=0 = touching only
            
            return VGroup(head, body).scale(scale)


        person_A = create_person_icon(YELLOW).move_to(target_A)
        person_C = create_person_icon(RED).move_to(target_C)
        person_P = create_person_icon(BLUE).move_to(target_P)

        self.play(
            Transform(A_letter, person_A),
            Transform(C_letter, person_C),
            Transform(P_letter, person_P),
            run_time=1.5
        )



        # === SIDE SPEECH BUBBLES ===
        def create_speech_bubble(text_str, person_pos, side="right"):
            bubble = RoundedRectangle(width=2.5, height=1.3, corner_radius=0.15)
            bubble.set_fill(WHITE, 1.0)
            bubble.set_stroke(BLACK, width=4)
            
            text = Text(text_str, font_size=22, color=BLACK)
            text.move_to(bubble.get_center())
            
            # Side positioning
            if side == "right":
                bubble_pos = person_pos + LEFT*2.3
            else:
                bubble_pos = person_pos + RIGHT*2.3
                
            bubble_group = VGroup(bubble, text).move_to(bubble_pos)
            return bubble_group

        bubble_A = create_speech_bubble("Availability", person_A.get_center(), "right")
        bubble_C = create_speech_bubble("Consistency", person_C.get_center(), "left")
        bubble_P = create_speech_bubble("Partition\nTolerance", person_P.get_center(), "right")

        self.play(FadeIn(bubble_A, bubble_C, bubble_P), run_time=1.5)


        self.wait(4.0)  # Brief pause

        # === PERSON_C TURNS GREY + BUBBLE DISAPPEARS (21 seconds total) ===
        self.play(
            person_C.animate.set_color(GREY).set_opacity(1.4),
            FadeOut(bubble_C),
            run_time=5.0  # Smooth color transition
        )
        self.wait(12.0)  # Hold the failure state (total 21s)


        



        # # === 15 SECONDS: SPEECH BUBBLES FADE → PEOPLE BACK TO VERTEX LETTERS ===
        # self.wait(3.0)  # Setup pause

        # # 1. Speech bubbles fade out FIRST (2s)
        # self.play(FadeOut(bubble_A), FadeOut(bubble_P), run_time=2.0)

        # # 2. People transform back to INITIAL letters AT SAME VERTEX POSITIONS (2s)
        # self.play(
        #     Transform(person_A, Text("A", font_size=140, color=YELLOW).move_to(target_A)),
        #     Transform(person_C, Text("C", font_size=140, color=RED).move_to(target_C)),
        #     Transform(person_P, Text("P", font_size=140, color=BLUE).move_to(target_P)),
        #     run_time=2.0
        # )

        # self.wait(9.0)  # Hold triangle letters (total 15s)





        # === 15 SECONDS: BUBBLES FADE → PEOPLE DISAPPEAR + LETTERS APPEAR ===
      

        # 1. Bubbles fade FIRST (keep people visible)
        self.play(FadeOut(bubble_A), FadeOut(bubble_P), run_time=2.0)

        # 2. FORCE DESTROY EVERYTHING - No mercy
        self.play(
            *[FadeOut(mob, shift=UP*2) for mob in self.mobjects],
            run_time=0.3
        )
        self.clear()  # WIPES SCREEN COMPLETELY - BULLETPROOF

        # 3. NEW letters appear on CLEAN screen
        new_A = Text("A", font_size=45, color=YELLOW).move_to(target_A)
        new_C = Text("C", font_size=45, color=RED).move_to(target_C)
        new_P = Text("P", font_size=45, color=BLUE).move_to(target_P)

        self.play(FadeIn(new_A, new_C, new_P), run_time=0.8)
        self.wait(11.0)






                    
        # === 10s GLOW EFFECT: P glows + others fade + Network text ===
        glow_group = VGroup(new_A, new_C, new_P)

        # 1. P GLOWS, others fade (2s)
        self.play(
            new_P.animate.scale(1.3).set_stroke(BLUE, width=12),
            new_A.animate.set_opacity(0.6),
            new_C.animate.set_opacity(0.6),
            run_time=2.0
        )

        # 2. EQUIDISTANT WORDS with wiggle on "Network"
        words = ["Network", "failures", "are", "inevitable"]
        word_objects = [Text(word, font_size=48, color=WHITE) for word in words]

        # Equal spacing across frame
        total_width = 8.0
        gap = total_width / (len(words) - 1)
        start_x = -total_width / 2

        for i, word in enumerate(word_objects):
            word.move_to(RIGHT * (start_x + i * gap))

        network_text_group = VGroup(*word_objects).to_edge(UP)

        # Wiggle ONLY first word ("Network")
        def wiggle_network(mob, dt):
            mob.shift(RIGHT * 0.08 * np.sin(15 * self.time) * dt)
            mob.shift(UP * 0.03 * np.cos(20 * self.time) * dt)

        word_objects[0].add_updater(wiggle_network)  # FIXED: word_objects[0], not network_part

        self.play(
            Write(network_text_group),
            new_P.animate.scale(1.4).set_stroke(BLUE, width=15),
            run_time=1.0
        )

        self.wait(7.0)  # Total 10s

        # Cleanup - FIXED variable name
        word_objects[0].clear_updaters()  # word_objects[0] = Network


            # === SPLIT SCREEN TRANSITION ===
        # 1. ONLY Network text disappears (letters stay)
        self.play(FadeOut(network_text_group), run_time=0.5)

        # 2. P stops glowing, returns to normal
        self.play(
            new_P.animate.scale(1.0).set_stroke(width=0),
            run_time=0.5
        )

        # 3. Split screen rectangles (EXACTLY like first part)
        left_rect = Rectangle(width=7, height=8, color=WHITE, stroke_width=2).to_edge(LEFT)
        right_rect = Rectangle(width=7, height=8, color=WHITE, stroke_width=2).to_edge(RIGHT)
        self.play(FadeIn(left_rect), FadeIn(right_rect), run_time=0.5)

        # 4. **CRITICAL FIX**: Position FIRST, then glow - NO updaters
        self.play(
            new_P.animate.set_opacity(0.2),  # P to background
            new_C.animate.move_to(left_rect.get_center()).scale(1.4).set_stroke(RED, width=15),
            new_A.animate.move_to(right_rect.get_center()).scale(1.4).set_stroke(YELLOW, width=15),
            run_time=6.0
        )

        # 5. **STATIC GLOW** - One-time scale + stroke boost (NO updater)
        self.play(
            new_C.animate.scale(1.05).set_stroke(RED, width=20),
            new_A.animate.scale(1.05).set_stroke(YELLOW, width=20),
            run_time=9.0  # Continuous "glow" effect without drift
        )


     