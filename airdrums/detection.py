
import cv2
import numpy as np


def detect_circles(frame_bgr, minRadius=None, maxRadius=None):

    minRadius = minRadius or 10
    maxRadius = maxRadius or 70    # Separa o canal azul

    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # Threshold of blue in HSV space
    lower_blue = np.array([90, 50, 140])  # Valores de referência para o azul
    upper_blue = np.array([130, 255, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(frame_bgr, frame_bgr, mask=mask)

    # Convert to grayscale.
    gray = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)

    # Blur using 3 * 3 kernel.
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image.
    detected_circles = cv2.HoughCircles(gray_blurred,
                                        cv2.HOUGH_GRADIENT, 1, 50, param1=50,
                                        param2=30, minRadius=minRadius, maxRadius=maxRadius)

    # Draw circles that are detected.
    if detected_circles is not None:
        # Convert the circle parameters a, b and r to integers.
        detected_circles = np.uint16(np.around(detected_circles))
        cicles = detected_circles[0, :]
        return cicles

    return []
