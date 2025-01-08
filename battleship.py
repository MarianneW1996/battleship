example_grid = ([(0,0),(4,5),(6,2),(9,4)])

### Ships are no longer only single spaces, but create 1x five
### space big ships, 2x three space big ships, and 3x two space ones. If a player or
### computer hits a ship, tell them the size of their target.

# ships:
# 1x five spaces
# 2x three spaces
# 3x two spaces
# 4x one space

# create a grid
def create_grid(coordinates: list, print_grid):
    grid = [["." for x in range(10)] for y in range(10)]
    for x, y in coordinates:
        grid[x][y] = 'X'
    if print_grid == True:
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
        self.positions = self.calculate_position()
        self.hits = []
    def calculate_position(self):
        positions = []
        for i in range(self.size):
            if self.direction == 'horizontal':
                positions.append((self.start_x, self.start_y + i))
            elif self.direction == 'vertical':
                positions.append((self.start_x + i, self.start_y))
        return positions
    def valid_position(self, coordinates, grid_size=10):
        for x, y in self.positions:
            if not (0 <= x < grid_size and 0 <= y < grid_size):
                return False
            if (x, y) in coordinates:
                return False
        return True
    def hit(self, position):
        if position in self.positions and position not in self.hits:
            self.hits.append(position)
            return True
        return False
    def sink(self):
        return len(self.hits) == len(self.positions)
        
# player selection
def player_selection(grid_size = 10):
    ships = []
    coordinates = []
    ship_sizes = [5, 3, 3, 2, 2, 2, 1, 1, 1, 1]     
    for size in ship_sizes:
        while True:
            try:
                print(f"Create your ship (size: {size}):")
                start_x = int(input("Starting Position x (0-9): "))
                start_y = int(input("Starting Position y (0-9): "))
                if size > 1:
                    direction = input("Enter a direction for the ship (horizontal/vertical): ")
                else: direction = "horizontal"
                if direction not in ["horizontal", "vertical"]:
                    print("Invalid direction. Please enter 'horizontal' or 'vertical'.")
                    continue
                ship = Ship(size, start_x, start_y, direction)
                if ship.valid_position(coordinates, grid_size):
                    ships.append(ship)
                    coordinates.extend(ship.positions)
                    break
                else:
                    print("Invalid ship placement. Try again.")
            except ValueError:
                print("Position outside if the grid. Please enter values between 0 and 9!")
    player_grid = create_grid(coordinates, True)
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
                print(f"Ship (size: {ship.size} destroyed!")
                return "sunk"
            else:
                print(f"Ship (size: {ship.size} hit!")
                return "hit"
            return True
    print("No ships hit.")
    return "missed"

# gaming part (main function)
def gaming(grid_size = 10):
    coordinates = []
    number_ships_max = 10
    player_ships = player_selection(grid_size)
    computer_ships = computer_selection(grid_size)
    player_hits = 0
    player_sunken = 0
    computer_hits = 0
    computer_sunken = 0
    print("Game starts")
    while len(player_ships) > 0 and len(computer_ships) > 0:
        try:
            # player's turn
            selection_x_player = int(input("Position x (0-9): "))
            selection_y_player = int(input("Position y (0-9): "))
            if not (0 <= selection_x_player < grid_size and 0 <= selection_y_player < grid_size):
                print("Position outside the grid. Please enter values between 0 and 9!")
                continue
            result = moving(computer_ships, selection_x_player, selection_y_player)
            if result == "hit":
                player_hits += 1
            elif result == "sunk":
                player_hits += 1
                player_sunken += 1
                computer_ships = [ship for ship in computer_ships if not ship.sink()]
            print(f"Player: Hits: {player_hits}, Sunken Ships: {player_sunken}")
            if len(computer_ships) == 0:
                break
            # computer's turn
            selection_x_computer = randrange(0, 10)
            selection_y_computer = randrange(0, 10)
            print(f"Computer attacks: ({selection_x_computer}, {selection_y_computer})")
            result = moving(player_ships, selection_x_computer, selection_y_computer)
            if result == "hit":
                computer_hits += 1
            elif result == "sunk":
                computer_hits += 1
                computer_sunken += 1
                player_ships = [ship for ship in player_ships if not ship.sink()]
            print(f"Computer: Hits: {computer_hits}, Sunken Ships: {computer_sunken}")
        except ValueError:
            print("Invalid input. Please enter numeric values between 0 and 9.")
    if len(player_ships) > 0:
        print("Game over!\nYou won!")
    elif len(computer_ships) > 0:
        print("Game over!\nComputer won!")
    else: print("Draw!")
    print("\nFinal scores:")
    print(f"Player:\nhits: {player_hits}, sunken ships: {player_sunken}")
    print(f"Computer:\nhits: {computer_hits}, sunken ships: {computer_sunken}")
gaming()