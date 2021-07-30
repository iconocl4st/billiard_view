import numpy as np
from client_app_state import AppState
from geometry2d import Geometry


def in_bounds(loc, r):
	return (
		r <= loc[0] <= AppState.POOL_DIMENSIONS['table']['width'] - r and
		r <= loc[1] <= AppState.POOL_DIMENSIONS['table']['height'] - r)


def quad_to_js(q):
	return {
		'ball': q['ball'],
		'begin': [Geometry.to_js(p) for p in q['begin']],
		'end': [Geometry.to_js(p) for p in q['end']],
	}


def has_intersection(quads, cue_idx, obj_idx):
	for idx, js_loc in enumerate(AppState.BALL_LOCATIONS):
		if idx == cue_idx or idx == obj_idx:
			continue
		r1 = AppState.POOL_DIMENSIONS['balls'][idx]['r']
		for quad in quads:
			r2 = AppState.POOL_DIMENSIONS['balls'][quad['ball']]['r']
			if Geometry.distance_to_quad(
				quad['begin'][0],
				quad['begin'][1],
				quad['end'][0],
				quad['end'][1],
				Geometry.from_js(js_loc)
			) < r1 + r2:
				return True
	return False


def calculate_simple_shot_from_location(cue_idx, obj_idx, pocket, cue, obj):
	cue_r = AppState.POOL_DIMENSIONS['balls'][0]['r']
	obj_r = AppState.POOL_DIMENSIONS['balls'][obj_idx]['r']

	gp1 = Geometry.from_js(AppState.POOL_DIMENSIONS['pockets'][pocket]['vertices'][0])
	gp2 = Geometry.from_js(AppState.POOL_DIMENSIONS['pockets'][pocket]['vertices'][1])

	[t1, t2] = Geometry.get_pocket_targets(obj, obj_r, gp1, gp2)
	g1 = Geometry.get_ghost_target(obj, obj_r, cue_r, t1)
	g2 = Geometry.get_ghost_target(obj, obj_r, cue_r, t2)
	b1 = Geometry.get_ghost_target(cue, cue_r, cue_r, g1)
	b2 = Geometry.get_ghost_target(cue, cue_r, cue_r, g2)

	cuts = Geometry.get_target_cuts(cue, obj, obj_r, [g1, g2])
	quads = [{
		'ball': 0,
		'begin': [cue, cue],
		'end': [g1, g2],
	}, {
		'ball': obj_idx,
		'begin': [g1, g2],
		'end': [t2, t1],
	}]
	paths = [[b1, g1, t1], [b2, g2, t2]]

	CUT_TOLERANCE = 0.2
	return {
		'key': {
			'type': 'simple-shot',
			'cue-idx': cue_idx,
			'obj-idx': obj_idx,
			'pocket-idx': pocket
		},
		'difficulty': np.linalg.norm(b1 - b2),  # Should probably be an angle...
		'cuts': cuts,
		'points': [Geometry.to_js(t1), Geometry.to_js(t2)],
		'paths': [[Geometry.to_js(point) for point in path] for path in paths],
		'quads': [quad_to_js(quad) for quad in quads],
		'angles': [
			Geometry.get_target_angles(cue, obj, t1),
			Geometry.get_target_angles(cue, obj, t2)],
		'possible': bool(
			np.linalg.norm(cue - g1) <= np.linalg.norm(cue - obj) and
			np.linalg.norm(cue - g2) <= np.linalg.norm(cue - obj) and
			in_bounds(g1, cue_r) and in_bounds(g2, cue_r) and
			np.max(cuts) > -2 + CUT_TOLERANCE and np.min(cuts) < 2 - CUT_TOLERANCE and
			not has_intersection(quads, cue_idx, obj_idx))
	}


def calculate_simple_shot(cue_idx, obj_idx, pocket):
	return calculate_simple_shot_from_location(
		cue_idx,
		obj_idx,
		pocket,
		Geometry.from_js(AppState.BALL_LOCATIONS[cue_idx]),
		Geometry.from_js(AppState.BALL_LOCATIONS[obj_idx])
	)

