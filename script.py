import numpy as np
from PIL import Image, ImageFont, ImageDraw
fonts = [
    "/usr/share/font/truetype/freefont/FreeMonoBold.ttf",
    "/usr/share/font/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "Pillow/Tests/fonts/DejaVuSansMono.ttf"
] 

# Configs
IMAGE_IN_PATH = "img/original_image.jpg"
IMAGE_OUT_PATH = "img/ascii_image.png"
STRATEGY = 1 # 1 = Average, 2 = Luminosity, 3 = Lightness
OUTPUT = 1 # 1 = Image, 2 = Terminal
FONT_SIZE = 8
FONT = fonts[2]
MAX_WIDTH = 400

# Loads image
img = Image.open(IMAGE_IN_PATH)
print("Successfully loaded image!")
height = img.height
width = img.width
print(f"Original image size: {width} x {height}")

# Reduces image size if width is greater than MAX_WIDTH
if (width > MAX_WIDTH):
    wpercent = (MAX_WIDTH/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((MAX_WIDTH,hsize), Image.ANTIALIAS)

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

ascii_text = '\n'.join(''.join(char*3 for char in line) for line in ascii_matrix)

if OUTPUT == 1:
    # Converts text to image
    fnt = ImageFont.truetype(fonts[0], FONT_SIZE)
    write_image_width, write_image_height = ImageDraw.Draw(Image.new('RGB', (1, 1))).textsize(ascii_text, font=fnt)
    im = Image.new('RGB', (write_image_width, write_image_height), color = (0,0,0))
    ImageDraw.Draw(im).text((0,0), ascii_text, font=fnt, fill=(255,255,255))

    # Resizes image and saves to file
    im = im.resize((width,height), Image.ANTIALIAS)
    im.save(IMAGE_OUT_PATH, "PNG")
else:
    print(ascii_text)