// Helper functions for graph operations
export function heuristic(node1, node2, nodes) {
    const n1 = nodes.find(n => n.id === node1);
    const n2 = nodes.find(n => n.id === node2);
    if (!n1 || !n2) return Infinity;
    
    return Math.sqrt(
        Math.pow(n2.x - n1.x, 2) + 
        Math.pow(n2.y - n1.y, 2)
    );
}

export function getNeighbors(node, edges) {
    const neighbors = [];
    
    edges.forEach(edge => {
        if (edge.from === node) {
            neighbors.push([edge.to, edge]);
        } else if (edge.to === node) {
            neighbors.push([edge.from, edge]);
        }
    });
    
    return neighbors;
}

export function reconstructPath(cameFrom, current) {
    const path = [current];
    
    while (cameFrom[current] !== undefined) {
        current = cameFrom[current];
        path.unshift(current);
    }
    
    return path;
}

export function getLowestFScore(openSet, fScore) {
    let lowest = null;
    let lowestScore = Infinity;
    
    openSet.forEach(node => {
        if (fScore[node] < lowestScore) {
            lowestScore = fScore[node];
            lowest = node;
        }
    });
    
    return lowest;
}