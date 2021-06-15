from math import pi
import cv2

class body:
	
	color = ()
	pos = []
	theta = 0	# angle
	v = []
	w = 0	# angular velocity in radians
	e = 0 	# coefficient of restitution
	mass = 0
	inv_mass = -1

	def __init__(self, color, pos, v, e, mass, w):
		self.color = color
		self.pos = pos
		self.v = v
		self.w = w
		self.e = e
		self.mass = mass
		if mass == 0:		# change this to checking if mass is infinite later
			self.inv_mass = 0
		else:
			self.inv_mass = 1/mass

	def update_pos(self, dt, frame):
		self.pos = (self.pos[0] + self.v[0]*dt, self.pos[1] + self.v[1]*dt)
		self.theta += self.w*dt
		self.draw_body(frame)

	# Abstract function to be implemented by child class
	def draw_body(self, frame):
		pass