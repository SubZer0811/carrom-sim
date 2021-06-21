import cv2
import numpy as np
import random
import yaml
from circle import *
from ..vector import vector

with open("config.yaml") as f:
	data = yaml.load(f, Loader=yaml.FullLoader)

FPS = data['FPS']
width = data['width']
height = data['height']
scene = np.zeros((width, height, 3), dtype=np.uint8)+255
frame = scene.copy()
body = []


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

	if(dot_product(collision_normal, relative_velocity) > 0):
		print("HERERERERASDFASDFASDFAWERLJASDFLKJ\n")
		return

	e = min(A.e, B.e)
	# velocity_f = -(1+e)*dot_product(relative_velocity, collision_normal)
	velocity_f = -(1+e)*dot_product(relative_velocity, collision_unit_v)

	# J stands for the impulse
	temp_A = ()
	J_mag = velocity_f / (A.inv_mass + B.inv_mass + temp_A + temp_B)
	# J_vec = [J_mag*collision_normal[0], J_mag*collision_normal[1]]
	J_vec = [J_mag*collision_unit_v[0], J_mag*collision_unit_v[1]]

	A.v[0] += J_vec[0]*A.inv_mass
	A.v[1] += J_vec[1]*A.inv_mass
	B.v[0] -= J_vec[0]*B.inv_mass
	B.v[1] -= J_vec[1]*B.inv_mass
	
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

def resolve_out_of_bounds(obj):
	# This needs to be handled by resolve collision
	if(obj.pos[0]+obj.radius > width or obj.pos[0]-obj.radius < 0):
		obj.v[0] = -obj.v[0]
	if(obj.pos[1]+obj.radius > height or obj.pos[1]-obj.radius < 0):
		obj.v[1] = -obj.v[1]

# create_bodies_random(body_count)
body.append(circle(30, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [100, 250], [20, 0], 1, 1, 1))
body.append(circle(30, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [300, 250], [-20, 0], 1, 1, 1))
# body.append(circle(100, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [250, 250], [0, 0], 1, 0))
body_count = len(body)

while True:

	frame = scene.copy()
	for i in body:
		i.update_pos(0.1, frame)
		resolve_out_of_bounds(i)

	check_collisions()

	cv2.imshow("frame", frame)

	if(cv2.waitKey(10) == ord(chr(27))):
		break

print("End of simulation!")