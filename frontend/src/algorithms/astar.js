import { 
    heuristic, 
    getNeighbors, 
    reconstructPath, 
    getLowestFScore 
} from './graphUtils';

export const astar = (graph, start, end, weightType = 'distance') => {
    const nodes = graph.nodes;
    const edges = graph.edges;
    
    const openSet = new Set([start]);
    const cameFrom = {};
    
    const gScore = {};
    const fScore = {};
    
    // Initialize scores for all nodes
    nodes.forEach(node => {
        gScore[node.id] = Infinity;
        fScore[node.id] = Infinity;
    });
    
    gScore[start] = 0;
    fScore[start] = heuristic(start, end, nodes);
    
    while (openSet.size > 0) {
        const current = getLowestFScore(openSet, fScore);
        
        if (current === end) {
            return [reconstructPath(cameFrom, current), gScore[current]];
        }
        
        openSet.delete(current);
        
        getNeighbors(current, edges).forEach(([neighbor, edge]) => {
            // Calculate tentative gScore based on weight type
            let tentativeGScore;
            
            if (weightType === 'time') {
                tentativeGScore = gScore[current] + edge.time;
            } else if (weightType === 'accessibility') {
                // Penalize routes with stairs
                tentativeGScore = gScore[current] + edge.distance * (edge.has_stairs ? 2 : 1);
            } else { // default to distance
                tentativeGScore = gScore[current] + edge.distance;
            }
            
            if (tentativeGScore < gScore[neighbor]) {
                // This path to neighbor is better than any previous one
                cameFrom[neighbor] = current;
                gScore[neighbor] = tentativeGScore;
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, end, nodes);
                
                if (!openSet.has(neighbor)) {
                    openSet.add(neighbor);
                }
            }
        });
    }
    
    // No path found
    return [[], Infinity];
};

export const loadGraphForAstar = async () => {
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
                    has_stairs: edge[4],
                    has_ramp: edge[5]
                };
            }
            return edge;
        });
        
        return {
            nodes: data.nodes,
            edges: edges
        };
    } catch (error) {
        console.error('Error loading graph for A*:', error);
        throw error;
    }
};