from __future__ import print_function
from prettytable import PrettyTable
import copy


def adjacency_list(graph):
    """
    :param graph:
    :return:
    """
    adj_list = PrettyTable()  # initialize table to hold adjacency list
    adj_list.field_names = ["Vertex", "Neighbor(s)"]  # set headers
    for vertex, neighbor in graph.items():
        adj_list.add_row([vertex, ",".join(neighbor)])
    return adj_list


def load_graph_from_file(filename):
    with open(r'{}'.format(filename), 'r') as f:
        graph = {}
        for edge in f:
            edge = edge.split()
            graph.setdefault(edge[0], []).append(edge[1])
    return _preprocess_graph(graph)


def distances(graph, source_vertex):
    return traverse(graph, source_vertex)[0]


def traversal_path(graph, source_vertex):
    return traverse(graph, source_vertex)[1]


def traverse(graph, source_vertex):
    bfs_path = []
    distances = dict.fromkeys(graph, 0)  # Set all edges distances to zero
    queue = [str(source_vertex)]  # Enqueue the source vertex
    visited = dict.fromkeys(graph, False)  # Set all vertices to unvisited
    visited[queue[0]] = True  # Flag source vertex as visited
    while queue:
        bfs_path.append(queue[0])
        dequeue = queue.pop(0)  # Dequeue vertex
        for neighbor in graph[dequeue]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True
                distances[neighbor] = distances[dequeue] + 1

    return (distances, bfs_path)


def shortest_path(graph, source_vertex, destination_vertex):
    adj_list = {}
    paths = list([source_vertex])
    while True:
        if destination_vertex in graph[source_vertex] or source_vertex == destination_vertex:
            paths.append(destination_vertex)
            break
        if not graph[source_vertex]:  # if source vertex does not have any neighbors
            return None
        for neighbor in graph[source_vertex]:
            adj_list[neighbor] = single_edge_distance(graph, neighbor, destination_vertex)
        for node in adj_list.copy():
            if adj_list[node] == 0:
                adj_list.pop(node)
        if not adj_list:
            return None
        else:
            min_edge_value = min(adj_list.values())
            min_edges = list(filter(lambda e: adj_list[e] == min_edge_value, adj_list))
            if min_edges:
                paths.append(min_edges[0])
                source_vertex = min_edges[0]
        adj_list.clear()
    return paths


def single_edge_distance(graph, v, w):
    return _multi_source_distance(graph, v, w)


def _multi_source_distance(graph, source_vertex, destination_vertex, found_w=False):
    distance = 0
    queue, track = [], []
    source_v = [source_vertex]
    while not found_w:
        for vertex in source_v:
            track.append(vertex)
            for node in graph[vertex]:
                if node not in track:
                    queue.extend([node])
        if destination_vertex in queue:
            distance += 1
            found_w = True
        else:
            if not queue:  # if queue is empty
                distance = 0
                found_w = True
            else:  # if queue is not empty
                source_v = set(queue[:])
                distance += 1
            queue.clear()
    return distance


def _preprocess_graph(graph):
    """
    Takes a graph in the form of a dictionary and verifies that for every edge member there exists a source node.
    If no source node is found from existing edge members, one is created with an empty edge [].
    :param graph:
    :return:
    """
    graph_copy = copy.deepcopy(graph)
    vertices = [vertex for edge in graph_copy.values() for vertex in edge]
    for vertex in vertices:
        if vertex not in graph_copy.keys():
            graph_copy[vertex] = []
    return graph_copy


def main():
    filename = 'edges.txt'
    source_vertex = '1'
    destination_vertex = '10'
    graph = load_graph_from_file(filename)
    print("")
    # print(f"Adjacency list (all vertices):\n{adjacency_list(graph)}")
    print("")

    def format_path(p):
        return "->".join(p)

    def format_distances_table(t):
        distance_table = PrettyTable()
        distance_table.field_names = ["Destination Vertex", "Distance (hops)"]
        for destination_vertex, distance in t.items():
            distance_table.add_row([destination_vertex, distance])
        return distance_table

    shortest = shortest_path(graph, source_vertex, destination_vertex)
    formatted_shortest = format_path(shortest)

    distances, traversal_path = traverse(graph, source_vertex)
    formatted_traversal_path = format_path(traversal_path)
    formatted_distances = format_distances_table(distances)

    print(f"BFS traversal order (starting from vertex {source_vertex}): {formatted_traversal_path}")
    print(f"Single-source distances from source vertex [{source_vertex}]:")
    print(formatted_distances)
    print(f"\nShortest path from {source_vertex} to {destination_vertex} is ["
          f"{formatted_shortest}] at a distance of "
          f"{single_edge_distance(graph, source_vertex, destination_vertex)} hop(s).")


if __name__ == "__main__":
    main()
