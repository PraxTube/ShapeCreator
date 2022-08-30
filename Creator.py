from PIL import Image, ImageDraw

import Shapes

im_size = (400, 400)

im = Image.new("RGB", im_size, (0, 0, 0))
canvas = ImageDraw.Draw(im)
shape_manager = Shapes.ShapeManager()

rot = 90

for i in range(10):
    tr = Shapes.Triangle((0, 150), (2, 1), 36*i, 35, shape_manager)

re = Shapes.Rectangle((0, 0), (1, 1), 0, 120, shape_manager)

shape_manager.draw(canvas, im_size)
im.save("output.png")
