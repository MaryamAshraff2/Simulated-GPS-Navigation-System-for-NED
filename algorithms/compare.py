# # algorithms/compare.py
# import time
# import json
# import os
# from dijkstra import dijkstra
# from astar import astar

# def load_graph():
#     """Robust graph loading with path handling"""
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     json_path = os.path.abspath(os.path.join(script_dir, '../nodesandedges/enhanced_campus_routes.json'))
    
#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"Graph JSON not found at: {json_path}")
    
#     with open(json_path) as f:
#         return json.load(f)

# class AlgorithmComparator:
#     def __init__(self):
#         self.graph = load_graph()
#         self.node_names = {node['id']: node['name'] for node in self.graph['nodes']}
    
#     def compare_routes(self, start, end):
#         """Compare pathfinding between two nodes"""
#         print(f"\nComparing routes from {self.node_names[start]} to {self.node_names[end]}")
#         print("="*60)
        
#         # Test Dijkstra
#         start_time = time.perf_counter()
#         d_path, d_dist = dijkstra(self.graph, start, end)
#         d_time = time.perf_counter() - start_time
        
#         # Test A*
#         start_time = time.perf_counter()
#         a_path, a_dist = astar(self.graph, start, end)
#         a_time = time.perf_counter() - start_time
        
#         # Results
#         print("\nDIJKSTRA'S ALGORITHM")
#         print(f"Path: {' → '.join(self.node_names[n] for n in d_path)}")
#         print(f"Distance: {d_dist:.2f} units")
#         print(f"Time: {d_time:.6f} seconds")
#         print(f"Nodes visited: {len(d_path)}")
        
#         print("\nA* ALGORITHM")
#         print(f"Path: {' → '.join(self.node_names[n] for n in a_path)}")
#         print(f"Distance: {a_dist:.2f} units")
#         print(f"Time: {a_time:.6f} seconds")
#         print(f"Nodes visited: {len(a_path)}")
        
#         print("\nCOMPARISON")
#         print(f"Time difference: {(d_time-a_time):.6f} seconds (A* is {d_time/a_time:.1f}x faster)")
#         print(f"Distance difference: {(d_dist-a_dist):.2f} units")
#         print(f"Path length difference: {len(d_path)-len(a_path)} nodes")

#     def performance_test(self, test_cases=5):
#         """Run multiple test cases automatically"""
#         nodes = [node['id'] for node in self.graph['nodes']]
        
#         for i in range(test_cases):
#             start = nodes[i % len(nodes)]
#             end = nodes[(i + 3) % len(nodes)]  # Ensure different end points
            
#             print(f"\n\nPERFORMANCE TEST CASE {i+1}")
#             self.compare_routes(start, end)

#     def show_node_list(self):
#         """Display all available nodes"""
#         print("\nAVAILABLE NODES:")
#         for node in self.graph['nodes']:
#             print(f"{node['id']}: {node['name']}")

# if __name__ == "__main__":
#     comparator = AlgorithmComparator()
    
#     print("UNIVERSITY NAVIGATION ALGORITHM COMPARISON")
#     print("="*60)
    
#     comparator.show_node_list()
    
#     while True:
#         try:
#             print("\nEnter node IDs to compare (or 'q' to quit)")
#             start = input("Start node ID: ")
#             if start.lower() == 'q':
#                 break
#             end = input("End node ID: ")
#             if end.lower() == 'q':
#                 break
            
#             comparator.compare_routes(int(start), int(end))
#         except ValueError:
#             print("Please enter valid numeric node IDs")
#         except KeyError:
#             print("Invalid node ID - use the list above as reference")
    
#     # Run automated performance tests
#     print("\nRUNNING AUTOMATED PERFORMANCE TESTS...")
#     comparator.performance_test()


