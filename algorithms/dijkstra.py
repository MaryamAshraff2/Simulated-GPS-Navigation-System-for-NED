# # algorithms/dijkstra.py
# import json
# import heapq
# import os


# def load_graph():
#     """Load graph data with proper error handling"""
#     try:
#         script_dir = os.path.dirname(os.path.abspath(__file__))
#         json_path = os.path.join(script_dir, '../nodesandedges/enhanced_campus_routes.json')
        
#         with open(json_path) as f:
#             data = json.load(f)
            
#         # Convert edge format if needed
#         if data['edges'] and isinstance(data['edges'][0], list):
#             data['edges'] = [{
#                 'from': edge[0],
#                 'to': edge[1],
#                 'distance': edge[2] if len(edge) > 2 else 1.0,
#                 'time': edge[3] if len(edge) > 3 else 1.0,
#                 'has_stairs': edge[4] if len(edge) > 4 else False,
#                 'has_ramp': edge[5] if len(edge) > 5 else True
#             } for edge in data['edges']]
            
#         return data
#     except Exception as e:
#         print(f"Error loading graph: {str(e)}")
#         return None

# def dijkstra(graph, start, end, weight_type='distance'):
#     # Initialize data structures
#     nodes = {node['id']: node for node in graph['nodes']}
#     edges = graph.get('edges', [])
    
#     distances = {node_id: float('infinity') for node_id in nodes}
#     predecessors = {node_id: None for node_id in nodes}
#     distances[start] = 0
#     queue = [(0, start)]
    
#     visited = set()
    
#     while queue:
#         current_distance, current_node = heapq.heappop(queue)
        
#         if current_node in visited:
#             continue
#         visited.add(current_node)
        
#         if current_node == end:
#             break
            
#         # Find neighbors
#         neighbors = []
#         for edge in edges:
#             if isinstance(edge, dict):
#                 from_node, to_node = edge['from'], edge['to']
#                 edge_data = edge
#             else:  # list format
#                 from_node, to_node = edge[0], edge[1]
#                 edge_data = {
#                     'distance': edge[2],
#                     'time': edge[3],
#                     'has_stairs': edge[4],
#                     'has_ramp': edge[5]
#                 }
            
#             if from_node == current_node:
#                 neighbors.append((to_node, edge_data))
#             elif to_node == current_node:
#                 neighbors.append((from_node, edge_data))
        
#         for neighbor, edge in neighbors:
#             if weight_type == 'time':
#                 weight = edge['time']
#             elif weight_type == 'accessibility':
#                 weight = edge['distance'] * (2 if edge.get('has_stairs', False) else 1)
#             else:
#                 weight = edge['distance']
            
#             distance = current_distance + weight
            
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 predecessors[neighbor] = current_node
#                 heapq.heappush(queue, (distance, neighbor))
    
#     # Reconstruct path only if end is reachable
#     if distances[end] == float('infinity'):
#         return [], float('infinity')
    
#     path = []
#     current = end
#     while current is not None:
#         path.insert(0, current)
#         current = predecessors[current]
    
#     return path, distances[end]

# # def test_dijkstra():
# #     graph = load_graph()
# #     if graph is None:
# #         print("Failed to load graph data")
# #         return
    
# #     print("=== Dijkstra's Algorithm ===")
    
# #     # Print available nodes for reference
# #     print("\nAvailable Nodes:")
# #     for node in graph['nodes']:
# #         print(f"{node['id']}: {node['name']}")
    
# #     # Test with some default values
# #     start = 0  # Main Gate
# #     end = 5    # Student Center
    
# #     print(f"\nTesting path from {graph['nodes'][start]['name']} to {graph['nodes'][end]['name']}:")
    
# #     # Test different weight types
# #     for weight_type in ['distance', 'time', 'accessibility']:
# #         path, total = dijkstra(graph, start, end, weight_type)
        
# #         if not path:
# #             print(f"\nNo {weight_type} path found")
# #             continue
            
# #         print(f"\nBest {weight_type} path:")
# #         print(" -> ".join(graph['nodes'][node]['name'] for node in path))
# #         print(f"Total {weight_type}: {total:.2f}")

# def test_dijkstra():
#     graph = load_graph()
#     if graph is None:
#         print("Failed to load graph data")
#         return

#     print("=== Dijkstra's Algorithm ===")

#     # Print available nodes with IDs
#     print("\nAvailable Nodes:")
#     for node in graph['nodes']:
#         print(f"{node['id']:>2}: {node['name']}")

#     # Prompt user for input
#     try:
#         start = int(input("\nEnter start node ID: ").strip())
#         end = int(input("Enter destination node ID: ").strip())
#     except ValueError:
#         print("Invalid input. Please enter numeric node IDs.")
#         return

#     # Check for valid IDs
#     node_ids = {node['id'] for node in graph['nodes']}
#     if start not in node_ids or end not in node_ids:
#         print("Invalid node ID entered.")
#         return

#     print(f"\nTesting path from {graph['nodes'][start]['name']} to {graph['nodes'][end]['name']}:")

#     # Run and display Dijkstra’s for all modes
#     for weight_type in ['distance', 'time', 'accessibility']:
#         path, total = dijkstra(graph, start, end, weight_type)

#         if not path:
#             print(f"\nNo {weight_type} path found.")
#             continue

#         print(f"\nBest {weight_type} path:")
#         for node_id in path:
#             print(f"{node_id} ({graph['nodes'][node_id]['name']})", end=" -> ")
#         print("END")
#         print(f"Total {weight_type}: {total:.2f}")


# if __name__ == "__main__":
#     test_dijkstra()