from __future__ import print_function
from prettytable import PrettyTable


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


def bfs_traversal(graph, source_vertex):
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
    print(f"BFS traversal order (starting from vertex {source_vertex}): {'->'.join(bfs_path)}")
    print("")
    return single_source_path_table(distances)


def multi_source_path(graph, source_vertex, destination_vertex, found_w=False):
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


def read_data(filename):
    with open(r'{}'.format(filename), 'r') as f:
        graph = {}
        for edge in f:
            edge = edge.split()
            graph.setdefault(edge[0], []).append(edge[1])
    return graph


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
    paths = "->".join(paths)
    return paths


def single_edge_distance(graph, v, w):
    return multi_source_path(graph, v, w)


def single_source_path_table(distances):
    distance_table = PrettyTable()
    distance_table.field_names = ["Destination Vertex", "Distance (hops)"]
    for destination_vertex, distance in distances.items():
        distance_table.add_row([destination_vertex, distance])
    return distance_table


def validate_graph(graph):
    """
    Takes a graph in the form of a dictionary and verifies that for every edge member there exists a source node.
    If no source node is found from existing edge members, one is created with an empty edge [].
    :param graph:
    :return:
    """
    vertices = [vertex for edge in graph.values() for vertex in edge]
    for vertex in vertices:
        if vertex not in graph.copy().keys():
            graph[vertex] = []
    return graph


def driver_code():
    filename = 'edges.txt'
    try:
        source_vertex = '1'
        destination_vertex = '10'
        graph = read_data(filename)
        validate_graph(graph)
        print("")
        # print(f"Adjacency list (all vertices):\n{adjacency_list(graph)}")
        print("")
        print(f"Single-source distance from source vertex [{source_vertex}]:\n{bfs_traversal(graph, source_vertex)}")
        print(f"\nShortest path from {source_vertex} to {destination_vertex} is ["
              f"{shortest_path(graph, source_vertex, destination_vertex)}] at a distance of "
              f"{single_edge_distance(graph, source_vertex, destination_vertex)} hop(s).")
    except KeyError:
        source_vertex = None
        print("Source vertex {} not found in graph.".format(source_vertex))
    return


if __name__ == "__main__":
    driver_code()
