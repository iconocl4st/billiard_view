import threading
import time

from gopro_client import GoProClient
from image_cache import ImageCache


class ResetThread(threading.Thread):
	def __init__(self, reset):
		threading.Thread.__init__(self)
		self.reset = reset

	@staticmethod
	def _take_tmp_photo():
		gopro_client = GoProClient.get_instance()
		photo = gopro_client.take_photo()
		image_cache = ImageCache.get_instance()
		image_info = image_cache.add_tmp_image(photo)
		image_cache.current_reset_image = image_info

	def run(self):
		while True:
			if self.reset.resetting:
				ResetThread._take_tmp_photo()
			time.sleep(1)


class Reset:
	_INSTANCE = None
	_THREAD = None

	def __init__(self):
		self.resetting = False

	def begin_reset(self):
		self.resetting = True

	def end_reset(self):
		self.resetting = False

	@classmethod
	def get_instance(cls):
		if cls._INSTANCE is None:
			cls._INSTANCE = Reset()
			cls._THREAD = ResetThread(cls._INSTANCE)
			cls._THREAD.start()

		return cls._INSTANCE
