from math import pi
import vector.vector as vector

class body:
	
	color = ()
	pos = vector.point2d((0, 0))		# TODO should be able to create empty vectors and points
	theta = 0	# angle
	v = vector.vector2d((0, 0))
	w = 0	# angular velocity in radians
	e = 0 	# coefficient of restitution
	mass = 0
	inv_mass = -1

	def __init__(self, color, pos, v, e, mass, w):
		self.color = color
		self.pos = vector.point2d(pos)
		self.v = vector.vector2d(v)
		self.w = w
		self.e = e
		self.mass = mass
		if mass == 0:		# change this to checking if mass is infinite later
			self.inv_mass = 0
		else:
			self.inv_mass = 1/mass

	def update_pos(self, dt, frame):
		self.pos = vector.point(self.pos + self.v*dt)
		self.theta += self.w*dt
		self.draw_body(frame)

	# Abstract function to be implemented by child class
	def draw_body(self, frame):
		pass