import subprocess
from os import listdir, path
from os.path import isfile, join

import cv2

from vision_project.vision.image import Image
from vision_project.vision.util import PixelCoordinate


class ImageRepository:

    def get_next_image(self) -> Image:
        raise NotImplementedError()


class LocalDirectoryImageRepository(ImageRepository):

    def __init__(self, directory_path: str):
        self.directory = directory_path
        self.files = [f for f in listdir(self.directory) if isfile(join(self.directory, f))]
        self.current_file = path.basename(self.files[0])
        self.files.sort()

    def get_next_image(self) -> Image:
        next_file = self.files.pop()
        file_name = join(self.directory, next_file)
        self.current_file = path.basename(file_name)
        return Image(cv2.imread(file_name))

    def get_current_file(self):
        return self.current_file

    def more_images(self):
        return self.files


class LiveCaptureNoCacheEmptying:

    def __init__(self, camera_filename: str):
        self.capture = cv2.VideoCapture(camera_filename)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.get_next_image()
        load_camera_settings(camera_filename)

    def get_next_image(self) -> "Image":
        is_frame_returned, frame = self.capture.read()
        return Image(frame)

    def release_capture_device(self):
        self.capture.release()
        cv2.destroyAllWindows()

class LiveCapture:

    def __init__(self, camera_filename: str):
        self.capture = cv2.VideoCapture(camera_filename)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.get_next_image()
        load_camera_settings(camera_filename)

    def get_next_image(self) -> "Image":
        for i in range(4):
            self.capture.grab()
        is_frame_returned, frame = self.capture.read()
        return Image(frame)

    def release_capture_device(self):
        self.capture.release()
        cv2.destroyAllWindows()


def load_camera_settings(camera_file: str):
    try:
        subprocess.call(["uvcdynctrl", "-L", "../infra/cameraMondeSettings.txt", "-d", camera_file])
    except:
        pass



# for testing
import json

class LabelledImageRepository:
    def __init__(self, training_data_path: str, labelled_data_path: str):
        self.image_repository = LocalDirectoryImageRepository(training_data_path)
        f = open(labelled_data_path)
        self.label = dict([(path.basename(key), value) for key, value in json.load(f).items()])
        f.close()

    def get_test_data_from_dataset(self) -> tuple:
        image = self.image_repository.get_next_image()
        file_name = self.image_repository.get_current_file()
        return image, self.label[file_name], file_name

    def get_robot_test_data_from_dataset(self) -> dict:
        image = self.image_repository.get_next_image()
        file_name = self.image_repository.get_current_file()
        return {
            'file-name': file_name,
            'image': image,
            'position': PixelCoordinate(*self.label[file_name]["position"]),
            'orientation': PixelCoordinate(*self.label[file_name]["front"])
        }

    def more_images(self) -> bool:
        return self.image_repository.more_images()
