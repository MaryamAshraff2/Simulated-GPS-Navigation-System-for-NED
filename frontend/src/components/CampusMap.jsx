import { useEffect, useRef, useState, useCallback } from 'react';

const CampusMap = ({ nodes, edges, path }) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const canvasRef = useRef(null);
  const imgRef = useRef(new Image());
  const [scale, setScale] = useState(1);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  // Initialize canvas and load image
  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Load your campus map image
    imgRef.current.src = '/nedmap.jpg';
    
    imgRef.current.onload = () => {
        canvas.width = imgRef.current.width;
        canvas.height = imgRef.current.height;
        setImageLoaded(true);  // mark as loaded
      };

    imgRef.current.onerror = () => {
        console.error('Failed to load map image.');
      };

  }, []);

  // Redraw when dependencies change
useEffect(() => {
  if (imageLoaded) drawMap();
}, [nodes, edges, path, scale, offset, imageLoaded]);


  // Draw the map with current state
  const drawMap = useCallback(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Save the context state
    ctx.save();
    
    // Apply scaling and panning
    ctx.scale(scale, scale);
    ctx.translate(offset.x / scale, offset.y / scale);
    
    // Draw background image
    ctx.drawImage(imgRef.current, 0, 0);
    
    // Restore before drawing interactive elements
    ctx.restore();
    
    // Draw edges
    edges.forEach(edge => {
      const fromNode = nodes.find(n => n.id === edge.from);
      const toNode = nodes.find(n => n.id === edge.to);
      
      if (fromNode && toNode) {
        const isPathEdge = path && 
                         path.includes(edge.from) && 
                         path.includes(edge.to) &&
                         Math.abs(path.indexOf(edge.from) - path.indexOf(edge.to)) === 1;
        
        ctx.beginPath();
        ctx.moveTo(fromNode.x * scale + offset.x, fromNode.y * scale + offset.y);
        ctx.lineTo(toNode.x * scale + offset.x, toNode.y * scale + offset.y);
        ctx.strokeStyle = isPathEdge ? '#FF0000' : 'rgba(0, 0, 0, 0.2)';
        // ctx.strokeStyle = isPathEdge ? '#FF0000' : 'rgba(0, 0, 0, 0.2)';

        ctx.lineWidth = isPathEdge ? 4 * scale : 1 * scale;
        ctx.stroke();
      }
    });
    
    // Draw nodes
    nodes.forEach(node => {
      const isInPath = path && path.includes(node.id);
      
      ctx.beginPath();
      ctx.arc(
        node.x * scale + offset.x, 
        node.y * scale + offset.y, 
        (isInPath ? 8 : 5) * scale, 
        0, 
        Math.PI * 2
      );
      ctx.fillStyle = isInPath ? '#4CAF50' : '#2196F3';
      ctx.fill();
      ctx.strokeStyle = 'white';
      ctx.lineWidth = 1.5 * scale;
      ctx.stroke();
      
      if (isInPath) {
        ctx.font = `bold ${12 * scale}px Arial`;
        ctx.fillStyle = 'black';
        ctx.textAlign = 'center';
        ctx.fillText(
          node.name, 
          node.x * scale + offset.x, 
          node.y * scale + offset.y - (12 * scale)
        );
      }
    });
  }, [nodes, edges, path, scale, offset]);

  // Handle mouse down for panning
  const handleMouseDown = (e) => {
    if (e.button !== 0) return; // Only left mouse button
    setIsDragging(true);
    setDragStart({
      x: e.clientX - offset.x,
      y: e.clientY - offset.y
    });
    e.currentTarget.style.cursor = 'grabbing';
  };

  // Handle mouse move for panning
  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setOffset({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  // Handle mouse up to end panning
  const handleMouseUp = () => {
    setIsDragging(false);
    canvasRef.current.style.cursor = 'grab';
  };

  // Handle mouse leave to end panning
  const handleMouseLeave = () => {
    setIsDragging(false);
    canvasRef.current.style.cursor = 'grab';
  };

  // Zoom in/out
  const handleZoom = (direction) => {
    const zoomFactor = direction === 'in' ? 1.2 : 1/1.2;
    const newScale = scale * zoomFactor;
    
    // Limit zoom range
    const clampedScale = Math.max(0.5, Math.min(newScale, 3));
    setScale(clampedScale);
  };

  // Reset zoom and pan
  const handleReset = () => {
    setScale(1);
    setOffset({ x: 0, y: 0 });
  };

  return (
    <div className="campus-map-container">
      <canvas 
        ref={canvasRef} 
        className="campus-map"
        style={{
          cursor: isDragging ? 'grabbing' : 'grab',
          maxWidth: '100%',
          height: 'auto',
          border: '1px solid #ddd',
          borderRadius: '8px'
        }}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseLeave}
      />
      
      <div className="map-controls">
        <button 
          className="zoom-btn" 
          onClick={() => handleZoom('in')}
          aria-label="Zoom in"
        >
          +
        </button>
        <button 
          className="zoom-btn" 
          onClick={() => handleZoom('out')}
          aria-label="Zoom out"
        >
          -
        </button>
        <button 
          className="zoom-btn reset-btn"
          onClick={handleReset}
          aria-label="Reset view"
        >
          ⟲
        </button>
      </div>
    </div>
  );
};

export default CampusMap;