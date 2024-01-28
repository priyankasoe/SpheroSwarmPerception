import math

import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(0)  # 0 is the default camera (Mac in-built)

prev_coords = None

while (prev_coords == None):
    ret, frame = videoCapture.read()
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("greyFrame", grayFrame)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    prev_coords = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=20, param2=50, minRadius=10, maxRadius=150)

# prev_coords[0][ball#][coordinatePlane]

while True:

    ret, frame = videoCapture.read()
    if not ret: break  # Check what this is
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=20, param2=50, minRadius=10, maxRadius=150)

    # for j in range (len(circles[0])):
    #     for k in range (len(prev_coords[0])):
    #         # something

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 10)
            # print(i)
    cv.imshow("Circles", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    if (prev_coords != None and (np.ndarray.size(prev_coords[0]) == np.ndarray.size(circles[0]))):
        for i in prev_coords[0][:]:
            lowestDistanceCoord = circles[0][0]
            for j in circles[0][:]:
                xDifference = circles[0][j][0] - prev_coords[0][i][0]
                yDifference = circles[0][j][1] - prev_coords[0][i][1]
                newDistance = math.sqrt(math.pow(xDifference, 2) + math.pow(yDifference, 2))
                currentXDifference = lowestDistanceCoord[0] - prev_coords[0][i][0]
                currentYDifference = lowestDistanceCoord[1] - prev_coords[0][i][1]
                currentDistance = math.sqrt(math.pow(currentXDifference, 2) + math.pow(currentYDifference, 2))
                if(newDistance < currentDistance):
                    lowestDistanceCoord = circles[0][j]
            prev_coords[i] = lowestDistanceCoord
        for i in prev_coords[0][:]:
            print(i + ": " + prev_coords[0][i])

videoCapture.release()
cv.destroyAllWindows()
