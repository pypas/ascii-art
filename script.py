import numpy as np
from PIL import Image, ImageFont, ImageDraw
fonts = [
    "/usr/share/font/truetype/freefont/FreeMonoBold.ttf",
    "/usr/share/font/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "Pillow/Tests/fonts/DejaVuSansMono.ttf"
] 

# Configs
STRATEGY = 1 # 1 = Average, 2 = Luminosity, 3 = Lightness
BASEWIDTH = 150
FONT_SIZE = 8
FONT = fonts[0]

# Loads image
img = Image.open("img/original_image.jpg")
print("Successfully loaded image!")
height = img.height
width = img.width
print(f"Original image size: {width} x {height}")

# Reduces image size
wpercent = (BASEWIDTH/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((BASEWIDTH,hsize), Image.ANTIALIAS)

# Turns image into a 3d array
im_as_array = np.asarray(img)

# Converts RGB matrix into a brightness matrix
def formula(x):
    # Luminosity
    if STRATEGY == 2:
        return 0.21*x[0] + 0.72*x[1] + 0.07*x[2]
    # Lightness
    elif STRATEGY == 3:
        return (int(np.min(x)) + int(np.max(x)))/2
    # Average
    else:
        return np.mean(x)

brighteness_matrix = np.apply_along_axis(formula, 2, im_as_array)

# Convert this brightness matrix to an ASCII character matrix
ascii_brightness_scale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
idx_range = len(ascii_brightness_scale) - 1

def convert_brightness_ascii(x):
    return [ascii_brightness_scale[round(brightness/255*idx_range)] for brightness in x]

ascii_matrix = np.apply_along_axis(convert_brightness_ascii, 1, brighteness_matrix)
full_txt = ""
for line in ascii_matrix:
    new_line = []
    for item in line:
        new_line += [item]*3
    full_txt += "".join(new_line) + "\n"

write_image_width = 2100
write_image_height = 2000
print(f"Best write image size: {write_image_width} x {write_image_height}")
im = Image.new('RGB', (write_image_width, write_image_height), color = (0,0,0))
fnt = ImageFont.truetype(fonts[0], FONT_SIZE) 
ImageDraw.Draw(im).text((0,0), full_txt, font=fnt, fill=(255,255,255))

im = im.resize((width,height), Image.ANTIALIAS)
im.save("img/ascii_image.png", "PNG")