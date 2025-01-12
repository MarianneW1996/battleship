# create a grid
def create_grid(coordinates: list, print_grid):
    grid = [["." for x in range(10)] for y in range(10)]
    for x, y in coordinates:
        grid[y][x] = 'X' # changed the coordinates from x,y to y,x because the first character is vertical and the second is horizontal, but we are used to it the other way round
    if print_grid == True: # boolean values to specify in the further code whether the grid should also be printed
        print("\nGrid:")
        for row in grid:
            print("".join(row))
    return grid

# ship class
class Ship:
    def __init__(self, size, start_x, start_y, direction):
        self.size = size
        self.start_x = start_x
        self.start_y = start_y
        self.direction = direction
        self.positions = self.calculate_position() # for calculating the position of ships larger than 1
        self.hits = []
    def calculate_position(self):
        positions = []
        for i in range(self.size):
            if self.direction == 'horizontal':
                positions.append((self.start_x + i, self.start_y))
            elif self.direction == 'vertical':
                positions.append((self.start_x, self.start_y + i))
        return positions
    def valid_position(self, coordinates, grid_size=10):
        for x, y in self.positions:
            if not (0 <= x < grid_size and 0 <= y < grid_size): # check if the coordinates are in the grid
                return False
            if (x, y) in coordinates: # check if the coordinates are already being used by another ship
                return False
        return True
    def hit(self, position):
        if position in self.positions and position not in self.hits:
            self.hits.append(position)
            return True
        return False
    def sink(self):
        return len(self.hits) == len(self.positions) # returns True if the statement is correct and False if it is not correct
        
# player selection
def player_selection(grid_size = 10):
    ships = []
    coordinates = []
    ship_sizes = [5, 3, 3, 2, 2, 2, 1, 1, 1, 1]     
    for size in ship_sizes:
        while True:
            try:
                print(f"Place your ship (size: {size}):")
                start_x = int(input("Starting Position x (0-9): "))
                start_y = int(input("Starting Position y (0-9): "))
                if size > 1:
                    direction = input("Enter the ship's direction (horizontal/vertical): ")
                else: direction = "horizontal" # for one-dimensional ships, the direction is irrelevant
                if direction not in ["horizontal", "vertical"]:
                    print("Invalid input. Please type 'horizontal' or 'vertical'.")
                    continue
                ship = Ship(size, start_x, start_y, direction)
                if ship.valid_position(coordinates, grid_size):
                    ships.append(ship)
                    coordinates.extend(ship.positions)
                    break
                else:
                    print("Invalid ship placement. Make sure the ship fits within the grid and does not overlap with others.")
            except ValueError:
                print("Position outside if the grid. Please enter values between 0 and 9!")
    create_grid(coordinates, True)
    return ships

# computer selection
from random import randrange, choice
def computer_selection(grid_size = 10):
    ships = []
    coordinates = []
    ship_sizes = [5, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    directions = ["horizontal", "vertical"]    
    for size in ship_sizes:
        while True:
            try:
                start_x = randrange(0,10)
                start_y = randrange(0,10)
                if size > 1:
                    direction = choice(directions)
                else: direction = "horizontal"
                ship = Ship(size, start_x, start_y, direction)
                if ship.valid_position(coordinates, grid_size):
                    ships.append(ship)
                    coordinates.extend(ship.positions)
                    break
            except IndexError:
                print("Error: Generated position was out of bounds. Retrying...")
    return ships

# moving
def moving(ships, move_x, move_y):
    move_position = (move_x, move_y)
    for ship in ships:
        if ship.hit(move_position):
            if ship.sink():
                print(f"Ship (size: {ship.size}) destroyed!")
                return "sunk"
            else:
                print(f"Ship (size: {ship.size}) hit!")
                return "hit"
    print("Miss! No ships were hit.")
    return "missed"

# gaming part (main function)
def gaming(grid_size = 10):
    player_ships = player_selection(grid_size)
    computer_ships = computer_selection(grid_size)
    player_hits = 0 # ships of the computer hit by the player
    player_sunken = 0 # ships of the computer sunk by the player
    computer_hits = 0
    computer_sunken = 0
    hit_previous_turn = False
    coordinates_already_used_player = [] # to prehend using the same coordinates a second time
    coordinates_already_used_computer = [] # also for the computer for a better strategy
    print("\nGame starts...")
    while len(player_ships) > 0 and len(computer_ships) > 0:
        try:
            # player's turn
            selection_x_player = (input("\nTry to hit the opponent's ship (enter \"grid\" to show which positions you already tried)!\nPosition x (0-9): "))
            selection_y_player = (input("Position y (0-9): "))
            if selection_x_player == "grid" or selection_y_player == "grid":
                create_grid(coordinates_already_used_player, True)
                continue
            selection_x_player = int(selection_x_player)
            selection_y_player = int(selection_y_player)
            selection_player = (selection_x_player, selection_y_player)
            if not (0 <= selection_x_player < grid_size and 0 <= selection_y_player < grid_size):
                print("Position outside the grid. Please enter values between 0 and 9!")
                continue
            elif selection_player in coordinates_already_used_player:
                print("You already targeted this position!")
                continue
            coordinates_already_used_player.append(selection_player)
            result = moving(computer_ships, selection_x_player, selection_y_player)
            if result == "hit":
                player_hits += 1
            elif result == "sunk":
                player_hits += 1
                player_sunken += 1
                computer_ships = [ship for ship in computer_ships if not ship.sink()]
            if len(computer_ships) == 0:
                break
            # computer's turn
            if hit_previous_turn == True: # computer strategy for moving (strategy: take positions next to a hit)
                targets =  [(x + dx, y + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)] if 0 <= x + dx < 10 and 0 <= y + dy < 10]
                selection_x_computer, selection_x_computer = choice(targets)
            else:
                selection_x_computer = randrange(0, 10)
                selection_y_computer = randrange(0, 10)
            selection_computer = (selection_x_computer, selection_y_computer)
            if selection_computer in coordinates_already_used_computer:
                continue
            coordinates_already_used_computer.append(selection_computer)
            print(f"\nComputer's attack: ({selection_x_computer}, {selection_y_computer})")
            result = moving(player_ships, selection_x_computer, selection_y_computer)
            if result == "hit":
                computer_hits += 1
                hit_previous_turn = True
                x = selection_x_computer # x, y for the computer moving strategie above
                y = selection_y_computer
            elif result == "sunk":
                computer_hits += 1
                computer_sunken += 1
                player_ships = [ship for ship in player_ships if not ship.sink()]
                hit_previous_turn = False
            else: hit_previous_turn = False
            print(f"\nYour ships: hits: {computer_hits}, sunken: {computer_sunken}\nComputer's ships: hits: {player_hits}, sunken: {player_sunken}")
        except ValueError:
            print("Invalid input. Please enter numeric values between 0 and 9.")
    if len(player_ships) > 0:
        print("Game over! Congratulations, you won!")
    elif len(computer_ships) > 0:
        print("Game over!\nThe computer won!")
    else: print("Draw!")
    print("\nFinal scores:")
    print(f"Your ships:\nhits: {player_hits}, sunken ships: {player_sunken}")
    print(f"Computer's ships:\nhits: {computer_hits}, sunken ships: {computer_sunken}")

gaming()