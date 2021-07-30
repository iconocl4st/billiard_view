from flask import Flask, request, send_file
from flask_cors import CORS

from gopro_client import GoProClient
from image_cache import ImageCache
from calibration import Calibrator
from environment import Environment
from resetter import Reset

app = Flask(__name__)
CORS(app)


# gpCam.downloadLastMedia(gpCam.shoot_video(i), custom_filename="VIDEO_"+str(i)+".MP4")


@app.route('/')
def hello_world():
	return 'Hello World!'


@app.route('/video/')
def video():
	return {
		'success': False,
		'message': 'Video not supported yet'
	}


@app.route('/status/')
def status():
	return {
		'success': True,
		'message': '',
		'connected': False
	}


@app.route('/image/')
def get_image():
	image_cache = ImageCache.get_instance()
	image_id = int(request.args.get('id'))
	try:
		image_info = image_cache.get_image(image_id)
		image_path = image_info.path
	except:
		print('unable to load image', image_id)
		image_path = Environment.get_default_image_path()
	return send_file(image_path, mimetype='image/png')


@app.route('/snapshots/', methods=['GET', 'PUT', 'DELETE'])
def snapshots():
	image_cache = ImageCache.get_instance()
	if request.method == 'GET':
		return {
			'success': True,
			'message': 'retrieved current snapshots',
			'snapshots': [
				info.to_json()
				for info in image_cache.get_snapshots()
			]
		}
	elif request.method == 'PUT':
		gopro = GoProClient.get_instance()
		photo = gopro.take_photo()
		info = image_cache.add_snapshot(photo)
		return {
			'success': True,
			'message': '',
			'image-info': info.to_json()
		}
	elif request.method == 'DELETE':
		image_cache.remove_image(request.json['id'])
		return {
			'success': True,
			'message': 'removed the snapshot'
		}


@app.route('/reset/', methods=['GET', 'PUT', 'DELETE'])
def reset():
	reset = Reset.get_instance()
	# status = GoProClient.get_instance().status()
	if request.method == 'GET':
		image_cache = ImageCache.get_instance()
		info = image_cache.current_reset_image
		if info is None:
			return {
				'success': False,
				'message': 'currently no image'
			}
		return {
			'success': True,
			'message': '',
			'image': info.to_json()
		}
	elif request.method == 'PUT':
		reset = Reset.get_instance()
		if reset.resetting:
			return {
				'success': True,
				'message': 'already resetting'
			}
		reset.begin_reset()
		return {
			'success': True,
			'message': 'started resetting'
		}
	elif request.method == 'DELETE':
		if not reset.resetting:
			return {
				'success': True,
				'message': 'not currently resetting'
			}
		reset.end_reset()
		return {
			'success': True,
			'message': 'stopped resetting'
		}


@app.route('/calibration/', methods=['GET', 'PUT'])
def calibration():
	a = ImageCache.get_instance()
	if request.method == 'GET':
		# return the current calibration image
		pass
	elif request.method == 'PUT':
		c = Calibrator.get_instance()
		c.calibrate()


if __name__ == '__main__':
	app.run()
