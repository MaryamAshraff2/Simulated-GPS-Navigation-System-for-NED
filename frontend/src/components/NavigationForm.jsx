import { useState } from 'react';

const NavigationForm = ({ 
  locations, 
  onRouteCalculate,
  defaultFrom,
  defaultTo
}) => {
  const [fromLocation, setFromLocation] = useState(defaultFrom || '');
  const [toLocation, setToLocation] = useState(defaultTo || '');
  const [preferShade, setPreferShade] = useState(false);
  const [preferLessCrowd, setPreferLessCrowd] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!fromLocation || !toLocation) return;
    
    onRouteCalculate({
      from: fromLocation,
      to: toLocation,
      preferShade,
      preferLessCrowd
    });
  };

//   const swapLocations = () => {
//     setFromLocation(toLocation);
//     setToLocation(fromLocation);
//   };

  return (
    <form onSubmit={handleSubmit} className="navigation-form">
      <div className="form-group">
        <label htmlFor="from-location">From:</label>
        <select
          id="from-location"
          value={fromLocation}
          onChange={(e) => setFromLocation(e.target.value)}
          required
        >
          <option value="">Select starting point</option>
          {locations.sort((a, b) => a.name.localeCompare(b.name)).map(location => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>
      </div>

      {/* <button 
        type="button" 
        className="swap-btn"
        onClick={swapLocations}
        aria-label="Swap locations"
      >
        ⇅
      </button> */}

      <div className="form-group">
        <label htmlFor="to-location">To:</label>
        <select
          id="to-location"
          value={toLocation}
          onChange={(e) => setToLocation(e.target.value)}
          required
        >
          <option value="">Select destination</option>
          {locations.sort((a, b) => a.name.localeCompare(b.name)).map(location => (
            <option key={location.id} value={location.id}>
              {location.name}
            </option>
          ))}
        </select>
      </div>

      <div className="comfort-options">
        <h4>Route Preferences:</h4>
        <div className="toggle-option">
          <label>
            <input
              type="checkbox"
              checked={preferShade}
              onChange={() => setPreferShade(!preferShade)}
            />
            <span className="toggle-label">Prefer Shaded Routes</span>
          </label>
        </div>

        <div className="toggle-option">
          <label>
            <input
              type="checkbox"
              checked={preferLessCrowd}
              onChange={() => setPreferLessCrowd(!preferLessCrowd)}
            />
            <span className="toggle-label">Prefer Less Crowded Routes</span>
          </label>
        </div>
      </div>

      <button 
        type="submit" 
        className="find-route-btn"
        disabled={!fromLocation || !toLocation}
      >
        Find Route
      </button>
    </form>
  );
};

export default NavigationForm;