import random
import arcade
from arcade.shape_list import ShapeElementList, create_line

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Maze solver"

RowCount = 50
ColCount = 50

Cell_width = 500 / RowCount
Cell_height = 500 / ColCount

x_offset = (SCREEN_WIDTH - (ColCount+1)*Cell_width) / 2
y_offset = (SCREEN_HEIGHT - (RowCount-1)*Cell_height) / 2

Background_Color = arcade.color.BLACK
Wall_Color = arcade.color.WHITE
Search_Color = arcade.color.CYAN
Explored_Color = arcade.color.BLUE
Start_Color = arcade.color.GREEN
End_Color = arcade.color.RED

chance = lambda n: n >= random.randint(1,100)
Center = lambda x,y: (x+Cell_width/2,y+Cell_height/2)

class Cell:
    def __init__(self):
        self.bottom_wall = False
        self.right_wall = False
        self.visited = True

class Maze(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Maze Visualizer")
        arcade.set_background_color(Background_Color)
        self.running = False
        self.grid = [[Cell() for j in range(ColCount)] for i in range(RowCount)]
        self.start = [0,1]
        self.end = [RowCount-2,ColCount-1]
        self.wall_list = None

    def on_draw(self):
        self.clear()
        if self.wall_list:
            self.wall_list.draw()

        row, col = self.start
        x = x_offset + col * Cell_width
        y = y_offset + row * Cell_height
        arcade.draw_line(x, y, x+Cell_width, y, Start_Color)

        row, col = self.end
        x = x_offset + col * Cell_width
        y = y_offset + row * Cell_height
        arcade.draw_line(x, y+Cell_height, x+Cell_width, y+Cell_height, End_Color)

    def on_update(self, delta_time):
        if self.running:
            pass

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE:
            self.running = not self.running

    def reset_grid(self):
        self.grid = [[Cell() for j in range(ColCount)] for i in range(RowCount)]
        self.start = [0,1]
        self.end = [RowCount-2,ColCount-1]

    def add_wall(self,row,col,wall_type):
        if wall_type == 1:
            self.grid[row][col].bottom_wall = True
        elif wall_type == 2:
            self.grid[row][col].right_wall = True

    def remove_wall(self,row,col,wall_type):
        if wall_type == 1:
            self.grid[row][col].bottom_wall = False
        elif wall_type == 2:
            self.grid[row][col].right_wall = False

    def generate_grid(self, row, col):
        self.start = [0,random.randint(1,ColCount-1)]
        self.end = [RowCount-2,random.randint(1,ColCount-1)]

        for i in range(RowCount-1):
            self.add_wall(i,0,2)
            self.add_wall(i,ColCount-1,2)
        for j in range(1,ColCount):
            if j != self.start[1]:
                self.add_wall(0, j,1)
            if j != self.end[1]:
                self.add_wall(RowCount-1, j,1)

        add = lambda x,y: (x[0]+y[0],x[1]+y[1])
        path_stack = []
        path = set()
        fails = set()
        i,j = self.start
        dirs = [(1,0),(0,1),(-1,0),(0,-1)]
        while [i,j] != self.end:
            valid = []
            for d in dirs:
                if (0 <= i+d[0] < RowCount-1 and 0 < j+d[1] < ColCount and
                        add((i,j),d) not in path and add((i,j),d) not in fails):
                    valid.append(d)
            if j in [1,ColCount-1] and (-1,0) in valid:
                valid.remove((-1,0))
            if i == RowCount-2:
                if j < self.end[1] and (0,-1) in valid:
                    valid.remove((0,-1))
                elif j > self.end[1] and (0,1) in valid:
                    valid.remove((0,1))
            if not valid:
                fails.add((i,j))
                if (i,j) in path:
                    path.remove((i,j))
                    path_stack.pop()
                (i,j) = path_stack[-1]
                continue
            if (i,j) not in path:
                path.add((i,j))
                path_stack.append((i,j))
            (i,j) = add((i,j),random.choice(valid))
        path.add((i,j))
        path_stack.append((i,j))

        diff = 0
        for i in range(RowCount-1):
            for j in range(1, ColCount):
                valid = [1,2]
                in_path = False
                if (i,j) in path:
                    in_path = True
                    idx = path_stack.index((i,j))
                    prev = path_stack[idx-1] if idx > 0 else None
                    next = path_stack[idx+1] if idx+1 < len(path_stack) else None
                    if (i-1, j) in [prev, next]:
                        valid.remove(1)
                    if (i,j+1) in [prev, next]:
                        valid.remove(2)
                if not valid:
                    continue
                if 1 in valid and 2 in valid:
                    if in_path and chance(85):
                        right = True
                        bottom = True
                    elif chance(5):
                        right = True
                        bottom = True
                    else:
                        right = bottom = False
                        if chance(50+diff):
                            bottom = True
                        else:
                            right = True
                else:
                    base = 90 if in_path else 50
                    bottom = chance(base+diff) if 1 in valid else False
                    right = chance(base-diff) if 2 in valid else False
                if chance(9.35):
                    continue
                if bottom:
                    diff -= 1
                    self.add_wall(i, j,1)
                if right:
                    diff += 1
                    self.add_wall(i, j,2)

        self.wall_list = ShapeElementList()
        for row in range(RowCount):
            for col in range(ColCount):
                x = x_offset + col * Cell_width
                y = y_offset + row * Cell_height
                if self.grid[row][col].right_wall:
                    line = create_line(x+Cell_width, y, x+Cell_width, y+Cell_height, Wall_Color)
                    self.wall_list.append(line)
                if [row,col] == self.start:
                    continue
                if self.grid[row][col].bottom_wall:
                    line = create_line(x, y, x+Cell_width, y, Wall_Color)
                    self.wall_list.append(line)

if __name__ == "__main__":
    maze = Maze()
    maze.generate_grid(RowCount,ColCount)
    arcade.run()