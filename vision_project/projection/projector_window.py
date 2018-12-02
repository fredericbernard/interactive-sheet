from tkinter import *

from jivago.lang.registry import Singleton, Component


@Singleton
@Component
class ProjectorWindow(object):

    # w.create_line(0, 0, 200, 100)
    # w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

    # w.create_rectangle(50, 25, 150, 75, fill="blue")
    # w.create_line(0, 0, 600, 600, fill='black', width=5)

    def main(self):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=800, height=600, background='white')
        self.canvas.pack()
        mainloop()

