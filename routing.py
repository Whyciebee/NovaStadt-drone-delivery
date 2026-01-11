import heapq

# find the lowest energy route, ignoring restricted corridors
def dijkstra(graph, start_node_id, target_node_id):

    # if start or target node doesn't exist route is not possible
    if start_node_id not in graph.node_types or target_node_id not in graph.node_types:
        return [], float("inf")

    priority_queue = [(0.0, start_node_id)]

    # dist[node_id] = best known distance so far
    dist = {node_id: float("inf") for node_id in graph.node_types}
    dist[start_node_id] = 0.0

    # previous[node_id] = node_id before it on the best path
    previous = {}

    while priority_queue:
        current_cost, current_node_id = heapq.heappop(priority_queue)

        # process only the best (known) version
        if current_cost != dist[current_node_id]:
            continue

        # reached target
        if current_node_id == target_node_id:
            break

        # explore outgoing edges
        for edge in graph.adjacency_list.get(current_node_id, []):

            # gg go next
            if edge.restricted:
                continue

            next_node_id = edge.destination_node_id
            new_cost = current_cost + edge.energy_cost

            # check for improvement and update best path
            if new_cost < dist[next_node_id]:
                dist[next_node_id] = new_cost
                previous[next_node_id] = current_node_id
                heapq.heappush(priority_queue, (new_cost, next_node_id))

    # if destination was never reached
    if dist[target_node_id] == float("inf"):
        return [], float("inf")

    # reconstruct path by walking backwards from target to start
    path = [target_node_id]
    while path[-1] != start_node_id:
        path.append(previous[path[-1]])
    path.reverse()

    return path, dist[target_node_id]
