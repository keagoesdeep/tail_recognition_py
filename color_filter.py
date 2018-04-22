import cv2
import numpy as np
import imutils
import threading
import camera_settings
from camera_settings import LOW_BLUE, LOW_RED, LOW_YELLOW, UPPER_BLUE, UPPER_RED, UPPER_YELLOW
from shapedetector import detect_shape


def hsv_to_opencv(color):
    hue = int(color["hue"] / 2)
    saturation = int(color["saturation"] * 255 / 100)
    value = int(color["value"] * 255 / 100)
    return [hue, saturation, value]


camera_settings = camera_settings.CameraSettings()
threading.Thread(target=camera_settings.init_ui).start()

shapes = {'red': None, 'blue': None, 'yellow': None, 'none': 'No colour'}
biggest_contour_areas = {'red': -1, 'blue': -1, 'yellow': -1}

cap = cv2.VideoCapture(1)
# TODO: Lower the frame rate to like 20
while True:
    read, frame = cap.read()
    if read:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_red = np.array(hsv_to_opencv(camera_settings.get_values(LOW_RED)))
        upper_red = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_RED)))

        lower_yellow = np.array(hsv_to_opencv(camera_settings.get_values(LOW_YELLOW)))
        upper_yellow = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_YELLOW)))

        lower_blue = np.array(hsv_to_opencv(camera_settings.get_values(LOW_BLUE)))
        upper_blue = np.array(hsv_to_opencv(camera_settings.get_values(UPPER_BLUE)))

        masks = {'red': cv2.inRange(hsv, lower_red, upper_red), 'blue': cv2.inRange(hsv, lower_blue, upper_blue),
                 'yellow': cv2.inRange(hsv, lower_yellow, upper_yellow)}

        cv2.imshow('red', masks['red'])
        cv2.imshow('blue', masks['blue'])
        cv2.imshow('yellow', masks['yellow'])

        for key in masks.keys():

            mask = masks[key]
            res = cv2.bitwise_and(frame, frame, mask=mask)
            # cv2.imshow('res', res)  # for debugging

            # edge = cv2.Canny(res, 10, 20)
            # cv2.imshow('edge', edge)  # for debugging

            # gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
            # thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)[1]

            # cv2.imshow('gray', gray)
            # cv2.imshow('thresh', thresh)

            # find contours in the edged image
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if imutils.is_cv2() else contours[1]

            biggest_contour_area = -1
            biggest_contour = None

            if len(contours) != 0:

                # find the biggest area
                c = max(contours, key=cv2.contourArea)

                # find the biggest contour for the colour
                contour_area = cv2.contourArea(c)
                # if contour_area < 200:
                #     continue

                if contour_area > biggest_contour_area:
                    biggest_contour_area = contour_area
                    biggest_contour = c
                    biggest_contour_areas[key] = biggest_contour_area
                    shapes[key] = detect_shape(c)

                M = cv2.moments(c)

                # Compare if area of the contour is the same
                # As the area of the image, with an error of 3 %
                if M["m00"] >= frame.shape[0] * frame.shape[1] * 0.97:
                    print("Contour of the same size as the image, skipped")
                    continue

                try:
                    cX = int((M["m10"] / M["m00"]))
                    cY = int((M["m01"] / M["m00"]))
                except ZeroDivisionError:
                    print("Skipping a contour")
                    continue

                cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)

        temp = -1
        final_key = 'none'
        for key in biggest_contour_areas.keys():
            area = biggest_contour_areas[key]
            if area > temp:
                temp = area
                final_key = key

        if shapes[final_key] is not None:
            print(final_key + ' ' + shapes[final_key])

        cv2.imshow('cont', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
cap.release()
