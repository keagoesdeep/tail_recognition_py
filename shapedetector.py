# import the necessary packages
import cv2


def detect_shape(contours):
    # approximate the contour
    peri = cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, 0.04 * peri, True)
    if len(approx) == 3:
        return "triangle"
    elif len(approx) == 4:
        return "rectangle"
    else:
        return None
