from collections import deque


def BFS(self, start, goal, reachable):
    grid = self.grid
    q = deque([start])
    reached_from = {start:start}
    seen = {start}
    while q:
        node = q.popleft()
        yield "Searching", node, reached_from
        if node == goal:
            break
        if reachable(*node,'L'):
            next_node = (node[0],node[1]-1)
            if next_node not in seen:
                reached_from[next_node] = node
                q.append(next_node)
                seen.add(next_node)
        if reachable(*node, 'R'):
            next_node = (node[0],node[1]+1)
            if next_node not in seen:
                reached_from[next_node] = node
                q.append(next_node)
                seen.add(next_node)
        if reachable(*node, 'U'):
            next_node = (node[0]+1,node[1])
            if next_node not in seen:
                reached_from[next_node] = node
                q.append(next_node)
                seen.add(next_node)
        if reachable(*node, 'D'):
            next_node = (node[0]-1,node[1])
            if next_node not in seen:
                reached_from[next_node] = node
                q.append(next_node)
                seen.add(next_node)

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