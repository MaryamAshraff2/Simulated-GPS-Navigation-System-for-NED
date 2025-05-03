export const calculateRoute = async (from, to, preferences) => {
    try {
      const response = await fetch('/api/calculate-route', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from,
          to,
          preferences
        }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to calculate route');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error calculating route:', error);
      throw error;
    }
  };
  
  export const getMapData = async () => {
    try {
      const response = await fetch('/nodesandedges/enhanced_campus_routes.json');
      if (!response.ok) {
        throw new Error('Failed to load map data');
      }
      return await response.json();
    } catch (error) {
      console.error('Error loading map data:', error);
      throw error;
    }
  };