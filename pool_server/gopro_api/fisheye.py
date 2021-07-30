import os
import cv2
import numpy as np
import glob
import json

from environment import Environment


USE_OLD_CODE = False


def get_image_paths():
	root_directory = '/mnt/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/ProjectsForFun/Pool/pool_server/checkerboard_images/'
	return glob.glob(root_directory + 'GOPR0*.JPG')


def save_fisheye_params():
	board_physical_width = 700
	board_physical_height = 490
	# Number of interior corners:
	board_w = 9
	board_h = 6

	detected_corners = []
	expected_corners = []

	true_corners = np.zeros((board_h * board_w, 3), np.float32)
	true_corners[:, :2] = np.mgrid[
		0:(board_w * board_physical_width):board_physical_width,
		0:(board_h * board_physical_height):board_physical_height
	].T.reshape(-1, 2)

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

	fisheye_image_directory = Environment.get_fisheye_image_directory()

	shape = None
	for idx, path in enumerate(get_image_paths()):
		image = cv2.imread(path)
		shape = image.shape
		desired_shape = (int(shape[1] / 3), int(shape[0] / 3))
		grey_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

		print('Looking for corners...')
		found, corners = cv2.findChessboardCorners(grey_image, (board_w, board_h))
		print('...able to find corners:', found)
		if not found:
			corners_path = os.path.join(
				fisheye_image_directory, 'corners_not_found_' + str(idx) + '.png')
			cv2.imwrite(corners_path, image)
			continue

		# Improve the accuracy of the checkerboard corners
		cv2.cornerSubPix(grey_image, corners, (20, 20), (-1, -1), criteria)

		detected_corners.append(corners)
		expected_corners.append(true_corners)

		corners_path = os.path.join(
			fisheye_image_directory, 'corners_found_' + str(idx) + '.png')
		cv2.drawChessboardCorners(image, (board_w, board_h), corners, found)
		cv2.imwrite(corners_path, image)
	print('shape', shape)

	# intrinsic_matrix = np.zeros((3, 3), np.float32)
	# distCoeffs = np.zeros((5, 1), np.float32)
	ret, intrinsic_matrix, distCoeff, rvecs, tvecs = (
		cv2.calibrateCamera(
			expected_corners,
			detected_corners,
			(shape[1], shape[0]),
			None, None)
	)

	# Save matrices
	print('Intrinsic Matrix:')
	print(intrinsic_matrix)
	print(' ')
	print('Distortion Coefficients:')
	print(distCoeff)
	print(' ')

	save_path = Environment.get_fisheye_file()
	with open(save_path, 'w') as fisheye_out:
		json.dump({
			'intrinsic-matrix': [[aij for aij in ai] for ai in intrinsic_matrix],
			'dist-coeff': [[aij for aij in ai] for ai in distCoeff],
			'shape': [shape[1], shape[0]],
		}, fisheye_out, indent=2)

	# Calculate the total reprojection error.
	# The closer to zero the better.
	tot_error = 0
	for i in range(len(expected_corners)):
		imgpoints2, _ = cv2.projectPoints(expected_corners[i], rvecs[i], tvecs[i], intrinsic_matrix, distCoeff)
		error = cv2.norm(detected_corners[i], imgpoints2, cv2.NORM_L2) / len(imgpoints2)
		tot_error += error

	print("Total Reprojection error: ", tot_error / len(expected_corners))


def load_fisheye_params():
	save_path = Environment.get_fisheye_file()
	with open(save_path, 'r') as fisheye_in:
		return json.load(fisheye_in)


def create_fisheye_mapper():
	fish_eye_params = load_fisheye_params()
	intrinsic_matrix = np.array(fish_eye_params['intrinsic-matrix'], np.float32)
	dist_coeff = np.array(fish_eye_params['dist-coeff'], np.float32)
	shape = fish_eye_params['shape']

	if not USE_OLD_CODE:
		return lambda image: cv2.undistort(image, intrinsic_matrix, dist_coeff, None)
	else:
		def old_code(img):
			DIM = shape
			K = intrinsic_matrix
			D = dist_coeff

			dim2 = None
			dim3 = None
			balance = 0.8

			# dim1 is the dimension of commands image to un-distort
			dim1 = img.shape[:2][::-1]
			assert dim1[0] / dim1[1] == DIM[0] / DIM[1], \
				"Image to undistort needs to have same aspect ratio as the ones used in calibration"
			if not dim2:
				dim2 = dim1
			if not dim3:
				dim3 = dim1

			scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
			scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
			# This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image.
			# OpenCV document failed to make this clear!
			new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
			map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
			undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
			return undistorted_img
		return old_code


def test_fisheye():
	fisheye_image_directory = Environment.get_fisheye_image_directory()
	mapper = create_fisheye_mapper()
	for idx, p in enumerate(get_image_paths()):
		image = cv2.imread(p)
		dst = mapper(image)

		undistorted_path = os.path.join(
			fisheye_image_directory, 'undistorted_' + str(idx) + '.png')
		cv2.imwrite(undistorted_path, dst)


if __name__ == '__main__':
	# save_fisheye_params()
	test_fisheye()
