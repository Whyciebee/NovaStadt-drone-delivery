from network_io import load_graph_from_json
from reachability import reachable_from_hub
from routing import dijkstra
from capacity import edmonds_karp
from resilience import find_bottleneck_edges, find_min_cut_edges
from communication import compute_communication_network
from modify_network import set_no_fly_zone, clear_no_fly_zone


HELP_TEXT = """
Available commands:

  reach <hub>
      Check if all nodes are reachable from hub (enter ID even if you have only 1 hub)

  route <start> <target>
      Shortest path using Dijkstra

  flow <source> <sink>
      Maximum delivery capacity (Max Flow)

  resilience <source> <sink>
      Bottlenecks and minimum cut

  mst
      Communication network (Minimum Spanning Tree)

  nofly <u> <v>
      Add no-fly zone

  clear <u> <v>
      Remove no-fly zone

  help
      Show this help

  exit
      Quit program
"""

# IF YOU WANNA CHANGE THE TESTDATA, DO SO IN CODE HERE:
def main():
    print("Drone Network Test Console")
    print("Loading network...")
    graph = load_graph_from_json("drone_testdata_1.json") # <--------
    print("Network loaded.")
    print("Type 'help' for commands.")

    while True:
        try:
            command = input("\n> ").strip()
        except EOFError:
            break

        if not command:
            continue

        parts = command.split()
        cmd = parts[0].lower()

        if cmd == "exit":
            print("Bye.")
            break

        elif cmd == "help":
            print(HELP_TEXT)

        elif cmd == "reach" and len(parts) == 2:
            hub = parts[1]
            result = reachable_from_hub(graph, hub)
            print("All delivery nodes reachable:", result)

        elif cmd == "route" and len(parts) == 3:
            start, target = parts[1], parts[2]
            path, cost = dijkstra(graph, start, target)
            if path:
                print("Path:", " -> ".join(path))
                print("Cost:", cost)
            else:
                print("No path found.")

        elif cmd == "flow" and len(parts) == 3:
            source, sink = parts[1], parts[2]
            max_flow, _ = edmonds_karp(graph, source, sink)
            print("Maximum flow:", max_flow)

        elif cmd == "resilience" and len(parts) == 3:
            source, sink = parts[1], parts[2]
            max_flow, flow_map = edmonds_karp(graph, source, sink)

            bottlenecks = find_bottleneck_edges(graph, flow_map)
            min_cut = find_min_cut_edges(graph, source, flow_map)

            print("Max flow:", max_flow)
            print("Bottlenecks:", bottlenecks)
            print("Min-cut edges:", min_cut)

        elif cmd == "mst":
            cost, edges = compute_communication_network(graph)
            print("Total cost:", cost)
            for u, v, w in edges:
                print(f"{u} -- {v} ({w})")

        elif cmd == "nofly" and len(parts) >= 3:
            u, v = parts[1], parts[2]
            bidir = len(parts) == 4 and parts[3].lower() == "true"
            ok = set_no_fly_zone(graph, u, v, bidir)
            print("No-fly zone added:", ok)

        elif cmd == "clear" and len(parts) >= 3:
            u, v = parts[1], parts[2]
            bidir = len(parts) == 4 and parts[3].lower() == "true"
            ok = clear_no_fly_zone(graph, u, v, bidir)
            print("No-fly zone removed:", ok)

        else:
            print("Unknown or invalid command. Type 'help'.")


if __name__ == "__main__":
    main()
