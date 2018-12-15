import numpy as np
import cv2
from cv2 import aruco
import glob
import yaml

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
parameters = aruco.DetectorParameters_create()

"""
with open('camera_calibration.yaml') as f:
    loaded_dict = yaml.load(f)

camera_matrix = loaded_dict.get('camera_matrix')
camera_matrix = np.asarray(camera_matrix)
dist = loaded_dict.get('dist_coeff')
dist = np.asarray(dist)

images = glob.glob('./aruco_iamges/*jpg')
 = 0

for filename in images:
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    image_in_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(image_in_gray, aruco_dict, parameters=parameters)
    rvec, tvec, t = aruco.estimatePoseSingleMarkers(corners, 100, camera_matrix, dist)
    image_with_corner = aruco.drawDetectedMarkers(image, corners, ids, (0, 255, 0))
    image_with_corner = aruco.drawAxis(image_with_corner, camera_matrix, dist, rvec, tvec, 100)
    cv2.imwrite('./aruco_iamges/aruco_image_with_corner/image{}.jpg'.format(i), image_with_corner)
    i += 1
    
"""
camera = cv2.VideoCapture(1)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
while True:
    ret, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners)

    gray = aruco.drawDetectedMarkers(frame, corners)

    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
