import Image

img = Image.new( 'RGBA', (255,255), "black") # create a new black image
pixels = img.load() # create the pixel map

for i in range(img.size[0]):    # for every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i/2, j/2, 0) # set the colour accordingly

img.save("out.png")
