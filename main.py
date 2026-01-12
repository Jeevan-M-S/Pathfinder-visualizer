import random
from collections import deque
from typing import Hashable, Any
import arcade
from arcade.shape_list import ShapeElementList, create_line
from Algorithms.A_Star import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Maze Visualizer"

RowCount = 25
ColCount = 25

Cell_width = 500 / RowCount
Cell_height = 500 / ColCount

x_offset = (SCREEN_WIDTH - (ColCount+1)*Cell_width) / 2
y_offset = (SCREEN_HEIGHT - (RowCount-1)*Cell_height) / 2

Background_Color = arcade.color.BLACK
Wall_Color = arcade.color.WHITE
Search_Color = arcade.color.CYAN
Explored_Color = arcade.color.GOLD
Start_Color = arcade.color.GREEN
End_Color = arcade.color.RED

chance = lambda n: n >= random.randint(1,100)
Center = lambda point: (point[0]+Cell_width/2,point[1]+Cell_height/2)

#Classic Disjoint Set Union (DSU) Implementation
class UnionFind:
    def __init__(self, adj: dict[Hashable, list[tuple[Hashable, Any]]]):
        self.parent: dict[Hashable, Hashable] = {}
        self.size: dict[Hashable, int] = {}
        self.components: list[set[Hashable]] = self.partition(adj)

    # Attempts to partition the graph into disjoint sub-graphs in O(V+E)
    def partition(self, adj: dict[Hashable, list[tuple[Hashable, Any]]]) -> list[set[Hashable]]:
        if not adj:
            return []
        res: list[set[Hashable]] = []
        seen: set[Hashable] = set()
        for start in adj:
            if start in seen:
                continue
            comp: set[Hashable] = set()
            q = deque([start])
            self.parent[start] = start
            seen.add(start)
            while q:
                u = q.popleft()
                comp.add(u)
                for v, _w in adj.get(u, ()):
                    if v not in seen:
                        seen.add(v)
                        q.append(v)
                        self.parent[v] = start
            self.size[start] = len(comp)
            res.append(comp)
        return res

    # Finds representative of sub-graph in which node is present in O(log(V))
    def find(self, node: Hashable) -> Hashable:
        if node not in self.parent:
            raise KeyError(f"Node {node} is not present in the union")
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    # Joins the sub-graphs containing node1 and node2 in O(log(V))
    def unite(self, node1: Hashable, node2: Hashable) -> bool:
        if node1 not in self.parent or node2 not in self.parent:
            node = node1 if node1 not in self.parent else node2
            raise KeyError(f"Node {node} is not present in the union")
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 == root2:
            return False
        if self.size[root1] < self.size[root2]:
            root1, root2 = root2, root1
        self.parent[root2] = root1
        self.size[root1] += self.size[root2]
        del self.size[root2]
        return True

#Definition of a Cell of the maze
class Cell:
    def __init__(self):
        self.bottom_wall = True
        self.right_wall = True

#Maze generator and solver
class Maze(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(Background_Color)
        self.running = True
        self.grid = [[Cell() for j in range(ColCount)] for i in range(RowCount)]
        self.maze = None
        self.start = [0,1]
        self.end = [RowCount-2,ColCount-1]
        self.wall_list = None
        self.generator = None
        self.reached_from = {}
        self.path = []
        self.show_search = True
        self.path_delay_time = 0
        self.segment_delay_time = 0
        self.idx = 1

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

        if self.show_search:
            for child, parent in self.reached_from.items():
                if parent:
                    p1 = Center((x_offset + child[1] * Cell_width, y_offset + child[0] * Cell_height))
                    p2 = Center((x_offset + parent[1] * Cell_width, y_offset + parent[0] * Cell_height))
                    arcade.draw_line(p1[0], p1[1], p2[0], p2[1], Search_Color)

        if self.path and not self.show_search:
            points = ([(x_offset+(self.start[1]+0.5)*Cell_width, y_offset+self.start[0]*Cell_height)] +
                      [Center((x_offset + c * Cell_width, y_offset + r * Cell_height)) for r, c in self.path] +
                      [(x_offset+(self.end[1]+0.5)*Cell_width, y_offset+(self.end[0]+1)*Cell_height)])
            for i in range(1, self.idx+1):
                p1,p2 = points[i], points[i-1]
                arcade.draw_line(p1[0],p1[1],p2[0],p2[1],Explored_Color,4)

    def reachable(self,x,y,direction):
        if direction == 'L':
            return y > 1 and not self.grid[x][y-1].right_wall
        if direction == 'R':
            return y < ColCount-1 and not self.grid[x][y].right_wall
        if direction == 'U':
            return x < RowCount-2 and not self.grid[x+1][y].bottom_wall
        if direction == 'D':
            return x > 0 and not self.grid[x][y].bottom_wall
        return False

    def on_update(self, delta_time):
        if self.running:
            if self.generator is None:
                self.generator = A_Star(self.grid, self.start, self.end, self.reachable)
            try:
                if not isinstance(self.generator, str):
                    res = next(self.generator)
                    if res[0] == 'Searching':
                        _, current, self.reached_from = res
                    elif res[0] == 'Done':
                        self.path = res[1]
                        self.generator = "Done"
            except StopIteration:
                pass

            if self.generator == "Done":
                self.path_delay_time += delta_time
                if self.path_delay_time > 0.5:
                    self.show_search = False
                    self.segment_delay_time += delta_time
                    if self.segment_delay_time > 0.05:
                        if self.idx < len(self.path)+1:
                            self.idx += 1
                        self.segment_delay_time = 0.0

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
        self.start = (0,random.randint(1,ColCount-1))
        self.end = (RowCount-2,random.randint(1,ColCount-1))

        #Boundary
        for i in range(RowCount):
            self.remove_wall(i,0,1)
        for j in range(ColCount):
            if j == self.start[1]:
                self.remove_wall(0, j,1)
            elif j == self.end[1]:
                self.remove_wall(RowCount-1, j,1)
            self.remove_wall(RowCount - 1, j, 2)

        #Generate Maze
        for i in range(RowCount-1):
            for j in range(1,ColCount):
                if (i,j) == (0,ColCount-1):
                    continue
                if chance(10) and i > 0 and j < ColCount-1:
                    self.remove_wall(i,j,1)
                    self.remove_wall(i,j,2)
                elif chance(50):
                    self.remove_wall(i,j,1) if i > 0 else self.remove_wall(i,j,2)
                else:
                    self.remove_wall(i,j,2) if j < ColCount-1 else self.remove_wall(i,j,1)
                if i == 0 and chance(35):
                    self.add_wall(i,j,2)
                elif j == ColCount-1 and chance(35):
                    self.add_wall(i,j,1)

        #Guarantee a soln path exists
        adj = {}
        walls = []
        for i in range(RowCount-1):
            for j in range(1,ColCount):
                edges = []
                if self.reachable(i,j,'L'):
                    edges.append(((i,j-1),1))
                if self.reachable(i,j,'R'):
                    edges.append(((i,j+1),1))
                if self.reachable(i,j,'U'):
                    edges.append(((i+1,j),1))
                if self.reachable(i,j,'D'):
                    edges.append(((i-1,j),1))
                adj[(i,j)] = edges
                if self.grid[i][j].bottom_wall and i > 0:
                    walls.append(((i, j, 1),1))
                if self.grid[i][j].right_wall and j < ColCount-1:
                    walls.append(((i, j, 2),1))

        self.maze = UnionFind(adj)
        random.shuffle(walls)

        for wall in walls:
            if wall[0][2] == 1 and self.maze.unite((wall[0][0],wall[0][1]),(wall[0][0]-1,wall[0][1])):
                self.remove_wall(*wall[0])
            elif wall[0][2] == 2 and self.maze.unite((wall[0][0],wall[0][1]),(wall[0][0],wall[0][1]+1)):
                self.remove_wall(*wall[0])


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