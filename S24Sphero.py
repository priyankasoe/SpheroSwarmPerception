import cv2
import numpy as np

# Read video.
cap = cv2.VideoCapture('Vid1.mp4')

while cap.isOpened():
    # Read a frame from the video.
    ret, frame = cap.read()
    if not ret:
        break  # Break the loop if no frame is read.

    # Convert the frame to grayscale.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the gray image to create a binary mask of white regions (balls).
    _, thresholded = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Find contours in the binary mask.
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through detected contours to find circles.
    for contour in contours:
        # Approximate the contour to a polygon to get the center and radius of the enclosing circle.
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)

        # Filter out small circles (noise).
        if radius > 10:
            # Draw the detected circle.
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.circle(frame, center, 1, (0, 0, 255), 1)

    # Display the frame with detected circles.
    cv2.imshow("Detected Circles", frame)

    # Check for 'q' key press to exit the loop.
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# Release the video capture object and close all windows.
cap.release()
cv2.destroyAllWindows()
