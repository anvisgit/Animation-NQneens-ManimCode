from manim import *

BG = "#101827"
LIGHT = "#E5E7EB"
DARK = "#64748B"
RED = "#EF4444"
GREEN = "#22C55E"
GOLD = "#FBBF24"

class QueenBoard(VGroup):
    def __init__(self, n=4, square_size=1.05):
        super().__init__()
        self.n = n
        self.square_size = square_size
        self.squares = VGroup()
        for r in range(n):
            for c in range(n):
                square = Square(side_length=square_size, stroke_width=1, stroke_color=BG)
                square.set_fill(LIGHT if (r+c)%2 == 0 else DARK, opacity=1)
                square.move_to(RIGHT*(c-(n-1)/2)*square_size + DOWN*(r-(n-1)/2)*square_size)
                self.squares.add(square)
        self.add(self.squares)

    def cell(self, r, c):
        return self.squares[r*self.n+c]

    def queen(self, r, c, color=GOLD):
        q = Text("♛", font_size=49, color=color)
        q.move_to(self.cell(r,c).get_center())
        return q

    def highlight(self, r, c, color=RED):
        return self.cell(r,c).copy().set_fill(color, opacity=0.68).set_stroke(color, width=1)

class QueenMovement(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("How does a queen attack?", font_size=36, color=WHITE).to_edge(UP)
        board = QueenBoard()
        board.shift(DOWN*0.25)
        self.play(Write(title), FadeIn(board), run_time=1.5)
        q = board.queen(1,1)
        self.play(FadeIn(q, scale=0.6))
        groups = [
            ("Same row", [(1,c) for c in range(4) if c!=1]),
            ("Same column", [(r,1) for r in range(4) if r!=1]),
            ("Both diagonals", [(r,c) for r in range(4) for c in range(4) if abs(r-1)==abs(c-1) and (r,c)!=(1,1)]),
        ]
        label = Text("", font_size=26)
        label.next_to(board, DOWN, buff=0.35)
        for name, cells in groups:
            new_label = Text(name, font_size=26, color=WHITE).next_to(board, DOWN, buff=0.35)
            marks = VGroup(*[board.highlight(r,c) for r,c in cells])
            self.play(Transform(label,new_label), FadeIn(marks), run_time=0.8)
            self.wait(1.5)
            self.play(FadeOut(marks), run_time=0.5)
        self.wait(0.5)

class InvalidPlacement(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("An invalid placement", font_size=36).to_edge(UP)
        board = QueenBoard()
        board.shift(DOWN*0.25)
        self.play(Write(title), FadeIn(board))
        first = board.queen(0,0)
        second = board.queen(1,1)
        self.play(FadeIn(first))
        self.wait(0.5)
        self.play(FadeIn(second))
        conflict = Line(first.get_center(), second.get_center(), color=RED, stroke_width=10)
        cross = Text("✕", font_size=55, color=RED).move_to(second)
        message = Text("Diagonal conflict!", font_size=27, color=RED).next_to(board, DOWN, buff=0.35)
        self.play(Create(conflict), FadeIn(cross), Write(message))
        self.wait(2)

class ValidSolution(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("A valid 4-Queens arrangement", font_size=34).to_edge(UP)
        board = QueenBoard()
        board.shift(DOWN*0.25)
        self.play(Write(title), FadeIn(board))
        columns = [1,3,0,2]  # Zero-based columns: 2,4,1,3 in the narration
        queens = VGroup()
        for row, col in enumerate(columns):
            queen = board.queen(row,col)
            queens.add(queen)
            self.play(FadeIn(queen, scale=0.7), Indicate(board.cell(row,col), color=GREEN), run_time=0.8)
            self.wait(0.4)
        outline = SurroundingRectangle(board, color=GREEN, buff=0.08, stroke_width=5)
        caption = Text("Q = [2, 4, 1, 3]", font_size=30, color=GREEN).next_to(board, DOWN, buff=0.3)
        self.play(Create(outline), Write(caption))
        self.wait(2)
