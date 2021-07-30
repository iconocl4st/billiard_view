from flask import Flask, request, send_file
from flask_cors import CORS
from client_app_state import AppState
from api_methods import generate_random_ball_locations, calculate_shots, ensure_initialized
from spot_shots import SpotShotGenerator

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
	ensure_initialized()
	return 'Hello World!'


# Post should be a get with query params...
@app.route('/practice/', methods=['POST'])
def practice():
	ensure_initialized()
	if request.method == 'POST':
		params = request.json['params']
		print(params)
		shot_key = SpotShotGenerator.generate_random_spot_shot()
		return {
			'success': True,
			'message': 'Generated a random spot shot',
			'shot-key': shot_key,
		}
	elif request.method == 'PUT':
		return {
			'success': False,
			'message': 'Idk why this is here...',
		}


@app.route('/image/')
def get_image():
	location = '/mnt/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/gopro/output/all_corrected.png'
	return send_file(location, mimetype='image/png')


@app.route('/cuts/', methods=['GET', 'POST'])
def cuts():
	ensure_initialized()
	if request.method == 'POST':
		AppState.CUTS = request.json['cuts']
		return {
			'success': True,
			'message': 'successfully set the cuts'
		}
	elif request.method == 'GET':
		return {
			'success': True,
			'message': '',
			'cuts': AppState.CUTS
		}


@app.route('/balls/', methods=['GET', 'POST'])
def balls():
	ensure_initialized()
	if request.method == 'POST':
		generate_random_ball_locations()
		print(request.form)
		return {
			'success': True,
			'message': 'generated random ball locations',
		}
	elif request.method == 'GET':
		return {
			'success': True,
			'message': '',
			'locations': AppState.BALL_LOCATIONS
		}


@app.route('/shots/', methods=['GET', 'POST'])
def shots():
	ensure_initialized()
	if request.method == 'POST':
		print(request.form)
		return {
			'success': True,
			'message': 'generated random ball locations',
		}
	elif request.method == 'GET':
		return {
			'success': True,
			'message': 'found all simple shots',
			'shots': calculate_shots()
		}


# # change to sending the whole shot
# @app.route('/shots/selected/', methods=['GET', 'POST'])
# def selected_shot():
# 	ensure_initialized()
# 	if request.method == 'POST':
# 		selection_index = request.json['shot-index']
# 		AppState.SELECTED_SHOT = selection_index
# 		return {
# 			'success': True,
# 			'message': 'set selected shot to ' + str(selection_index),
# 		}
# 	elif request.method == 'GET':
# 		return {
# 			'success': True,
# 			'selected-shot': AppState.SELECTED_SHOT
# 		}


@app.route('/dimensions/')
def dimensions():
	ensure_initialized()
	return {
		'success': True,
		'message': 'Sent table dimensions',
		'dimensions': AppState.POOL_DIMENSIONS
	}


if __name__ == '__main__':
	ensure_initialized()
	app.run()

