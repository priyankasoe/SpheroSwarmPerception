import math

import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture("SpheroMiniTest2.mp4")  # 0 is the default camera (Mac in-built)

prev_coords = None

while (True):
    ret, frame = videoCapture.read()
    print(ret)
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    cv.imshow("greyFrame", grayFrame)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    prev_coords = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=20, param2=50, minRadius=10, maxRadius=150)
    if (prev_coords is not None):
        if (prev_coords.shape[1] == 2):
            break

# prev_coords[0][ball#][coordinatePlane]

while True:

    ret, frame = videoCapture.read()
    if not ret: break  # Check what this is
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=30, param2=10, minRadius=5, maxRadius=50)

    # for j in range (len(circles[0])):
    #     for k in range (len(prev_coords[0])):
    #         # something

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(frame, (i[0], i[1]), i[2], (0, 0, 0), 3)

    if circles is not None:
        # if (circles.shape[1] == prev_coords.shape[1]):q
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
    
    cv.imshow("Numbers", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
