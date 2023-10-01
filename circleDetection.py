import cv2 as cv
import numpy as np

videoCapture = cv.VideoCapture(0)  # 0 is the default camera (Mac in-built)

while True:

    ret, frame = videoCapture.read()
    if not ret: break
    grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurFrame = cv.GaussianBlur(grayFrame, (17, 17), 0)
    circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1, 40, param1=20, param2=50, minRadius=20, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(frame, (i[0], i[1]), i[2], (255, 0, 255), 10)
            print(i)
        cv.waitKey(100)
    cv.imshow("Circles", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

videoCapture.release()
cv.destroyAllWindows()
