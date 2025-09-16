import sys
import json
import math  # If you want to use math.inf for infinity
import netfuncs
import copy

class Graph:
    def __init__(self):
        self._nodes = set()
        self._edges = {}

    def add_node(self, a):
        self._nodes.add(a)
        self._edges[a] = {}
        
    def update_edge(self, a, b, w):
        if a not in self._nodes:
            self.add_node(a)
        if b not in self._nodes:
            self.add_node(b)
            
        self._edges[a][b] = w

    def get_neighbors(self, a):
        neighbors = None
        if a in self._nodes:
            neighbors = self._edges[a]

        return copy.deepcopy(neighbors)

    def get_distance(self, source, dest):
        return self._edges[source][dest]


    def get_edges(self):
        return copy.deepcopy(self._edges)
        
    def get_nodes(self):
        return copy.deepcopy(self._nodes)


def dijkstra(graph, source):
    not_visited = graph.get_nodes()
    parents = dict.fromkeys(not_visited, None)
    distances = dict.fromkeys(not_visited, math.inf)
    distances[source] = 0

    while not_visited:
        min_dist = math.inf
        min_node = None
        for node in not_visited:
            current_dist = distances[node]
            if current_dist < min_dist:
                min_node = node
                min_dist = distances[node]
        
        neighbors = graph.get_neighbors(min_node)

        for neighbor in neighbors:
            current_dist= graph.get_distance(min_node, neighbor) + min_dist
            if current_dist< distances[neighbor]:
                distances[neighbor] = current_dist
                parents[neighbor] = min_node

        not_visited.remove(min_node)
        
    return distances, parents

def get_path(parents, dest):
    next_node = dest
    path = []
    while next_node:
        path.append(next_node)
        next_node = parents[next_node]

    path.reverse()
    return path

def build_router_graph(routers):
    graph = Graph()
    for router in routers:
        for connection in routers[router]['connections']:
            weight = routers[router]['connections'][connection]['ad']
            graph.update_edge(router, connection, weight)
            
    return graph

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    To search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...p

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """

    src_router = netfuncs.find_router_for_ip(routers, src_ip)
    dest_router = netfuncs.find_router_for_ip(routers, dest_ip)
    graph = build_router_graph(routers)
    nodes = graph.get_nodes()

    if src_router == dest_router:
        return []

    edges = graph.get_edges()

    distances, parents = dijkstra(graph, src_router)
    return get_path(parents, dest_router)


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):

    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
