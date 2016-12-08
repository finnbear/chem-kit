# Chem Kit V3.0 - main.py
# Author: Finn Bear
# Date: December 7, 2016

###########
# Imports #
###########
import math
import time
import datetime
import pygame

#########
# Input #
#########

force = (math.pi, 0.1) # Force to apply to all particles

############
# Settings #
############

# Simulation
fps_target = 10 # Frames per second to target

# Physics


# Rendering
window_width, window_height = 800, 800 # Dimensions of the window
window_caption = "Chem Kit - V3.0" # Title of the window
window_background_color = (0, 0, 0) # Background color of the window

###########
# Classes #
###########

class Particle:
	def __init__(self, type, (x, y), mass, radius, color):
		self.type = type
		self.x = x
		self.y = y
		self.angle = 0
		self.speed = 0
		self.mass = mass
		self.radius = radius
		self.color = color

	def update(self):
		# Apply force
		(self.angle, self.speed) = addVectors((self.angle, self.speed), force)
	
		# Check for boundary collisions
		if self.x > window_width - self.radius:
			self.x = 2*(window_width - self.radius) - self.x
			self.angle = - self.angle
		elif self.x < self.radius:
			self.x = 2*self.radius - self.x
			self.angle = - self.angle
		if self.y > window_height - self.radius:
			self.y = 2*(window_height - self.radius) - self.y
			self.angle = math.pi - self.angle
		elif self.y < self.radius:
			self.y = 2*self.radius - self.y
			self.angle = math.pi - self.angle
	
		# Apply velocity
		self.x += math.sin(self.angle) * self.speed
		self.y -= math.cos(self.angle) * self.speed
	
	def draw(self):
		pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius, 5)

#############
# Variables #
#############

# Simulation
particles = []

# Rendering
window = {}

#############
# Constants #
#############

# Simulation
spf_target = float(1) / fps_target # Seconds per frame

# Rendering
window_center_x = window_width / 2
window_center_y = window_height / 2

##########
# main() #
##########
def main():
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
		
		# Log time after tick
		t1 = datetime.datetime.now()
		
		# Calculate elapsed (delta) time
		tDelta = t1 - t0
		
		# Delay if necessary to meet target fps
		if (spf_target > tDelta.total_seconds()):
			time.sleep(spf_target - tDelta.total_seconds())
		
		# Draw window
		draw()
		
		# Log time after draw
		t2 = datetime.datetime.now()
		
		# Calculate and display elapsed (delta) time
		tDelta = t2 - t0
		print("Draw delta: " + str((tDelta.total_seconds() - spf_target) * 1000) + "ms")

############
# Routines #
############
def init():
	global window

	pygame.init()
	window = pygame.display.set_mode((window_width, window_height))
	pygame.display.set_caption(window_caption)
	
	for i in range(0,200):
		particles.append(Particle("Br", (0, 0), 5, 5, (255, 255, 255)))
	for i in range(0,20):
		particles.append(Particle("Br", (0, 0), 10, 10, (255, 255, 255)))
	for i in range(0,20):
		particles.append(Particle("Br", (0, 0), 20, 20, (255, 255, 255)))
	for i in range(0,2):
		particles.append(Particle("Br", (0, 0), 50, 50, (255, 255, 255)))	

def tick():
	for i, particle in enumerate(particles):
		particle.update()
		for particle2 in particles[i+1:]:
			collide(particle, particle2)

def draw():
	global particles

	window.fill(window_background_color)

	for particle in particles:
		particle.draw()

	pygame.display.flip()

#############
# Functions #
#############

def dist((x1, y1), (x2, y2)):
    return math.hypot(x1 - x2, y1 - y2), x1 - x2, y1 - y2

def addVectors((a1, l1), (a2, l2)):
	x  = math.sin(a1) * l1 + math.sin(a2) * l2
	y  = math.cos(a1) * l1 + math.cos(a2) * l2
	length = math.hypot(x, y)
	angle = 0.5 * math.pi - math.atan2(y, x)
	return (angle, length)

def collide(particle1, particle2):
	# Measure distance between particles
	distance, dx, dy = dist((particle1.x, particle1.y), (particle2.x, particle2.y))
	
	# Check for collision
	if distance <= particle1.radius + particle2.radius:
		angle = math.atan2(dy, dx) + 0.5 * math.pi
		total_mass = particle1.mass + particle2.mass

		(particle1.angle, particle1.speed) = addVectors((particle1.angle, particle1.speed*(particle1.mass-particle2.mass)/total_mass), (angle, 2*particle2.speed*particle2.mass/total_mass))
		(particle2.angle, particle2.speed) = addVectors((particle2.angle, particle2.speed*(particle2.mass-particle1.mass)/total_mass), (angle+math.pi, 2*particle1.speed*particle1.mass/total_mass))
		
		# Fudge the missed collision
		overlap = 0.5*(particle1.radius + particle2.radius - distance+1)
		particle1.x += math.sin(angle)*overlap
		particle1.y -= math.cos(angle)*overlap
		particle2.x -= math.sin(angle)*overlap
		particle2.y += math.cos(angle)*overlap

###########
# Program #
###########
main()
