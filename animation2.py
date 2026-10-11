from manim import *
from itertools import permutations
from math import factorial, comb

BG = '#101827'
WHITE_SQ = '#E5E7EB'
DARK_SQ = '#64748B'
ACCENT = '#FBBF24'
GOOD = '#22C55E'
BAD = '#FB7185'
BLUE2 = '#38BDF8'
MUTED = '#CBD5E1'

class WhyNotBruteForce(Scene):
    """Section 5: 12-minute silent, narration-paced explainer. No LaTeX dependency."""
    def construct(self):
        self.camera.background_color = BG
        self.elapsed = 0.0
        self.header = None
        self.sub = None
        self.stage = VGroup()
        self.chapter('WHY NOT BRUTE FORCE?', 'N-Queens | Search-space analysis', 45)
        self.board_choices(70)
        self.restrict_permutations(70)
        self.permutation_gallery(95)
        self.factorial_growth(90)
        self.bad_prefix(75)
        self.tree_explosion(80)
        self.validation_cost(65)
        self.side_by_side(75)
        self.conclusion(65)
        # Deliberate narration-friendly pacing; target >= 12 minutes.
        self.wait(max(0, 735 - self.elapsed))

    def play_t(self, *anims, run_time=1.0, **kwargs):
        self.play(*anims, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def wait_t(self, seconds):
        self.wait(seconds)
        self.elapsed += seconds

    def clear_stage(self):
        if len(self.stage):
            self.play_t(FadeOut(self.stage), run_time=0.6)
        self.stage = VGroup()

    def add_stage(self, *objects):
        for obj in objects:
            self.stage.add(obj)
        return objects

    def text(self, content, size=28, color=WHITE, **kwargs):
        return Text(content, font_size=size, color=color, **kwargs)

    def heading(self, title, subtitle):
        if self.header is not None:
            self.play_t(FadeOut(self.header), FadeOut(self.sub), run_time=.4)
        self.header = self.text(title, 36, ACCENT).to_edge(UP, buff=.32)
        self.sub = self.text(subtitle, 21, MUTED).next_to(self.header, DOWN, buff=.12)
        self.play_t(FadeIn(self.header), FadeIn(self.sub), run_time=.8)

    def pace(self, target, started):
        self.wait_t(max(0, target-(self.elapsed-started)))

    def chessboard(self, n=4, cell=.76, center=ORIGIN, placement=None, label=True):
        group = VGroup()
        board = VGroup()
        for r in range(n):
            for c in range(n):
                square = Square(side_length=cell, stroke_width=1, stroke_color='#CBD5E1')
                square.set_fill(WHITE_SQ if (r+c)%2==0 else DARK_SQ, opacity=1)
                square.move_to(((c-(n-1)/2)*cell)*RIGHT+(((n-1)/2-r)*cell)*UP+center)
                board.add(square)
        group.add(board)
        if placement is not None:
            for r,c in enumerate(placement):
                if c is not None:
                    q = self.text('Q', int(cell*45), '#111827', weight=BOLD)
                    q.move_to(board[r*n+c].get_center())
                    group.add(q)
        if label:
            for r in range(n):
                t=self.text(str(r+1), 16, MUTED).next_to(board[r*n], LEFT, buff=.12)
                group.add(t)
            for c in range(n):
                t=self.text(str(c+1), 16, MUTED).next_to(board[c], UP, buff=.12)
                group.add(t)
        return group, board

    def panel(self, lines, center, size=24, color=WHITE):
        return VGroup(*[self.text(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=.25).move_to(center)

    def chapter(self, title, subtitle, duration):
        start=self.elapsed
        big=self.text(title, 48, ACCENT)
        small=self.text(subtitle, 25, MUTED).next_to(big, DOWN, buff=.3)
        self.add_stage(big,small)
        self.play_t(Write(big), FadeIn(small), run_time=3)
        self.pace(duration,start)
        self.clear_stage()

    def board_choices(self, duration):
        start=self.elapsed
        self.heading('1. GENERATE, THEN TEST', 'A naive selection of N squares from N x N squares')
        board, cells=self.chessboard(center=LEFT*3.1,cell=.85)
        explanation=self.panel(['4 x 4 board = 16 squares','Choose any 4 squares','C(16, 4) = 1,820','Most choices violate the rules'], RIGHT*3.0, 27)
        self.add_stage(board,explanation)
        self.play_t(Create(board), FadeIn(explanation), run_time=3)
        for picks in [(0,1,2,3),(0,5,10,15),(1,7,8,14),(1,7,8,14)]:
            highlights=VGroup(*[cells[i].copy().set_fill(ACCENT,opacity=.65).set_stroke(ACCENT,width=3) for i in picks])
            self.play_t(FadeIn(highlights),run_time=1.1)
            self.wait_t(3)
            self.play_t(FadeOut(highlights),run_time=.5)
        self.pace(duration,start)
        self.clear_stage()

    def restrict_permutations(self,duration):
        start=self.elapsed
        self.heading('2. EXPLOIT ROW AND COLUMN RULES', 'Exactly one queen per row and column')
        board,cells=self.chessboard(center=LEFT*3.0,cell=.83,placement=[1,3,0,2])
        lines=self.panel(['Represent the board by columns:', '[2, 4, 1, 3]', 'One entry for each row', 'No repeated columns', '4! = 24 permutations'],RIGHT*3.0,26)
        self.add_stage(board,lines)
        self.play_t(FadeIn(board),FadeIn(lines),run_time=2)
        arrow=self.text('1,820  -->  24',32,GOOD).next_to(lines,DOWN,buff=.45)
        self.add_stage(arrow)
        self.play_t(Write(arrow),run_time=2)
        self.pace(duration,start)
        self.clear_stage()

    def permutation_gallery(self,duration):
        start=self.elapsed
        self.heading('3. ALL 24 COLUMN PERMUTATIONS', 'Two valid solutions; twenty-two invalid arrangements')
        perms=list(permutations(range(4)))
        gallery=VGroup()
        labels=VGroup()
        for i,p in enumerate(perms):
            col=i%8; row=i//8
            pos=LEFT*5.65+RIGHT*(col*1.62)+UP*(1.8-row*1.62)
            b,_=self.chessboard(cell=.285,center=pos,placement=p,label=False)
            valid=all(abs(p[i]-p[j])!=abs(i-j) for i in range(4) for j in range(i+1,4))
            frame=SurroundingRectangle(b,buff=.045,color=GOOD if valid else BAD,stroke_width=2)
            gallery.add(VGroup(b,frame))
            labels.add(self.text('VALID' if valid else 'X',11,GOOD if valid else BAD).next_to(frame,DOWN,buff=.04))
        self.add_stage(gallery,labels)
        for i in range(0,24,4):
            self.play_t(*[FadeIn(gallery[j]) for j in range(i,i+4)],run_time=1.8)
            self.wait_t(3)
        self.play_t(FadeIn(labels),run_time=2)
        summary=self.text('2 valid / 24 tested = 8.33%',26,ACCENT).to_edge(DOWN,buff=.35)
        self.add_stage(summary)
        self.play_t(Write(summary),run_time=2)
        self.pace(duration,start)
        self.clear_stage()

    def factorial_growth(self,duration):
        start=self.elapsed
        self.heading('4. FACTORIAL SEARCH-SPACE GROWTH', 'Column permutations increase as N!')
        values=[(4,24),(5,120),(6,720),(7,5040),(8,40320),(10,3628800),(12,479001600)]
        # Log-scaled bar heights preserve readability.
        from math import log10
        bars=VGroup(); annotations=VGroup()
        for i,(n,v) in enumerate(values):
            h=.35+.43*log10(v)
            x=-5.0+i*1.67
            rect=Rectangle(width=.85,height=h,stroke_width=0,fill_color=BLUE2,fill_opacity=.85).move_to([x,-2.2+h/2,0])
            label=self.text('N='+str(n),19).next_to(rect,DOWN,buff=.16)
            count=self.text(f'{v:,}',16,ACCENT).next_to(rect,UP,buff=.14)
            bars.add(rect);annotations.add(label,count)
        self.add_stage(bars,annotations)
        for i in range(7):
            self.play_t(GrowFromEdge(bars[i],DOWN),FadeIn(annotations[2*i]),FadeIn(annotations[2*i+1]),run_time=1.4)
            self.wait_t(3)
        note=self.text('Bar height uses a logarithmic scale',18,MUTED).to_edge(DOWN,buff=.18)
        self.add_stage(note)
        self.play_t(FadeIn(note),run_time=1)
        self.pace(duration,start)
        self.clear_stage()

    def bad_prefix(self,duration):
        start=self.elapsed
        self.heading('5. A CONFLICTING PREFIX', 'The first two queens already attack one another')
        board,cells=self.chessboard(center=LEFT*3.0,cell=.85,placement=[0,1,None,None])
        diagonal=Line(cells[0].get_center(),cells[15].get_center(),color=BAD,stroke_width=8)
        msg=self.panel(['Prefix: [1, 2]', 'Queens share a diagonal', 'Every continuation is invalid', 'Yet brute force may still finish it'],RIGHT*3.1,26)
        self.add_stage(board,diagonal,msg)
        self.play_t(FadeIn(board),Create(diagonal),FadeIn(msg),run_time=3)
        for perm in [(0,1,2,3),(0,1,3,2)]:
            full,_=self.chessboard(center=RIGHT*3.2+DOWN*1.55,cell=.35,placement=perm,label=False)
            cross=Cross(full,color=BAD,stroke_width=5)
            self.add_stage(full,cross)
            self.play_t(FadeIn(full),Create(cross),run_time=1.5)
            self.wait_t(4)
            self.play_t(FadeOut(full),FadeOut(cross),run_time=.6)
        self.pace(duration,start)
        self.clear_stage()

    def tree_explosion(self,duration):
        start=self.elapsed
        self.heading('6. A TREE OF POSSIBLE CHOICES', 'An invalid prefix has no valid descendants')
        # General row-by-row selection tree: allowing column reuse yields 4^2 continuations.
        root=self.text('[]',25,ACCENT).move_to(UP*2.2)
        first=[self.text(f'[{i}]',20) for i in range(1,5)]
        for i,node in enumerate(first):node.move_to(UP*.9+RIGHT*((i-1.5)*2.6))
        edges=VGroup(*[Line(root.get_bottom(),n.get_top(),color=MUTED) for n in first])
        self.add_stage(root,*first,edges)
        self.play_t(FadeIn(root),Create(edges),*map(FadeIn,first),run_time=3)
        branches=VGroup(); second=VGroup()
        for i,node in enumerate(first):
            for j in range(1,5):
                x=node.get_x()+(j-2.5)*.57
                dest=self.text(f'{i+1},{j}',13).move_to([x,-.6,0])
                branches.add(Line(node.get_bottom(),dest.get_top(),color='#64748B',stroke_width=1.4))
                second.add(dest)
        self.add_stage(branches,second)
        self.play_t(Create(branches),FadeIn(second),run_time=3)
        # Highlight one impossible prefix [1,2].
        target=second[1]
        box=SurroundingRectangle(target,color=BAD,buff=.12)
        cross=self.text('PRUNE THIS BRANCH',26,BAD).move_to(DOWN*2.1)
        self.add_stage(box,cross)
        self.play_t(Create(box),FadeIn(cross),run_time=2)
        explanation=self.text('For permutations, prefix [1,2] has 2 completions; both fail.',19,MUTED).to_edge(DOWN,buff=.35)
        self.add_stage(explanation)
        self.play_t(FadeIn(explanation),run_time=1)
        self.pace(duration,start)
        self.clear_stage()

    def validation_cost(self,duration):
        start=self.elapsed
        self.heading('7. VALIDATION HAS A COST', 'Pairwise diagonal checking for a complete permutation')
        board,cells=self.chessboard(center=LEFT*3,cell=.85,placement=[1,3,0,2])
        items=self.panel(['Compare every pair of queens', 'Number of pairs: N(N-1)/2', 'For N=4: 6 comparisons', 'For N=8: 28 comparisons', 'Naive total: O(N! x N^2)'],RIGHT*3,26)
        self.add_stage(board,items)
        self.play_t(FadeIn(board),FadeIn(items),run_time=3)
        pairs=list(combinations(range(4),2)) if False else [(i,j) for i in range(4) for j in range(i+1,4)]
        for i,j in pairs:
            line=Line(cells[i*4+[1,3,0,2][i]].get_center(),cells[j*4+[1,3,0,2][j]].get_center(),color=GOOD,stroke_width=5)
            self.add_stage(line)
            self.play_t(Create(line),run_time=.65)
            self.wait_t(2)
            self.play_t(FadeOut(line),run_time=.35)
        self.pace(duration,start)
        self.clear_stage()

    def side_by_side(self,duration):
        start=self.elapsed
        self.heading('8. LATE CHECKING VS EARLY REJECTION', 'Both approaches are systematic; timing of validation differs')
        left,_=self.chessboard(center=LEFT*3.3+UP*.3,cell=.62,placement=[0,1,3,2])
        right,_=self.chessboard(center=RIGHT*3.3+UP*.3,cell=.62,placement=[0,1,None,None])
        ltitle=self.text('BRUTE FORCE',26,ACCENT).next_to(left,UP,buff=.4)
        rtitle=self.text('EARLY REJECTION',26,GOOD).next_to(right,UP,buff=.4)
        lnote=self.panel(['Complete permutation','Then check conflicts','Reject entire result'],LEFT*3.3+DOWN*2.3,19)
        rnote=self.panel(['Check partial placement','Detect diagonal conflict','Never expand prefix'],RIGHT*3.3+DOWN*2.3,19)
        divider=Line(UP*2.3,DOWN*3,color='#475569')
        self.add_stage(left,right,ltitle,rtitle,lnote,rnote,divider)
        self.play_t(FadeIn(left),FadeIn(right),FadeIn(ltitle),FadeIn(rtitle),Create(divider),run_time=3)
        self.play_t(FadeIn(lnote),FadeIn(rnote),run_time=2)
        self.pace(duration,start)
        self.clear_stage()

    def conclusion(self,duration):
        start=self.elapsed
        self.heading('9. THE KEY QUESTION', 'Can we reject an impossible branch before finishing it?')
        lines=self.panel(['Brute force: generate -> validate', 'Backtracking: choose -> check -> explore -> undo', 'Reject impossible prefixes immediately', 'Next: HOW BACKTRACKING WORKS'],ORIGIN,30)
        lines[1].set_color(GOOD)
        lines[-1].set_color(ACCENT)
        self.add_stage(lines)
        for line in lines:
            self.play_t(Write(line),run_time=1.8)
            self.wait_t(3)
        self.pace(duration,start)
        self.clear_stage()
