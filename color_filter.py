import cv2
import numpy as np
import imutils
import threading
import camera_settings
from camera_settings import LOW_BLUE, LOW_RED, LOW_YELLOW, UPPER_BLUE, UPPER_RED, UPPER_YELLOW


def hsv_to_opencv(color):
    hue = int(color["hue"] / 2)
    saturation = int(color["saturation"] * 255 / 100)
    value = int(color["value"] * 255 / 100)
    return [hue, saturation, value]


camera_settings = camera_settings.CameraSettings()
threading.Thread(target=camera_settings.init_ui).start()

cap = cv2.VideoCapture(1)
# TODO: Lower the frame rate to like 20
while True:
    read, frame = cap.read()
    if read:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # lower_red = np.array([150, 150, 50])
        # upper_red = np.array([180, 255, 255])
        #
        # lower_yellow = np.array([25, 50, 50])
        # upper_yellow = np.array([32, 255, 255])

        # upper_blue = np.array([140, 255, 255])
        # lower_blue = np.array([int(225 / 2), int(54 * 255 / 100), int(77 * 255 / 100)])
        # upper_blue = np.array([int(225 / 2), int(92 * 255 / 100), int(50 * 255 / 100)])
        # lower_blue = np.array([110, 50, 50])
        # upper_blue = np.array([130, 255, 255])

        lower_red = np.array(hsv_to_opencv(camera_settings.get_values(LOW_RED)))
        upper_red = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_RED)))

        lower_yellow = np.array(hsv_to_opencv(camera_settings.get_values(LOW_YELLOW)))
        upper_yellow = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_YELLOW)))

        lower_blue = np.array(hsv_to_opencv(camera_settings.get_values(LOW_BLUE)))
        upper_blue = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_BLUE)))

        # masks = [cv2.inRange(hsv, lower_red, upper_red), cv2.inRange(hsv, lower_blue, upper_blue),
        #          cv2.inRange(hsv, lower_yellow, upper_yellow)]
        # for mask in masks:
        #     res = cv2.bitwise_and(frame, frame, mask=mask)

        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res += cv2.bitwise_and(frame, frame, mask=mask)
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        res += cv2.bitwise_and(frame, frame, mask=mask)

        # define range of blue color in HSV
        # lower_blue = np.array([100, 40, 40])

        # Threshold the HSV image to get only blue colors
        # mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        # res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('res', res)

        # gaus = cv2.GaussianBlur(frame, (5, 5), 0)
        edge = cv2.Canny(res, 10, 20)
        # cv2.imshow('gaus', gaus)
        cv2.imshow('edge', edge)

        # find contours in the thresholded image
        cnts = cv2.findContours(edge, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # compute the center of the contour
            if cv2.contourArea(c) < 200:
                continue

            M = cv2.moments(c)

            # Compare if area of the contour is the same
            # As the area of the image, with an error of 3 %
            if M["m00"] >= frame.shape[0] * frame.shape[1] * 0.97:
                print("Contour of the same size as the image skipped")
                continue

            try:
                cX = int((M["m10"] / M["m00"]))
                cY = int((M["m01"] / M["m00"]))
            except ZeroDivisionError:
                print("Skipping a contour")
                continue

            cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

        cv2.imshow('cont', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
cap.release()
