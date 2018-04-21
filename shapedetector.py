# import the necessary packages
import cv2


def detect_shape(contours):
    # approximate the contour
    peri = cv2.arcLength(contours, True)
    approx = cv2.approxPolyDP(contours, 0.07 * peri, True)
    # if the shape is a triangle, it will have 3 vertices
    if len(approx) == 3:
        shape = "triangle"
    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(approx) == 4:
        shape = "rectangle"
    # otherwise, we assume the shape is a circle
    else:
        shape = None

    # return the name of the shape
    return shape
