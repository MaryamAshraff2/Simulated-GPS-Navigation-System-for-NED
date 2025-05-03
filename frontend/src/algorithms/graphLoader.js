export const loadGraph = async () => {
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
                    // has_stairs: edge[4],
                    // has_ramp: edge[5],
                    has_shade: edge[4],  // Same index as has_stairs in your data
                    less_crowd: edge[5]   // Same index as has_ramp in your data
                };
            }
            return edge;
        });
        
        return {
            nodes: data.nodes,
            edges: edges
        };
    } catch (error) {
        console.error('Error loading graph:', error);
        throw error;
    }
};