import cv2
camera = cv2.VideoCapture(0)
counter = 1
while(1):
    ret, image = camera.read()
    cv2.imshow("image", image)
    key = cv2.waitKey(33)
    if key == ord('y'):
        cv2.imwrite("image_{}.jpg".format(counter), image) 
        counter += 1
    elif key == ord('q'):
        break


