# Chem Kit V3.0 - main.py
# Author: Finn Bear
# Date: December 7, 2016
version = "3.5"

###########
# Imports #
###########
import os
import math
import random
from random import randint
import time
import datetime
import pygame
pygame.init()
pygame.font.init()

#########
# Input #
#########

# Simulation
force = (math.pi, 0.01) # Force to apply to all particles 

membrane = True # Whether a membrane exists
membrane_position = 0.5 # A percentage of window height
membrane_velocity = 0 # Velocity of the membrane
membrane_velocity_max = 0.02 # Max velocity of the membrane
membrane_friction_factor = 0.5 # Friction factor applied to the membrane's velocity
membrane_width = 50 # Width of the membrane
membrane_mass = 1000000 # Mass of membrane

# Rendering
particle_image = pygame.image.load("../asset/sphere.png")

############
# Settings #
############

# Simulation
fps_target = 15 # Frames per second to target

# Physics
field_mass = 0.01

# Rendering
save_video = True
video_begin_tick = 5 # Initial tick to record
video_end_tick = 10 # Final tick to record, 0 for infinite
window_width, window_height = 1000, 1000 # Dimensions of the window
window_caption = "Chem Kit - V" + version # Title of the window
window_background_color = (0, 0, 0) # Background color of the window
font, font_color = pygame.font.SysFont("monospace", 15, bold=True), (255, 55, 55)
window_title, window_title_position = font.render("Virtual Chemistry - v" + version, 1, font_color), (10, 10)
window_subtitle, window_subtitle_position = font.render("By: Finn Bear", 1, font_color), (10, 30)
window_temperature_gauge_position = (10, window_height - 40)
window_pressure_gauge_position = (10, window_height - 20)

###########
# Classes #
###########

class Particle:
	def __init__(self, type, (x, y), mass, radius, color):
		self.type = type
		self.x = x
		self.y = y
		self.angle = randomDirection()
		self.speed = randomSpeed()
		self.mass = mass
		self.radius = radius
		self.color = color

	def update(self):
		global total_pressure
	
		# Apply force
		(self.angle, self.speed) = addVectors((self.angle, self.speed), force)
	
		# Apply friction from field
		self.speed *= (self.mass / (self.mass + field_mass)) ** self.radius
	
		# Check for boundary collisions
		if self.x > window_width - self.radius:
			self.x = 2*(window_width - self.radius) - self.x
			self.angle = - self.angle
			total_pressure += self.speed * self.mass
		elif self.x < self.radius:
			self.x = 2*self.radius - self.x
			self.angle = - self.angle
			total_pressure += self.speed * self.mass
		if self.y > window_height - self.radius:
			self.y = 2*(window_height - self.radius) - self.y
			self.angle = math.pi - self.angle
			total_pressure += self.speed * self.mass
		elif self.y < self.radius:
			self.y = 2*self.radius - self.y
			self.angle = math.pi - self.angle
			total_pressure += self.speed * self.mass
	
		# Apply velocity
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
	
	def draw(self):
		image = pygame.transform.scale(particle_image, (self.radius * 2, self.radius * 2))
		#image = pygame.transform.rotate(image, 0)
		window.blit(image, (self.x - self.radius, self.y - self.radius))
		#pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius, 0)

#############
# Variables #
#############

# Simulation
particles = [] # A list of particles in the simulation
total_speed = 0 # Total speed of the particles
max_total_speed = 0 # Maximum Recorded Total Speed
total_pressure = 0 # Total pressure of the environment
max_total_pressure = 0 # Maximum Recorded Total Pressure
total_pressure_smoothing = 0.995 # For display purposes

# Rendering
window = {} # The graphics window
tick_counter = 0 # How many ticks have elapsed

#############
# Constants #
#############

# Simulation
spf_target = float(1) / fps_target # Seconds per frame

# Rendering
window_center_x = window_width / 2 # The center of the window
window_center_y = window_height / 2 # The center of the window

##########
# main() #
##########
def main():
	global tick_counter

	init()
	
	running = True
	while (running):
		global spf_target
		
		# Log initial time
		t0 = datetime.datetime.now()
		
		# Check for events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		# Update Logic		
		tick()
		tick_counter += 1
		
		# Log time after tick
		t1 = datetime.datetime.now()
		
		# Calculate elapsed (delta) time
		tDelta = t1 - t0
		
		# Delay if necessary to meet target fps
		if (spf_target > tDelta.total_seconds()):
			time.sleep(spf_target - tDelta.total_seconds())
		
		# Draw window
		if draw() == False:
			running = False
		
		# Log time after draw
		t2 = datetime.datetime.now()
		
		# Calculate and display elapsed (delta) time
		tDelta = t2 - t0
		print("Draw delta: " + str((tDelta.total_seconds() - spf_target) * 1000) + "ms")
		
	# Compile video if necessary
	if save_video:
		os.system("yes y | ffmpeg -framerate " + str(fps_target) + " -i ../out/frame-%05d.png -c:v libx264 -r 30 -pix_fmt yuv420p ../out/out.mp4")
		os.system("rm ../out/*.png")

############
# Routines #
############
def init():
	global window

	window = pygame.display.set_mode((window_width, window_height))
	pygame.display.set_caption(window_caption)

	for i in range(0,150):
		particles.append(Particle("Br", randomPosition(), 20, 6, (255, 255, 255)))
	for i in range(0,15):
		particles.append(Particle("Br", randomPosition(), 300, 20, (255, 255, 255)))
	for i in range(0,2):
		particles.append(Particle("Br", randomPosition(), 4000, 40, (255, 255, 255)))
	for i in range(0,1):
		particles.append(Particle("Br", randomPosition(), 50000, 50, (255, 255, 255)))	

def tick():
	global total_speed
	global max_total_speed
	global total_pressure
	global max_total_pressure
	global membrane_position
	global membrane_velocity
	
	# Reset totals
	total_speed = 0
	total_pressure *= total_pressure_smoothing
	
	for i, particle in enumerate(particles):
		total_speed += particle.speed
		particle.update()
		if membrane:
			membraneCollide(particle)
		for particle2 in particles[i+1:]:
			collide(particle, particle2)
			
	# Simulate membrane
	if membrane:
		# Clamp membrane velocity
		membrane_velocity = clamp(membrane_velocity, -membrane_velocity_max, membrane_velocity_max)
		
		# Apply membrane velocity
		membrane_position += membrane_velocity

		# Apply friction to membrane
		membrane_velocity *= membrane_friction_factor

	# Reset maximums
	max_total_speed = max(max_total_speed, total_speed)
	max_total_pressure = max(max_total_pressure, total_pressure)

def draw():
	global particles

	window.fill(window_background_color)

	# Draw particles
	for particle in particles:
		particle.draw()

	if membrane:
		pygame.draw.rect(window,(200,200,255),(0,membrane_position * window_height + membrane_width / float(-2),window_width,membrane_width), 0)

	# Create procedural overlays (Text)
	window_temperature_gauge = font.render("Temperature: " + str(round(temperatureGauge(), 4)) + "%", 1, font_color)
	window_pressure_gauge = font.render("Pressure: " + str(round(pressureGauge(), 4)) + "%", 1, font_color)

	# Draw overlays (Text)
	window.blit(window_title, window_title_position)
	window.blit(window_subtitle, window_subtitle_position)
	window.blit(window_temperature_gauge, window_temperature_gauge_position)
	window.blit(window_pressure_gauge, window_pressure_gauge_position)

	if save_video and tick_counter >= video_begin_tick:
		if tick_counter <= video_end_tick:
			pygame.image.save(window, '../out/frame-%05d.png' % (tick_counter))
		else:
			return False

	pygame.display.flip()
	return True
	

#############
# Functions #
#############

def chance(probability):
	return random.random() < probability

def translate(value, leftMin, leftMax, rightMin, rightMax):
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin
	valueScaled = float(value - leftMin) / float(leftSpan)

	return rightMin + (valueScaled * rightSpan)

def clamp(value, minimum, maximum):
	return max(minimum, min(maximum, value))

def dist((x1, y1), (x2, y2)):
	return math.hypot(x1 - x2, y1 - y2), x1 - x2, y1 - y2

def randomPosition():
	return (randint(0, window_width), randint(0, window_height))

def randomSpeed():
	return translate(randint(0, 100), 0, 100, 0, 10)

def randomDirection():
	return translate(randint(0, 360), 0, 360, 0, math.pi * 2)

def addVectors((a1, l1), (a2, l2)):
	x = math.sin(a1) * l1 + math.sin(a2) * l2
	y = math.cos(a1) * l1 + math.cos(a2) * l2
	length = math.hypot(x, y)
	angle = 0.5 * math.pi - math.atan2(y, x)
	return (angle, length)

def collide(particle1, particle2):
	# Measure distance between particles
	distance, dx, dy = dist((particle1.x, particle1.y), (particle2.x, particle2.y))
	
	# Check for collision
	if distance <= particle1.radius + particle2.radius + 0.5:
		angle = math.atan2(dy, dx) + 0.5 * math.pi
		total_mass = particle1.mass + particle2.mass
		
		# Miss the collision :(
		(particle1.angle, particle1.speed) = addVectors((particle1.angle, particle1.speed*(particle1.mass-particle2.mass)/total_mass), (angle, 2*particle2.speed*particle2.mass/total_mass))
		(particle2.angle, particle2.speed) = addVectors((particle2.angle, particle2.speed*(particle2.mass-particle1.mass)/total_mass), (angle+math.pi, 2*particle1.speed*particle1.mass/total_mass))
		
		# Mathematically correct missed colllision
		overlap = (particle1.radius + particle2.radius - distance+1)
		if (particle1.radius < particle2.radius):
			particle1.x += math.sin(angle)*overlap
			particle1.y -= math.cos(angle)*overlap
		elif (particle1.radius > particle2.radius):
			particle2.x -= math.sin(angle)*overlap
			particle2.y += math.cos(angle)*overlap
		else:
			overlap = 0.5*(particle1.radius + particle2.radius - distance+1)
			particle1.x += math.sin(angle)*overlap
			particle1.y -= math.cos(angle)*overlap
			particle2.x -= math.sin(angle)*overlap
			particle2.y += math.cos(angle)*overlap
		
def membraneCollide(particle):
	global membrane_velocity

	# Collect information about the particle and the membrane
	# Keep in mind the upside-down coordinate system
	# These calculations deal with Y coordinates only
	membraneTop = (membrane_position * window_height) - (membrane_width / float(2))
	membraneBottom = (membrane_position * window_height) + (membrane_width / float(2))

	particleTop = particle.y - particle.radius
	particleBottom = particle.y + particle.radius

	# Check if particle intersects membrane
	if (particleTop >= membraneTop and particleTop <= membraneBottom) or (particleBottom <= membraneBottom and particleBottom >= membraneTop):
		# Particle has collided with the membrane
		# Check which direction the particle was travelling
		particleVelocityY = -1 * particle.speed * math.cos(particle.angle)

		if particleVelocityY < -1:
			# Trust velocity
			membrane_velocity += (particleVelocityY * particle.mass) / membrane_mass
			particle.y += membraneBottom - particleTop
		elif particleVelocityY > 1:
			# Trust velocity
			membrane_velocity += (particleVelocityY * particle.mass) / membrane_mass
			particle.y -= particleBottom - membraneTop
		else:
			# Don't trust velocity
			if particleTop >= membraneTop and particleTop <= membraneBottom:
				membrane_velocity -= (particle.speed * particle.mass) / membrane_mass
				particle.y += membraneBottom - particleTop
 			elif particleBottom <= membraneBottom and particleBottom >= membraneTop:
				membrane_velocity += (particle.speed * particle.mass) / membrane_mass
				particle.y -= particleBottom - membraneTop

		# Bounce particle
		particle.angle = math.pi - particle.angle
	

def temperatureGauge():
	return (float(1) / (1 + math.exp(-0.05 * total_speed / len(particles))) - 0.5) * 200

def pressureGauge():
	return (float(1) / (1 + math.exp(-0.000001 * total_pressure)) - 0.5) * 200

###########
# Program #
###########
main()
