import numpy as np
import cv2
import yaml

from numpy.linalg import inv

with open('camera_calibration.yaml') as f:
    loaded_dict = yaml.load(f)

mtx = loaded_dict.get('camera_matrix')
mtx = np.asarray(mtx)
dist = loaded_dict.get('dist_coeff')
dist = np.asarray(dist)
39.71869
imagePoints = np.array([[722, 539], [351, 524], [379, 167], [731, 187]], dtype=np.float32)
objectPoints = np.array([[0, 0, 0], [0, 1110, 0], [2310, 1110, 0], [2310, 0, 0]], dtype=np.float32) 

ret, rvec, tvec = cv2.solvePnP(objectPoints, imagePoints, mtx, dist)
rotation_vector = cv2.Rodrigues(rvec)[0]
rotation_matrix = np.matrix(rotation_vector)
cameraMatrix = np.matrix(mtx)

uvPoint = np.array([390, 498, np.ones(shape=1)]).reshape(3, 1)

iR = inv(rotation_matrix)
iC = inv(cameraMatrix)

data = {'inverse_rotation_matrix': np.asarray(iR).tolist(), 'inverse_camera_matrix': np.asarray(iC).tolist(), 'tvec': np.asarray(tvec).tolist()}

with open('distance_calibration.yaml', 'w') as f:
    yaml.dump(data, f)
