import numpy as np
import cv2
import pickle
import glob

from environment import Environment


class ImageProcessor:
	_INSTANCE = None

	def __init__(self, h, map1, map2, width, height):
		self.h = h
		self.map1 = map1
		self.map2 = map2
		self.width = width
		self.height = height
		self.reset_required = False
		self.remove_fisheye = True

	def process(self, image):
		if self.remove_fisheye:
			image = cv2.remap(
				image,
				self.map1,
				self.map2,
				interpolation=cv2.INTER_LINEAR,
				borderMode=cv2.BORDER_CONSTANT)
		# crop...
		return image

	@staticmethod
	def get_instance():
		if ImageProcessor._INSTANCE is None:
			with open(Environment.get_calibration_file(), 'rb') as info_file:
				ci = pickle.load(info_file)

			ImageProcessor._INSTANCE = ImageProcessor(
				ci['h'], ci['map1'], ci['map2'], ci['W'], ci['H'])

		return ImageProcessor._INSTANCE





'''
cap = cv2.VideoCapture('/media/thallock/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/raw/usable/GX010027.MP4')
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
if (not cap.isOpened()):
	raise Exception("Unable to open file.")
print(total_frames)


index = 0
while cap.isOpened():
  ret, frame = cap.read()
  if not ret:
    continue
  print(index, index / total_frames)
  index += 1
  undistorted_img = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
  fixed_image = cv2.warpPerspective(undistorted_img, h, (W, H))
  cv2.imwrite('./corrected/fixed_' + str(index) + '.png', fixed_image)

cap.release()


for idx, original_file in enumerate(glob.glob('/media/thallock/1f0ab4b3-c472-49e1-92d8-c0b5664f7fdb/pool/raw/usable/images/video_image_[0-9]*.png')):
  image = cv2.imread(original_file)
  undistorted_img = cv2.remap(image, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
  fixed_image = cv2.warpPerspective(undistorted_img, h, (W, H))
  cv2.imwrite('./corrected/fixed_' + str(idx) + '.png', fixed_image)

  #output = fixed_image.copy()
  #gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
  #circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=0,maxRadius=0)
  #if circles is None:
  #  continue
  #circles = np.round(circles[0, :]).astype("int")
  #circles = np.uint16(np.around(circles))
  #for i in circles[0,:]:
  #  # draw the outer circle
  #  cv2.circle(output,(i[0],i[1]),i[2],(0,255,0),2)
  #  # draw the center of the circle
  #  cv2.circle(output,(i[0],i[1]),2,(0,0,255),3)
  #cv2.imwrite("output/circled_" + str(idx) + ".png", output)
'''

