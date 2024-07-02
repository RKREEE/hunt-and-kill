import random, time, os, colorama

colorama.init()
maze_colour = f"{colorama.Fore.WHITE}{colorama.Back.BLACK}"
start_colour = f"{colorama.Fore.GREEN}{colorama.Back.GREEN}"
end_colour = f"{colorama.Fore.RED}{colorama.Back.RED}"
reset_colour = f"{colorama.Fore.RESET}{colorama.Back.RESET}"

slept = 0
size = 20
RIGHT, LEFT, UP, DOWN = -1, 1, -size, size
last_hunted_index = 0

class Square:
    def __init__(self):
        self.walls = {'up': True, 'right': True, 'down': True, 'left': True}
        self.visited = False

def hunt_and_kill(grid, print=True):
    global slept
    index = random.randint(0, len(grid)-1)
    current_square = grid[index]
    current_square.visited = True
    
    edges = [
                [i * size for i in range(size)],
                [(i + 1) * size - 1 for i in range(size)],
                list(range(size)),
                list(range(size * (size - 1), size * size))
            ]
    edge = random.choice(edges)
    start = random.choice(edge)

    while True: 
        # kill phase
        while True:
            neighbours = get_neighbours(grid, index, visited=False)

            if print:
                os.system("cls" if os.name == "nt" else "clear")
                display_maze(grid, index, start=start)
                time.sleep(0.1)
                slept += 0.1


            if not neighbours:
                break
            
            index, direction = random.choice(neighbours)
            next_square = grid[index]

            remove_wall(next_square, current_square, direction)
            current_square = next_square
            current_square.visited = True
        
        # hunt phase
        result = find_new_square(grid)
        
        if not result:
            break
        
        new_index, neighbours = result
        index, direction = random.choice(neighbours)
        current_square = grid[index]
        next_square = grid[new_index]

        remove_wall(current_square, next_square, direction, True)
    return grid

def find_new_square(grid):
    for index, square in enumerate(grid):
        visited_neighbours = get_neighbours(grid, index, visited=True)
        if visited_neighbours and not square.visited:
            return index, visited_neighbours
        
def remove_wall(square1, square2, direction, hunt=False):
    if direction == RIGHT:
        square1.walls['right'] = False
        square2.walls['left'] = False

    elif direction == LEFT:
        square1.walls['left'] = False
        square2.walls['right'] = False

    elif direction == UP:
        square2.walls['up'] = False
        square1.walls['down'] = False

    elif direction == DOWN:
        square2.walls['down'] = False
        square1.walls['up'] = False



def get_neighbours(grid, index, visited: bool):
    neighbours = []

    invalid = [
                [i * size for i in range(size)],
                [(i + 1) * size - 1 for i in range(size)],
                list(range(size)),
                list(range(size * (size - 1), size * size))
            ]
    directions = [LEFT, RIGHT, DOWN, UP]
    for i, direction in enumerate(directions):
        if index + direction < 0 or index + direction >= len(grid):
            continue
        if index+direction not in invalid[i] and grid[index+direction].visited == visited:
            neighbours.append((index+direction, direction))


    return neighbours

def create_grid(size):
    return [Square() for _ in range(size * size)]

def display_maze(grid, index=0, start=0):
    maze_str = ""

    maze_str += f"{maze_colour}┌" + "───┬" * (size - 1) + f"───┐\n{reset_colour}"

    top = "│"
    bottom = "├"

    for i, square in enumerate(grid):

        if i != 0 and i % size == 0:
            row = f"{maze_colour}" + top + "\n" + bottom
            maze_str += row[:-1] + f"┤\n{reset_colour}"
            top = "│"
            bottom = "├"

        square_info = " "
        if i == start:
            square_info = f"{start_colour}x{maze_colour}"
        elif i == (size*size) - 1 - start:
            square_info = f"{end_colour}x{maze_colour}"

        if square.walls["right"] or (i+1) % size == 0:
            top += f" {square_info} │"
        else:
            top += f" {square_info}  "
        
        if square.walls["down"]:
            bottom += "───┼"
        else:
            bottom += "   ┼"
    
    maze_str += f"{maze_colour}" + top + f"\n{reset_colour}"
    maze_str += f"{maze_colour}└" + "───┴" * (size - 1) + f"───┘\n{reset_colour}"
    print(maze_str + colorama.Fore.RESET)

def main():
    grid = create_grid(size)
    start = time.time()
    maze = hunt_and_kill(grid)
    print(f"{round(time.time() - start, 1)}s")
    if slept: 
        print(f"{round(time.time() - start - slept, 1)}s without sleeps")

if __name__ == "__main__":
    main()
