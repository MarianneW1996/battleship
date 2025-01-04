example_grid = ([(0,0),(4,5),(6,2),(9,4)])

# create a grid
def create_grid(coordinates: list):
    grid = [["." for x in range(10)] for y in range(10)]
    for i in range(len(grid)):
        for x,y in coordinates:
            grid[x][y] = 'X'
        print (grid[i])
    return grid

# user selection
def user_selection():
    coordinates = []
    number_ships_max = 20
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
    return create_grid(coordinates)

# computer selection
from random import randrange
def computer_selection():
    coordinates = []
    number_ships_max = 20
    number_ships_used = 0
    while number_ships_used <= number_ships_max:
            selection_x = randrange(0,9)
            selection_y = randrange(0,9)
            selected_position = (selection_x, selection_y)
            if selected_position not in coordinates:
                coordinates.append((selection_x, selection_y))
                number_ships_used += 1
    return create_grid(coordinates)