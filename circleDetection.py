import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture("SpheroMiniTest3.mp4")  # 0 is the default camera (Mac in-built)

# ret, frame = videoCapture.read()
# grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
# blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
# prev_coords = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 100, param1=20, param2=50, minRadius=10, maxRadius=150)
# # prev_coords[0][ball#][coordinatePlane]

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
        print(len(circles[0]))
        for i in circles[0, :]:
            cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 10)
            # print(i)
    cv.imshow("Circles", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    prev_coords = circles

videoCapture.release()
cv.destroyAllWindows()
