def blank_board(width, height):
    """
    This function should return a "2-D array" that
    we can use to represent a 2-D board for a game
    like Tic-Tac-Toe or Battleships. For more on
    using 2-D arrays, see:

    * https://robertheaton.com/2018/06/12/programming-projects-for-advanced-beginners-ascii-art/
    * https://robertheaton.com/2018/07/20/project-2-game-of-life/
    * https://robertheaton.com/2018/10/09/programming-projects-for-advanced-beginners-3-a/
    """
    board = []
    row = []
    for _ in range(height):
        for _ in range(width):
            row.append(None)
        board.append(row)
        return board

if __name__ == "__main__":
    test_board = blank_board(4, 3)

    expected_board = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    # TODO: it looks like there's a bug with our
    # blank-board generating function! We should
    # figure out what it is and fix it so that
    # this test passes.
    if test_board == expected_board:
        print("TEST PASSED!!")
    else:
        print("TEST FAILED!!")
