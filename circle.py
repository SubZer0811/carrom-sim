from math import cos, sin
from body import body
import cv2

class circle(body):
	
	radius = 0

	def __init__(self, radius, color, pos, v, e, mass, w):
		super().__init__(color, pos, v, e, mass, w)
		self.radius = radius

	def draw_body(self, frame):
		print(self.pos.point)
		self.pos.point = tuple([int(i) for i in self.pos.point])
		# cv2.circle(frame, (int(self.pos[0]), int(self.pos[1])), self.radius, self.color, 3)
		cv2.circle(frame, self.pos.point, self.radius, self.color, 3)
		# cv2.line(frame, (int(self.pos[0]), int(self.pos[1])), (int(self.pos[0]+self.radius), int(self.pos[1])), self.color, 3)
		cv2.line(frame, self.pos.point, (int(self.pos.point[0]+self.radius*cos(self.theta)), int(self.pos.point[1]+self.radius*sin(self.theta))), self.color, 3)
