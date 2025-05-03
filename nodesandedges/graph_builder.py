import json
from collections import defaultdict

# def load_graph(input_file="enhanced_campus_routes.json"):
#     with open(input_file) as f:
#         data = json.load(f)
    
#     nodes = data["nodes"]
#     edges = data["edges"]

#     graph = defaultdict(list)

#     for start, end in edges:
#         x1, y1 = nodes[start]
#         x2, y2 = nodes[end]
#         weight = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

#         graph[start].append((end, weight))
#         graph[end].append((start, weight))  # undirected graph

#     return graph

def load_graph(input_file="enhanced_campus_routes.json"):
    with open(input_file) as f:
        data = json.load(f)
    
    nodes = data["nodes"]
    edges = data["edges"]

    graph = defaultdict(list)

    for edge in edges:
        start, end, distance, weight, bidirectional, accessible = edge
        
        graph[start].append((end, {"distance": distance, "time": weight, "shade": accessible, "lesser crowd": accessible}))
  # you can also use `weight` if preferred

        if bidirectional:
            graph[end].append((end, {"distance": distance, "time": weight, "shade": accessible, "lesser shade": accessible}))
  # add reverse edge if bidirectional is True

    return graph


def save_graph(graph, output_file="graph_structure.json"):
    # Convert defaultdict to normal dict and ensure keys are strings for JSON compatibility
    graph_dict = {str(k): v for k, v in graph.items()}

    with open(output_file, "w") as f:
        json.dump(graph_dict, f, indent=2)
    
    print(f"Saved graph structure to {output_file}")

if __name__ == "__main__":
    graph = load_graph()
    save_graph(graph)
