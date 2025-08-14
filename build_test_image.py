# Builds a test image, 16x16 containing one of each color from the palette per-pixel

from PIL import Image
from palette import load_color_palette, load_nes_palette

# Create the Image with the desired palette
desired_palette = load_color_palette()

test_image = Image.new("RGB", (16, 16))
test_image = test_image.convert("RGB", palette=desired_palette.palette)

val = 0
for color in desired_palette.palette.colors:
    x = val // 16
    y = val % 16
    test_image.putpixel((x, y), color)
    val += 1


test_image.save("sprites/test_image_256.png")

nes_palette = load_nes_palette()
test_image_nes = Image.new("RGB", (8, 8))
test_image_nes = test_image_nes.convert("RGB", palette=nes_palette)
val = 0
color_list = list(nes_palette.palette.colors)
for color in color_list:
    x = val % 8
    y = val // 8
    test_image_nes.putpixel((x, y), color)
    print("(x,y): ({x},{y})".format(x=x, y=y))
    print("Color (RGB): {color}".format(color=color))
    print("Color index: {index}".format(index=color_list.index(color)))
    val += 1

test_image_nes.save("sprites/test_image_nes.png")
