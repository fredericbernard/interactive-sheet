import cv2

from vision_project.vision.image import Image


def bgr_to_hsv(image: Image) -> Image:
    return image.to_color_space(cv2.COLOR_BGR2HSV)


def hsv_to_bgr(image: Image) -> Image:
    return image.to_color_space(cv2.COLOR_HSV2BGR)


def bgr_to_gray(image: Image) -> Image:
    return image.to_color_space(cv2.COLOR_BGR2GRAY)


def hsv_to_gray(image: Image) -> Image:
    temp = image.to_color_space(cv2.COLOR_HSV2BGR)
    return temp.to_color_space(cv2.COLOR_BGR2GRAY)


def gray_to_bgr(image: Image) -> Image:
    return image.to_color_space(cv2.COLOR_GRAY2BGR)
