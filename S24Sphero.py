import cv2
import numpy as np

# Read image.
img = cv2.imread('sphero4.jpg', cv2.IMREAD_COLOR)

# Convert to grayscale.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Blur using 3 * 3 kernel.
gray_blurred = cv2.blur(gray, (3, 3))

# Apply Hough transform on the blurred image.
detected_circles = cv2.HoughCircles(gray_blurred,
                                    cv2.HOUGH_GRADIENT, 1, 400, param1=50,
                                    param2=30, minRadius=450, maxRadius=500)

# Draw circles that are detected.
if detected_circles is not None:

    # Convert the circle parameters a, b and r to integers.
    detected_circles = np.uint16(np.around(detected_circles))
    print(detected_circles)

    first_circle = True
    unique_circle_x = 0
    unique_circle_y = 0
    unique_circle_r = 0
    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        # if first_circle:
        #     unique_circle_x = a  # 1406
        #     unique_circle_y = b  # 2688
        #     unique_circle_r = r  # 464
        #     first_circle = False
        #     # Draw the circumference of the circle.
        #     cv2.circle(img, (a, b), r, (0, 255, 0), 20)
        #     print("Hi!")
        # else:
        #     lower_bound_x = unique_circle_x - r  # 942
        #     upper_bound_x = unique_circle_x + r  # 1870
        #     lower_bound_y = unique_circle_y - r  # 2224
        #     upper_bound_y = unique_circle_y + r  # 3152
        #     if (a < lower_bound_x or a > upper_bound_x) or (b < lower_bound_y or b > upper_bound_y):
        #         # 1634 < 942 or 1634 > 1870 or 1218 < 2224 or 1218 > 3152
        #         unique_circle_x = a
        #         unique_circle_y = b
        #         unique_circle_r = r
        #         # Draw the circumference of the circle.
        #         cv2.circle(img, (a, b), r, (0, 255, 0), 20)
        #         print("Hello to all!")

        # Draw the circumference of the circle.
        cv2.circle(img, (a, b), r, (0, 255, 0), 20)

        # Draw a small circle (of radius 1) to show the center.
        cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
        cv2.imshow("Detected Circle", img)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break

cv2.destroyAllWindows()
