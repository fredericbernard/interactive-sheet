import numpy as np
import yaml

with open('distance_calibration.yaml') as f:
    loaded_dict = yaml.load(f)

iR = loaded_dict.get('inverse_rotation_matrix')
iR = np.asarray(iR)
iC = loaded_dict.get('inverse_camera_matrix')
iC = np.asarray(iC)
tvec = loaded_dict.get('tvec')
tvec = np.asarray(tvec)


uvPoint = np.array([351, 324, np.ones(shape=1)]).reshape(3, 1)
t = iR.dot(iC).dot(uvPoint)
t2 = iR.dot(tvec)
s = (0 + t2[2]) / t[2]
objectPoint = (iR.dot(s.item(0) * iC.dot(uvPoint) - tvec))
print(objectPoint)
