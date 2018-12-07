import numpy as np
import os
import cv2
import glob
import yaml

from numpy.linalg import inv

import infra

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
objp = 23 * objp

objpoints = []
imgpoints = []

images = glob.glob(os.path.join(os.path.dirname(infra.__file__), "training_datasets/calibration-éclairée2/*.jpg"))

for filename in images:
    image = cv2.imread(filename)
    image_in_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    value_returned, corners = cv2.findChessboardCorners(image_in_gray, (9,6), None)

    if value_returned:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(image_in_gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        cv2.drawChessboardCorners(image, (9,6), corners2, value_returned)
        cv2.imshow('img', image)
        cv2.waitKey(0)
    else:
        os.remove(filename)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, image_in_gray.shape[::-1], None, None)

img = cv2.imread(os.path.join(os.path.dirname(infra.__file__), "training_datasets/720p-touching/image_1.jpg"))
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
#x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
cv2.imwrite('./image_without_distortion.jpg', dst)

mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print('total error: {}'.format(mean_error/len(objpoints)))

data = {'camera_matrix': np.asarray(mtx).tolist(), 'dist_coeff': np.asarray(dist).tolist()}
with open('../distance_calibration/camera_calibration.yaml', 'w') as f:
    yaml.dump(data, f)
