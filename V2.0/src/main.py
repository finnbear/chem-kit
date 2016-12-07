# Chem Kit V2.0 - main.py
# Author: Finn Bear
# Date: December 6, 2016

#########
# Input #
#########

# Gassium [Ga] (A fictional gas)
gassium_particles_initial = 150 # How many gassium particles are in the simulation initially
gassium_rate = 0 # How many gassium particles to add or subtract each tick
gassium_radius = 5 # The radius of a gassium particle

# Brownium [Br] (A fictional particle for brownian motion)
brownium_particles_initial = 300 # How many brownium particles are in the simulation initially
brownium_rate = 0 # How many brownium particles to add or subtract each tick
brownium_radius = 1 # The radius of a brownium particle

############
# Settings #
############

# Physics
max_velocity = 2
gravity = 0

# Rendering
output_directory = "../out/"
length = 20 # Length of the video in seconds
width = 1000 # How many pixels wide is the video
height = 1000 # How many pixels tall is the video
ticks_per_frame = 1 # How many simulation updates per frame of video
frames_per_second = 10 # How many frames of video per second
background_color = "black" # The color of the background
overlay_title_text = "Particle Simulator" # The title text of the overlay
overlay_subtitle_text = "By Finn Bear" # The subtitle text of the overlay

###########
# Imports #
###########
import os
import math
import random
import datetime
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#############
# Variables #
#############

# Physics
tick_counter = 0 # How many simulation updates have been made
particles = [] # Store the particles in the simulation

# Rendering
frame_counter = 0 # How many frames have been created

#############
# Constants #
#############

# Rendering
center_x = width / 2;
center_y = height / 2;
max_frames = length * frames_per_second # Number of frames to render in total
overlay_title_position = (5, 5) # Position of overlay title text
overlay_subtitle_position = (5, 15) # Position of overlay subtitle text
overlay_frames_position = (5, 25) # Position of frame counter

##########
# main() #
##########

def main():
	global ticks_per_frame
	global frams_per_second
	global tick_counter
	global frame_counter

	init()

	try:
		while True:
			t0 = datetime.datetime.now()
			tick()
			tick_counter += 1
			if frame_counter < max_frames:
				if tick_counter % ticks_per_frame == 0:
					draw()
					frame_counter += 1
			else:
				# Compile video
				os.system("yes y | ffmpeg -framerate " + str(frames_per_second) + " -i " + output_directory + "frame%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p " + output_directory + "out.mp4")
				os.system("rm " + output_directory + "*.png")

				# Exit
				exit(0)
			t1 = datetime.datetime.now()

			print("Tick #" + str(tick_counter) + " took " + str(int((t1 - t0).total_seconds() * 1000)) + "ms")

	except KeyboardInterrupt:
		# Compile video
		os.system("yes y | ffmpeg -framerate " + str(frames_per_second) + " -i " + output_directory + "frame%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p " + output_directory + "out.mp4")
		os.system("rm " + output_directory + "*.png")

		# Exit
		exit(0)


############
# Routines #
############

# Physics
def init():
	global center_x
	global center_y
	global particles
	global gassium_particles_initial
	global gassium_radius
	global brownium_particles_initial
	global brownium_radius

	# Clear the output directory to remove old frames
	for file in os.listdir(output_directory):
		path = os.path.join(output_directory, file)
		try:
		    if os.path.isfile(path) and "frame" in path:
		        os.unlink(path)
		except Exception as e:
		    print(e)

	# Create particles
	gassium_particles = []
	brownium_particles = []
	id = 0;
	for i in range(0, gassium_particles_initial):
		gassium_particles.append({'id': id, 'type': 'Ga', 'radius': gassium_radius, 'x': center_x, 'y': center_y, 'vx': 0, 'vy': 0})
		id += 1

	for i in range(0, brownium_particles_initial):
		brownium_particles.append({'id': id, 'type': 'Br', 'radius': brownium_radius, 'x': center_x, 'y': center_y, 'vx': 0, 'vy': 0})
		id += 1;
	
	# Add the new particles to the list of particles
	particles.extend(gassium_particles)
	particles.extend(brownium_particles)

def tick():
	global particles
	global center_x
	global center_y

	# A list to store the updated particles
	newParticles = []

	# Iterate throught the particles
	for particle1 in particles:
		newParticle = particle1
		for particle2 in particles:
			if particle1 != particle2:
				newParticle = physics(newParticle, particle2)
		newParticles.append(newParticle)

	# Put the new particles back into the list of particles
	particles = newParticles

def physics(particle1, particle2):
	distance = distanceParticles(particle1, particle2)
	angle = vecRadians(particle1["x"], particle1["y"], particle2["x"], particle2["y"])
	multiplier = 1 / (distance + 0.001);

	# Check if the particles intersect
	if distance < particle1["radius"] + particle2["radius"]:
		multiplier = 2 / (distance + 0.001);

	particle1["vx"] -= multiplier * math.cos(angle + (random.random() - 0.5))
	particle1["vy"] -= multiplier * math.sin(angle + (random.random() - 0.5))

	# <Hack>
	#cAngle = vecRadians(particle1["x"], particle1["y"], center_x, center_y)
	#particle1["vx"] += 1 * math.cos(cAngle + (random.random() - 0.5))
	#particle1["vy"] += 1 * math.sin(cAngle + (random.random() - 0.5))
	# </Hack>

	# Apply gravity
	particle1["y"] += gravity

	# Apply velocity
	particle1["x"] += particle1["vx"]
	particle1["y"] += particle1["vy"]

	# Constrain position
	particle1["x"] = clamp(particle1["x"], 0, width)
	particle1["y"] = clamp(particle1["y"], 0, height)

	# Constrain velocity
	particle1["vx"] = clamp(particle1["vx"], 0, max_velocity)
	particle1["vy"] = clamp(particle1["vy"], 0, max_velocity)

	return particle1

# Rendering
def draw():
	global particles
	global frame_counter
	global output_directory

	# Create a blank frame
	frame = Image.new( 'RGB', (width, height), background_color)

	# Load the pixels of the blank frame
	pixels = frame.load()

	# Render
	for particle in particles:
		pt = particle['type']
		px = int(particle['x'])
		py = int(particle['y'])
		pr = particle['radius']
		
		for x in range(int(px) - pr - 1, int(px) + pr + 1):
			for y in range(int(py) - pr - 1, int(py) + pr + 1):
				if inRect(x, y, 0, 0, frame.size[0] - 1, frame.size[1] - 1) and distance(x, y, particle['x'], particle['y']) <= particle['radius']:
					if (pt == "Ga"):
						pixels[x,y] = (0, 255, 255)
					elif (pt == "Br"):
						pixels[x,y] = (255, 255, 255)

	# Overlays
	overlay = ImageDraw.Draw(frame)
	overlay.text(overlay_title_position, overlay_title_text, (255,255,0))
	overlay.text(overlay_subtitle_position, overlay_subtitle_text, (255,255,0))
	overlay.text(overlay_frames_position, "Frame: #" + str(frame_counter), (255,255,0))

	# Save the frame
	frame.save(output_directory + "frame" + str(str(frame_counter).zfill(5)) + ".png")

#############
# Functions #
#############

# Math
def chance(probability):
	return random.random() < probability

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)

	return rightMin + (valueScaled * rightSpan)

def clamp(value, minimum, maximum):
	return max(minimum, min(maximum, value))

def distance(x1, y1, x2, y2):
	return math.hypot(x2 - x1, y2 - y1)

def distanceParticles(particle1, particle2):
	return math.hypot(particle2["x"] - particle1["x"], particle2["y"] - particle1["y"])

def inRect(x, y, bx1, by1, bx2, by2):
	return (bx1 <= x <= bx2 and by1 <= y <= by2) or (bx1 >= x >= bx2 and by1 >= y >= by2)

def vecRadians(x1, y1, x2, y2):
	angle = math.atan2(y1 - y2, x1 - x2);
	while (angle < 0):
		angle += math.pi;
	return angle

###########
# Program #
###########
main()

