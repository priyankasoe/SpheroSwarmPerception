import cv2

cap = cv2.VideoCapture('TestVideos/Vid1.mp4')

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

    cv2.imshow("Detected Circles", frame)

    # Tracking code goes here

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
