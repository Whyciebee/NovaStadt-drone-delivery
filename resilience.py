from collections import deque

# returns a list of edges that form a minimum cut
def find_min_cut_edges(graph, from_node_id, capacity_map):

    reachable = set([from_node_id])
    queue = deque([from_node_id])

    # BFS on residual graph
    while queue:
        current_node_id = queue.popleft()
        for next_node_id, remaining_capacity in capacity_map[current_node_id].items():
            if remaining_capacity > 0 and next_node_id not in reachable:
                reachable.add(next_node_id)
                queue.append(next_node_id)

    min_cut_edges = []

    for from_id in reachable:
        for edge in graph.adjacency_list.get(from_id, []):
            if edge.restricted:
                continue
            if edge.destination_node_id not in reachable:
                min_cut_edges.append((from_id, edge.destination_node_id))

    return min_cut_edges


# return edges that are fully used in maximum flow (bottle necks)
def find_bottleneck_edges(graph, capacity_map):

    bottlenecks = []

    for from_id in graph.adjacency_list:
        for edge in graph.adjacency_list[from_id]:
            if edge.restricted:
                continue

            if edge.capacity > 0 and capacity_map[from_id][edge.destination_node_id] == 0:
                bottlenecks.append((from_id, edge.destination_node_id))

    return bottlenecks