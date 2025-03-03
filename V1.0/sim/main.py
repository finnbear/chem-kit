# Physics Settings
min_atomic_weight = 1
#max_initial_atomic_weight = 5
fusion_difference_threshold = 8
initial_atomic_weights = [1,2,4,8]
max_atomic_weight = 150
min_energy = 0
max_energy = 255
atomic_energy_damper_threshold, atomic_energy_damper_threshold_percent = 0, 0.5
atomic_energy_damper = 0.90
fusion_threshold, fusion_threshold_percent = 0, 0.4
fission_threshold, fission_threshold_percent = 0, 0.7
min_temperature = 0
max_temperature = 70
temperature_damper = 0.95
fusion_temperature_change = 10000
fusion_area, fusion_ammount, fusion_radius = 0, 0, 15
fission_temperature_change = 100000
fission_area, fission_amount, fission_radius = 0, 0, 30
fusion_energy_boost = 1.2
fission_energy_boost = 0.8

chance_initial_atom = 0.08

# Output Settigns
output_directory_prefix = "../output/"
tick_counter, frame_counter, ticks_per_frame = 0, 0, 1
max_frames = 1500

atomic_weight_display_offset = 40 # Must be less than or equal to 255 - max_atomic_weight

canvas_size = 256
canvas_color = "black"
canvas_text_line_spacing = 10
canvas_text_left_margin = 2
limit_viewport = True

# Imports
import math
import random
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Data Storage
canvas = {}

# main()
def main():
    preinit()
    init()
    while True:
        tick()

# preinit()
def preinit():
    # Globals
    global atomic_energy_damper_threshold
    global fusion_threshold
    global fission_threshold
    global fusion_area
    global fission_area
    global fusion_ammount
    global fission_ammount

    # Calculate thresholds based on percents
    atomic_energy_damper_threshold = translate(atomic_energy_damper_threshold_percent, 0, 1, min_energy, max_energy)
    fusion_threshold = translate(fusion_threshold_percent, 0, 1, min_energy, max_energy)
    fission_threshold = translate(fission_threshold_percent, 0, 1, min_energy, max_energy)

    # Calculate areas based on radii
    fusion_area = fusion_radius * fusion_radius
    fission_area = fission_radius * fission_radius

    # Calculate ammounts based on areas
    fusion_ammount = int(fusion_temperature_change / fusion_area)
    fission_ammount = int(fission_temperature_change / fission_area)

# init()
def init():
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            if chance(chance_initial_atom):
                canvas[x, y] = {'weight': randomWeight(), 'energy': randomEnergy(), 'temperature': randomTemperature()}
            else:
                canvas[x, y] = {'weight': 0, 'energy': 0, 'temperature': randomTemperature()}

# tick()
def tick():
    # Globals
    global tick_counter
    global canvas

    # Initialize new canvas
    new_canvas = {}
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            new_canvas[x, y] = {'weight': 0, 'energy': 0, 'temperature': newTemperature(canvas[x, y]['temperature'])}

    # Apply movement due to energy of atoms
    num_atoms = 0
    for x in range(0, canvas_size):
        for y in range(0, canvas_size):
            # Check if an atom exists at the coordinates
            atom_weight = canvas[x, y]['weight']
            atom_energy = canvas[x, y]['energy']
            if atom_weight >= min_atomic_weight:
                # Increment number of atoms
                num_atoms += 1

                # Define variables to store the resulting position
                new_x = x
                new_y = y

                # Calculate probability of movement
                movement_probability = translate(atom_energy, min_energy, max_energy, 0, 0.9)

                # X-axis movement
                if (chance(movement_probability)):
                    new_x += random.choice([-1.0, 1.0])
                    
                # Y-axis movement
                if (chance(movement_probability)):
                    new_y += random.choice([-1.0, 1.0])

                # Calculate forces

                # Limit resulting position to canvas
                new_x = limitCoordinate(new_x)
                new_y = limitCoordinate(new_y)

                # Check if there is an atom already at the resulting position
                original_weight = new_canvas[new_x, new_y]['weight']
                original_energy = new_canvas[new_x, new_y]['energy']
                if original_weight >= min_atomic_weight:
                    # Handle atomic collision
                    if (original_weight - atom_weight) <= fusion_difference_threshold and (original_weight + atom_weight) < max_atomic_weight and (original_energy > fusion_threshold or atom_energy > fusion_threshold):
                        # Fusion
                        for x2 in range(x - fusion_radius, x + fusion_radius):
                            for y2 in range(y - fusion_radius, y + fusion_radius):
                                try:
                                    new_canvas[x2, y2]['temperature'] += int(fusion_ammount / (0.1 + 0.5 * math.sqrt((x-x2)*(x-x2)+(y-y2)*(y-y2))) * random.random())
                                    new_canvas[x2, y2]['temperature'] = min(max_temperature, new_canvas[x2, y2]['temperature'])
                                except KeyError:
                                    z = 0
                        new_canvas[new_x, new_y] = {'weight': atom_weight * original_weight, 'energy': int((atom_energy + original_energy) * fusion_energy_boost), 'temperature': newTemperature(canvas[x, y]['temperature'])}
                    elif original_weight > 2 * atom_weight and (original_energy > fission_threshold and atom_energy > fission_threshold):
                        # Fission
                        for x2 in range(x - fission_radius, x + fission_radius):
                            for y2 in range(y - fission_radius, y + fission_radius):
                                try:
                                    new_canvas[x2, y2]['temperature'] += int(fission_ammount / (0.1 + math.sqrt((x-x2)*(x-x2)+(y-y2)*(y-y2))) * random.random())
                                    new_canvas[x2, y2]['temperature'] = min(max_temperature, new_canvas[x2, y2]['temperature'])
                                except KeyError:
                                    z = 0
                        new_canvas[new_x, new_y] = {'weight': int(original_weight / float(2)), 'energy': int(original_energy / 2 * fission_energy_boost), 'temperature': newTemperature(canvas[x, y]['temperature'])}
                        new_canvas[new_x + random.choice([-1.0, 1.0]), new_y] = {'weight': int(original_weight / float(2)), 'energy': int(original_energy / 2 * fission_energy_boost), 'temperature': newTemperature(canvas[x, y]['temperature'])}
                        new_canvas[new_x, new_y + random.choice([-1.0, 1.0])] = {'weight': atom_weight, 'energy': atom_energy, 'temperature': newTemperature(canvas[x, y]['temperature'])}
                    elif atom_weight > 2 * original_weight and (original_energy > fission_threshold and atom_energy > fission_threshold):
                        # Fission
                        for x2 in range(x - fission_radius, x + fission_radius):
                            for y2 in range(y - fission_radius, y + fission_radius):
                                try:
                                    new_canvas[x2, y2]['temperature'] += int(fission_ammount / (0.1 + math.sqrt((x-x2)*(x-x2)+(y-y2)*(y-y2))) * random.random())
                                    new_canvas[x2, y2]['temperature'] = min(max_temperature, new_canvas[x2, y2]['temperature'])
                                except KeyError:
                                    z = 0
                        new_canvas[new_x, new_y] = {'weight': int(original_weight / float(2)), 'energy': int(atom_energy / 2 * fission_energy_boost), 'temperature': newTemperature(canvas[x, y]['temperature'])}
                        new_canvas[new_x + random.choice([-1.0, 1.0]), new_y] = {'weight': int(original_weight / float(2)), 'energy': int(atom_energy / 2 * fission_energy_boost), 'temperature': newTemperature(canvas[x, y]['temperature'])}
                        new_canvas[new_x, new_y + random.choice([-1.0, 1.0])] = {'weight': original_weight, 'energy': original_energy, 'temperature': newTemperature(canvas[x, y]['temperature'])}
                    else:
                        new_canvas[new_x + random.choice([-1.0, 1.0]), new_y] = {'weight': atom_weight, 'energy': atom_energy, 'temperature': newTemperature(canvas[x, y]['temperature'])}
                        new_canvas[new_x, new_y + random.choice([-1.0, 1.0])] = {'weight': original_weight, 'energy': original_energy, 'temperature': newTemperature(canvas[x, y]['temperature'])}
                else:
                    # Move atom to resulting position
                    new_canvas[new_x, new_y] = {'weight': atom_weight, 'energy': newEnergy(atom_energy), 'temperature': newTemperature(canvas[x, y]['temperature'])}

    # Save the resulting canvas to the old canvas to overwrite
    canvas = new_canvas

    # Save a frame if needed
    if frame_counter < max_frames:
        if tick_counter % ticks_per_frame == 0:
            save_frame(num_atoms)
            print "Tick: " + str(tick_counter) + " Frame: " + str(frame_counter)

    # Increment tick counter
    tick_counter += 1

# Physics Functions
def randomWeight():
    #return random.randint(min_atomic_weight, max_initial_atomic_weight)
    return random.choice(initial_atomic_weights)

def randomEnergy():
    return random.randint(min_energy, max_energy)

def newEnergy(energy):
    if energy > atomic_energy_damper_threshold:
        return int(energy * atomic_energy_damper)
    else:
        return energy

def randomTemperature():
    return random.randint(min_temperature, max_temperature)

def newTemperature(temperature):
    return int(temperature * temperature_damper)

# Output Functions
def save_frame(num_atoms):
    # Globals
    global frame_counter

    # Create a blank image
    frame = Image.new( 'RGB', (canvas_size, canvas_size), canvas_color)
    
    # Load it as a bitmap
    bitmap = frame.load()

    # Loop through all pixels, setting them to the state of the canvas
    for x in range(frame.size[0]):
        for y in range(frame.size[1]):
            local_atomic_weight = canvas[x, y]['weight']
            local_atomic_energy = canvas[x, y]['energy']
            local_temperature = canvas[x, y]['temperature']
            if limit_viewport:
                # Check if the viewport should be limited
                if ((x - (canvas_size / 2))*(x - (canvas_size / 2))) + ((y - (canvas_size / 2))*(y - (canvas_size / 2))) < (canvas_size / 2)*(canvas_size / 2):
                    # Check if there is an atom
                    if local_atomic_weight > min_atomic_weight:
                        # Draw atom
                        bitmap[x, y] = (local_atomic_weight + atomic_weight_display_offset, local_atomic_weight + atomic_weight_display_offset, local_atomic_weight + atomic_weight_display_offset)
                    else:
                        # Draw energy
                        bitmap[x, y] = (local_temperature, local_temperature, 0)
                else:
                    bitmap[x, y] = (0, 0, 0)
            else:
                # Check if there is an atom
                if local_atomic_weight > min_atomic_weight:
                    # Draw atom
                    bitmap[x, y] = (local_atomic_weight, local_atomic_weight, local_atomic_weight)
                else:
                    # Draw energy
                    bitmap[x, y] = (local_temperature, local_temperature, 0)

    # Add text overlays
    overlay = ImageDraw.Draw(frame)
    overlay.text((canvas_text_left_margin, 0), "Chemistry Kit", (255,255,0))
    overlay.text((canvas_text_left_margin, canvas_text_line_spacing), "Frame   " + str(frame_counter), (255,255,0))
    overlay.text((canvas_text_left_margin, canvas_text_line_spacing * 2), "# Atoms " + str(num_atoms), (255,255,0))

    frame.save(output_directory_prefix + "frame" + str(str(frame_counter).zfill(5)) + ".png")

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
