import cv2
import abc
import shutil
import os
import time
import numpy as np
import datetime

from image_processing import ImageProcessor
from environment import Environment

try:
	from goprocam import GoProCamera
	from goprocam import constants
except:
	print('no go pro libraries')


def _get_random_string(l=50):
	return ''.join([y for y in np.random.choice(
		[x for x in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'], l
	)])


def _replace_suffix(original, new_suffix):
	return original[:-len('.png')] + new_suffix


class GoProBase:
	def __init__(self):
		self.last_photo = None

	@abc.abstractmethod
	def sub_take_raw_photo(self):
		pass

	@abc.abstractmethod
	def turn_off(self):
		pass

	@abc.abstractmethod
	def turn_on(self):
		pass

	def take_photo(self):
		ret = {'date': datetime.datetime.now()}
		original_file = self.sub_take_raw_photo()
		current_time = time.localtime()
		formatted_time = time.strftime('_%Y_%b_%d_%H_%M_%S', current_time)
		filename = _replace_suffix(original_file, formatted_time + '.png')
		ret['raw-path'] = os.path.join(
			Environment.get_raw_images_directory(), filename)
		ret['default-path'] = ret['raw-path']
		shutil.move(original_file, ret['raw-path'])
		try:
			raw_image = cv2.imread(ret['raw-path'])
			processed_image = ImageProcessor.get_instance().process(raw_image)
			ret['processed-path'] = os.path.join(
				Environment.get_processed_images_directory(), filename)
			cv2.imwrite(ret['processed-path'], processed_image)
			ret['default-path'] = ret['processed-path']
		except:
			print('Unable to process image')
		return ret


	# def take_photo(self):
	# 	_, persp_path, raw_image = self.take_raw_photo()
	# 	undistorted = undistort_image(raw_image)
	# 	cv2.imwrite(persp_path, undistorted)
	# 	self.last_photo = persp_path
	# 	return persp_path, undistorted
	#
	# def take_tmp_photo(self):
	# 	raw_path, persp_path, raw_image = self.take_raw_photo()
	# 	undistorted = undistort_image(raw_image)
	# 	os.remove(raw_path)
	# 	return undistorted
	#
	# def get_last_photo(self):
	# 	if self.last_photo is None:
	# 		# raise Exception('No last image currently available.')
	# 		return None
	# 	return cv2.imread(self.last_photo)


class MockGoPro(GoProBase):
	def __init__(self, mock_image_paths):
		GoProBase.__init__(self)
		self.mock_image_paths = mock_image_paths
		self.mock_image_index = 0

	def sub_take_raw_photo(self):
		image_path = self.mock_image_paths[self.mock_image_index]
		self.mock_image_index = (self.mock_image_index + 1) % len(self.mock_image_paths)
		filename = _get_random_string() + '.png'
		cv2.imwrite(filename, cv2.imread(image_path))
		return filename

	def turn_off(self):
		pass

	def turn_on(self):
		pass


class RealGoPro(GoProBase):
	def __init__(self, gopro_ref):
		GoProBase.__init__(self)
		self.gopro = gopro_ref

	def sub_take_raw_photo(self):
		photo_url = self.gopro.take_photo(timer=0)
		photo_info = self.gopro.getInfoFromURL(photo_url)
		# Could set the filename with a custom file name...
		self.gopro.downloadMedia(folder=photo_info[0], file=photo_info[1])
		filename = photo_info[1]
		return filename

	def turn_off(self):
		pass

	def turn_on(self):
		pass


def _create_gopro():
	if Environment.USE_REAL_GOPRO:
		gopro = GoProCamera.GoPro()
		gopro.mode(constants.Mode.PhotoMode)
		return RealGoPro(gopro)
	if Environment.MOCK_GOPRO_IMAGES is None or len(Environment.MOCK_GOPRO_IMAGES) == 0:
		print('No mock images set.')
	else:
		return MockGoPro(Environment.MOCK_GOPRO_IMAGES)


class GoProClient:
	_INSTANCE = None

	@classmethod
	def get_instance(cls):
		if cls._INSTANCE is None:
			cls._INSTANCE = _create_gopro()
		return cls._INSTANCE
