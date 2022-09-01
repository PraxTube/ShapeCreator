from PIL import Image, ImageDraw

import Shapes


class Creator:
    def __init__(self, im_size):
        if type(im_size) != tuple or len(im_size) != 2:
            raise ValueError(
                "Position must be tuple with length 2", im_size)
        self.im_size = im_size

        self.image = Image.new("RGBA", self.im_size, (0, 0, 0))
        self.canvas = ImageDraw.Draw(self.image)
        self.shape_manager = Shapes.ShapeManager()

    def draw_canvas(self):
        self.shape_manager.draw(self.canvas, self.im_size)

    def save_canvas(self, output_filename="output.png"):
        self.make_background_transparent()
        self.image.save(output_filename)

    def show_image(self):
        self.image.show("Image")

    def make_background_transparent(self):
        pixel_map = self.image.load()
        width, height = self.image.size

        for i in range(width):
            for j in range(height):
                r, g, b, a = self.image.getpixel((i, j))

                if 0 == r == g == b:
                    pixel_map[i, j] = (0, 0, 0, 0)

    def create_triangle(self, position, scale, rotation, local_rotation, height):
        triangle = Shapes.Triangle(
            position, scale, rotation, local_rotation, height, self.shape_manager)
        return triangle

    def create_rectangle(self, position, scale, rotation, local_rotation, size):
        rectangle = Shapes.Rectangle(
            position, scale, rotation, local_rotation, size, self.shape_manager)
        return rectangle

    def create_hexagon(self, position, scale, rotation, local_rotation, size):
        hexagon = Shapes.Hexagon(
            position, scale, rotation, local_rotation, size, self.shape_manager)
        return hexagon

    def create_ellipse(self, position, scale, radius):
        ellipse = Shapes.Ellipse(
            position, scale, radius, self.shape_manager)
        return ellipse


def enemy_one(creator):
    creator.create_triangle((0, -50), (1, 1), 0, 0, 100)
    creator.create_triangle((0, 50), (1, 1), 0, 180, 100)

    creator.create_triangle((-65, 65), (1, 1), 0, 0, 50)
    creator.create_triangle((65, 65), (1, 1), 0, 0, 50)


def player(creator):
    size = 125
    creator.create_rectangle((0, 0), (1, 1), 0, 0, size)

    size = size/2 + 30
    creator.create_triangle((0, -size), (1, 1), 0, 0, 35)


def bullet(creator):
    creator.create_ellipse((0, 0), (1, 1), 25)
    creator.create_rectangle((0, 25), (1, 1), 0, 0, 50)


def main():
    creator = Creator((50, 50))

    bullet(creator)

    creator.draw_canvas()
    creator.save_canvas()
    # creator.show_image()


if __name__ == "__main__":
    main()
