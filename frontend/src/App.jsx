import { useState, useEffect } from 'react';
import { astar } from './algorithms/astar';
import { comfortDijkstra } from './algorithms/comfortDijkstra';
import { loadGraph } from './algorithms/graphLoader';
import NavigationForm from './components/NavigationForm';
import CampusMap from './components/CampusMap';
import './App.css';

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], edges: [] });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [calculatedPath, setCalculatedPath] = useState(null);
  const [pathDetails, setPathDetails] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await loadGraph();
        setGraphData(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);

  const handleCalculateRoute = async ({ from, to, preferShade, preferLessCrowd }) => {
    try {
      setIsLoading(true);
      setError(null);
      
      let path, cost, algorithm;
      
      if (preferShade || preferLessCrowd) {
        // Use comfort Dijkstra's algorithm
        [path, cost] = comfortDijkstra(
          graphData,
          parseInt(from),
          parseInt(to),
          preferShade,
          preferLessCrowd
        );
        algorithm = 'dijkstra';
      } else {
        // Use A* algorithm for shortest path
        [path, cost] = astar(
          graphData,
          parseInt(from),
          parseInt(to),
          'distance' // or 'time' for fastest route
        );
        algorithm = 'astar';
      }
      
      if (path.length === 0) {
        throw new Error('No path found between selected locations');
      }
      
      setCalculatedPath(path);
      setPathDetails({
        from: graphData.nodes.find(n => n.id === parseInt(from)).name,
        to: graphData.nodes.find(n => n.id === parseInt(to)).name,
        preferShade,
        preferLessCrowd,
        cost,
        algorithm
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading && graphData.nodes.length === 0) {
    return <div className="loading">Loading campus map...</div>;
  }

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Campus Navigation System</h1>
      </header>
      
      <div className="main-content">
        <div className="controls-panel">
          <NavigationForm
            locations={graphData.nodes}
            onRouteCalculate={handleCalculateRoute}
          />
          
          {calculatedPath && pathDetails && (
            <div className="path-info">
              <h3>Route from {pathDetails.from} to {pathDetails.to}</h3>
              <p>
                Algorithm: {pathDetails.algorithm === 'astar' ? 'A* (Shortest Path)' : 'Dijkstra (Comfort Path)'}
              </p>
              <p>
                Preferences: 
                {pathDetails.preferShade ? ' Shade' : ''}
                {pathDetails.preferShade && pathDetails.preferLessCrowd ? ',' : ''}
                {pathDetails.preferLessCrowd ? ' Less Crowded' : ''}
                {!pathDetails.preferShade && !pathDetails.preferLessCrowd ? ' None (Shortest Path)' : ''}
              </p>
              <p>Total cost: {pathDetails.cost.toFixed(2)}</p>
              
              <div className="path-nodes">
                <h4>Path:</h4>
                <ol>
                  {calculatedPath.map(nodeId => {
                    const node = graphData.nodes.find(n => n.id === nodeId);
                    return <li key={nodeId}>{node.name}</li>;
                  })}
                </ol>
              </div>
            </div>
          )}
        </div>
        
        <div className="map-panel">
          <CampusMap 
            nodes={graphData.nodes} 
            edges={graphData.edges} 
            path={calculatedPath}
            algorithm={pathDetails?.algorithm}
          />
        </div>
      </div>
    </div>
  );
}

export default App;