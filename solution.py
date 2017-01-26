from collections import defaultdict
import string

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [x + y for x in A for y in B]


# CONSTANTS
ROWS = 'ABCDEFGHI'
COLS = '123456789'
BOXES = cross(ROWS, COLS)
ROW_UNITS = [cross(r, COLS) for r in ROWS]
COLUMN_UNITS = [cross(ROWS, c) for c in COLS]
SQUARE_UNITS = [cross(rs, cs)
                for rs in ('ABC', 'DEF', 'GHI')
                for cs in ('123', '456', '789')]
DIAG_UNITS = [[a + b for a, b in zip(ROWS, _cols)]
              for _cols in [COLS, ''.join(reversed(COLS))]]
_diag_unit_2 = [a + b for a, b in zip(ROWS, reversed(COLS))]
UNITLIST = ROW_UNITS + COLUMN_UNITS + SQUARE_UNITS + DIAG_UNITS
UNITS = dict((s, [u for u in UNITLIST if s in u]) for s in BOXES)
PEERS = dict((s, set(sum(UNITS[s], [])) - set([s])) for s in BOXES)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    digits = '123456789'
    chars = (c if c != '.' else digits for c in grid)
    return dict(zip(BOXES, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF':
            print(line)


# STRATEGIES

def eliminate(values):
    """
    Eliminates any assigned value as an option for every peer
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value,
            then the value will be '123456789'.
    """
    assigned = ((k, v) for k, v in values.items() if len(v) == 1)
    for box, digit in assigned:
        for peer in PEERS[box]:
            new_value = values[peer].replace(digit, '')
            assign_value(values, peer, new_value)
    return values


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    for unit in UNITLIST:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values


def build_option_map(values, unit):
    """
    Builds a map of digit options to the boxes that have those options
    Args:
        values(dict): A sudoku in dictionary form.
        unit(list): A list of boxes that belong to a unit
    Returns:
        option_map(dict): maps digit options -> boxes
    """
    option_map = defaultdict(set)
    for box, digits in ((box, values[box]) for box in unit):
        option_map[digits].add(box)
    return option_map


def filter_twins(option_map):
    """
    Filters (option, boxes) pairs out of an option_map that satisfy
    the twin criteria

    A twin occurs when when the length of the option AND the length of
    the boxes is equal to two
    """
    return ((option, boxes) for option, boxes in option_map.items() if
            (len(option) == 2) and (len(boxes) == 2))


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in UNITLIST:
        option_map = build_option_map(values, unit)
        for option, boxes in filter_twins(option_map):
            peers = (u for u in unit if u not in boxes)
            for peer in peers:
                trans = str.maketrans('', '', option)
                new_value = values[peer].translate(trans)
                assign_value(values, peer, new_value)
    return values

# Executors

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there
    is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the
    same, return the sudoku.
    Args:
        values(dict): A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box, choices in values.items()
                                    if len(choices) == 1])
        assert solved_values_before == sum(len(v)==1 for v in values.values())
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box, choices in values.items()
                                   if len(choices) == 1])
        assert solved_values_after == sum(len(v)==1 for v in values.values())
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            display(values)
            return False
    return values


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in BOXES):
        return values  # Solved!
    # Chose one of the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
