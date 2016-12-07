# Chem Kit V2.0 - main.py
# Author: Finn Bear
# Date: December 6, 2016

#########
# Input #
#########

############
# Settings #
############

# Physics

# Rendering
output_directory = "../out/"
length = 1 # Length of the video in seconds
width = 1000 # How many pixels wide is the video
height = 1000 # How many pixels tall is the video
ticks_per_frame = 1 # How many simulation updates per frame of video
frames_per_second = 30 # How many frames of video per second
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


############
# Routines #
############

# Physics
def init():
	# Clear the output directory to remove old frames
	for file in os.listdir(output_directory):
		path = os.path.join(output_directory, file)
		try:
		    if os.path.isfile(path) and "frame" in path:
		        os.unlink(path)
		except Exception as e:
		    print(e)

def tick():
	print("Tick")

# Rendering
def draw():
	global frame_counter
	global output_directory

	# Create a blank frame
	frame = Image.new( 'RGB', (width, height), background_color)

	# Load the pixels of the blank frame
	pixels = frame.load()

	# Render

	# Overlays
	overlay = ImageDraw.Draw(frame)
	overlay.text(overlay_title_position, overlay_title_text, (255,255,0))
	overlay.text(overlay_subtitle_position, overlay_subtitle_text, (255,255,0))

	# Save the frame
	frame.save(output_directory + "frame" + str(str(frame_counter).zfill(5)) + ".png")

#############
# Functions #
#############

# Physics
def chance(probability):
	return random.random() < probability

###########
# Program #
###########
main()

