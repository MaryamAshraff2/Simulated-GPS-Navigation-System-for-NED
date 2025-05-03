import matplotlib.pyplot as plt
import numpy as np
import json
import os

def annotate_map(image_path):
    # Load the image
    img = plt.imread(image_path)
    
    # Create a figure and display the image
    fig, ax = plt.subplots()
    ax.imshow(img)
    
    plt.title("Click on important locations (e.g., gates, buildings). Press 'enter' when done.")
    
    # Use ginput to collect points
    points = plt.ginput(n=-1, timeout=0, show_clicks=True)
    
    # Convert to numpy array for easier handling
    points = np.array(points)
    
    plt.close()
    
    return points

def save_points(points, output_file):
    # Convert numpy array to list of tuples for JSON serialization
    points_list = [(x, y) for x, y in points]
    
    with open(output_file, 'w') as f:
        json.dump(points_list, f, indent=4)
    
    print(f"Saved {len(points_list)} points to {output_file}")

def load_points(input_file):
    if not os.path.exists(input_file):
        return None
    
    with open(input_file, 'r') as f:
        points_list = json.load(f)
    
    return np.array(points_list)

def main():
    # Configuration
    image_file = "nedmap.jpg"  # Change this to your image filename
    output_file = "map_points.json"
    
    # Check if we already have points
    existing_points = load_points(output_file)
    
    if existing_points is not None:
        print(f"Found existing points file with {len(existing_points)} points.")
        response = input("Do you want to add more points? (y/n): ").lower()
        if response == 'y':
            # Annotate and get new points
            new_points = annotate_map(image_file)
            # Combine with existing points
            all_points = np.vstack([existing_points, new_points])
            save_points(all_points, output_file)
        else:
            print("Using existing points without modification.")
    else:
        # Annotate and save new points
        points = annotate_map(image_file)
        save_points(points, output_file)

if __name__ == "__main__":
    main()







