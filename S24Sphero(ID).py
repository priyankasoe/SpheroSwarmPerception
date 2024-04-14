import cv2
import numpy as np
import math

cap = cv2.VideoCapture('TestVideos/Vid1.mp4')

prev_coords = []
num_circles = 3
sentinel = 0
minDist = 10

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Thresholding the gray image to create a binary mask of white regions (balls).
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Finding contours in the binary mask.
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    prev_coords = []

    # Iterating through detected contours to find circles.
    for contour in contours:
        # Approximating the contour to a polygon to get the center and radius of the enclosing circle.
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Filtering out small circles (noise).
        if radius > 10:
            prev_coords.append((x, y, radius))
    
    # prev_coords = np.uint16(np.around(prev_coords))
    
    if (prev_coords is not None):
        if (len(prev_coords) == num_circles):
            for i in range (0, num_circles):
                for j in range (0, num_circles):
                    xDiff = prev_coords[i][0] - prev_coords[j][0]
                    yDiff = prev_coords[i][1] - prev_coords[j][1]
                    distBetween = abs(pow(xDiff, 2) + pow(yDiff, 2))
                    if (i != j and distBetween < minDist):
                        print(prev_coords)
                        sentinel = -1
                
            if (sentinel != -1):
                cv2.imshow("Detected Circles", frame)
                break

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Thresholding the gray image to create a binary mask of white regions (balls).
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Finding contours in the binary mask.
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    circles = []

    # Iterating through detected contours to find circles.
    for contour in contours:
        # Approximating the contour to a polygon to get the center and radius of the enclosing circle.
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Filtering out small circles (noise).
        if radius > 10:
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.circle(frame, center, 1, (0, 0, 255), 1)
            circles.append((x, y, radius))

    if circles is not None:
        if (len(circles) >= len(prev_coords)):
            for i in range (0, len(prev_coords)):
                lowestDistanceCoord = circles[0]
                for j in range (0, len(circles)):
                    xDifference = circles[j][0] - prev_coords[i][0]
                    yDifference = circles[j][1] - prev_coords[i][1]
                    newDistance = math.sqrt(math.pow(xDifference, 2) + math.pow(yDifference, 2))
                    currentXDifference = lowestDistanceCoord[0] - prev_coords[i][0]
                    currentYDifference = lowestDistanceCoord[1] - prev_coords[i][1]
                    currentDistance = math.sqrt(math.pow(currentXDifference, 2) + math.pow(currentYDifference, 2))
                    if(newDistance < currentDistance):
                        lowestDistanceCoord = circles[j]
                prev_coords[i] = lowestDistanceCoord
            for i in range (0, len(prev_coords)):
                print(i, ": ", prev_coords[i])
                cv2.putText(frame, str(i), (int(prev_coords[i][0]), int(prev_coords[i][1])), cv2.FONT_ITALIC, 1, (0, 0, 0), 1, cv2.LINE_AA)

    # prev_coords = np.uint16(np.around(prev_coords))
    count = 0
    for i in range(0, len(prev_coords)):
        print(prev_coords[i])
        color = (0, count * 100 , 0)
        count += 1
        coord = (int(prev_coords[i][0]), int(prev_coords[i][1]))
        cv2.circle(frame, coord, prev_coords[i][2], color, 3)

    cv2.imshow("Detected Circles", frame)

    # Tracking code goes here

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
