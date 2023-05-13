from PIL import Image

im = Image.open('Map.png')
pixels = list(im.getdata())
width, height = im.size
for i in range(len(pixels)):
    if pixels[i] == (255, 255, 255):
        pixels[i] = 0
    else:
        pixels[i] = 1
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]