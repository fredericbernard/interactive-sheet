from tkinter import *

from jivago.lang.registry import Singleton, Component

from vision_project.vision.util import ProjectorCoordinate


@Singleton
@Component
class ProjectorWindow(object):

    def draw_line(self, start: ProjectorCoordinate, end: ProjectorCoordinate):
        self.canvas.create_line(start.x, start.y, end.x, end.y, fill='black', width=1)

    def clear_canvas(self):
        self.canvas.delete('all')

    def main(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=800, height=600, background='white')
        self.canvas.pack()
        mainloop()
