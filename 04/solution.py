def init():
    with open("input.txt") as f:
        numbers = [int(n) for n in f.readline().strip().split(",")]
        lines = f.readlines()
        boards = []
        for bingo_i in range(len(lines) // 6):
            boards.append(make_board(lines[6 * bingo_i + 1:6 * bingo_i + 6]))
        return numbers, boards

def make_board(lines):
    board = []
    for index, l in enumerate(lines):
        board.append([])
        for num in l.strip().split():
            board[index].append(int(num))
    return board

def play(board, numbers):
    marked = [[False] * 5 for i in range(5)]
    for r, num in enumerate(numbers):
        for i in range(5):
            for j in range(5):
                if board[i][j] == num:
                    marked[i][j] = True
                    if has_won(marked, (i, j)):
                        return r+1, num * unmarked_score(board, marked)

def unmarked_score(board, marked):
    score = 0
    for i in range(5):
        for j in range(5):
            if not marked[i][j]:
                score += board[i][j]
    return score

def has_won(marked, new_index):
    if all(marked[new_index[0]]):
        return True
    if all([marked[i][new_index[1]] for i in range(5)]):
        return True
    return False

if __name__ == "__main__":
    numbers, boards = init()
    top_round, top_score = len(numbers), 0
    for board in boards:
        win_round, score = play(board, numbers)
        if win_round < top_round:
            top_round, top_score = win_round, score
        elif win_round == top_round and score > top_score:
            top_score = score
    print(top_score)
    
    
    bad_round, bad_score = 0, 0
    for board in boards:
        win_round, score = play(board, numbers)
        if win_round > bad_round:
            bad_round, bad_score = win_round, score
        elif win_round == bad_round and score < bad_score:
            bad_score = score
    print(bad_score)
