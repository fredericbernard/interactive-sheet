import argparse
import json
import tkinter as tk
from tkinter import simpledialog

import subprocess
from PIL import Image, ImageTk

import os

parser = argparse.ArgumentParser(description="dataset labelmaker")
parser.add_argument("--base-dir", help='base dir destination [default : labelled_dataset]', dest='base_dir',
                    default="labelled_datasets", type=str)
parser.add_argument(help='dataset name', dest='dataset_name', type=str)
parser.add_argument("--unlabelled-datasets", help="unlabelled datasets [default: training_datasets]",
                    dest='unlabelled_datasets', default="training_datasets", type=str)
parser.add_argument("--parameter-name", help="label parameter name [default: position]", dest="parameter_name",
                    default="position", type=str)
args = parser.parse_args()

dataset_files = os.listdir(args.unlabelled_datasets + "/" + args.dataset_name)


def getNextPicture():
    return args.unlabelled_datasets + "/" + args.dataset_name + "/" + dataset_files.pop(0)


class MainWindow:
    def __init__(self):
        self.master = tk.Tk()
        self.canvas = tk.Canvas(self.master, width=1280, height=720)
        self.datasetNameLabel = tk.Label(self.master, text=args.dataset_name)
        self.currentPictureFilenameLabel = tk.Label(self.master, text='')
        self.doneButton = tk.Button(self.master, text="Next Picture", command=self.update_picture)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.attributes = [args.parameter_name]
        self.attributeValues = {}
        self.grabbing = self.attributes[0]
        self.serializedData = {}
        self.picture = None
        self.newAttributeButton = tk.Button(self.master, text="New Attribute", command=self.new_attribute)

        self.attributeLabels = [tk.Label(self.master, text=attribute + ":") for attribute in self.attributes]
        self.attributeValueBoundVariables = [tk.StringVar() for attribute in self.attributes]
        self.attributeValueBoxes = [tk.Entry(self.master, textvariable=v) for v in self.attributeValueBoundVariables]
        self.attributeButtons = [
            tk.Button(self.master, text="grab {}".format(attribute), command=lambda: self.grab_position(attribute)) for
            attribute in self.attributes]

        self.update_picture()

    def draw_components(self):
        self.canvas.grid(row=1, column=1)
        self.datasetNameLabel.grid(row=0, column=0)
        self.currentPictureFilenameLabel.grid(row=0, column=1)
        self.doneButton.grid(row=2, column=1)
        self.newAttributeButton.grid(row=2, column=2)

        for i in range(len(self.attributes)):
            self.attributeLabels[i].grid(row=i, column=3)
            self.attributeValueBoundVariables[i].set(self.attributeValues.get(self.attributes[i]))
            self.attributeValueBoxes[i].grid(row=i, column=4)
            self.attributeButtons[i].grid(row=i, column=5)
            self.attributeValueBoxes[i].bind("<Return>", lambda _: self.manually_set_attribute(i))

    def update_picture(self):
        if self.picture is not None:
            self.serializedData[self.picture] = dict(self.attributeValues)
            self.save_attributes()
        if dataset_files:
            self.grabbing = self.attributes[0]
            self.picture = getNextPicture()

            self.canvas.image = ImageTk.PhotoImage(Image.open(self.picture))
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')
            self.currentPictureFilenameLabel = tk.Label(self.master, text=self.picture)
            self.draw_components()
        else:
            print("done! there are no more pictures.")
            tk.simpledialog.askstring("you are done", "there are no more images. You can close this program.")

    def on_canvas_click(self, event):
        if self.grabbing:
            self.attributeValues[self.grabbing] = (event.x, event.y)
            self.grabbing = None
            self.draw_components()
        print(self.attributeValues)

    def grab_position(self, attributeName):
        self.grabbing = attributeName
        print("grabbing attribute {}".format(attributeName))

    def new_attribute(self):
        attribute = simpledialog.askstring("New Attribute", "New Attribute name:")
        self.attributes.append(attribute)
        self.attributeLabels.append(tk.Label(self.master, text=attribute + ":"))
        v = tk.StringVar()
        self.attributeValueBoundVariables.append(v)
        self.attributeValueBoxes.append(tk.Entry(self.master, textvariable=v))
        self.attributeButtons.append(tk.Button(self.master, text="grab {}".format(attribute),
                                               command=lambda: self.grab_position(attribute)))
        self.draw_components()

    def manually_set_attribute(self, attribute_index):
        attribute_value = self.attributeValueBoundVariables[attribute_index].get()
        self.attributeValues[self.attributes[attribute_index]] = attribute_value
        self.draw_components()

    def save_attributes(self):

        subprocess.call(["mkdir", "-p", args.base_dir])
        subprocess.call(["touch", args.base_dir + "/" + args.dataset_name])
        with open(args.base_dir + "/" + args.dataset_name, 'w') as file:
            json.dump(self.serializedData, file, ensure_ascii=False)

    def mainloop(self):
        self.master.mainloop()


MainWindow().mainloop()
