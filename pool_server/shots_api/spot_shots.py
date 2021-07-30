import numpy as np

from geometry2d import Geometry
from shot_calculation import calculate_simple_shot_from_location
from client_app_state import AppState


def _location_equal(loc1, loc2):
	return loc1[0] == loc2[0] and loc1[1] == loc2[1]


def _pocket_to_spot(pocket):
	description = AppState.POOL_DIMENSIONS['pockets'][pocket]['description']
	return [
		{'left': 0, 'right': 4}[description[1]],
		{'lower': 0, 'middle': 4, 'upper': 8}[description[0]],
	]


def _flip_pocket_across_x(pocket):
	description = AppState.POOL_DIMENSIONS['pockets'][pocket]['description']
	return AppState.get_pocket_from_description([
		{'lower': 'upper', 'middle': 'middle', 'upper': 'lower'}[description[0]],
		description[1],
	])


def _flip_pocket_across_y(pocket):
	description = AppState.POOL_DIMENSIONS['pockets'][pocket]['description']
	return AppState.get_pocket_from_description([
		description[0],
		{'left': 'right', 'right': 'left'}[description[1]],
	])


def _flip_location_across_x(location):
	return np.array([
		location[0],
		SpotShot.NUM_Y_SPOTS - location[1] + 1
	], dtype=np.int32)


def _flip_location_across_y(location):
	return np.array([
		SpotShot.NUM_X_SPOTS - location[0] + 1,
		location[1],
	], dtype=np.int32)


def get_spot_location(location):
	w = AppState.POOL_DIMENSIONS['table']['width']
	h = AppState.POOL_DIMENSIONS['table']['height']
	return np.asarray([
		w * location[0] / (SpotShot.NUM_X_SPOTS + 1),
		h * location[1] / (SpotShot.NUM_Y_SPOTS + 1)
	], dtype=np.float64)


class SpotShot:
	NUM_X_SPOTS = 3
	NUM_Y_SPOTS = 7

	def __init__(self, cue, obj, pocket):
		self.cue = cue
		self.obj = obj
		self.pocket = pocket

	def ascii_plot(self):
		# import pdb; pdb.set_trace()
		d = (
			['┌---┐'] +
			['|   |'] * 7 +
			['└---┘']
		)

		return '\n'.join([
			' '.join(
				'c' if _location_equal(self.cue, [c, 8-r]) else (
					'o' if _location_equal(self.obj, [c, 8-r]) else (
						'x' if _location_equal(_pocket_to_spot(self.pocket), [c, 8-r]) else d[r][c]
					)
				)
				for c in range(5)
			)
			for r in range(9)
		])

	@staticmethod
	def from_tuple(t):
		return SpotShot([t[0], t[1]], [t[2], t[3]], t[4])

	def to_tuple(self):
		return (
			self.cue[0],
			self.cue[1],
			self.obj[0],
			self.obj[1],
			self.pocket,
		)

	@staticmethod
	def enumerate_all(include_walls=False):
		num_pockets = len(AppState.POOL_DIMENSIONS['pockets'])
		if include_walls:
			x_range = range(0, SpotShot.NUM_X_SPOTS + 2)
			y_range = range(0, SpotShot.NUM_Y_SPOTS + 2)
		else:
			x_range = range(1, SpotShot.NUM_X_SPOTS + 1)
			y_range = range(1, SpotShot.NUM_Y_SPOTS + 1)
		return [
			SpotShot([cx, cy], [ox, oy], pocket)
			for cx in x_range
			for cy in y_range
			for ox in x_range
			for oy in y_range
			for pocket in range(num_pockets)
			if not _location_equal([cx, cy], [ox, oy])
			# if cx != ox or cy != oy
		]

	@staticmethod
	def group_all_by_canonical(include_walls=False):
		ret = {}
		for shot in SpotShot.enumerate_all(include_walls):
			if not shot.get_simple_shot()['possible']:
				continue
			key = shot.to_canonical().to_tuple()
			if key not in ret:
				ret[key] = [shot]
			else:
				ret[key] = sorted(ret[key] + [shot], key=lambda x: x.to_tuple())
		return ret

	# @staticmethod
	# def group_all_by_angle(include_walls=False):
	# 	ret = {}
	# 	for shot in SpotShot.enumerate_all(include_walls):
	# 		key = shot.to_canonical().to_delta()
	# 		if key not in ret:
	# 			ret[key] = [shot]
	# 		else:
	# 			ret[key] = sorted(ret[key] + [shot], key=lambda x: x.to_tuple())
	# 	return ret

	def __copy__(self):
		return SpotShot(
			self.cue.copy(),
			self.obj.copy(),
			self.pocket
		)

	def copy(self):
		return self.__copy__()

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.cue) + ';' + str(self.obj) + ';' + str(self.pocket)

	def flip_across_x(self):
		return SpotShot(
			_flip_location_across_x(self.cue),
			_flip_location_across_x(self.obj),
			_flip_pocket_across_x(self.pocket))

	def flip_across_y(self):
		return SpotShot(
			_flip_location_across_y(self.cue),
			_flip_location_across_y(self.obj),
			_flip_pocket_across_y(self.pocket))

	def to_delta(self):
		# Not quite right, needs to have the orientation too.
		# Want: [2,1],[1,1],[lower left] to be equivalent to
		#		[1,2],[1,3],[middle, left]
		pocket_spot = _pocket_to_spot(self.pocket)
		return (
			self.obj[0] - self.cue[0],
			self.obj[1] - self.cue[1],
			pocket_spot[0] - self.obj[0],
			pocket_spot[1] - self.obj[1],
		)

	def to_canonical(self):
		return min(
			[
				self.copy(),
				self.flip_across_y(),
				self.flip_across_x(),
				self.flip_across_x().flip_across_y(),
				# there are two more axis of rotation...
			],
			key=lambda shot: shot.to_tuple()
		)
		# minimum_shot = None
		# for equiv in [
		#
		# ]:
		# 	if minimum_shot is None or minimum_shot.to_tuple() < equiv.to_tuple():
		# 		minimum_shot =
		# return minimum_shot

	def get_cue_location(self):
		return get_spot_location(self.cue)

	def get_obj_location(self):
		return get_spot_location(self.obj)

	def get_simple_shot(self):
		return calculate_simple_shot_from_location(
			0, 1,
			self.pocket,
			self.get_cue_location(),
			self.get_obj_location()
		)

	def get_key(self):
		return {
			'type': 'simple-shot',
			'cue-idx': 0,
			'obj-idx': 1,
			'pocket-idx': self.pocket
		}


class SpotShotGenerator:
	_INSTANCE = None
	_NOT_INCLUDING_WALLS = None
	_NOT_INCLUDING_WALLS_KEYS = None

	def __init__(self, shots):
		self.shots = shots

	@classmethod
	def get_uniformly_random_shot(cls):
		cls.get_instance()

		key = cls._NOT_INCLUDING_WALLS_KEYS[
			np.random.randint(len(cls._NOT_INCLUDING_WALLS_KEYS))
		]
		shots = cls._NOT_INCLUDING_WALLS[key]
		return shots[np.random.randint(len(shots))]

	@classmethod
	def generate_random_spot_shot(cls):
		cls.get_instance()

		shot = cls.get_uniformly_random_shot()
		simple_shot = shot.get_simple_shot()
		AppState.BALL_LOCATIONS[0] = Geometry.to_js(shot.get_cue_location())
		AppState.BALL_LOCATIONS[1] = Geometry.to_js(shot.get_obj_location())
		for i in range(2, len(AppState.BALL_LOCATIONS)):
			AppState.BALL_LOCATIONS[i] = Geometry.to_js([-1, -1])
		AppState.CUTS = simple_shot['cuts']
		return shot.get_key()

	@classmethod
	def get_instance(cls):
		if cls._INSTANCE is None:
			cls._INSTANCE = SpotShotGenerator(None)
			cls._NOT_INCLUDING_WALLS = SpotShot.group_all_by_canonical()
			cls._NOT_INCLUDING_WALLS_KEYS = [key for key in cls._NOT_INCLUDING_WALLS.keys()]

		return cls._INSTANCE


if __name__ == '__main__':
	print(generate_random_spot_shot())
	# for shot in SpotShot.enumerate_all():
	# 	print(shot)
	# group by cut...
	# for idx, (key, values) in enumerate(SpotShot.group_all_by_canonical().items()):
	# 	print(idx, key)
	# 	print(SpotShot.from_tuple(key).ascii_plot())
	# 	# print(SpotShot.from_tuple(key))
	# 	for value in values:
	# 		print('\t', value)
	#
	# print(_pocket_to_spot(2))
	# print(SpotShot.from_tuple((2,4,2,3,0)).ascii_plot())

	# pocket_idx = 1
	# x_idx = _flip_pocket_across_x(pocket_idx)
	# y_idx = _flip_pocket_across_y(pocket_idx)
	# print(AppState.POOL_DIMENSIONS['pockets'][pocket_idx]['description'])
	# print('x', AppState.POOL_DIMENSIONS['pockets'][x_idx]['description'])
	# print('y', AppState.POOL_DIMENSIONS['pockets'][y_idx]['description'])
