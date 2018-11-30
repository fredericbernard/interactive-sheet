import argparse

import cv2
import tkinter as tk
from tkinter import messagebox

import subprocess

import os

parser = argparse.ArgumentParser(description="dataset creator")
parser.add_argument("--base-dir", help='base dir destination [default : training_datasets]', dest='base_dir',
                    default="training_datasets", type=str)
parser.add_argument("--camera", help="camera file [default: /dev/video0]", dest='camera', default="/dev/video0",
                    type=str)
parser.add_argument("--dataset-name", help='dataset name', dest='dataset_name', default="my_dataset1", type=str)
parser.add_argument("--numbering-start", help='numbering start value', dest='numbering_start', default=0, type=int)

args = parser.parse_args()

capture = cv2.VideoCapture(args.camera)

capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)


def get_latest_image(capture: cv2.VideoCapture):
    for i in range(4):
        capture.grab()
    is_frame_returned, frame = capture.read()
    return frame


imageCount = args.numbering_start


def get_next_filename():
    global imageCount
    imageCount += 1
    return imageCount


def on_button_click():
    global imageComponent
    image = get_latest_image(capture)
    cv2.imwrite("{}/image_{}.jpg".format(args.base_dir + "/" + args.dataset_name, get_next_filename()), image)
    cv2.imwrite("currentFrame.png", image)
    imageComponent = tk.PhotoImage(file="currentFrame.png")
    tk.Button(window, image=imageComponent).grid(row=1, column=2)


def load_camera_settings():
    subprocess.call(["uvcdynctrl", "-L", "cameraSettings.txt", "-d", args.camera])


def check_dataset_existence_or_create_dir():
    if os.path.isdir(args.base_dir + "/" + args.dataset_name):
        res = messagebox.askokcancel("Warning",
                                     "Dataset '{}' already exists. Images will be overwritten. Do you want to continue?".format(
                                         args.dataset_name))
        if not res:
            quit(0)
    else:
        os.makedirs(args.base_dir + "/" + args.dataset_name)


window = tk.Tk()

dataset_name_label = tk.Label(window, text=args.dataset_name)
captureButton = tk.Button(window, text="capture", command=on_button_click)

dataset_name_label.grid(row=0, column=0)

captureButton.grid(row=2, column=0)

image = get_latest_image(capture)

load_camera_settings()
check_dataset_existence_or_create_dir()

window.mainloop()

capture.release()
