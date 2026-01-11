# defaultdict automatically creates missing dictionary entries
from collections import deque, defaultdict

# computes maximum number of drones per hour from source to sink
def edmonds_karp(graph, from_node_id, to_node_id):
    
    # flow not possible if either node doesn't exist 
    if from_node_id not in graph.node_types or to_node_id not in graph.node_types:
        return 0

    # capacity_map[u][v] = remaining capacity from u to v
    capacity_map = defaultdict(lambda: defaultdict(int))

    # build the initial capacity map from graph edges
    for source_node_id in graph.adjacency_list:
        for edge in graph.adjacency_list[source_node_id]:

            if edge.restricted:
                continue

            # safety: avoid infinity in max-flow
            if edge.capacity == float("inf"):
                raise ValueError("Got infinity, expected finite capacity")

            capacity_map[source_node_id][edge.destination_node_id] += int(edge.capacity)

    total_flow = 0

    while True:
        # find an augmenting path with BFS
        parent = {from_node_id: None}
        queue = deque([from_node_id])

        # stop early if we reach sink
        while queue and to_node_id not in parent:
            current_node_id = queue.popleft()

            for next_node_id, remaining_capacity in capacity_map[current_node_id].items():
                if remaining_capacity > 0 and next_node_id not in parent:
                    parent[next_node_id] = current_node_id
                    queue.append(next_node_id)

        # no augmenting path found
        if to_node_id not in parent:
            break

        # compute bottleneck capacity along the path
        path_flow = float("inf")
        node_id = to_node_id
        while parent[node_id] is not None:
            previous_node_id = parent[node_id]
            path_flow = min(path_flow, capacity_map[previous_node_id][node_id])
            node_id = previous_node_id

        # update residual capacities
        node_id = to_node_id
        while parent[node_id] is not None:
            previous_node_id = parent[node_id]

            capacity_map[previous_node_id][node_id] -= path_flow
            capacity_map[node_id][previous_node_id] += path_flow  # reverse edge in residual graph

            node_id = previous_node_id

        total_flow += path_flow

    return total_flow, capacity_map
