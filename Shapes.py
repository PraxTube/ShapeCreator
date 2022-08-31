import math

from PIL import Image, ImageDraw


class ShapeManager:
    def __init__(self):
        self.shapes = []

    def subscribe(self, shape):
        self.shapes.append(shape)

    def unsubscribe(self, shape):
        self.shapes.remove(shape)

    def draw(self, canvas, im_size):
        canvas.polygon((0, 0, im_size[0], 0, im_size[0], im_size[1], 0, im_size[1]), fill=(0, 0, 0))
        for shape in self.shapes:
            shape.draw(canvas, im_size)


class Shape:
    position = None
    scale = None
    rotation = None
    color = None

    def __init__(self, position, scale, rotation, manager, color=(255, 255, 255)):
        self.set_position(position)
        self.set_scale(scale)
        self.set_rotation(rotation)
        self.set_color(color)

        self.manager = manager
        self.manager.subscribe(self)

    def __del__(self):
        self.manager.unsubscribe(self)

    def set_position(self, position):
        if type(position) != tuple or len(position) != 2:
            raise ValueError(
                "Position must be tuple with length 2", position)
        self.position = position

    def set_scale(self, scale):
        if type(scale) != tuple or len(scale) != 2:
            raise ValueError(
                "Scale must be tuple with length 2 (x, y)", scale)
        self.scale = scale

    def set_rotation(self, rotation):
        if type(rotation) != int:
            raise ValueError(
                "Rotation must be integer", rotation)
        self.rotation = rotation

    def set_color(self, color):
        if type(color) != tuple or len(color) != 3:
            raise ValueError(
                "Color must be tuple with length 3", color)
        self.color = color

    def draw(self, canvas, im_size):
        pixels = self.calculate_rotation(self.calculate_pixels())
        self.add_offset_to_pixels(pixels, (im_size[0], im_size[1]))
        canvas.polygon(tuple(pixels), fill=self.color)

    def calculate_pixels(self):
        raise NotImplementedError("Need to create inherent function.")

    def calculate_rotation(self, pixels):
        for i in range(len(pixels)):
            polar_pixel = [
                math.sqrt(pixels[i][0]**2 + pixels[i][1]**2),
                0]
            if pixels[i][0] == 0:
                polar_pixel[1] = math.pi/2 if pixels[i][1] >= 0 else -math.pi/2
            else:
                polar_pixel[1] = math.atan(pixels[i][1] / pixels[i][0])

            if pixels[i][0] < 0:
                polar_pixel[1] += math.pi
            elif pixels[i][0] > 0 and pixels[i][1] < 0:
                polar_pixel[1] += 2*math.pi
            polar_pixel[1] += math.radians(self.rotation)

            pixels[i][0] = polar_pixel[0] * math.cos(polar_pixel[1])
            pixels[i][1] = polar_pixel[0] * math.sin(polar_pixel[1])
        return pixels

    @staticmethod
    def add_offset_to_pixels(pixels, im_size):
        for i in range(len(pixels)):
            pixels[i] = (
                pixels[i][0] + im_size[0]/2,
                pixels[i][1] + im_size[1]/2)


class Triangle(Shape):
    def __init__(self, position, scale, rotation, height, manager, color=(255, 255, 255)):
        super().__init__(position, scale, rotation, manager, color)
        self.height = height

    def calculate_pixels(self):
        scaled_height_x = self.height * self.scale[0] * 0.5
        scaled_height_y = self.height * self.scale[1] * 0.5
        x_offset = 4/3*scaled_height_x
        #      1
        #
        #
        # 2         3
        pixels = [
            [self.position[0], self.position[1] - scaled_height_y],
            [self.position[0] - x_offset, self.position[1] + scaled_height_y],
            [self.position[0] + x_offset, self.position[1] + scaled_height_y]]
        return pixels


class Rectangle(Shape):
    def __init__(self, position, scale, rotation, size, manager, color=(255, 255, 255)):
        super().__init__(position, scale, rotation, manager, color)
        self.size = size

    def calculate_pixels(self):
        size_x = self.size/2 * self.scale[0]
        size_y = self.size/2 * self.scale[1]
        # 1     2
        #
        #
        # 4     3
        pixels = [
            [self.position[0] - size_x, self.position[1] - size_y],
            [self.position[0] + size_x, self.position[1] - size_y],
            [self.position[0] + size_x, self.position[1] + size_y],
            [self.position[0] - size_x, self.position[1] + size_y]]
        return pixels


class Ellipse(Shape):
    def __init__(self, position, scale, radius, manager, color=(255, 255, 255)):
        super().__init__(position, scale, 0, manager, color)
        self.radius = radius

    def draw(self, canvas, im_size):
        scaled_radius_x = self.radius * self.scale[0]
        scaled_radius_y = self.radius * self.scale[1]

        pixels = [[self.position[0], self.position[1]]]
        self.add_offset_to_pixels(pixels, im_size)

        min_val = (pixels[0][0] - scaled_radius_x,
                   pixels[0][1] - scaled_radius_y)
        max_val = (pixels[0][0] + scaled_radius_x,
                   pixels[0][1] + scaled_radius_y)

        canvas.ellipse((min_val[0], min_val[1],
                        max_val[0], max_val[1]),
                       fill=self.color)

    def calculate_pixels(self):
        pass
