import threading
from time import sleep

from vision_project.projection.projector_window import ProjectorWindow
from vision_project.vision.coordinate_converter import CoordinateConverter
from vision_project.vision.image_repository import LiveCapture


def draw_circle(canvas, x, y, rad):
    return canvas.create_oval(x - rad, y - rad, x + rad, y + rad, width=0, fill='blue')

if __name__ == '__main__':
    window = ProjectorWindow()
    thread = threading.Thread(target=window.main)
    thread.start()
    capture = LiveCapture("/dev/video0")



    print("wating 5 seconds before starting...")
    sleep(5)

    converter = CoordinateConverter()

    for x in range(-200, 1000, 100):
        print(f"({x},{x})")
        camera_coord = (x, x)
        projector_coord = converter.camera_coordinate_to_projector_coordinate(*camera_coord)

        draw_circle(window.canvas, projector_coord.x, projector_coord.y, rad=10)

        capture.get_next_image().show_do_not_close()
        sleep(1)

    while True:
        capture.get_next_image().show_do_not_close()
        sleep(1)
