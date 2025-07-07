#  Campus Navigation System (Simulation-Based GPS)

A simulation-based navigation system built for the NED University campus using static node-edge data and graph search algorithms like A* and Dijkstra’s. The system helps users find the optimal or most comfortable paths across campus, considering factors like distance, shade, and crowd levels.

---

##  Features

-  Node-edge representation of campus map (JSON-based)
-  A* Algorithm for shortest/time/accessibility-based routing
-  Modified Dijkstra's Algorithm for comfort-based routing (shade, crowd)
-  Frontend built with React + Vite
-  Route comparison based on time, distance, and comfort
-  Simulation-ready for environments without GPS (e.g., indoor or closed campuses)

---

##  Algorithms Used

### A\* (A-Star) Search
- Optimized for shortest path or time
- Uses heuristic (Euclidean distance)

### Comfort-Based Dijkstra's
- Prioritizes shaded, less crowded paths
- Useful for accessible and relaxed navigation

---

##  How to Run

```bash
# Clone the repo
git clone https://github.com/MaryamAshraff2/Simulated-GPS-Navigation-System-for-NED.git

# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev

```
---
![Image](https://github.com/user-attachments/assets/e8b235ba-69b8-4b69-9482-f4eacdd0f3bf)
---
