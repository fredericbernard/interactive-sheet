import glob
import os

import cv2

import learning


class LocalImageRepository(object):

    def __init__(self, dataset_name: str):
        folder_name = os.path.join(os.path.dirname(os.path.dirname(learning.__file__)), "infra/training_datasets")
        folder_name = os.path.join(folder_name, dataset_name)
        self.files = glob.glob(folder_name + "/*.jpg")

    def get_image(self):
        return cv2.imread(self.files.pop(0))
