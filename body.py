import cv2

class body:
	
	color = ()
	pos = []
	v = []
	e = 0 	# coefficient of restitution
	mass = 0

	def __init__(self, color, pos, v, e, mass):
		self.color = color
		self.pos = pos
		self.v = v
		self.e = e
		self.mass = mass

	def update_pos(self, dt, frame):
		self.pos = (self.pos[0] + self.v[0]*dt, self.pos[1] + self.v[1]*dt)
		self.draw_body(frame)

	# Abstract function to be implemented by child class
	def draw_body(self, frame):
		pass