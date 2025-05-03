# import cv2
# import numpy as np
# import math


# # Load your map image
# image_path = "nedmapwithnodes.jpg"  # Change this to your image file
# img = cv2.imread(image_path)
# clone = img.copy()


    
# # Store clicked points
# points = []

# def calculate_distance(p1, p2):
#     return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# def mouse_callback(event, x, y, flags, param):
#     global points, img

#     if event == cv2.EVENT_LBUTTONDOWN:
#         points.append((x, y))
#         cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
#         if len(points) == 2:
#             cv2.line(img, points[0], points[1], (255, 0, 0), 2)
#             dist = calculate_distance(points[0], points[1])
#             mid_x = (points[0][0] + points[1][0]) // 2
#             mid_y = (points[0][1] + points[1][1]) // 2
#             cv2.putText(img, f"{dist:.2f}px", (mid_x, mid_y), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#             print(f"Distance between points: {dist:.2f} pixels")
#             points = []

# # Set up window and mouse callback
# cv2.namedWindow("Map Distance Estimator")
# cv2.setMouseCallback("Map Distance Estimator", mouse_callback)

# while True:
#     cv2.imshow("Map Distance Estimator", img)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('r'):
#         img = clone.copy()
#         points = []
#     elif key == 27 or key == ord('q'):  # ESC or 'q' to quit
#         break

# cv2.destroyAllWindows()


import cv2
import numpy as np
import math

# Load your map image
image_path = "nedmapwithnodes.jpg"  # Change this to your image file
img = cv2.imread(image_path)
clone = img.copy()

# Store clicked points
points = []

def calculate_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def mouse_callback(event, x, y, flags, param):
    global points, img

    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        if len(points) == 2:
            cv2.line(img, points[0], points[1], (255, 0, 0), 2)
            dist = calculate_distance(points[0], points[1])
            mid_x = (points[0][0] + points[1][0]) // 2
            mid_y = (points[0][1] + points[1][1]) // 2

            # Draw text inside a black box
            label = f"{dist:.2f}px"
            (text_w, text_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            box_x, box_y = mid_x, mid_y - text_h - 10
            cv2.rectangle(img, (box_x, box_y), (box_x + text_w + 6, box_y + text_h + baseline + 6), (0, 0, 0), -1)
            cv2.putText(img, label, (box_x + 3, box_y + text_h + 3), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

            print(f"Distance between points: {dist:.2f} pixels")
            points = []

# Set up window and mouse callback
cv2.namedWindow("Map Distance Estimator")
cv2.setMouseCallback("Map Distance Estimator", mouse_callback)

while True:
    cv2.imshow("Map Distance Estimator", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        img = clone.copy()
        points = []
    elif key == 27 or key == ord('q'):  # ESC or 'q' to quit
        break

cv2.destroyAllWindows()

