import cv2
import numpy as np
import random
import yaml

with open("config.yaml") as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

FPS = data['FPS']
width = data['width']
height = data['height']
scene = np.zeros((width, height, 3), dtype=np.uint8)+255
frame = scene.copy()
body = []
body_count = 2

class circle:
	
	radius = 0
	color = ()
	pos = []
	v = []
	e = 0 	# coefficient of restitution
	mass = 0

	def __init__(self, radius, color, pos, v, e, mass):
		self.radius = radius
		self.color = color
		self.pos = pos
		self.v = v
		self.e = e
		self.mass = mass

	def update_pos(self, dt):
		self.pos = (self.pos[0] + self.v[0]*dt, self.pos[1] + self.v[1]*dt)
		if(self.pos[0]+self.radius > width or self.pos[0]-self.radius < 0):
			self.v[0] = -self.v[0]
		if(self.pos[1]+self.radius > height or self.pos[1]-self.radius < 0):
			self.v[1] = -self.v[1]

		# print(self.v)
		self.draw_body()

	def draw_body(self):
		cv2.circle(frame, (int(self.pos[0]), int(self.pos[1])), self.radius, self.color, 3)

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
				# cv2.waitKey(0)
				resolve_collision(body[i], body[j])
			j += 1
		i += 1

def magnitude(v):
	return pow(v[0]**2 + v[1]**2, 1/2)

def resolve_collision(A, B):
	print("RESOLVING COLLISION")
	collision_normal = [A.pos[0] - B.pos[0], A.pos[1] - B.pos[1]]
	collision_mag = magnitude(collision_normal)
	collision_unit_v = [i/collision_mag for i in collision_normal]
	
	relative_velocity = [A.v[0] - B.v[0], A.v[1] - B.v[1]]

	print(collision_normal)
	print(relative_velocity)
	if(dot_product(collision_normal, relative_velocity) > 0):
		print("HERERERERASDFASDFASDFAWERLJASDFLKJ\n")
		return

	e = min(A.e, B.e)
	# velocity_f = -(1+e)*dot_product(relative_velocity, collision_normal)
	velocity_f = -(1+e)*dot_product(relative_velocity, collision_unit_v)

	# J stands for the impulse
	J = velocity_f / (1/A.mass + 1/B.mass)
	# J_vec = [J*collision_normal[0], J*collision_normal[1]]
	J_vec = [J*collision_unit_v[0], J*collision_unit_v[1]]

	A.v[0] += J_vec[0]/A.mass
	A.v[1] += J_vec[1]/A.mass
	B.v[0] -= J_vec[0]/B.mass
	B.v[1] -= J_vec[1]/B.mass

	print(velocity_f)
	
def dot_product(v1, v2):
	return (v1[0]*v2[0] + v1[1]*v2[1])

def create_bodies_random(n):
	
	for i in range(n):
		rad = random.randint(10, 30)
		color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
		pos = [random.randint(0, 500), random.randint(0, 500)]
		v = [random.randint(-50, 50), random.randint(-50, 50)]
		e = 0.8
		# e = random.randrange(0,100) / 100
		mass = random.randint(5, 10)
		body.append(circle(rad, color, pos, v, e, mass))

# create_bodies_random(body_count)
body.append(circle(10, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [100, 250], [20, 0], 0.8, 10))
body.append(circle(10, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [300, 250], [5, 0], 0.8, 10))
# body.append(circle(20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [0, 500], [10, -10], 0.8, 10))

while True:

	frame = scene.copy()
	for i in body:
		i.update_pos(0.1)
	
	check_collisions()

	cv2.imshow("frame", frame)

	if(cv2.waitKey(10) == ord(chr(27))):
		break

print("End of simulation!")