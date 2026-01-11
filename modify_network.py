# mark corridor as restricted
def set_no_fly_zone(graph, from_node_id, to_node_id, also_reverse=False):
    return graph.set_edge_restriction(
        from_node_id,
        to_node_id,
        bidirectional=also_reverse,
        restricted=True
    )

# remove restriction from corridor
def clear_no_fly_zone(graph, from_node_id, to_node_id, also_reverse=False):
    return graph.set_edge_restriction(
        from_node_id,
        to_node_id,
        bidirectional=also_reverse,
        restricted=False
    )
