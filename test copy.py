import sys

input_text = """
1 0 4 7 6 8
0 5 4 4 5 5
2 1 4 4 4 6
4 1 3 7 4 4
"""

rows = []


def how_many_rows(input_text):
    lines = input_text.replace(' ', '')
    number = lines.count('\n')
    rows_number = number - 1
    lines_new = lines.replace('\n', '')
    list1 = list(lines_new)
    initial = 0
    final = int(len(list1) / rows_number)
    global rows
    for i in range(rows_number):
        row = list1[initial:final]
        integer_row = [int(s) for s in row]
        rows.append(integer_row)
        initial += 6
        final += 6

    return rows

columns = []


def how_many_columns(input_text):
    lines = input_text.replace(' ', '')
    number = lines.count('\n')
    rows_number = number - 1
    lines_new = lines.replace('\n', '')
    list1 = list(lines_new)
    size_list = len(list1)
    columns_number = len(rows[0])
    start_num = 0
    global columns
    for i in range(columns_number):
        column = list1[start_num:start_num + 6 * (rows_number):6]
        integer_column = [int(s) for s in column]
        columns.append(integer_column)
        start_num += 1

    return columns


def print_table(rows):
    for row in rows:
        print(" ".join(map(str, row)))


selected_num = 0
counter = 0


def trying(a, b):
    global rows, counter
    if 0 <= a < len(rows) and 0 <= b < len(rows[0]) and rows[a][b] == selected_num:
        rows[a][b] = " "
        counter += 1
        trying(a, b - 1)  # Check left
        trying(a, b + 1)  # Check right
        trying(a - 1, b)  # Check above
        trying(a + 1, b)  # Check below
        return True
    else:
        return False

score = 0


def calculating_score():
    global selected_num, counter, score
    score += counter
    return score


def check_game_over():
    global rows
    for i in range(len(rows)):
        for j in range(len(rows[0])):
            if rows[i][j] != " ":
                neighbors = [
                    (i, j - 1),  # left
                    (i, j + 1),  # right
                    (i - 1, j),  # above
                    (i + 1, j),  # below
                ]
                for neighbor in neighbors:
                    ni, nj = neighbor
                    if 0 <= ni < len(rows) and 0 <= nj < len(rows[0]) and rows[i][j] == rows[ni][nj]:
                        return False  # There are adjacent cells with the same value
    return True  # No adjacent cells with the same value


def merge_columns():
    global rows
    empty_columns = [col for col in range(len(rows[0])) if all(row[col] == " " for row in rows)]
    for col in reversed(empty_columns):
        for row in rows:
            del row[col]
    return rows


def shift_numbers_upward():
    global rows
    for col in range(len(rows[0])):
        non_empty_cells = [rows[row][col] for row in range(len(rows)) if rows[row][col] != " "]
        empty_cells = [" "] * (len(rows) - len(non_empty_cells))
        updated_column = empty_cells + non_empty_cells
        for row in range(len(rows)):
            rows[row][col] = updated_column[row]
    return rows


def printing():
    global rows, columns, selected_num, counter, score
    try:
        print_table(rows)
        print(f"Your score is: {score}")
        a, b = input("Please enter a row and a column number: ").split()
        a = int(a) - 1
        b = int(b) - 1
        selected_num = rows[a][b]
        movement_happened = trying(a, b)
        calculating_score()
        shift_numbers_upward()
        calculating_score()
        merge_columns()
        calculating_score()
        if not movement_happened:
            print("No movement happened. Try again.")
            printing()
        elif check_game_over():
            print("Game over.")
        else:
            printing()

    except (ValueError, IndexError):
        print("Please enter valid row and column numbers!")
        printing()


how_many_rows(input_text)
how_many_columns(input_text)
printing()
    