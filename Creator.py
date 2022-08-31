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

    def save_canvas(self, output_filename="output.png"):
        self.image.save(output_filename)

    def show_image(self):
        self.image.show("Image")

    def create_triangle(self, position, scale, rotation, height):
        triangle = Shapes.Triangle(
            position, scale, rotation, height, self.shape_manager)
        return triangle

    def create_rectangle(self, position, scale, rotation, size):
        rectangle = Shapes.Rectangle(
            position, scale, rotation, size, self.shape_manager)
        return rectangle

    def create_ellipse(self, position, scale, radius):
        ellipse = Shapes.Ellipse(
            position, scale, radius, self.shape_manager)
        return ellipse


def main():
    creator = Creator((400, 400))
    creator.save_canvas()
    creator.show_image()


if __name__ == "__main__":
    main()
