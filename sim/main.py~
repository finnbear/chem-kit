# Physics Settings
min_atomic_weight = 1
max_atomic_weight = 10
min_energy = 0
max_energy = 100

chance_initial_atom = 0.10

# Output Settigns
tick_counter, frame_counter, ticks_per_frame = 0, 0, 10
max_frames = 250

canvas_size = 64
canvas_color = "black"

# Imports
import random
import Image

# Data Storage
canvas = {}

# main()
def main():
    init()
    while True:
        tick()

# init()
def init():
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            if chance(chance_initial_atom):
                canvas[x, y] = {'weight': randomWeight(), 'energy': randomEnergy()}
            else:
                canvas[x, y] = {'weight': 0, 'energy': 0}

# tick()
def tick():
    # Globals
    global tick_counter
    global canvas

    # Initialize new canvas
    new_canvas = {}
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            new_canvas[x, y] = {'weight': 0, 'energy': 0}

    # Apply movement due to energy of atoms
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            # Check if an atom exists at the coordinates
            if canvas[x, y]['weight'] >= min_atomic_weight:
                # Define variables to store the resulting position
                new_x = x
                new_y = y

                # Calculate probability of movement
                movement_probability = translate(canvas[x, y]['energy'], min_energy, max_energy, 0, 1)

                # X-axis movement
                if (chance(movement_probability)):
                    new_x += random.choice([-1.0, 1.0])
                    
                # Y-axis movement
                if (chance(movement_probability)):
                    new_y += random.choice([-1.0, 1.0])

                # Limit resulting position to canvas
                new_x = limitCoordinate(new_x)
                new_y = limitCoordinate(new_y)

                # Check if there is an atom already at the resulting position
                if new_canvas[new_x, new_y]['weight'] >= min_atomic_weight:
                    # Handle atomic collision
                    z = 1
                else:
                    # Move atom to resulting position
                    new_canvas[new_x, new_y] = {'weight': canvas[x, y]['weight'], 'energy': canvas[x, y]['energy']}

    # Save the resulting canvas to the old canvas to overwrite
    canvas = new_canvas

    # Save a frame if needed
    if frame_counter < max_frames:
        if tick_counter % ticks_per_frame == 0:
            save_frame()

    # Increment tick counter
    tick_counter += 1

# Physics Functions
def randomWeight():
    return random.randint(min_atomic_weight, max_atomic_weight)

def randomEnergy():
    return random.randint(min_energy, max_energy)

# Output Functions
def save_frame():
    # Globals
    global frame_counter

    # Create a blank image
    frame = Image.new( 'RGBA', (canvas_size, canvas_size), canvas_color)
    
    # Load it as a bitmap
    bitmap = frame.load()

    # Loop through all pixels, setting them to the state of the canvas
    for x in range(frame.size[0]):
        for y in range(frame.size[1]):
            local_atomic_weight = canvas[x, y]['weight']
            bitmap[x, y] = (local_atomic_weight * 25, local_atomic_weight * 15, local_atomic_weight * 5)

    frame.save("frame" + str(str(frame_counter).zfill(5)) + ".png")

    # Increment frame counter
    frame_counter += 1

# Utility Funcitons
def limitCoordinate(coordinate):
    return min(canvas_size - 1, max(0, coordinate))

def chance(probability):
    return random.random() < probability

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# Program
main()
