from PIL import Image, ImageDraw

import Shapes
import Input
import Signal


class Creator(Signal.SignalListener):
    def __init__(self, im_size):
        if type(im_size) != tuple or len(im_size) != 2:
            raise ValueError(
                "Position must be tuple with length 2", im_size)
        self.im_size = im_size

        self.image = Image.new("RGB", self.im_size, (0, 0, 0))
        self.canvas = ImageDraw.Draw(self.image)
        self.shape_manager = Shapes.ShapeManager()

        self.input_manager = Input.Input()
        self.input_manager.subscribe(self)

    def save_canvas(self, output_file="output.png"):
        self.image.save(output_file)

    def undo_command(self):
        print("undoing...")

    def redo_command(self):
        print("redoing...")

    def check_command(self, command):
        commands = [
            ["undo", self.undo_command],
            ["redo", self.redo_command]
        ]

        for c in commands:
            if c[0] == command:
                c[1]()
                break

    def signal_raised(self, message):
        self.check_command(message)

    def temp(self):
        tr = []

        for i in range(10):
            tr.append(Shapes.Triangle((0, 150), (1, 1), 36 * i, 60, self.shape_manager))

        re = Shapes.Triangle((0, -50), (1, 1), 0, 200, self.shape_manager)

        self.shape_manager.draw(self.canvas, self.im_size)

        for t in tr:
            new_pos = (t.position[0], t.position[1] - 50)
            t.set_position(new_pos)

        self.shape_manager.draw(self.canvas, self.im_size)


def main():
    creator = Creator((400, 400))


if __name__ == "__main__":
    main()
