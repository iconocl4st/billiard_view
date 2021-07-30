import os
import datetime
import glob


def _get_mock_images():
	ROOT = '/mnt/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/raw/usable/images/'
	ROOT = '/mnt/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/gopro/samples/'
	return [p for p in glob.glob(ROOT + 'video_image_*.png')]


class Environment:
	USE_REAL_GOPRO = False
	MOCK_GOPRO_IMAGES = _get_mock_images()

	INPUT_DIRECTORY = './resources/'
	DATA_DIRECTORY = './output/'
	DEFAULT_IMAGE = '/mnt/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/gopro/output/all_corrected.png'
	TEMPORARY_IMAGE_DURATION = datetime.timedelta(minutes=10)


	@classmethod
	def ensure_directory(cls, directory):
		if os.path.isdir(directory):
			return
		if directory[-1] == '/':
			directory = directory[:-1]
		cls.ensure_directory(os.path.dirname(directory))
		os.mkdir(directory)

	@classmethod
	def get_raw_images_directory(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'images', 'raw')
		if not cls.USE_REAL_GOPRO:
			p = os.path.join(p, 'mocks')
		cls.ensure_directory(p)
		return p

	@classmethod
	def get_processed_images_directory(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'images', 'undistorted')
		if not cls.USE_REAL_GOPRO:
			p = os.path.join(p, 'mocks')
		cls.ensure_directory(p)
		return p

	@classmethod
	def get_calibration_images_directory(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'images', 'calibrations')
		cls.ensure_directory(p)
		return p

	@classmethod
	def get_image_info_dump_directory(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'image_infos')
		cls.ensure_directory(p)
		return p

	@classmethod
	def get_calibration_file(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'calibration_info.json')
		cls.ensure_directory(cls.DATA_DIRECTORY)
		return p

	@classmethod
	def get_fisheye_file(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'fisheye.json')
		cls.ensure_directory(cls.DATA_DIRECTORY)
		return p

	@classmethod
	def get_fisheye_image_directory(cls):
		p = os.path.join(cls.DATA_DIRECTORY, 'images', 'fisheye')
		cls.ensure_directory(p)
		return p

	@classmethod
	def get_default_image_path(cls):
		return cls.DEFAULT_IMAGE

