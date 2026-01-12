import heapq
from math import inf


def A_Star(self, start, goal, reachable):
    def manhattan_distance(p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    grid = self.grid
    rows = range(len(grid)-1)
    cols = range(1,len(grid[0]))
    distance = {start : 0}
    reached_from = {start:start}
    nodes = [(manhattan_distance(start,goal),start)]
    seen = set()
    while nodes:
        top = heapq.heappop(nodes)
        yield "Searching", top[1], reached_from
        if top[1] == goal:
            break
        seen.add(top[1])
        valid = []
        x, y = top[1]
        if reachable(x,y,'L'):
            valid.append((x,y-1))
        if reachable(x,y,'R'):
            valid.append((x,y+1))
        if reachable(x,y,'U'):
            valid.append((x+1,y))
        if reachable(x,y,'D'):
            valid.append((x-1,y))
        for v in valid:
            if v in seen:
                continue
            if distance.get(v,inf) > distance[top[1]] + 1:
                distance[v] = distance[top[1]] + 1
                score = manhattan_distance(v, goal) + distance[v]
                reached_from[v] = top[1]
                heapq.heappush(nodes,(score,v))



    if goal not in reached_from:
        return "No Solution Path Exists"

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = reached_from[node]
    path.append(start)
    yield "Done", path[::-1]

    return None