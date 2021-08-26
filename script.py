from PIL import Image
import numpy as np

img = Image.open("image.jpg")
print("Successfully loaded image!")
print(f"Image size: {img.height} x {img.width}")

basewidth = 250
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)

# Turn image into a 3d array
im_as_array = np.asarray(img)
print(im_as_array.shape)

def formula_lightness(x):
    return (int(np.min(x)) + int(np.max(x)))/2
def formula_average(x):
    return np.mean(x)
def formula_luminosity(x):
    return 0.21*x[0] + 0.72*x[1] + 0.07*x[2]

# Converting RGB matrix into a brightness matrix
brighteness_matrix = np.apply_along_axis(formula_average, 2, im_as_array)
print(brighteness_matrix.shape)

# Convert this brightness matrix to an ASCII character matrix
ascii_brightness_scale = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
idx_range = len(ascii_brightness_scale) - 1

def convert_brightness_ascii(x):
    return [ascii_brightness_scale[round(brightness/255*idx_range)] for brightness in x]

ascii_matrix = np.apply_along_axis(convert_brightness_ascii, 1, brighteness_matrix)
for line in ascii_matrix:
    new_line = []
    for item in line:
        new_line.append(item)
        new_line.append(item)
        new_line.append(item)
    print("".join(new_line))