def DFS(self, start, goal, reachable):
    grid = self.grid
    reached_from = {start:start}
    stack = [start]
    seen = set()
    while stack:
        current = stack.pop()
        if current == goal:
            break
        seen.add(current)
        valid = []
        x, y = current
        if reachable(x, y, 'L'):
            valid.append((x, y - 1))
        if reachable(x, y, 'R'):
            valid.append((x, y + 1))
        if reachable(x, y, 'U'):
            valid.append((x + 1, y))
        if reachable(x, y, 'D'):
            valid.append((x - 1, y))
        for v in valid:
            if v in seen:
                continue
            stack.append(v)
            reached_from[v] = current

        yield "Searching", current, reached_from

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