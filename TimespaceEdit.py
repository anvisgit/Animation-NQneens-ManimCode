from manim import *

# Manim Community v0.19.x. No LaTeX installation required.
# Render: python -m manim -pql nqueens_complexity_animation.py NQueensComplexity

class NQueensComplexity(Scene):
    def construct(self):
        self.camera.background_color = '#0B1220'
        WHITE2 = '#E8EDF7'
        MUTED = '#9BAAC4'
        GOLD = '#F6C453'
        GREEN2 = '#56D7A4'
        BLUE2 = '#70B8FF'

        def line(s, size=29, color=WHITE2):
            t = Text(s, font_size=size, color=color)
            t.scale_to_fit_width(min(t.width, 12.2))
            return t

        title = line('N-Queens Backtracking: Complexity', 40)
        title.to_edge(UP, buff=.35)
        rule = Line(LEFT*6.1, RIGHT*6.1, color=BLUE2, stroke_width=2).next_to(title, DOWN, buff=.18)
        self.play(Write(title), Create(rule), run_time=2)
        self.wait(2)

        # Time complexity: choices shrink by row.
        head = line('TIME COMPLEXITY', 33, BLUE2).move_to(UP*2.05)
        self.play(FadeIn(head), run_time=1)
        choices = VGroup(*[line(s, 31, GOLD) for s in ['Row 1: N choices', 'Row 2: at most N - 1', 'Row 3: at most N - 2', '...', 'Last row: at most 1']])
        choices.arrange(DOWN, buff=.17).move_to(DOWN*.15)
        for t in choices:
            self.play(FadeIn(t, shift=UP*.12), run_time=.7)
            self.wait(1.6)
        factorial = line('Maximum search states: O(N!)', 33, GREEN2).move_to(DOWN*2.65)
        self.play(Write(factorial), run_time=1.6)
        self.wait(4)

        self.play(FadeOut(choices), FadeOut(factorial), run_time=1)
        checks = VGroup(
            line('Each recursive call checks up to N columns.', 29),
            line('Each column + diagonal check takes O(1).', 29),
            line('Conservative search bound: O(N x N!)', 34, GREEN2),
        ).arrange(DOWN, buff=.38).move_to(DOWN*.3)
        for t in checks:
            self.play(Write(t), run_time=1.5)
            self.wait(3)
        self.wait(4)

        # Printing is part of the given C++ implementation.
        self.play(FadeOut(checks), run_time=.8)
        printing = VGroup(
            line('The code prints EVERY valid chessboard.', 30),
            line('One board: N x N = O(N^2)', 30, GOLD),
            line('S(N) solutions: O(S(N) x N^2)', 30, GOLD),
            line('TOTAL: O(N x N! + S(N) x N^2)', 31, GREEN2),
        ).arrange(DOWN, buff=.36).move_to(DOWN*.35)
        for t in printing:
            self.play(FadeIn(t, shift=UP*.1), run_time=1.1)
            self.wait(3.4)
        self.wait(4)

        # Space complexity.
        self.play(FadeOut(printing), Transform(head, line('SPACE COMPLEXITY', 33, BLUE2).move_to(UP*2.05)), run_time=1)
        space = VGroup(
            line('board array: O(N)', 29),
            line('column + diagonal arrays: O(N)', 29),
            line('recursion depth: O(N)', 29),
            line('AUXILIARY SPACE: O(N)', 35, GREEN2),
        ).arrange(DOWN, buff=.39).move_to(DOWN*.3)
        for t in space:
            self.play(FadeIn(t, shift=RIGHT*.15), run_time=1)
            self.wait(3.3)
        self.wait(4)

        self.play(FadeOut(space), FadeOut(head), run_time=1)
        summary = VGroup(
            line('FINAL COMPLEXITY', 36, BLUE2),
            line('Search time: O(N x N!)', 34, GOLD),
            line('Including output: O(N x N! + S(N) x N^2)', 29, GOLD),
            line('Auxiliary space: O(N)', 34, GREEN2),
            line('Pruning rejects invalid branches early.', 27, MUTED),
        ).arrange(DOWN, buff=.4).move_to(DOWN*.3)
        self.play(LaggedStart(*[FadeIn(t) for t in summary], lag_ratio=.25), run_time=3)
        self.wait(9)
