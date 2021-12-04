from pprint import pprint

board_size = 5
boards = []


def check_for_winner(marks):
    for index, board in enumerate(marks):
        # check rows
        for row in board:
            if all(row):
                return index

        # check cols
        for col_index in range(len(board[0])):
            if all(row[col_index] for row in board):
                return index

    return None


def check_for_winners(marks):
    for index, board in enumerate(marks):
        # check rows
        for row in board:
            if all(row):
                yield index

        # check cols
        for col_index in range(len(board[0])):
            if all(row[col_index] for row in board):
                yield index


def get_unmarked_sum(marks, board):
    sum = 0
    for row_index, row in enumerate(board):
        for col_index, cell in enumerate(row):
            if not marks[row_index][col_index]:
                sum += cell
    return sum


with open("day4.in") as f:
    order = [int(i) for i in f.readline().split(",")]

    for line in f:
        if not line.strip():
            boards.append([])
        else:
            boards[-1].append([int(i) for i in line.split()])


marked = [[[False for k in range(5)] for j in range(5)] for i in range(len(boards))]

last_num = 0
unmarked_sum = 0
for number in order:
    for board_index, board in enumerate(boards):
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == number:
                    marked[board_index][row_index][col_index] = True

    winning_index = check_for_winner(marked)
    if winning_index is not None:
        last_num = number
        unmarked_sum = get_unmarked_sum(marked[winning_index], boards[winning_index])
        break

print(last_num * unmarked_sum)

# part 2

marked = [[[False for k in range(5)] for j in range(5)] for i in range(len(boards))]
last_num = 0
unmarked_sum = 0
winning_boards = set()
for number in order:
    for board_index, board in enumerate(boards):
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == number:
                    marked[board_index][row_index][col_index] = True

    for winning_index in check_for_winners(marked):
        if winning_index not in winning_boards:
            winning_boards.add(winning_index)
            last_num = number
            unmarked_sum = get_unmarked_sum(marked[winning_index], boards[winning_index])

print(last_num * unmarked_sum)
