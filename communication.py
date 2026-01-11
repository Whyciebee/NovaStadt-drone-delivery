import heapq

# compute minimum spanning tree
def compute_communication_network(graph):

    # no nodes mean no network
    if not graph.adjacency_list:
        return 0, []

    # choose an arbitrary start node
    start_node_id = next(iter(graph.adjacency_list))

    visited_node_ids = set()
    selected_edges = []
    total_cost = 0

    priority_queue = []

    def add_outgoing_edges(from_node_id):
    
        for edge in graph.adjacency_list.get(from_node_id, []):
            if edge.restricted:
                continue

            to_node_id = edge.destination_node_id
            if to_node_id not in visited_node_ids:
                heapq.heappush(
                    priority_queue,
                    (edge.capacity, from_node_id, to_node_id)
                )

    # Prim's algorithm
    visited_node_ids.add(start_node_id)
    add_outgoing_edges(start_node_id)

    while priority_queue and len(visited_node_ids) < len(graph.adjacency_list):
        edge_cost, from_node_id, to_node_id = heapq.heappop(priority_queue)

        if to_node_id in visited_node_ids:
            continue

        # accept this edge
        visited_node_ids.add(to_node_id)
        selected_edges.append((from_node_id, to_node_id, edge_cost))
        total_cost += edge_cost

        add_outgoing_edges(to_node_id)

    # if not all nodes were reached, the graph is disconnected
    if len(visited_node_ids) != len(graph.adjacency_list):
        raise ValueError("Graph is disconnected - communication network cannot connect all stations")

    return total_cost, selected_edges