from manim import *

# Manim Community Edition 0.19.1
# Render: python -m manim -pqh nqueens_section4.py Section4NQueens
# Narration-friendly 510-second scene; no audio is embedded.

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
        self.formula_obj = None
        self.caption_obj = None
        self.chapter('THE N-QUEENS PROBLEM', 'Section 4 | Problem formulation')
        self.board_create()
        self.caption('An N by N board contains N queens to be placed safely.')
        self.hold_to(18)
        self.caption('For this demonstration, N = 4: sixteen squares and four queens.')
        self.hold_to(33)
        self.caption('Every row must contain exactly one queen.')
        self.hold_to(46)

        self.chapter('HOW A QUEEN MOVES', 'Three distinct attack directions')
        self.place(1, 1)
        self.caption('A queen attacks horizontally along its entire row.')
        self.attack_highlight(1, 1, 'row', RED)
        self.hold_to(65)
        self.caption('The same queen attacks vertically along its column.')
        self.attack_highlight(1, 1, 'column', RED)
        self.hold_to(83)
        self.caption('It also attacks both diagonals.')
        self.attack_highlight(1, 1, 'diagonal', RED)
        self.hold_to(100)
        self.caption('All attacked squares are unavailable to another queen.')
        self.attack_highlight(1, 1, 'all', RED)
        self.hold_to(118)

        self.chapter('IDENTIFYING CONFLICTS', 'A single conflicting pair invalidates a placement')
        self.clear_marks()
        self.clear_queens()
        self.place(0, 0)
        self.caption('Place the first queen at row 1, column 1.')
        self.hold_to(132)
        self.place(1, 1, RED)
        self.conflict_line((0,0), (1,1))
        self.caption('Invalid: row 2, column 2 shares a diagonal.')
        self.hold_to(151)
        self.remove_queen(1)
        self.clear_marks()
        self.place(2, 0, RED)
        self.conflict_line((0,0), (2,0))
        self.caption('Invalid: row 3, column 1 shares the same column.')
        self.hold_to(170)
        self.remove_queen(2)
        self.clear_marks()
        self.place(0, 0)
        self.attack_highlight(0, 0, 'row', RED)
        self.caption('Every other square in row 1 is already attacked horizontally.')
        self.hold_to(187)
        self.remove_queen(0)
        self.clear_marks()
        self.clear_queens()

        self.chapter('MATHEMATICAL FORMULATION', 'Represent each queen using a row and a column')
        self.show_formula(r'Q(i) \in \{1,2,\ldots,N\}', 'Q(i) is the column selected for the queen in row i.')
        self.hold_to(208)
        self.show_formula(r'i \ne j', 'Every queen occupies a different row by construction.')
        self.hold_to(227)
        self.show_formula(r'Q(i) \ne Q(j)', 'Distinct rows must also use distinct columns.')
        self.hold_to(247)
        self.show_formula(r'|i-j| = |Q(i)-Q(j)|', 'Equality indicates that two queens share a diagonal.')
        self.hold_to(268)
        self.show_formula(r'|i-j| \ne |Q(i)-Q(j)|', 'A valid arrangement requires the two distances to differ.')
        self.hold_to(292)
        self.hide_formula()

        self.chapter('WHY THE DIAGONAL RULE WORKS', 'Compare row distance with column distance')
        self.place(0,0)
        self.place(2,2, RED)
        self.conflict_line((0,0),(2,2))
        self.caption('From (1,1) to (3,3): row change = 2, column change = 2.')
        self.hold_to(312)
        self.remove_queen(2)
        self.clear_marks()
        self.place(2,3, GREEN)
        self.caption('From (1,1) to (3,4): row change = 2, column change = 3.')
        self.hold_to(330)
        self.caption('Different absolute changes mean these two squares are not diagonal.')
        self.hold_to(345)
        self.clear_queens()

        self.chapter('ONE-DIMENSIONAL REPRESENTATION', 'One column choice for each row')
        self.caption('A complete configuration can be represented by Q = [q1, q2, q3, q4].')
        self.hold_to(365)
        self.caption('The index specifies the row; the value specifies its column.')
        self.hold_to(381)
        self.caption('No separate row constraint check is needed with this representation.')
        self.hold_to(396)

        self.chapter('CONSTRUCT A VALID ARRANGEMENT', 'Q = [2, 4, 1, 3]')
        for r,c,target in [(0,1,415),(1,3,432),(2,0,449),(3,2,466)]:
            self.place(r,c)
            self.caption(f'Row {r+1} -> Column {c+1}')
            self.hold_to(target)
        self.caption('The columns 2, 4, 1 and 3 are all distinct.')
        self.hold_to(481)
        self.verify_solution()
        self.caption('Every row, column and diagonal constraint is satisfied.')
        self.hold_to(496)
        self.chapter('HOW DO WE FIND THIS ARRANGEMENT?', 'Next: brute-force search and backtracking')
        self.hold_to(510)

    def hide_formula(self):
        if self.formula_obj is not None:
            self.play(FadeOut(self.formula_obj), run_time=.4)
            self.formula_obj = None

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
