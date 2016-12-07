# Chem Kit V2.0 - main.py
# Author: Finn Bear
# Date: December 6, 2016

#########
# Input #
#########

# Gassium [Ga] (A fictional gas)
gassium_particles_initial = 5 # How many gassium particles are in the simulation initially
gassium_rate = 0 # How many gassium particles to add or subtract each tick
gassium_radius = 3 # The radius of a gassium particle

# Brownium [Br] (A fictional particle for brownian motion)
brownium_particles_initial = 50 # How many brownium particles are in the simulation initially
brownium_rate = 0 # How many brownium particles to add or subtract each tick
brownium_radius = 1 # The radius of a brownium particle

############
# Settings #
############

# Physics

# Rendering
output_directory = "../out/"
length = 1 # Length of the video in seconds
width = 500 # How many pixels wide is the video
height = 500 # How many pixels tall is the video
ticks_per_frame = 1 # How many simulation updates per frame of video
frames_per_second = 5 # How many frames of video per second
background_color = "black" # The color of the background
overlay_title_text = "Particle Simulator" # The title text of the overlay
overlay_subtitle_text = "By Finn Bear" # The subtitle text of the overlay

###########
# Imports #
###########
import os
import math
import random
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

##########
# main() #
##########

def main():
	global ticks_per_frame
	global tick_counter
	global frame_counter

	init()
	while True:
		tick()
		tick_counter += 1
		if frame_counter < max_frames:
			if tick_counter % ticks_per_frame == 0:
				draw()
				frame_counter += 1
		else:
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
	#float angle = circle1.getPosition().angleToRad(circle2.getPosition());
    #circle1.changeAcceleration(-1 * (float)Math.cos(angle), -1 * (float)Math.sin(angle));
    #circle2.changeAcceleration((float)Math.cos(angle), (float)Math.sin(angle));
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
		px = particle['x']
		py = particle['y']
		pr = particle['radius']
		
		for x in range(px - pr - 1, px + pr + 1):
			for y in range(py - pr - 1, py + pr + 1):
				if inRect(x, y, 0, 0, frame.size[0], frame.size[1]) and distance(x, y, particle['x'], particle['y']) <= particle['radius']:
					pixels[x, y] = (255, 255, 255)
				

	# Overlays
	overlay = ImageDraw.Draw(frame)
	overlay.text(overlay_title_position, overlay_title_text, (255,255,0))
	overlay.text(overlay_subtitle_position, overlay_subtitle_text, (255,255,0))

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

def distance(x1, y1, x2, y2):
	return math.hypot(x2 - x1, y2 - y1)

def inRect(x, y, bx1, by1, bx2, by2):
	return (bx1 <= x <= bx2 and by1 <= y <= by2) or (bx1 >= x >= bx2 and by1 >= y >= by2)


###########
# Program #
###########
main()

