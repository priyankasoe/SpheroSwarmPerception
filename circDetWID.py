import math

import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture("SpheroMiniTest3.mp4")  # 0 is the default camera (Mac in-built)

prev_coords = None
num_circles = 2
sentinel = 0
minDist = 30

while (True):
    ret, frame = videoCapture.read()
    print(ret)
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("greyFrame", grayFrame)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    prev_coords = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 50, param1=30, param2=15, minRadius=5, maxRadius=50)
    if (prev_coords is not None):
        if (prev_coords.shape[1] == num_circles):
            for i in range (0, num_circles):
                for j in range (0, num_circles):
                    xDiff = prev_coords[0, i, 0] - prev_coords[0, j, 0]
                    yDiff = prev_coords[0, i, 1] - prev_coords[0, j, 1]
                    distBetween = abs(pow(xDiff, 2) + pow(yDiff, 2))
                    if (i != j and distBetween < minDist):
                        sentinel = -1
            if (sentinel != -1):
                break
# prev_coords[0][ball#][coordinatePlane]

while True:

    ret, frame = videoCapture.read()
    if not ret: break  # Check what this is
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 50, param1=30, param2=15, minRadius=5, maxRadius=50)

    # for j in range (len(circles[0])):
    #     for k in range (len(prev_coords[0])):
    #         # something

    if circles is not None:
        if (circles.shape[1] >= prev_coords.shape[1]):
            for i in range (0, prev_coords.shape[1]):
                lowestDistanceCoord = circles[0, 0]
                for j in range (0, circles.shape[1]):
                    xDifference = circles[0, j, 0] - prev_coords[0, i, 0]
                    yDifference = circles[0, j, 1] - prev_coords[0, i, 1]
                    newDistance = math.sqrt(math.pow(xDifference, 2) + math.pow(yDifference, 2))
                    currentXDifference = lowestDistanceCoord[0] - prev_coords[0, i, 0]
                    currentYDifference = lowestDistanceCoord[1] - prev_coords[0, i, 1]
                    currentDistance = math.sqrt(math.pow(currentXDifference, 2) + math.pow(currentYDifference, 2))
                    if(newDistance < currentDistance):
                        lowestDistanceCoord = circles[0, j]
                prev_coords[0, i] = lowestDistanceCoord
            for i in range (0, prev_coords.shape[1]):
                print(i, ": ", prev_coords[0, i])
                cv.putText(frame, str(i), (int(prev_coords[0, i, 0]), int(prev_coords[0, i, 1])), cv.FONT_ITALIC, 1, (0, 0, 0), 1, cv.LINE_AA)

    prev_coords = np.uint16(np.around(prev_coords))
    count = 0
    for i in prev_coords[0, :]:
        color = (0, count * 100 , 0)
        count += 1
        cv.circle(frame, (i[0], i[1]), i[2], color, 3)

    cv.imshow("Numbers", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
