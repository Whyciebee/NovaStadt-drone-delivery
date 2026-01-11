# deque has faster removal from the front than Python lists
from collections import deque

# checks if all delivery nodes are reachable from hub
def reachable_from_hub(graph, hub_node_id):

    # safety check if hub actually exists
    if hub_node_id not in graph.adjacency_list:
        return False

    # track visited nodes to not loop
    visited_nodes = set()

    # start queue and start at the hub
    queue = deque([hub_node_id])
    visited_nodes.add(hub_node_id)

    # BFS (breadth-first search)
    while queue:
        current_node_id = queue.popleft()

        for edge in graph.adjacency_list.get(current_node_id, []):

            # skip no-fly corridors
            if edge.restricted:
                continue  

            next_node_id = edge.destination_node_id
            if next_node_id not in visited_nodes:
                visited_nodes.add(next_node_id)
                queue.append(next_node_id)

    # collect all delivery nodes
    delivery_node_ids = [
        node_id
        for node_id, node_type in graph.node_types.items()
        if node_type == "delivery"
    ]

    # check if every delivery node is in visited_nodes
    return all(node_id in visited_nodes for node_id in delivery_node_ids)
