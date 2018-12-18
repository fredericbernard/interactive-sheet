import cv2
import yaml
import numpy as np


class DistortionRemover:

    def __init__(self):
        with open('/cameracalibration/camera_calibration_hi_res.yaml') as f:
            loaded_dict = yaml.load(f)

        camera_matrix = loaded_dict.get('camera_matrix')
        self.camera_matrix = np.asarray(camera_matrix)
        distortion_coefficient = loaded_dict.get('dist_coeff')
        self.distortion_coefficient = np.asarray(distortion_coefficient)

    def remove_distortion(self, image):
        height, width = image.shape[:2]
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.distortion_coefficient,
                                                               (width, height), 1, (width, height))

        return cv2.undistort(image, self.camera_matrix, self.distortion_coefficient, None, new_camera_matrix)
