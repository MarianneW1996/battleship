example_grid = ([(0,0),(4,5),(6,2),(9,4)])

# create a grid
def create_grid(coordinates: list):
    grid = [["." for x in range(10)] for y in range(10)]
    for i in range(len(grid)):
        for x,y in coordinates:
            grid[x][y] = 'X'
        print (grid[i])
    return grid
create_grid(example_grid)