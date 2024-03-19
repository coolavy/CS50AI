import sys
from time import sleep

# Node structure
class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

# Stack structure
class StackFrontier(): # LIFO
    def __init__(self):
        self.frontier = []
    
    def add(self, node):
        self.frontier.append(node)
    
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

# Queue structure
class QueueFrontier(StackFrontier): # FIFO
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Maze():
    def __init__(self, filename, version):
        # Read file
        self.version = version
        with open(filename) as fl:
            contents = fl.read()

        # Validate start and end
        if contents.count("A") != 1:
            raise Exception("There must be exactly one start.")
        if contents.count("B") != 1:
            raise Exception("There must be exactly one ending.")

        # Set h/w of maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(lines) for lines in contents)

        # Keep track of walls
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.end = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")  # ??? It was colored in the video
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.end:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")

            print()
        print()

    def neighbors(self, state):
        row, col = state

        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue

        return result

    def solve(self):
        self.num_explored = 0

        start = Node(state=self.start, parent=None, action=None)

        if self.version:
            frontier = QueueFrontier()
        else:
            frontier = StackFrontier()

        frontier.add(start)

        self.explored = set()

        while True:
            if frontier.empty():
                raise Exception("NO SOLUTION FOUND")

            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.end:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            self.explored.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

def main():
    filename = input("Enter your maze txt file: ")
    filename = f".\{filename}"

    maze = Maze(filename=filename, version=0)

    maze.solve()

    print("Solving . . .")
    print()
    sleep(0.5)
    print(f"Solved in {len(maze.solution[0])} steps with Queue")
    maze.print()

    maze = Maze(filename=filename, version=1)

    maze.solve()

    print("Solving . . .")
    print()
    sleep(0.5)
    print(f"Solved in {len(maze.solution[0])} steps with Stack")
    maze.print()

    return

if __name__ == "__main__":
    main()