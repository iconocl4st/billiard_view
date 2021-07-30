import random

from client_app_state import AppState
from shot_calculation import calculate_simple_shot
from spot_shots import SpotShotGenerator


def generate_random_ball_locations():
	w = AppState.POOL_DIMENSIONS['table']['width']
	h = AppState.POOL_DIMENSIONS['table']['height']
	balls = AppState.POOL_DIMENSIONS['balls']

	locations = []
	for ball in balls:
		if ball['num'] != 0 and random.random() < 0.3:
			locations.append({'x': -1, 'y': -1})
			continue

		intersects_other_ball = True
		location = None
		while intersects_other_ball:
			location = {
				'x': ball['r'] + (w - 2 * ball['r']) * random.random(),
				'y': ball['r'] + (h - 2 * ball['r']) * random.random()
			}
			intersects_other_ball = False
			for idx, prev_location in enumerate(locations):
				dx = location['x'] - prev_location['x']
				dy = location['y'] - prev_location['y']
				r = ball['r'] + balls[idx]['r']
				if dx ** 2 + dy ** 2 < r ** 2:
					intersects_other_ball = True
					continue
		locations.append(location)
	AppState.BALL_LOCATIONS = locations
	AppState.SELECTED_SHOT = -1


def calculate_shots():
	num_balls = len(AppState.POOL_DIMENSIONS['balls'])
	num_pockets = len(AppState.POOL_DIMENSIONS['pockets'])
	cue_idx = 0
	return [
		shot
		for obj_idx in range(1, num_balls)
		for pocket in range(num_pockets)
		for shot in [calculate_simple_shot(cue_idx, obj_idx, pocket)]
		if shot['possible']
	]


def ensure_initialized():
	if AppState.INITIALIZED:
		return

	generate_random_ball_locations()
	AppState.INITIALIZED = True
	SpotShotGenerator.get_instance()

