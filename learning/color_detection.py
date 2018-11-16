import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i")
args = vars(ap.parse_args())

img = cv2.imread(args["i"])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('img', img)
cv2.imshow('mask', mask)
cv2.imshow('result', result)

cv2.waitKey(0)

