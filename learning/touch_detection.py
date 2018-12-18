import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["i"])


def get_area(contours):
    contour_area = []
    for i in range(len(contours)):
        cnt = contours[i]
        contour_area.append(cv2.contourArea(cnt))

    return zip(contours, contour_area)


while cap.isOpened():
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([40, 25, 25])
    upper_color = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    dilate = cv2.dilate(closing, kernel, iterations=1)

    _, threshold = cv2.threshold(mask, 40, 255, 0)
    _, contours, _ = cv2.findContours(threshold, 1, 2)
    areas = sorted(get_area(contours), key=lambda tup: tup[1])

    if(areas[-2][1] < 1200.0):
        print("TOUCHING!")
    else:
        print("not touching...")

    cv2.imshow("Live Feed closing", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
