import { PriorityQueue } from './PriorityQueue';
import { getNeighbors, reconstructPath } from './graphUtils';

export const comfortDijkstra = (
    graph, 
    start, 
    end, 
    preferShade = false, 
    preferLessCrowded = false
) => {
    const nodes = graph.nodes;
    const edges = graph.edges;
    
    const distances = {};
    const previous = {};
    const visited = new Set();
    const priorityQueue = new PriorityQueue();
    
    // Initialize distances
    nodes.forEach(node => {
        distances[node.id] = Infinity;
    });
    distances[start] = 0;
    
    priorityQueue.enqueue(start, 0);
    
    while (!priorityQueue.isEmpty()) {
        const { element: current } = priorityQueue.dequeue();
        
        if (current === end) {
            return [reconstructPath(previous, end), distances[end]];
        }
        
        if (visited.has(current)) continue;
        visited.add(current);
        
        getNeighbors(current, edges).forEach(([neighbor, edge]) => {
            if (visited.has(neighbor)) return;
            
            // Calculate base weight
            let weight = edge.distance;
            
            // Apply comfort factors
            if (preferShade && !edge.has_shade) {
                weight *= 1.5; // Penalize unshaded paths
            }
            
            if (preferLessCrowded && !edge.less_crowd) {
                weight *= 1.3; // Penalize crowded paths
            }
            
            const totalDistance = distances[current] + weight;
            
            if (totalDistance < distances[neighbor]) {
                distances[neighbor] = totalDistance;
                previous[neighbor] = current;
                
                // Update priority queue
                if (priorityQueue.has(neighbor)) {

                    priorityQueue.enqueue(neighbor, totalDistance);
                } else {
                    priorityQueue.enqueue(neighbor, totalDistance);
                }
            }
        });
    }
    
    // No path found
    return [[], Infinity];
};

export const loadGraphForDijkstra = async () => {
    try {
        const response = await fetch('/nodesandedges/enhanced_campus_routes.json');
        if (!response.ok) throw new Error('Failed to load graph data');
        
        const data = await response.json();
        
        // Convert edge format if needed
        const edges = data.edges.map(edge => {
            if (Array.isArray(edge)) {
                return {
                    from: edge[0],
                    to: edge[1],
                    distance: edge[2],
                    time: edge[3],
                    has_shade: edge[4],
                    less_crowd: edge[5]
                };
            }
            return edge;
        });
        
        return {
            nodes: data.nodes,
            edges: edges
        };
    } catch (error) {
        console.error('Error loading graph for Dijkstra:', error);
        throw error;
    }
};