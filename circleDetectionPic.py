import cv2 as cv
import numpy as np
import math

frame = cv.imread("IMG_0963.jpg")
DIMENSIONS = (4032, 3024)

TARGET_POS_1 = (100, 2000)
TARGET_POS_2 = (500, 1000)
TARGET_POS_3 = (200, 0)

TARGET_POSITIONS_LIST = [TARGET_POS_1, TARGET_POS_2, TARGET_POS_3]

grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=20, param2=50, minRadius=50, maxRadius=400)

distances = []
if circles is not None:
    print(circles)
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 10)
        for target in TARGET_POSITIONS_LIST:
            distances.append((i[0]-target[0], i[1]-target[1]))
# [(x,y), (x,y), (x,y)]

for distance in distances:
    print(math.sqrt(math.pow(distance[0], 2) + math.pow(distance[1], 2)))

for target_position in TARGET_POSITIONS_LIST:
    cv.circle(frame, (target_position[0], target_position[1]), 50, (0, 255, 255), 10)

cv.imshow("Circles", frame)

cv.waitKey(10000)
cv.destroyAllWindows()
