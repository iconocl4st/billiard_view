import json
import os
from datetime import datetime
import time

from environment import Environment


class ImageInfo:
	SNAPSHOT_IMAGE = 0
	TEMPORARY_IMAGE = 1
	CALIBRATION_IMAGE = 2

	def __init__(self, id, image_info, expiration_time, image_type):
		self.id = id
		self.raw_path = image_info['raw-path']
		self.processed_path = (
			image_info['processed-path']
			if 'processed-path' in image_info
			else None)
		self.path = image_info['default-path']
		self.date = image_info['date']
		self.expiration_time = expiration_time
		self.image_type = image_type

	def to_json(self):
		return {
			'id': self.id,
			'expires': self.expiration_time,
			'path': self.path,
			'date': self.date,
			'processed-path': self.processed_path,
			'raw-path': self.raw_path,
			'url': 'http://localhost:5001/image/?id=' + str(self.id)
		}


class ImageCache:
	_INSTANCE = None

	def __init__(self):
		self.next_id = 0
		self.current_reset_image = None
		self.images = {}

	def save_image_infos(self):
		directory = Environment.get_image_info_dump_directory()
		current_time = time.localtime()
		formatted_time = time.strftime('_%Y_%b_%d_%H_%M_%S', current_time)
		output_path = os.path.join(directory, formatted_time + '.json')
		save_object = {
			'infos': [info.to_json() for info in self.images.values()],
			'next-id': self.next_id
		}
		with open(output_path, 'w') as out:
			json.dump(save_object, out, indent=2)

	def get_image(self, ident):
		return self.images[ident]

	def _add_image(self, gopro_output, expiration_time, image_type):
		info = ImageInfo(self.next_id, gopro_output, expiration_time, image_type)
		self.images[self.next_id] = info
		self.next_id += 1
		self.save_image_infos()
		return info

	def add_tmp_image(self, gopro_output):
		expiration_time = gopro_output['date'] + Environment.TEMPORARY_IMAGE_DURATION
		return self._add_image(gopro_output, expiration_time, ImageInfo.TEMPORARY_IMAGE)

	def add_calibration_image(self, image):
		pass

	def add_snapshot(self, gopro_output):
		return self._add_image(gopro_output, None, ImageInfo.SNAPSHOT_IMAGE)

	def remove_image(self, ident):
		del self.images[ident]

	def get_snapshots(self):
		return sorted(
			[
				image
				for image in self.images.values()
				if image.image_type == ImageInfo.SNAPSHOT_IMAGE
			],
			key=lambda x: x.date,
			reverse=True
		)

	def remove_unused_images(self):
		pass

	def save_snapshots(self):
		pass

	@staticmethod
	def get_instance():
		if ImageCache._INSTANCE is None:
			ImageCache._INSTANCE = ImageCache()
			# load previous images?
		return ImageCache._INSTANCE

