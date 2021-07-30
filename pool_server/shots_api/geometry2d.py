import numpy as np

TOLERANCE = 1e-12


class Geometry:
	@staticmethod
	def to_homo(x):
		return np.array([x[0], x[1], 1.0], dtype=np.float64)

	@staticmethod
	def from_homo(x):
		if abs(x[2]) < TOLERANCE:
			raise Exception('Point at infinity')
		return np.array([x[0] / x[2], x[1] / x[2]])

	@staticmethod
	def to_js(x):
		return {'x': x[0], 'y': x[1]}

	@staticmethod
	def from_js(obj):
		return np.array([obj['x'], obj['y']], dtype=np.float64)

	@staticmethod
	def get_orthogonal_at(line, p):
		return np.array([line[1], -line[0], -(line[1] * p[0] - line[0] * p[1])], dtype=np.float64)

	@staticmethod
	def det2d(v1, v2):
		return v1[0] * v2[1] - v1[1] * v2[0]

	@staticmethod
	def is_to_the_right_of(v1, v2):
		return Geometry.det2d(v1, v2) < 0

	'''
	Solves the system of equations:
	\|x\|^2 == r ** 2
	x @ (x - w) == 0
	
	x ** 2 + y ** 2 = r ** 2
	x * (x - a) + y * (y - b) == 0
	// https://www.wolframalpha.com/input/?i=systems+of+equations+calculator&assumption=%7B%22F%22%2C+%22SolveSystemOf2EquationsCalculator%22%2C+%22equation1%22%7D+-%3E%22x%5E2+%2B+y%5E2+%3D+r%5E2%22&assumption=%22FSelect%22+-%3E+%7B%7B%22SolveSystemOf2EquationsCalculator%22%7D%7D&assumption=%7B%22F%22%2C+%22SolveSystemOf2EquationsCalculator%22%2C+%22equation2%22%7D+-%3E%22x+*+%28x+-+a%29+%2B+y+*+%28y+-+a%29+%3D+0%22
	'''
	@staticmethod
	def solve_edge_system(w, r):
		if abs(w[1]) < TOLERANCE:
			if abs(w[0]) < TOLERANCE:
				if abs(r) < TOLERANCE:
					raise Exception('Infinitely many solutions')
				else:
					raise Exception('No solutions')
			else:
				x = r ** 2 / w[0]
				y = np.sqrt(r ** 2 - (1 - r ** 2 / w[0] ** 2))
				return np.array([[x, y], [x, -y]], dtype=np.float64)
		elif abs(w[0]) < TOLERANCE:
			y = r ** 2 / w[1]
			x = np.sqrt(r ** 2 - (1 - r ** 2 / w[1] ** 2))
			return np.array([[x, y], [-x, y]], dtype=np.float64)
		else:
			rad = np.sqrt(w[0] ** 2 + w[1] ** 2 - r ** 2)
			x_den = w[0] ** 2 + w[1] ** 2
			xp = w[0] * r ** 2
			y_den = w[1] * (w[0] ** 2 + w[1] ** 2)
			yp = w[1] ** 2 * r ** 2
			return np.array([[
				(xp -        w[1] * r * rad) / x_den,
				(yp + w[0] * w[1] * r * rad) / y_den
			], [
				(xp +        w[1] * r * rad) / x_den,
				(yp - w[0] * w[1] * r * rad) / y_den
			]], dtype=np.float64)


	@staticmethod
	def distance_to_segment(l1, l2, p):
		nrm = np.linalg.norm(l1 - l2)
		if nrm < TOLERANCE:
			return np.linalg.norm(l1 - p)
		t = max(0, min(1, (p - l1) @ (l2 - l1) / nrm ** 2))
		proj = l1 + t * (l2 - l1)
		return np.linalg.norm(p - proj)

	@staticmethod
	def on_same_side(l1h, l2h, p1h, p2h):
		line = np.cross(l1h, l2h)
		d1 = line @ p1h
		d2 = line @ p2h
		return abs(d1) < TOLERANCE or abs(d2) < TOLERANCE or np.sign(d1) == np.sign(d2)

	@staticmethod
	def points_are_colinear(p1, p2, p3):
		return abs(Geometry.to_homo(p3) @ np.cross(Geometry.to_homo(p1), Geometry.to_homo(p2))) < TOLERANCE

	@staticmethod
	def distinct_triangle_contains(v1, v2, v3, p):
		v1h = Geometry.to_homo(v1)
		v2h = Geometry.to_homo(v2)
		v3h = Geometry.to_homo(v3)
		ph = Geometry.to_homo(p)
		return (
			Geometry.on_same_side(v1h, v2h, v3h, ph) and
			Geometry.on_same_side(v2h, v3h, v1h, ph) and
			Geometry.on_same_side(v1h, v3h, v2h, ph))

	@staticmethod
	def triangle_contains(v1, v2, v3, p):
		if np.linalg.norm(v1 - v2) < TOLERANCE:
			return Geometry.points_are_colinear(v1, v3, p)
		if np.linalg.norm(v2 - v3) < TOLERANCE:
			return Geometry.points_are_colinear(v1, v2, p)
		if np.linalg.norm(v1 - v3) < TOLERANCE:
			return Geometry.points_are_colinear(v1, v2, p)
		return Geometry.distinct_triangle_contains(v1, v2, v3, p)

	@staticmethod
	def distinct_quad_contains(b1, b2, e1, e2, p):
		b1h = Geometry.to_homo(b1)
		b2h = Geometry.to_homo(b2)
		e1h = Geometry.to_homo(e1)
		e2h = Geometry.to_homo(e2)
		ph = Geometry.to_homo(p)
		if (not Geometry.on_same_side(b1h, b2h, e1h, e2h) or
			not Geometry.on_same_side(b2h, e2h, b1h, e1h) or
			not Geometry.on_same_side(e2h, e1h, b1h, b2h) or
			not Geometry.on_same_side(e1h, b1h, b2h, e2h)):
			raise Exception('bug')
		return (
			Geometry.on_same_side(b1h, b2h, e1h, ph) and
			Geometry.on_same_side(b2h, e2h, b1h, ph) and
			Geometry.on_same_side(e2h, e1h, b1h, ph) and
			Geometry.on_same_side(e1h, b1h, b2h, ph))

	@staticmethod
	def quad_contains(b1, b2, e1, e2, p):
		if np.linalg.norm(b1 - b2) < TOLERANCE:
			return Geometry.triangle_contains(b1, e1, e2, p)
		if np.linalg.norm(e1 - e2) < TOLERANCE:
			return Geometry.triangle_contains(b1, b2, e1, p)
		if np.linalg.norm(e1 - b1) < TOLERANCE:
			return Geometry.triangle_contains(b1, b2, e2, p)
		if np.linalg.norm(e2 - b2) < TOLERANCE:
			return Geometry.triangle_contains(b1, b2, e1, p)
		return Geometry.distinct_quad_contains(b1, b2, e1, e2, p)

	@staticmethod
	def distance_to_quad(b1, b2, e1, e2, p):
		if Geometry.quad_contains(b1, b2, e1, e2, p):
			return 0.0
		return np.min([
			Geometry.distance_to_segment(b1, e1, p),
			Geometry.distance_to_segment(e1, e2, p),
			Geometry.distance_to_segment(e2, b2, p),
			Geometry.distance_to_segment(b2, b1, p),
		])

	@staticmethod
	def extend_line(p1, p2, d):
		return p1 + (1 + d / np.linalg.norm(p2 - p1)) * (p2 - p1)

	@staticmethod
	def get_edge_point(obj_location, goal_post, radius, inner):
		line = np.cross(Geometry.to_homo(obj_location), Geometry.to_homo(goal_post))
		orientation = np.sign(line @ Geometry.to_homo(inner))
		for sol in Geometry.solve_edge_system(obj_location - goal_post, radius):
			ret = goal_post + sol
			if orientation == np.sign(line @ Geometry.to_homo(ret)):
				return ret
		raise Exception('bug')

	@staticmethod
	def get_cushion_target():
		pass

	@staticmethod
	def get_pocket_targets(obj, obj_r, gp1, gp2):
		return [
			Geometry.get_edge_point(obj, gp1, obj_r, gp2),
			Geometry.get_edge_point(obj, gp2, obj_r, gp1)]

	@staticmethod
	def get_ghost_target(obj, obj_r, cue_r, target):
		return Geometry.extend_line(target, obj, obj_r + cue_r)

	@staticmethod
	def get_target_cuts(cue, obj, obj_r, targets):
		cueh = Geometry.to_homo(cue)
		objh = Geometry.to_homo(obj)
		direct_line = np.cross(cueh, objh)
		orthog_line = Geometry.get_orthogonal_at(direct_line, obj)

		if np.linalg.norm(cue - obj) < TOLERANCE:
			return []

		cuts = []
		for target in targets:
			tarh = Geometry.to_homo(target)
			aim_line = np.cross(cueh, tarh)
			interh = np.cross(aim_line, orthog_line)
			inter = Geometry.from_homo(interh)
			dist = np.linalg.norm(inter - obj)
			signum = -1 \
				if Geometry.is_to_the_right_of(cue - obj, target - cue) \
				else 1
			cuts.append(signum * dist / obj_r)
		return sorted(cuts)

	@staticmethod
	def get_target_angles(cue, obj, target):
		tp1 = cue - obj
		tp2 = target - obj
		a1 = np.arctan2(tp1[1], tp1[0])
		a2 = np.arctan2(tp2[1], tp2[0])
		a = a2 - a1
		while a < 0:
			a += 2 * np.pi
		while a > 2 * np.pi:
			a -= 2 * np.pi
		return 180 * a / np.pi
