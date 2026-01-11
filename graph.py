# Quick Python note: if we don't do "self", all objects have the same stuff. 
# Example: "adjacency_list = {}" -> all Graphs now share the SAME adjacency list


# directed corridor from a node to another (Hub -> CH1)
class Edge:
    def __init__(self, destination_node_id, energy_cost, capacity, distance=0.0, restricted=False):
        self.destination_node_id = destination_node_id
        self.energy_cost = float(energy_cost)
        self.capacity = int(capacity)
        self.distance = float(distance)
        self.restricted = bool(restricted)


# directed graph, using adjacency list
# adjacency list = list of edge objects leaving a specific node (Hub: CH1, D1...)
class Graph:
    def __init__(self):
        self.node_types = {}
        self.adjacency_list = {}

    def add_node(self, node_id, node_type):
        self.node_types[node_id] = node_type

        # ensure adjacency list exists
        if node_id not in self.adjacency_list:
            self.adjacency_list[node_id] = []

    # add a directed edge from -> to
    def add_edge(self, from_node_id, to_node_id, energy_cost, capacity, bidirectional=False, distance=0.0, restricted=False):

        # safety check, ensure both nodes are in adjacency list
        if from_node_id not in self.adjacency_list:
            self.adjacency_list[from_node_id] = []
        if to_node_id not in self.adjacency_list:
            self.adjacency_list[to_node_id] = []

        self.adjacency_list[from_node_id].append(
            Edge(to_node_id, energy_cost, capacity, distance=distance, restricted=restricted)
        )

        # if bidirectional=True, add the reverse edge ("to -> from")
        if bidirectional:
            self.adjacency_list[to_node_id].append(
                Edge(from_node_id, energy_cost, capacity, distance=distance, restricted=restricted)
            )

    # update corridor to restricted/unrestricted
    def set_edge_restriction(self, from_node_id, to_node_id, bidirectional=False, restricted=True):
        updated_any = False

        for edge in self.adjacency_list.get(from_node_id, []):
            if edge.destination_node_id == to_node_id:
                edge.restricted = bool(restricted)
                updated_any = True

        # set the same for reverse
        if bidirectional:
            for edge in self.adjacency_list.get(to_node_id, []):
                if edge.destination_node_id == from_node_id:
                    edge.restricted = bool(restricted)
                    updated_any = True

        return updated_any
