import os

import cv2

import infra
from vision_project.vision.image import Image
from vision_project.vision.image_repository import LocalDirectoryImageRepository, LiveCapture, \
    LiveCaptureNoCacheEmptying

# image_repository = LocalDirectoryImageRepository(os.path.join(os.path.dirname(infra.__file__), "training_datasets/720p-not-touching"))

image_repository = LiveCaptureNoCacheEmptying(os.path.join(os.path.dirname(infra.__file__),"videos/3.avi"))

# image_repository.capture.set(cv2.CV_CAP_PROP_FPS, 10)

fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    image = image_repository.get_next_image()
    image.show_do_not_close(25, name="image")

    fgmask = fgbg.apply(image.frame)

    # cv2.imshow('frame', fgmask)

    Image(fgmask).show_do_not_close(25, name="bgmask")



