import cv2
import numpy as np
import requests


def streaming():
	cap = cv2.VideoCapture("rtsp://192.168.75.51:8554/live/all")

	# Check if camera opened successfully
	if (cap.isOpened()== False):
		print("Error opening video stream or file")

	url = "http://192.168.75.51/rest/system/battery:level"

	payload = ""
	headers = {}

	response = requests.request("POST", url, headers=headers, data=payload)

	print(response.text)

	# Read until video is completed
	while(cap.isOpened()):
		# Capture frame-by-frame
		ret, frame = cap.read()
		if ret == True:
			#height, width = frame.shape[:2]
			#if data_gp['ts'] > 0:
			#   cv2.circle(frame,(int(data_gp['gp'][0]*width),int(data_gp['gp'][1]*height)), 60, (0,0,255), 5)

			# Display the resulting frame
			cv2.imshow('Tobii Pro Glasses 2 - Live Scene',frame)

			# Press Q on keyboard to  exit
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

			# Break the loop
		else:
			break

	# When everything done, release the video capture object
	cap.release()

	# Closes all the frames
	cv2.destroyAllWindows()