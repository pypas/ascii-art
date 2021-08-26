from PIL import Image
from numpy import asarray

im = Image.open("image.jpg")
print("Successfully loaded image!")
#im.show()
print(f"Image size: {im.height} x {im.width}")

im_as_array = asarray(im)
print(im_as_array.shape)
