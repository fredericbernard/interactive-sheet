import numpy as np

import cv2

from typing import Optional

from jivago.lang.registry import Component

from vision_project.detection.finger import Finger
from vision_project.vision.image import Image
from vision_project.vision.util import Mask

MAX_THRESHOLD = 255
THRESHOLD = 40
HIGER_RANGE = [75, 255, 255]
LOWER_RANGE = [50, 50, 50]


@Component
class FingerDetector(object):

    def find_finger(self, image: Image) -> Optional[Finger]:
        mask = image.to_color_space(cv2.COLOR_BGR2HSV).get_in_range_mask(LOWER_RANGE, HIGER_RANGE)
        contours = self.get_contours(mask)
        max_area = self.max_area(contours)
        point = self.get_farthest_point(max_area)
        return self.coord_to_finger(point)

    def get_contours(self, mask: Mask):
        _, threshold = cv2.threshold(mask.matrix, THRESHOLD, MAX_THRESHOLD, 0)
        _, contours, _ = cv2.findContours(threshold, 1, 2)
        return contours

    def max_area(self, contour_list):
        largest_area = 0;
        largest_contour_index = 0

        for i in range(len(contour_list)):
            cnt = contour_list[i]
            area_cnt = cv2.contourArea(cnt)

            if (area_cnt > largest_area):
                largest_area = area_cnt
                largest_contour_index = i

        return contour_list[largest_contour_index]

    def get_centroid(self, contour):
        moment = cv2.moments(contour)
        cx = int(moment['m10'] / moment['m00'])
        cy = int(moment['m01'] / moment['m00'])
        return cx, cy

    def get_farthest_point(self, max_area):
        centroid = self.get_centroid(max_area)
        conv_hull = cv2.convexHull(max_area, returnPoints=False)
        conv_defects = cv2.convexityDefects(max_area, conv_hull)

        if centroid is not None and conv_defects is not None:
            s = conv_defects[:, 0][:, 0]
            cx, cy = centroid
            x = np.array(max_area[s][:, 0][:, 0], dtype=np.float)
            y = np.array(max_area[s][:, 0][:, 1], dtype=np.float)
            dist = cv2.squrt(cv2.add(cv2.pow(cv2.substract(x, cx), 2), cv2.pow(cv2.substract(y, cy), 2)))
            max_dist = np.argmax(dist)

            if max_dist < len(s):
                far_conv_defect = s[max_dist]
                farthest_point = tuple(max_area[far_conv_defect][0])
                return farthest_point
            else:
                return None

    def coord_to_finger(self, point):
        if point is not None:
            return Finger(point)
        return None
