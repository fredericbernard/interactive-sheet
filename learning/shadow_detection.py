import cv2

if __name__ == "__main__":
    capture = cv2.VideoCapture()
    image = cv2.imread("../infra/training_datasets/dataset_1/image_2.jpg", cv2.IMREAD_GRAYSCALE)



    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
