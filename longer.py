from manim import *

# Manim Community Edition 0.19.1
# Render: python -m manim -pqh nqueens_section4.py Section4NQueens
# Narration-friendly 240-second scene; no audio is embedded.

BG = '#101827'
LIGHT = '#E9F0FA'
MUTED = '#9DB1C9'
GOLD = '#FFD166'
RED = '#F07178'
GREEN = '#67D6A0'
BLUE = '#66B8F5'
SQUARE_A = '#DCE5EE'
SQUARE_B = '#7894AE'

class Section4NQueens(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.t0 = self.renderer.time
        self.board = None
        self.queens = {}
        self.marks = VGroup()
        self.heading = None
        self.subtitle = None
        self.chapter('THE N-QUEENS PROBLEM', 'Section 4  |  Problem formulation')
        self.board_create()
        self.hold_to(12)
        self.caption('Four rows. Four columns. Exactly four queens.')
        self.hold_to(22)
        self.caption('Goal: no two queens may attack each other.')
        self.hold_to(30)

        # 00:30-01:05 — attack geometry
        self.chapter('HOW A QUEEN ATTACKS', 'Horizontal, vertical and diagonal directions')
        self.place(1, 1)
        self.hold_to(38)
        self.attack_highlight(1, 1, 'row', RED)
        self.caption('Horizontal: every other square in the same row.')
        self.hold_to(47)
        self.attack_highlight(1, 1, 'column', RED)
        self.caption('Vertical: every other square in the same column.')
        self.hold_to(56)
        self.attack_highlight(1, 1, 'diagonal', RED)
        self.caption('Diagonal: equal changes in row and column.')
        self.hold_to(65)

        # 01:05-01:40 — invalid examples
        self.chapter('CONFLICT DETECTION', 'A single conflict makes a placement invalid')
        self.clear_marks()
        self.clear_queens()
        self.place(0, 0)
        self.caption('Start at row 1, column 1.')
        self.hold_to(73)
        self.attack_highlight(0, 0, 'all', RED)
        self.hold_to(80)
        self.place(1, 1, color=RED)
        self.conflict_line((0, 0), (1, 1))
        self.caption('Row 2, column 2 is invalid: same diagonal.')
        self.hold_to(91)
        self.remove_queen(1)
        self.clear_marks()
        self.place(2, 0, color=RED)
        self.conflict_line((0, 0), (2, 0))
        self.caption('Row 3, column 1 is invalid: same column.')
        self.hold_to(101)
        self.remove_queen(2)
        self.clear_marks()
        self.hold_to(105)

        # 01:40-02:25 — mathematical constraints
        self.chapter('MATHEMATICAL CONSTRAINTS', 'Define Q(i) as the column chosen for row i')
        self.clear_queens()
        self.show_formula(r'Q(i) \in \{1,2,\ldots,N\}', 'One column is selected for every row.')
        self.hold_to(119)
        self.show_formula(r'Q(i) \ne Q(j)', 'Different rows must use different columns.')
        self.hold_to(134)
        self.show_formula(r'|i-j| \ne |Q(i)-Q(j)|', 'Equal row and column distances mean a diagonal conflict.')
        self.hold_to(150)

        # 02:25-03:05 — row-wise representation
        self.chapter('A SMALLER REPRESENTATION', 'One decision per row, not one per square')
        self.caption('We do not need sixteen independent square decisions.')
        self.hold_to(162)
        self.caption('Each row is assigned exactly one column.')
        self.hold_to(174)
        self.caption('Represent the complete arrangement with four values.')
        self.hold_to(185)

        # 03:05-03:45 — final configuration and verification
        self.chapter('BUILD A VALID SOLUTION', 'Q = [2, 4, 1, 3]')
        self.clear_queens()
        self.clear_marks()
        for r, c, at in [(0,1,194),(1,3,204),(2,0,214),(3,2,224)]:
            self.place(r, c, color=GOLD)
            self.caption(f'Row {r+1}  →  Column {c+1}')
            self.hold_to(at)
        self.caption('All columns are unique; no pair shares a diagonal.')
        self.verify_solution()
        self.hold_to(235)

        # 03:45-04:00 — transition
        self.chapter('BUT HOW DO WE FIND IT?', 'Next: brute-force enumeration versus backtracking')
        self.hold_to(240)

    def hold_to(self, seconds):
        elapsed = self.renderer.time - self.t0
        if seconds > elapsed:
            self.wait(seconds - elapsed)

    def chapter(self, title, subtitle):
        new_heading = Text(title, font_size=31, weight=BOLD, color=LIGHT).to_edge(UP, buff=.32)
        new_subtitle = Text(subtitle, font_size=19, color=MUTED).next_to(new_heading, DOWN, buff=.12)
        outgoing = VGroup(*[x for x in [self.heading, self.subtitle] if x is not None])
        if len(outgoing):
            self.play(FadeOut(outgoing), run_time=.35)
        self.play(FadeIn(new_heading), FadeIn(new_subtitle), run_time=.55)
        self.heading, self.subtitle = new_heading, new_subtitle

    def board_create(self):
        self.s = 1.12
        self.origin = LEFT * 2.3 + DOWN * .20
        self.board = VGroup()
        for r in range(4):
            for c in range(4):
                tile = Square(side_length=self.s, stroke_width=1.3,
                              stroke_color='#3E5268',
                              fill_color=SQUARE_A if (r+c)%2==0 else SQUARE_B,
                              fill_opacity=1)
                tile.move_to(self.center(r,c))
                self.board.add(tile)
        labels = VGroup()
        for k in range(4):
            labels.add(Text(str(k+1), font_size=18, color=MUTED).move_to(self.center(k,0)+LEFT*.72))
            labels.add(Text(str(k+1), font_size=18, color=MUTED).move_to(self.center(3,k)+DOWN*.72))
        self.board.add(labels)
        self.play(LaggedStart(*[FadeIn(x) for x in self.board[:16]], lag_ratio=.045),
                  FadeIn(labels), run_time=2.0)

    def center(self, r, c):
        return self.origin + RIGHT*(c-1.5)*self.s + UP*(1.5-r)*self.s

    def place(self, r, c, color=GOLD):
        if r in self.queens:
            self.remove_queen(r)
        # Text symbol avoids requiring external image files.
        q = Text('♛', font_size=63, color=color).move_to(self.center(r,c))
        self.queens[r] = q
        self.play(FadeIn(q, scale=.5), run_time=.65)

    def remove_queen(self, r):
        if r in self.queens:
            self.play(FadeOut(self.queens[r], scale=.6), run_time=.5)
            del self.queens[r]

    def clear_queens(self):
        if self.queens:
            self.play(*[FadeOut(q) for q in self.queens.values()], run_time=.5)
            self.queens.clear()

    def clear_marks(self):
        if len(self.marks):
            self.play(FadeOut(self.marks), run_time=.35)
        self.marks = VGroup()

    def attack_highlight(self, r, c, mode, color):
        self.clear_marks()
        squares = []
        for rr in range(4):
            for cc in range(4):
                if (rr,cc)==(r,c):
                    continue
                row = rr==r
                col = cc==c
                diag = abs(rr-r)==abs(cc-c)
                if (mode=='row' and row) or (mode=='column' and col) or (mode=='diagonal' and diag) or (mode=='all' and (row or col or diag)):
                    mark = Square(side_length=self.s*.88, stroke_width=0,
                                  fill_color=color, fill_opacity=.55).move_to(self.center(rr,cc))
                    squares.append(mark)
        self.marks = VGroup(*squares)
        if squares:
            self.play(LaggedStart(*[FadeIn(x) for x in squares], lag_ratio=.08), run_time=1.1)
        self.bring_to_front(*self.queens.values())

    def conflict_line(self, a, b):
        line = Line(self.center(*a), self.center(*b), color=RED, stroke_width=7)
        self.marks.add(line)
        self.play(Create(line), run_time=.65)

    def caption(self, words):
        new = Text(words, font_size=21, color=LIGHT)
        new.scale_to_fit_width(min(new.width, 11.7))
        new.to_edge(DOWN, buff=.42)
        if hasattr(self, 'caption_obj') and self.caption_obj is not None:
            self.play(FadeOut(self.caption_obj), FadeIn(new), run_time=.35)
        else:
            self.play(FadeIn(new), run_time=.35)
        self.caption_obj = new

    def show_formula(self, tex, explanation):
        if hasattr(self, 'formula_obj') and self.formula_obj is not None:
            self.play(FadeOut(self.formula_obj), run_time=.35)
        new = MathTex(tex, color=GOLD, font_size=44).move_to(RIGHT*3.1+UP*.1)
        self.play(Write(new), run_time=1.5)
        self.formula_obj = new
        self.caption(explanation)

    def verify_solution(self):
        if hasattr(self, 'formula_obj') and self.formula_obj is not None:
            self.play(FadeOut(self.formula_obj), run_time=.3)
            self.formula_obj = None
        check = Text('VALID CONFIGURATION', font_size=27, color=GREEN).move_to(RIGHT*3.15+UP*.3)
        values = Text('[2, 4, 1, 3]', font_size=32, color=GOLD).next_to(check, DOWN, buff=.35)
        self.play(FadeIn(check), Write(values), run_time=1.1)
        self.wait(1)
        self.play(FadeOut(check), FadeOut(values), run_time=.4)
