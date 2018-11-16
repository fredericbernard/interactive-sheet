import cv2

from learning.local_image_repository import LocalImageRepository

image_repository = LocalImageRepository("dataset_1")

cv2.imshow('image', image_repository.get_image())
cv2.waitKey(0)
