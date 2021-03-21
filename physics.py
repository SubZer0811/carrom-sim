import cv2
import numpy as np
import random
import yaml

with open("config.yaml") as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

FPS = data['FPS']
scene = np.zeros((data['width'], data['height'], 3), dtype=np.uint8)+255
frame = scene.copy()
body = []
body_count = 2

class circle:
	
	radius = 0
	color = ()
	pos = []
	v = ()

	def __init__(self, radius, color, pos, v):
		self.radius = radius
		self.color = color
		self.pos = pos
		self.v = v

	def update_pos(self, dt):
		self.pos = (self.pos[0] + self.v[0]*dt, self.pos[1] + self.v[1]*dt)
		print(self.pos)
		self.draw_body()

	def draw_body(self):
		cv2.circle(frame, (int(self.pos[0]), int(self.pos[1])), self.radius, self.color, 3)

def create_bodies_random(n):
	
	for i in range(n):
		rad = random.randint(10, 30)
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		pos = [random.randint(0, 300), random.randint(0, 300)]
		v = [random.randint(0, 30), random.randint(0, 30)]
		body.append(circle(rad, color, pos, v))

def distance(pt1, pt2):
	return pow(((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2), 1/2)

def is_coliding(A, B):
	if distance(A.pos, B.pos) <= A.radius + B.radius:
		return True
	else:
		False

def check_collisions():
	
	i = 0; j = i + 1
	while i < body_count:
		j = i + 1
		while j < body_count:
			if is_coliding(body[i], body[j]):
				print(f"Colliding: {body[i].radius} and {body[j].radius}")
				cv2.waitKey(0)
			j += 1
		i += 1


create_bodies_random(body_count)

while True:

	frame = scene.copy()
	for i in body:
		i.update_pos(0.1)
	
	check_collisions()

	cv2.imshow("frame", frame)

	if(cv2.waitKey(10) == ord(chr(27))):
		break

print("End of simulation!")