from __future__ import annotations
from four_in_a_row import *
from a0 import *
from a0 import _is_diagonal


def square_repr(self):
    if self.symbol is None:
        return f"Square({self.coord}, None)"
    else:
        return f"Square({self.coord}, '{self.symbol}')"


Square.__repr__ = square_repr


def line_repr(self):
    return f"Line({self.cells})"


Line.__repr__ = line_repr


class TestTask0:
    def test_init(self):
        fiar = FourInARow(6, True, False)
        assert fiar.result == -1
        assert fiar.p1_to_play
        assert fiar.p1_human
        assert not fiar.p2_human


class TestTask1:

    def test_within_grid_in_grid(self):
        assert within_grid((0, 0), 4)

    def test_within_grid_outside_grid(self):
        assert not within_grid((4, 4), 4)
        assert not within_grid((5, 3), 4)
        assert not within_grid((2, 5), 4)

    def test_all_within_grid_all_in_grid(self):
        assert all_within_grid([(0, 0), (1, 1), (2, 2), (3, 3)], 4)
        assert all_within_grid([], 4)
        assert not all_within_grid([(1, 6), (0, 0), (2, 2), (3, 3)], 4)
        assert not all_within_grid([(0, 0), (3, 5), (2, 2), (3, 3)], 4)

    def test_reflect_vertically(self):
        assert reflect_vertically((0, 1), 5) == (4, 1)
        assert reflect_vertically((2, 1), 5) == (2, 1)
        assert reflect_vertically((3, 1), 5) == (1, 1)
        assert reflect_vertically((2, 2), 4) == (1, 2)
        assert reflect_vertically((2, 2), 6) == (3, 2)
        assert reflect_vertically((1, 2), 6) == (4, 2)

    def test_reflect_points(self):
        assert reflect_points([(0, 1), (1, 2)], 5) == [(4, 1), (3, 2)]
        assert reflect_points([(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)], 5) == [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)]


class TestTask2:

    def test_is_diagonal(self):

        squares = create_squares(5)
        assert _is_diagonal([squares[0][0], squares[1][1], squares[2][2],
                             squares[3][3], squares[4][4]], False)
        assert _is_diagonal([squares[1][0], squares[2][1], squares[3][2],
                             squares[4][3]], False)
        assert not _is_diagonal([squares[0][0], squares[2][2],
                                 squares[3][3], squares[4][4]], False)
        assert not _is_diagonal([squares[0][0], squares[1][2], squares[2][2],
                                 squares[3][3], squares[4][4]], False)

        assert _is_diagonal([squares[4][0], squares[3][1], squares[2][2],
                             squares[1][3], squares[0][4]], True)
        assert _is_diagonal([squares[4][1], squares[3][2], squares[2][3],
                             squares[1][4]], True)
        assert not _is_diagonal([squares[4][0], squares[2][2],
                                 squares[1][3], squares[0][4]], True)
        assert not _is_diagonal([squares[4][1], squares[4][2], squares[2][3],
                                 squares[1][4]], True)
        assert not _is_diagonal([squares[0][0], squares[1][1], squares[2][2],
                                 squares[3][3], squares[4][4]], True)
        assert not _is_diagonal([squares[4][0], squares[3][1], squares[2][2],
                                 squares[1][3], squares[0][4]], False)

    def test_line_method(self):
        squares = create_squares(5)
        line = Line([squares[0][1], squares[1][1], squares[2][1], squares[3][1], squares[4][1]])
        from random import choice
        for i in range(4, -1, -1):
            assert not line.is_full()
            symbol = choice(['O', 'X'])
            assert line.drop(symbol) == i
            assert squares[i][1].symbol == symbol
        assert line.is_full()

    def test_fiar(self):
        squares = create_squares(5)
        line = Line([squares[0][1], squares[1][1], squares[2][1], squares[3][1],
                     squares[4][1]])
        for s in line:
            assert not line.has_fiar(s.coord)
        for s in line:
            s.symbol = 'X'
        for s in line:
            assert line.has_fiar(s.coord)

    def test_fiar_2(self):
        squares = create_squares(5)
        line = Line([squares[0][1], squares[1][1], squares[2][1], squares[3][1],
                     squares[4][1]])
        for s in line:
            s.symbol = 'X'
        squares[2][1].symbol = 'O'
        for s in line:
            assert not line.has_fiar(s.coord)

    def test_fiar_3(self):
        squares = create_squares(5)
        temp = [squares[0][1], squares[1][1], squares[2][1], squares[3][1],
                squares[4][1]]
        line = Line(temp)
        for s in temp[1:]:
            s.symbol = 'X'
        for s in temp:
            assert line.has_fiar(s.coord)
        temp[-1].symbol = None
        for s in temp:
            assert not line.has_fiar(s.coord)


class TestTask3:

    def test_grid_init(self):
        grid = Grid(5)
        assert len(grid._rows) == len(grid._columns) == 5
        for i in range(5):
            for j in range(5):
                assert grid._rows[i][j] is grid._columns[j][i]

        assert len(grid._mapping) == 25
        coords_of_diagonals = get_coords_of_diagonals(5)

        for coord, lines in grid._mapping.items():
            count = self._count_diagonals(coords_of_diagonals, coord)
            assert len(lines) == 2 + count
            assert is_row(lines[0].cells)
            assert is_column(lines[1].cells)
            assert len(lines) != 3 or is_diagonal(lines[2].cells)
            assert len(lines) != 4 or (_is_diagonal(lines[2].cells, False)
                                       and _is_diagonal(lines[3].cells, True))

    def _count_diagonals(self, coords_of_diagonals, coord):
        count = 0
        for diagonal in coords_of_diagonals:
            if coord in diagonal:
                count += 1
        return count

    def test_get_down_diagonal_starts(self):
        assert get_down_diagonal_starts(4) == [(0, 0)]
        assert get_down_diagonal_starts(5) == [(1, 0), (0, 0), (0, 1)]
        assert get_down_diagonal_starts(6) == [(2, 0), (1, 0), (0, 0), (0, 1), (0, 2)]

    def test_down_diagonal(self):
        assert get_down_diagonal((0, 0), 4) == [(0, 0), (1, 1), (2, 2), (3, 3)]
        assert get_down_diagonal((0, 0), 5) == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
        assert get_down_diagonal((1, 0), 5) == [(1, 0), (2, 1), (3, 2), (4, 3)]

    def test_get_all_down_diagonals(self):
        assert get_all_down_diagonals(4) == [[(0, 0), (1, 1), (2, 2), (3, 3)]]
        expected = [[(1, 0), (2, 1), (3, 2), (4, 3)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                    [(0, 1), (1, 2), (2, 3), (3, 4)]]

        assert get_all_down_diagonals(5) == expected
        expected = [[(2, 0), (3, 1), (4, 2), (5, 3)],
                    [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
                    [(0, 2), (1, 3), (2, 4), (3, 5)]]

        assert get_all_down_diagonals(6) == expected

    def test_get_coords_of_diagonals(self):
        expected = [[(0, 0), (1, 1), (2, 2), (3, 3)], [(3, 0), (2, 1), (1, 2), (0, 3)]]
        assert get_coords_of_diagonals(4) == expected
        expected = [[(1, 0), (2, 1), (3, 2), (4, 3)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
                    [(0, 1), (1, 2), (2, 3), (3, 4)],
                    [(3, 0), (2, 1), (1, 2), (0, 3)],
                    [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)],
                    [(4, 1), (3, 2), (2, 3), (1, 4)]]

        assert get_coords_of_diagonals(5) == expected
        expected = [[(2, 0), (3, 1), (4, 2), (5, 3)],
                    [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
                    [(0, 2), (1, 3), (2, 4), (3, 5)],
                    [(3, 0), (2, 1), (1, 2), (0, 3)],
                    [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)],
                    [(5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)],
                    [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)],
                    [(5, 2), (4, 3), (3, 4), (2, 5)]]
        assert get_coords_of_diagonals(6) == expected

    def test_all_diagonals(self):
        expected = [[(0, 0), (1, 1), (2, 2), (3, 3)],
                    [(3, 0), (2, 1), (1, 2), (0, 3)]]
        diagonals = all_diagonals(create_squares(4))
        assert len(diagonals) == 2
        for i in range(2):
            assert len(diagonals[i]) == len(expected[i])
            for j in range(len(diagonals[i])):
                assert diagonals[i][j].coord == expected[i][j]

        expected = [[(2, 0), (3, 1), (4, 2), (5, 3)],
                    [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)],
                    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
                    [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
                    [(0, 2), (1, 3), (2, 4), (3, 5)],
                    [(3, 0), (2, 1), (1, 2), (0, 3)],
                    [(4, 0), (3, 1), (2, 2), (1, 3), (0, 4)],
                    [(5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)],
                    [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)],
                    [(5, 2), (4, 3), (3, 4), (2, 5)]]

        diagonals = all_diagonals(create_squares(6))
        assert len(diagonals) == 10
        for i in range(10):
            assert len(diagonals[i]) == len(expected[i])
            for j in range(len(diagonals[i])):
                assert diagonals[i][j].coord == expected[i][j]


if __name__ == '__main__':
    import pytest
    pytest.main()
