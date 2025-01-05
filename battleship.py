example_grid = ([(0,0),(4,5),(6,2),(9,4)])

# create a grid
def create_grid(coordinates: list, print_grid):
    grid = [["." for x in range(10)] for y in range(10)]
    for x, y in coordinates:
        grid[x][y] = 'X'
    if print_grid == True:
        for row in grid:
            print("".join(row))
    return grid

# player selection
def player_selection():
    coordinates = []
    number_ships_max = 3
    number_ships_used = 0
    while number_ships_used <= number_ships_max:
        try:
            selection_x = int(input("Position x: (0-9):"))
            selection_y = int(input("Position y: (0-9):"))
            selected_position = (selection_x, selection_y)
            if not (0 <= selection_x <= 9 and 0 <= selection_y <= 9):
                print("Position outside if the grid. Please enter values between 0 and 9!")
            elif selected_position not in coordinates:
                coordinates.append((selection_x, selection_y))
                number_ships_used += 1
            else:
                print("Position is already occupied. Please enter an new position.")
        except ValueError:
            print("Please enter values between 0 and 9!")
    return create_grid(coordinates, True)

# computer selection
from random import randrange
def computer_selection():
    coordinates = []
    number_ships_max = 3
    number_ships_used = 0
    while number_ships_used <= number_ships_max:
            selection_x = randrange(0,10)
            selection_y = randrange(0,10)
            selected_position = (selection_x, selection_y)
            if selected_position not in coordinates:
                coordinates.append((selection_x, selection_y))
                number_ships_used += 1
    return create_grid(coordinates, False)

# moving
def moving(coordinates_opponent, move_x, move_y):
    move_position = (move_x, move_y)
    if move_position in coordinates_opponent:
        coordinates_opponent.remove(move_position)
        return True
    elif move_position not in coordinates_opponent:
        return False

# gaming part (main function)
def gaming():
    number_ships_player = 3
    number_ships_computer = 3
    score_player = 0
    score_computer = 0
    ships_positions_player = player_selection()
    ships_positions_computer = computer_selection()
    while number_ships_player or number_ships_computer > 0:
        try:
            selection_x_player = int(input("Position x: (0-9):"))
            selection_y_player = int(input("Position y: (0-9):"))
            if not (0 <= selection_x_player <= 9 and 0 <= selection_y_player <= 9):
                print("Position outside if the grid. Please enter values between 0 and 9!")
            elif moving(ships_positions_computer, selection_x_player, selection_y_player) == True:
                number_ships_computer -= 1
                score_player += 1
                print("Ship destroyed!")
            else: print("You missed the ship.")
        except ValueError:
            print("Please enter values between 0 and 9!")
        selection_x_computer = randrange(0,10)
        selection_y_computer = randrange(0,10)
        if moving(ships_positions_player, selection_x_computer, selection_y_computer) == True:
            number_ships_player -= 1
            score_computer += 1
            print("The computer destroyed your ship!")
        else: print("The computer missed your ship.")
    if number_ships_player > number_ships_computer:
        print(f"Game over!\nYou won!\nYour score: {score_player}\nComputer score: {score_computer}")
    elif number_ships_player < number_ships_computer:
        print(f"Game over!\nComputer won!\nYour score: {score_player}\nComputer score: {score_computer}")
    else: print(f"\nYour score: {score_player}\nComputer score: {score_computer}")