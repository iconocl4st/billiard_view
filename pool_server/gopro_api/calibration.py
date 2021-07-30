import cv2
import os
import numpy as np
import glob
import pickle

from environment import Environment

stickers = [
	cv2.imread(sticker_path)
	for sticker_path in glob.glob('./data/stickers/[0-9]*.png')
]


def _union(stickers1, stickers2):
	if stickers1 is None or len(stickers1) == 0:
		return stickers2
	elif stickers2 is None or len(stickers2) == 0:
		return stickers1
	ret = []
	for s in stickers1:
		if len(ret) > 0 and min(np.linalg.norm(np.array(ret) - s, axis=1)) < 50:
			continue
		ret.append(s)
	for s in stickers2:
		if len(ret) > 0 and min(np.linalg.norm(np.array(ret) - s, axis=1)) < 10:
			continue
		ret.append(s)
	return np.array(ret)


_cart_to_homo = lambda img_coord: np.hstack((img_coord, np.ones((img_coord.shape[0], 1))))

_homo_to_cart = lambda homo_coord: homo_coord[:, 0:2] / homo_coord[:, 2, None]


def _create_homeography(fromCoord, toCoord):
	if fromCoord.shape[1] != 2 or toCoord.shape[1] != 2:
		raise Exception("Wrong dimension")
	if fromCoord.shape[0] != toCoord.shape[0]:
		raise Exception("Different number of points")
	h = np.linalg.lstsq(
		np.vstack([
			np.array([
				[p1[0], p1[1], 1, 0, 0, 0, -p1[0] * p2[0], -p1[1] * p2[0]],
				[0, 0, 0, p1[0], p1[1], 1, -p1[0] * p2[1], -p1[1] * p2[1]],
			])
			for p1, p2 in zip(fromCoord, toCoord)
		]),
		toCoord.reshape(2 * toCoord.shape[0]),
		rcond=None
	)[0]
	hmat = np.array([
		[h[0], h[1], h[2]],
		[h[3], h[4], h[5]],
		[h[6], h[7], 1],
	], np.float32)
	return lambda x: _homo_to_cart((hmat @ _cart_to_homo(x).T).T)


SAVED_FISH_EYE_INFO = {
	'intrinsic-matrix': np.array([
		[1941.662775454801, 0.0, 1928.2671227947174],
		[0.0, 1953.7483581582524, 1078.328660235385],
		[0.0, 0.0, 1.0]]),
	'dist-coef': np.array([
		[0.028583033212133114], [0.022017145724581813], [0.12299608165041478], [-0.17721206322389202]])
	'dimensions': (3840, 2160)
}

def save_calibration(
		calibration_photo,
		calibration_path
):
	current_stickers = None
	threshold = 0.8

	print('Detecting stickers...')
	current_stickers = None
	for template in stickers:
		w, h = template.shape[1], template.shape[0]
		res = cv2.matchTemplate(calibration_photo, template, cv2.TM_CCOEFF_NORMED)
		loc = np.where(res >= threshold)
		current_stickers = _union(np.array([
			[pt[0] + w / 2, pt[1] + h / 2]
			for pt in zip(*loc[::-1])
		]), current_stickers)

	print('Found ' + str(len(current_stickers)) + ' stickers.')

	corner_directions = np.array([
		[+1, +1, 0],
		[+1, -1, 0],
		[-1, +1, 0],
		[-1, -1, 0],
	]) / np.sqrt(2)

	NSPOTSX = 7
	NSPOTSY = 3

	corner_locations = np.array([
		[NSPOTSX / (NSPOTSX + 1), NSPOTSY / (NSPOTSY + 1)],
		[NSPOTSX / (NSPOTSX + 1), 1 / (NSPOTSY + 1)],
		[1 / (NSPOTSX + 1), NSPOTSY / (NSPOTSY + 1)],
		[1 / (NSPOTSX + 1), 1 / (NSPOTSY + 1)],
	])
	expected_locations = np.array([
		[x, y]
		for idx1, x in enumerate(np.linspace(0, 1, NSPOTSX + 2))
		if idx1 != 0 and idx1 != NSPOTSX + 1
		for idx2, y in enumerate(np.linspace(0, 1, NSPOTSY + 2))
		if idx2 != 0 and idx2 != NSPOTSY + 1
	])

	hs = _cart_to_homo(current_stickers)
	corners = _homo_to_cart(hs[np.argmax(hs @ corner_directions.T, axis=0)])
	homo = _create_homeography(corner_locations, corners)
	image_expected_locations = homo(expected_locations)
	closest_locations = np.array([
		current_stickers[np.argmin(np.linalg.norm(current_stickers - expected_sticker_location, axis=1))]
		for expected_sticker_location in image_expected_locations
	])

	debug_w = 75
	debug_h = 75
	debug_image = calibration_photo.copy()
	font = cv2.FONT_HERSHEY_SIMPLEX
	for pt in current_stickers:
		cv2.rectangle(
			img=debug_image,
			rec=(int(pt[0] - debug_w), int(pt[1] - debug_h), int(2 * debug_w), int(2 * debug_h)),
			color=(255, 255, 255), thickness=2)
	debug_w *= 0.75
	debug_h *= 0.75
	for pt in corners:
		cv2.rectangle(
			img=debug_image,
			rec=(int(pt[0] - debug_w), int(pt[1] - debug_h), int(2 * debug_w), int(2 * debug_h)),
			color=(255, 0, 0), thickness=2)
	debug_w *= 0.75
	debug_h *= 0.75
	for idx, pt in enumerate(image_expected_locations):
		# , 2, cv2.LINE_AA
		cv2.putText(
			img=debug_image,
			text=str(idx),
			org=(int(pt[0]), int(pt[1])),
			fontFace=font,
			fontScale=1,
			color=(0, 255, 0))
		cv2.rectangle(
			img=debug_image,
			rec=(int(pt[0] - debug_w), int(pt[1] - debug_h), int(2 * debug_w), int(2 * debug_h)),
			color=(0, 255, 0), thickness=2)
	debug_w *= 0.75
	debug_h *= 0.75
	for idx, pt in enumerate(closest_locations):
		# , 2, cv2.LINE_AA
		cv2.putText(
			img=debug_image,
			text=str(idx),
			org=(int(pt[0]), int(pt[1])),
			fontFace=font,
			fontScale=1,
			color=(0, 0, 255))
		cv2.rectangle(
			img=debug_image,
			rec=(int(pt[0] - debug_w), int(pt[1] - debug_h), int(2 * debug_w), int(2 * debug_h)),
			color=(0, 0, 255), thickness=2)

	p = os.path.join(
		Environment.get_calibration_images_directory(),
		'stickers_detected' + '' + '.png'
	)
	cv2.imwrite(p, debug_image)

	M = 30
	W = 92 * M
	H = 36 * M

	wb = 0.97
	hb = 0.96
	a1 = (np.array([[wb, 0], [0, hb]]) @ expected_locations.T).T + np.array([(1 - wb) / 2, (1 - hb) / 2])
	a2 = (np.array([[W, 0], [0, H]]) @ a1.T).T

	h, status = cv2.findHomography(closest_locations, a2)

	with open(calibration_path, 'wb') as info_file:
		pickle.dump(
			{
				'h': h,
				'map1': map1,
				'map2': map2,
				'W': W,
				'H': H,
			},
			info_file
		)


class Calibrator:
	_INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls._INSTANCE is None:
			cls._INSTANCE = Calibrator()
		return cls._INSTANCE

