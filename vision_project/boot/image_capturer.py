import os
import subprocess

import cv2
import time
from jivago.config.properties.system_environment_properties import SystemEnvironmentProperties
from jivago.lang.annotations import BackgroundWorker, Inject
from jivago.lang.runnable import Runnable

import infra
from vision_project.vision import config
from vision_project.vision.distortion_remover import DistortionRemover
from vision_project.vision.image import Image
from vision_project.vision.image_repository import ImageRepository, SimpleImageRepository

capture = None


@BackgroundWorker
class ImageCapturer(Runnable):

    @Inject
    def __init__(self, image_repository: ImageRepository, environment: SystemEnvironmentProperties, distortion_remover: DistortionRemover):
        self.distortion_remover = distortion_remover
        self.image_repository: SimpleImageRepository = image_repository
        self.video_capture_file = environment.get('CAPTURE')
        if self.video_capture_file is None and environment.get('DEBUG'):
            self.video_capture_file = os.path.join(os.path.dirname(infra.__file__), "videos/3.avi")
        elif self.video_capture_file is None:
            self.video_capture_file = "/dev/video0"

    def run(self):
        global capture
        while True:
            if capture is None:
                capture = cv2.VideoCapture(self.video_capture_file)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

                load_camera_settings(self.video_capture_file)

            is_frame_returned, frame = capture.read()
            if is_frame_returned:
                frame_without_distortion = self.distortion_remover.remove_distortion(frame)
                self.image_repository.set_image(Image(frame_without_distortion))
            else:
                capture = cv2.VideoCapture(self.video_capture_file)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

                load_camera_settings(self.video_capture_file)
            if os.environ.get('DEBUG'):
                time.sleep(0.1)

    def cleanup(self):
        capture.release()
        cv2.destroyAllWindows()


def load_camera_settings(camera_file: str):
    settings_file = os.path.join(os.path.dirname(config.__file__), "cameraSettings.txt")
    try:
        subprocess.call(["uvcdynctrl", "-L", settings_file, "-d", camera_file])
    except:
        pass
