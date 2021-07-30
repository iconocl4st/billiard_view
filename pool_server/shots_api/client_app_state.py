

def _generate_pockets():
	return [{
		'num': idx,
		'description': description,
		'type': t,
		'vertices': [
			{'x': x + r * vx, 'y': y + r * vy}
			for vx, vy in vertex_offsets]}
		for [r1, r2] in [[2.6, 3.1]]
		for idx, [x, y, r, vertex_offsets, description, t] in enumerate([
			[ 0,  0, r2, [[0,  1], [ 1, 0]], ['lower', 'left'], 'corner'],
			[ 0, 46, r1, [[0, -1], [ 0, 1]], ['middle', 'left'], 'side'],
			[ 0, 92, r2, [[0, -1], [ 1, 0]], ['upper', 'left'], 'corner'],
			[46,  0, r2, [[0,  1], [-1, 0]], ['lower', 'right'], 'corner'],
			[46, 46, r1, [[0, -1], [ 0, 1]], ['middle', 'right'], 'side'],
			[46, 92, r2, [[0, -1], [-1, 0]], ['upper', 'right'], 'corner'], ])]


class AppState:
	INITIALIZED = False

	# SELECTED_SHOT = -1

	POOL_DIMENSIONS = {
		'table': {'width': 46, 'height': 92},
		'balls': [
			{
				'type': ball_type,
				'num': idx,
				'r': 2.26 / 2,
				'label': 'cue' if idx == 0 else str(idx)
			}
			for idx, ball_type in enumerate(9 * ['solid'] + 7 * ['stripe'])
		],
		'pockets': _generate_pockets(),
	}

	BALL_LOCATIONS = [{'x': -1, 'y': -1} for _ in range(16)]

	CUTS = []

	@staticmethod
	def get_pocket_from_description(description):
		for idx, pocket in enumerate(AppState.POOL_DIMENSIONS['pockets']):
			if pocket['description'][0] != description[0]:
				continue
			if pocket['description'][1] != description[1]:
				continue
			return idx
		return -1
