import os

import cv2
import numpy as np

import infra
from vision_project.vision import colourspace
from vision_project.vision.image import Image
from vision_project.vision.image_repository import LocalDirectoryImageRepository

image_repository = LocalDirectoryImageRepository(
    os.path.join(os.path.dirname(infra.__file__), "training_datasets/720p-touching"))

# image_repository = LiveCaptureNoCacheEmptying(os.path.join(os.path.dirname(infra.__file__),"videos/3.avi"))

# image_repository.capture.set(cv2.CV_CAP_PROP_FPS, 10)


while True:
    image = image_repository.get_next_image()
    image = Image(cv2.imread(os.path.join(os.path.dirname(infra.__file__), "training_datasets/720p-touching/image_62.jpg")))
    image.show_do_not_close(2500, name="image")

    hsv_image = colourspace.bgr_to_hsv(image)

    white_mask = hsv_image.get_in_range_mask([0, 0, 150], [180, 255, 235])

    masked_image = image.apply_mask(white_mask)

    im, contours, hier = cv2.findContours(white_mask.matrix, cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)

    boxes = []

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if w > 100 and h > 100:
            cv2.rectangle(image.frame, (x,y), (x+w, y+h), (0,255,0), 2)

            min_rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(min_rect)
            print(min_rect)
            # convert all coordinates floating point values to int
            box = np.int0(box)

            cv2.drawContours(image.frame, [box], 0, (0, 0, 255))
            boxes.append(box)


    image.show_do_not_close(100)
    print(boxes)
    # cv2.imshow('frame', fgmask)

    # Image(fgmask).show_do_not_close(25, name="bgmask")
