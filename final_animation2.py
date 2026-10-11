from manim import *
from itertools import permutations
from math import factorial, comb

BG = '#0B1220'
INK = '#F8FAFC'
MUTED = '#CBD5E1'
GOLD = '#FBBF24'
GREEN = '#4ADE80'
RED = '#FB7185'
BLUE = '#38BDF8'
PALE = '#E2E8F0'
DARK = '#64748B'


def is_valid(p):
    return all(abs(p[i] - p[j]) != j - i for i in range(len(p)) for j in range(i + 1, len(p)))


class WhyNotBruteForceSilent(Scene):
    """12-minute silent educational video. All timing is in seconds."""

    def construct(self):
        self.camera.background_color = BG
        self.clock = 0.0
        self.active = VGroup()
        self.top = None
        self.explanation = None
        self.results = {}
        for n in range(1, 9):
            valid = [p for p in permutations(range(n)) if is_valid(p)]
            self.results[n] = (factorial(n), len(valid), valid)
        self.introduction(65)
        self.naive_search(65)
        self.permutation_reduction(65)
        self.enumeration(190)
        self.factorial_growth(65)
        self.redundancy(65)
        self.search_tree(65)
        self.validation(65)
        self.comparison(65)
        self.conclusion(65)
        # 775 seconds = 12 minutes 55 seconds, plus negligible frame rounding.
        print(f'Planned Manim timeline: {self.clock:.1f} seconds')

    def play_for(self, *animations, seconds=1, **kwargs):
        self.play(*animations, run_time=seconds, **kwargs)
        self.clock += seconds

    def hold(self, seconds):
        if seconds > 0:
            self.wait(seconds)
            self.clock += seconds

    def stage(self, *mobjects):
        self.active.add(*mobjects)
        return mobjects

    def reset(self, heading, subtitle):
        if len(self.active):
            self.play_for(FadeOut(self.active), seconds=.6)
        self.active = VGroup()
        title = Text(heading, font_size=34, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=.25)
        subtitle = Text(subtitle, font_size=19, color=MUTED)
        subtitle.next_to(title, DOWN, buff=.12)
        self.stage(title, subtitle)
        self.play_for(FadeIn(title), FadeIn(subtitle), seconds=.8)
        self.top = subtitle
        self.explanation = None

    def txt(self, content, size=24, color=INK):
        return Text(str(content), font_size=size, color=color)

    def paragraph(self, lines, size=23, color=INK):
        return VGroup(*[self.txt(line, size, color) for line in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=.16
        )

    def explain(self, lines, seconds=12):
        """Replace the reading card and keep it on screen for the requested time."""
        if isinstance(lines, str):
            lines = [lines]
        text = self.paragraph(lines, size=22)
        text.scale_to_fit_width(min(text.width, 11.8))
        text.to_edge(DOWN, buff=.36)
        box = SurroundingRectangle(text, color='#334155', buff=.22, corner_radius=.12)
        box.set_fill('#162238', opacity=.95)
        group = VGroup(box, text)
        if self.explanation is not None:
            self.play_for(FadeOut(self.explanation), seconds=.3)
            self.active.remove(self.explanation)
        self.stage(group)
        self.play_for(FadeIn(group), seconds=.45)
        self.explanation = group
        self.hold(max(0, seconds - .75))

    def fit(self, obj, max_w=12.1, max_h=4.8):
        if obj.width > max_w:
            obj.scale_to_fit_width(max_w)
        if obj.height > max_h:
            obj.scale_to_fit_height(max_h)
        return obj

    def board(self, n=4, queens=(), cell=None, labels=True):
        if cell is None:
            cell = min(.85, 4.1 / n)
        grid = VGroup()
        for r in range(n):
            for c in range(n):
                sq = Square(side_length=cell, stroke_width=.8, stroke_color='#94A3B8')
                sq.set_fill(PALE if (r+c) % 2 == 0 else DARK, opacity=1)
                sq.move_to(RIGHT * (c-(n-1)/2)*cell + UP*((n-1)/2-r)*cell)
                grid.add(sq)
        result = VGroup(grid)
        for r, c in enumerate(queens):
            if c is None:
                continue
            q = self.txt('Q', max(12, int(cell*40)), '#111827')
            q.move_to(grid[r*n+c].get_center())
            result.add(q)
        if labels and n <= 5:
            for r in range(n):
                t = self.txt(str(r+1), 15, MUTED).next_to(grid[r*n], LEFT, buff=.08)
                result.add(t)
            for c in range(n):
                t = self.txt(str(c+1), 15, MUTED).next_to(grid[c], UP, buff=.08)
                result.add(t)
        return result

    def replace_visual(self, old, new, seconds=.6):
        if old is not None:
            self.play_for(FadeOut(old), seconds=.25)
            self.active.remove(old)
        self.stage(new)
        self.play_for(FadeIn(new), seconds=seconds)
        return new

    def finish_at(self, start, duration):
        self.hold(max(0, start + duration - self.clock))

    def introduction(self, duration):
        start = self.clock
        self.reset('01  |  WHAT IS BRUTE FORCE?', 'Generate a complete candidate. Then test it.')
        visual = self.board(4, (0, 1, 2, 3)).shift(UP*.25)
        self.stage(visual)
        self.play_for(FadeIn(visual), seconds=1)
        self.explain(['We have four queens and a 4 x 4 chessboard.',
                      'Brute force tries candidate placements without using diagonal',
                      'conflicts to stop construction early.'], 16)
        for p in [(0, 1, 2, 3), (0, 2, 3, 1), (1, 3, 0, 2)]:
            new = self.board(4, p).shift(UP*.25)
            visual = self.replace_visual(visual, new, .8)
            self.explain([f'Candidate columns: {[x+1 for x in p]}',
                          'VALID arrangement' if is_valid(p) else 'INVALID: at least two queens share a diagonal.'], 12)
        self.finish_at(start, duration)

    def naive_search(self, duration):
        start = self.clock
        self.reset('02  |  THE NAIVE SEARCH SPACE', 'Choosing N squares from N x N squares')
        b = self.board(4).shift(UP*.3)
        self.stage(b)
        self.play_for(FadeIn(b), seconds=1)
        self.explain(['A 4 x 4 board has 16 squares. We must choose exactly 4.',
                      'If we ignore all row, column and diagonal restrictions,',
                      'the number of unordered choices is C(16, 4).'], 19)
        equation = self.txt('C(16, 4) = 16! / (4! x 12!) = 1,820', 29, GOLD).shift(UP*.35)
        b = self.replace_visual(b, equation, .8)
        self.explain(['1,820 counts selections of four distinct squares.',
                      'Many contain two queens in the same row or column.',
                      'These are impossible solutions from the outset.'], 18)
        self.explain(['We can reduce the number of candidates before checking diagonals.',
                      'This reduction does not yet require backtracking.'], 16)
        self.finish_at(start, duration)

    def permutation_reduction(self, duration):
        start = self.clock
        self.reset('03  |  REDUCE THE CANDIDATES', 'Exactly one queen in every row and every column')
        board = self.board(4, (0, 2, 1, 3)).shift(UP*.3)
        self.stage(board)
        self.play_for(FadeIn(board), seconds=.8)
        self.explain(['Since four queens must occupy four different rows,',
                      'we can choose exactly one column for each row.'], 15)
        self.explain(['Columns must also be different. Therefore the column list',
                      'must be a permutation of [1, 2, 3, 4].'], 16)
        board = self.replace_visual(board, self.txt('4! = 4 x 3 x 2 x 1 = 24', 35, GOLD).shift(UP*.3))
        self.explain(['Candidate count: 1,820  ->  24.',
                      'This permutation-based brute force guarantees unique rows',
                      'and columns, but it still checks diagonal validity afterward.'], 17)
        self.finish_at(start, duration)

    def enumeration(self, duration):
        start = self.clock
        self.reset('04  |  ENUMERATE N = 1 TO 8', 'Real exhaustive permutation counts, summarized visually')
        visual = None
        allocations = [15, 16, 18, 31, 22, 22, 23, 29]
        for n, allotted in zip(range(1, 9), allocations):
            t = self.clock
            total, good, valid = self.results[n]
            chosen = valid[0] if valid else tuple(range(n))
            board = self.board(n, chosen, labels=(n <= 5)).shift(LEFT*2.9+UP*.12)
            status = 'Example valid solution' if valid else 'No valid solution exists'
            detail = self.paragraph([
                f'N = {n}', f'Complete permutations: {total:,}',
                f'Valid arrangements: {good:,}',
                f'Invalid arrangements: {total-good:,}', status
            ], size=24)
            detail.move_to(RIGHT*2.15+UP*.15)
            next_visual = VGroup(board, detail)
            visual = self.replace_visual(visual, next_visual, .55)
            if n <= 4:
                self.explain([f'For N = {n}, brute force generates all {total:,} permutations.',
                              'Each complete arrangement is checked for diagonal attacks.',
                              f'Exactly {good} pass the test.'], 9)
                if n == 4:
                    gallery = VGroup()
                    for idx, p in enumerate(permutations(range(4))):
                        item = self.board(4, p, cell=.17, labels=False)
                        item.add(SurroundingRectangle(item, color=GREEN if is_valid(p) else RED,
                                                      buff=.03, stroke_width=1.2))
                        gallery.add(item)
                    gallery.arrange_in_grid(rows=4, cols=6, buff=(.17,.17))
                    gallery.move_to(UP*.12)
                    visual = self.replace_visual(visual, gallery, .7)
                    self.explain(['All 24 permutations are displayed here.',
                                  'Green outlines: 2 valid. Red outlines: 22 invalid.'], 11)
            else:
                self.explain([f'For N = {n}, the program still evaluates every permutation.',
                              f'That means {total:,} complete candidates, but only {good:,} solutions.',
                              'The animation summarizes them rather than displaying each individually.'], 11)
            self.finish_at(t, allotted)
        self.finish_at(start, duration)

    def factorial_growth(self, duration):
        start = self.clock
        self.reset('05  |  FACTORIAL GROWTH', 'Permutations increase rapidly as the board expands')
        ns = [4, 5, 6, 7, 8, 10, 12]
        values = [factorial(n) for n in ns]
        bars = VGroup()
        max_log = 9
        import math
        for n, value in zip(ns, values):
            h = .25 + 3.3 * math.log10(value) / max_log
            rect = Rectangle(width=.75, height=h, stroke_width=0, fill_color=BLUE, fill_opacity=.95)
            label = self.txt(str(n), 19, MUTED).next_to(rect, DOWN, buff=.14)
            bars.add(VGroup(rect, label))
        bars.arrange(RIGHT, buff=.36, aligned_edge=DOWN).move_to(UP*.1)
        self.stage(bars)
        self.play_for(LaggedStart(*[GrowFromEdge(g[0], DOWN) for g in bars], lag_ratio=.16), seconds=4)
        self.explain(['This chart uses a logarithmic height scale.',
                      'N! = N x (N-1) x ... x 2 x 1.',
                      'Each additional row multiplies the number of permutations.'], 18)
        self.explain(['N=8: 40,320 permutations. N=10: 3,628,800.',
                      'N=12: 479,001,600 complete permutations.',
                      'The number of candidates quickly becomes enormous.'], 19)
        self.finish_at(start, duration)

    def redundancy(self, duration):
        start = self.clock
        self.reset('06  |  REDUNDANT COMPUTATION', 'An invalid prefix cannot become valid later')
        b = self.board(4, (0, 1, None, None)).shift(UP*.2)
        self.stage(b)
        self.play_for(FadeIn(b), seconds=.9)
        self.explain(['Row 1, column 1 and row 2, column 2 share a diagonal.',
                      'The first two queens already violate the rules.'], 17)
        self.explain(['The unused columns are 3 and 4.',
                      'Exactly 2! = 2 column permutations extend this prefix:',
                      '[1, 2, 3, 4] and [1, 2, 4, 3].'], 18)
        b = self.replace_visual(b, self.board(4, (0, 1, 2, 3)).shift(UP*.2))
        self.explain(['Both complete candidates are invalid.',
                      'The diagonal conflict in rows 1 and 2 never disappears.',
                      'Yet complete-permutation brute force still checks them.'], 17)
        self.finish_at(start, duration)

    def search_tree(self, duration):
        start = self.clock
        self.reset('07  |  SEARCH-TREE EXPLOSION', 'Every decision creates possible continuations')
        root = self.txt('START', 22, GOLD).move_to(UP*2)
        first = [self.txt(f'[{i}]', 21, INK).move_to(UP*.85+RIGHT*(i-2.5)*2.0) for i in range(1,5)]
        lines = [Line(root.get_bottom(), x.get_top(), color=BLUE, stroke_width=2) for x in first]
        tree = VGroup(root, *lines, *first)
        self.stage(tree)
        self.play_for(FadeIn(tree), seconds=2)
        self.explain(['The first queen has four possible columns.',
                      'For each first choice, the second queen has three remaining columns.',
                      'Then two, then one: 4 x 3 x 2 x 1 = 24 leaves.'], 17)
        prefix = self.txt('[1, 2]', 31, RED).move_to(DOWN*.25)
        branch = Line(first[0].get_bottom(), prefix.get_top(), color=RED)
        subtree = VGroup(prefix, branch)
        self.stage(subtree)
        self.play_for(FadeIn(subtree), seconds=1)
        self.explain(['The branch [1, 2] already has a diagonal conflict.',
                      'It has 2! = 2 complete permutation leaves, both invalid.',
                      'For N queens, a fixed prefix of length k has (N-k)! completions.'], 19)
        self.explain(['This is the source of redundant work:',
                      'complete enumeration continues even when a prefix is impossible.'], 15)
        self.finish_at(start, duration)

    def validation(self, duration):
        start = self.clock
        self.reset('08  |  COST OF VALIDATION', 'Checking every pair of queens')
        b = self.board(4, (1, 3, 0, 2)).shift(UP*.35)
        self.stage(b)
        self.play_for(FadeIn(b), seconds=1)
        self.explain(['After generating a complete permutation, test its diagonals.',
                      'For each pair of rows i and j, compare column differences.',
                      'A diagonal conflict occurs if |i-j| = |Q[i]-Q[j]|.'], 19)
        b = self.replace_visual(b, self.txt('Number of pairs = N(N-1)/2', 32, GOLD).shift(UP*.4))
        self.explain(['There are C(N, 2) = N(N-1)/2 possible queen pairs.',
                      'A straightforward full pairwise check costs O(N^2).',
                      'It can stop early if a conflict is detected.'], 18)
        self.explain(['Combining all N! permutations with O(N^2) validation gives',
                      'an O(N^2 x N!) upper bound for this simple implementation.',
                      'This is an upper bound, not the cost of every possible validator.'], 17)
        self.finish_at(start, duration)

    def comparison(self, duration):
        start = self.clock
        self.reset('09  |  COMPLETE TESTING VS EARLY REJECTION', 'Two ways to handle the same conflicting prefix')
        left = RoundedRectangle(width=5.7, height=3.7, corner_radius=.15, color=RED)
        right = RoundedRectangle(width=5.7, height=3.7, corner_radius=.15, color=GREEN)
        left.move_to(LEFT*3.05+UP*.3)
        right.move_to(RIGHT*3.05+UP*.3)
        ltext = self.paragraph(['BRUTE FORCE', 'Generate full permutations', '[1, 2, 3, 4]  ->  reject',
                                '[1, 2, 4, 3]  ->  reject'], size=21).move_to(left)
        rtext = self.paragraph(['EARLY REJECTION', 'Inspect prefix [1, 2]', 'Diagonal conflict detected',
                                'Do not generate its children'], size=21).move_to(right)
        panels = VGroup(left, right, ltext, rtext)
        self.stage(panels)
        self.play_for(FadeIn(panels), seconds=1.5)
        self.explain(['Both methods enforce the same final N-Queens constraints.',
                      'The difference is WHEN a conflict is used.',
                      'Early rejection avoids extending an already invalid prefix.'], 20)
        self.explain(['The right-hand side previews pruning; it is not a full solver yet.',
                      'The next section explains recursive backtracking in detail.'], 18)
        self.finish_at(start, duration)

    def conclusion(self, duration):
        start = self.clock
        self.reset('10  |  WHY NOT BRUTE FORCE?', 'The motivation for backtracking')
        summary = self.paragraph([
            '1. Naive square selection creates many invalid candidates.',
            '2. Column permutations reduce the search to N! candidates.',
            '3. Diagonal conflicts invalidate most complete permutations.',
            '4. A failed partial arrangement cannot be repaired by adding queens.',
            '5. Detecting conflicts earlier can eliminate unnecessary continuations.'
        ], size=22).move_to(UP*.45)
        self.fit(summary, max_w=11.5)
        self.stage(summary)
        self.play_for(FadeIn(summary), seconds=1.2)
        self.explain(['The central question:',
                      'Why finish generating an arrangement that is already invalid?'], 20)
        self.explain(['NEXT: BACKTRACKING',
                      'Choose  ->  Check  ->  Explore  ->  Undo',
                      'Reject impossible partial configurations before expanding them.'], 20)
        self.finish_at(start, duration)
