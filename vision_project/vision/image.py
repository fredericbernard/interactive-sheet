import cv2
import numpy as np

from vision_project.vision.util import Mask, PixelCoordinate


class Image:

    def __init__(self, opencv_frame):
        self.frame = opencv_frame

    def to_color_space(self, color_space_transform) -> "Image":
        new_frame = cv2.cvtColor(self.frame, color_space_transform)
        return Image(new_frame)

    def show_on_window(self):
        cv2.namedWindow('frame')
        cv2.imshow('frame', self.frame)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def show_and_close(self, timeout=250):
        cv2.namedWindow('frame')
        cv2.imshow('frame', self.frame)
        cv2.waitKey(timeout)
        cv2.destroyAllWindows()

    def get_in_range_mask(self, lower: list, higer: list) -> Mask:
        matrix = cv2.inRange(self.frame, np.array(lower, dtype='uint8'), np.array(higer, dtype='uint8'))
        return Mask(matrix)

    def apply_mask(self, mask: Mask) -> "Image":
        masked_frame = cv2.bitwise_and(self.frame, self.frame, mask=mask.matrix)
        return Image(masked_frame)

    def erode_rect(self, size: int, *, iterations=1) -> "Image":
        return Image(cv2.erode(self.frame, np.ones((size, size), np.uint8), iterations=iterations))

    def dilate_rect(self, size: int, *, iterations=1) -> "Image":
        return Image(cv2.dilate(self.frame, np.ones((size, size), np.uint8), iterations=iterations))

    def binary_threshold(self, thresh: int, max_val: int) -> "Image":
        retval, image_binary = cv2.threshold(self.frame, thresh, max_val, cv2.THRESH_BINARY)
        return Image(image_binary)

    @property
    def width(self):
        return self.frame.shape[1]

    @property
    def height(self):
        return self.frame.shape[0]

    def __getitem__(self, pixel: PixelCoordinate) -> np.array:
        return self.frame[pixel.y, pixel.x]

    def __setitem__(self, pixel: PixelCoordinate, value):
        self.frame[pixel.y, pixel.x] = value

    def contains(self, pixel: PixelCoordinate) -> bool:
        return pixel.x >= 0 and pixel.y >= 0 and pixel.x < self.width and pixel.y < self.height
