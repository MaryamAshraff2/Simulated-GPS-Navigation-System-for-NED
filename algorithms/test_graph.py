# # algorithms/test_graph.py
# import sys
# import os

# # Add parent directory to path to import algorithms
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from algorithms.dijkstra import dijkstra
# from algorithms.astar import astar

# def create_test_graph():
#     """Create a simple test graph"""
#     return {
#         "nodes": [
#             {"id": 0, "x": 0, "y": 0, "name": "A"},
#             {"id": 1, "x": 1, "y": 1, "name": "B"},
#             {"id": 2, "x": 2, "y": 0, "name": "C"}
#         ],
#         "edges": [
#             {"from": 0, "to": 1, "distance": 1.0, "time": 2.0},
#             {"from": 1, "to": 2, "distance": 1.0, "time": 2.0}
#         ]
#     }

# def test_shortest_path():
#     graph = create_test_graph()
#     print("\nTesting simple path A -> B -> C")
    
#     # Dijkstra test
#     d_path, d_dist = dijkstra(graph, 0, 2)
#     path_names = [graph['nodes'][n]['name'] for n in d_path]
#     print("Dijkstra path:", " -> ".join(path_names))
#     print("Dijkstra distance:", d_dist)
    
#     # A* test
#     a_path, a_dist = astar(graph, 0, 2)
#     path_names = [graph['nodes'][n]['name'] for n in a_path]
#     print("A* path:", " -> ".join(path_names))
#     print("A* distance:", a_dist)
    
#     assert d_path == [0, 1, 2]
#     assert a_path == [0, 1, 2]
#     assert d_dist == 2.0
#     assert a_dist == 2.0

# def test_no_path():
#     graph = create_test_graph()
#     graph["edges"] = []  # Remove all edges
    
#     print("\nTesting no path scenario")
#     d_path, d_dist = dijkstra(graph, 0, 2)
#     assert d_path == []
#     assert d_dist == float('infinity')
#     print("No path test passed")

# def test_same_node():
#     graph = create_test_graph()
    
#     print("\nTesting same start and end node")
#     d_path, d_dist = dijkstra(graph, 0, 0)
#     assert d_path == [0]
#     assert d_dist == 0
#     print("Same node test passed")

# if __name__ == "__main__":
#     print("=== ALGORITHM CORRECTNESS TESTS ===")
#     test_shortest_path()
#     test_no_path()
#     test_same_node()
#     print("\nAll tests passed successfully!")