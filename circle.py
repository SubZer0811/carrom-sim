from body import body
import cv2

class circle(body):
	
	radius = 0

	def __init__(self, radius, color, pos, v, e, mass):
		super().__init__(color, pos, v, e, mass)
		self.radius = radius

	def draw_body(self, frame):
		cv2.circle(frame, (int(self.pos[0]), int(self.pos[1])), self.radius, self.color, 3)
		cv2.line(frame, (int(self.pos[0]), int(self.pos[1])), (int(self.pos[0]+self.radius), int(self.pos[1])), self.color, 3)
