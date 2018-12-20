import math
from tkinter import *

from jivago.lang.registry import Singleton, Component

from vision_project.vision.util import ProjectorCoordinate


@Singleton
@Component
class ProjectorWindow(object):

    def draw_line(self, start: ProjectorCoordinate, end: ProjectorCoordinate):
        self.canvas.create_line(start.x, start.y, end.x, end.y, fill='magenta', width=2)

    def add_text(self, text: str, center: ProjectorCoordinate, angle: int):
        angle_in_deg = -math.degrees(angle) - 70
        print(angle_in_deg)
        self.canvas.create_text(center.x, center.y, fill="darkblue", font="Times 12 bold", text=text,
                                angle=angle_in_deg)

    def clear_canvas(self):
        self.canvas.delete('all')

    def main(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=1024, height=768, background='white')
        self.canvas.pack()
        mainloop()


if __name__ == '__main__':
    ProjectorWindow().main()
