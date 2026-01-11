import json
from graph import Graph

# load drone network graph from a JSON file
def load_graph_from_json(json_file_path):
    
    """
    Expected JSON structure:

    "nodes": [
    {
      "id": "HUB",
      "name": "Central Hub",
      "type": "hub",
      "x": 0,
      "y": 0
    },
    ]
      "edges": [
    {
      "from": "HUB",
      "to": "D1",
      "energy_cost": 10,
      "capacity": 2,
      "distance": 5,
      "bidirectional": false,
      "restricted": false
    },
    ]

    """
    
    graph = Graph()

    with open(json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # add nodes
    for node in data.get("nodes", []):
        node_id = node["id"]
        node_type = node["type"]
        graph.add_node(node_id, node_type)

    # add edges
    for edge in data.get("edges", []):
        from_node_id = edge["from"]
        to_node_id = edge["to"]

        # get from JSON or default value in case data is missing
        energy_cost = edge.get("energy_cost", 0)
        capacity = edge.get("capacity", 0)
        bidirectional = edge.get("bidirectional", False)
        distance = edge.get("distance", 0.0)
        restricted = edge.get("restricted", False)

        graph.add_edge(
            from_node_id = from_node_id,
            to_node_id = to_node_id,
            energy_cost = energy_cost,
            capacity = capacity,
            bidirectional = bidirectional,
            distance = distance,
            restricted = restricted
        )

    return graph
