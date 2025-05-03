# import json
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# # Load map and data
# img = mpimg.imread("nedmap.jpg")
# with open("enhanced_campus_routes.json") as f:
#     data = json.load(f)

# # Plot
# fig, ax = plt.subplots(figsize=(12, 8))
# ax.imshow(img)

# # Plot nodes
# for x, y in data["nodes"]:
#     ax.plot(x, y, 'ro', markersize=8)  # Red dots

# # Plot edges
# for i, j in data["edges"]:
#     x1, y1 = data["nodes"][i]
#     x2, y2 = data["nodes"][j]
#     ax.plot([x1, x2], [y1, y2], 'b-', linewidth=2)  # Blue lines

# plt.title("Campus Navigation Routes")
# plt.show()


import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load map and data
img = mpimg.imread("nedmap.jpg")
with open("enhanced_campus_routes.json") as f:
    data = json.load(f)

# Create a map from node id to (x, y) coordinates
node_positions = {node["id"]: (node["x"], node["y"]) for node in data["nodes"]}

# Plot
fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(img)

# Plot nodes with labels
for node in data["nodes"]:
    x, y = node["x"], node["y"]
    ax.plot(x, y, 'ro', markersize=6)  # Red dot
    ax.text(x + 5, y - 5, node["name"], fontsize=8, color='black')

# Plot edges
for i, j, *_ in data["edges"]:
    x1, y1 = node_positions[i]
    x2, y2 = node_positions[j]
    ax.plot([x1, x2], [y1, y2], 'b-', linewidth=1.5)  # Blue line

plt.title("Campus Navigation Routes")
plt.axis('off')
plt.tight_layout()
plt.show()
