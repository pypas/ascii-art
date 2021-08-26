from PIL import Image

with Image.open("image.jpg") as im:
    print("Successfully loaded image!")
    im.show()
    print(f"Image size: {im.height} x {im.width}")