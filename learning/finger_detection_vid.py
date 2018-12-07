import cv2
import numpy as np

import numpy as np
import argparse
import cv2

def get_centroid(contour):
    moment = cv2.moments(contour)
    cx = int(moment['m10'] / moment['m00'])
    cy = int(moment['m01'] / moment['m00'])
    return cx, cy

def draw_circles(frame, traverse_point):
    if traverse_point is not None:
        for i in range(len(traverse_point)):
            cv2.circle(frame, traverse_point[i], int(5 - (5 * i * 3) / 100), [0, 255, 255], -1)

def farthest_point(defects, contour, centroid):
    if defects is not None and centroid is not None:
        s = defects[:, 0][:, 0]
        cx, cy = centroid

        x = np.array(contour[s][:, 0][:, 0], dtype=np.float)
        y = np.array(contour[s][:, 0][:, 1], dtype=np.float)

        xp = cv2.pow(cv2.subtract(x, cx), 2)
        yp = cv2.pow(cv2.subtract(y, cy), 2)
        dist = cv2.sqrt(cv2.add(xp, yp))

        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(contour[farthest_defect][0])
            return farthest_point
        else:
            return None


def max_area(contour_list):
    largest_area = 0;
    largest_contour_index = 0

    for i in range(len(contour_list)):
        cnt = contour_list[i]
        area_cnt = cv2.contourArea(cnt)

        if (area_cnt > largest_area):
            largest_area = area_cnt
            largest_contour_index = i

    return contour_list[largest_contour_index]

traverse_point = []

ap = argparse.ArgumentParser()
ap.add_argument("-i")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["i"])

while cap.isOpened():
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = np.array([50, 50, 50])
    upper_color = np.array([75, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    _, threshold = cv2.threshold(mask, 40, 255, 0)

    _, contours, _ = cv2.findContours(threshold, 1, 2)

    max_contour = max_area(contours)

    #cv2.drawContours(frame, max_contour, -1, 255, 3)
    cnt_centroid = get_centroid(max_contour)
    #cv2.circle(frame, cnt_centroid, 5, [255, 0, 255], -1)

    rows, cols = frame.shape[:2]
    [vx, vy, x, y] = cv2.fitLine(max_contour, cv2.DIST_L2, 0, 0.01, 0.01)
    lefty = int((-x * vy / vx) + y)
    righty = int(((cols - x) * vy / vx) + y)
    img = cv2.line(frame, (cols - 1, righty), (0, lefty), (0, 255, 0), 2)

    if max_contour is not None:
        hull = cv2.convexHull(max_contour, returnPoints=False)
        defects = cv2.convexityDefects(max_contour, hull)
        far_point = farthest_point(defects, max_contour, cnt_centroid)
        cv2.circle(frame, far_point, 5, [0, 0, 255], -1)
        if len(traverse_point) < 20:
            traverse_point.append(far_point)
        else:
            traverse_point.pop(0)
            traverse_point.append(far_point)

        draw_circles(frame, traverse_point)

    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()