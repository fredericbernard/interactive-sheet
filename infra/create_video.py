import cv2
import subprocess

import os

CAMERA_FILE = "/dev/video0"



def load_camera_settings():
    subprocess.call(["uvcdynctrl", "-L", "cameraSettings.txt", "-d", CAMERA_FILE])

load_camera_settings()
cap = cv2.VideoCapture(CAMERA_FILE)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

load_camera_settings()

load_camera_settings()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_file = 'output.avi'

counter = 0
while os.path.isfile(output_file):
    output_file = f'output{counter}.avi'
    counter +=1

out = cv2.VideoWriter(output_file, fourcc, 10.0, (1280, 800))
load_camera_settings()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
