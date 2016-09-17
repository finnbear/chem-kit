# Settigns
tick_counter, frame_counter, ticks_per_frame = 0, 0, 10
max_frames = 10

canvas_size = 32
canvas_color = "black"

# Imports
import Image

# main()
def main():
    init()
    while True:
        tick()

# init()
def init():
    print "INIT"

# tick()
def tick():
    # Globals
    global tick_counter

    # Update canvas

    # Save a frame if needed
    if frame_counter < max_frames:
        if tick_counter % ticks_per_frame == 0:
            save_frame()

    # Increment tick counter
    tick_counter += 1

# Functions
def save_frame():
    # Globals
    global frame_counter

    # Create a blank image
    frame = Image.new( 'RGBA', (canvas_size,canvas_size), canvas_color)
    
    # Load it as a bitmap
    bitmap = frame.load()

    # Loop through all pixels, setting them to the state of the canvas
    for x in range(frame.size[0]):
        for y in range(frame.size[1]):
            bitmap[x, y] = (128, 128, 0)

    frame.save("frame" + str(str(frame_counter).zfill(5)) + ".png")

    # Increment frame counter
    frame_counter += 1

# Program
main()
