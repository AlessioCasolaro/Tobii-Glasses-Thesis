import cv2
import numpy as np
import requests
import PySimpleGUI as sg


def streaming():
	cap = cv2.VideoCapture("rtsp://192.168.75.51:8554/live/all?gaze-overlay=true")

	#Controlla se lo streaming è stato aperto correttamente
	if (cap.isOpened()== False):
		print("Errore apertura streaming")

	# Leggi finche la streaming non è treminata
	while(cap.isOpened()):
		# Cattura frame per frame
		ret, frame = cap.read()
		if ret == True:
			# Mostra i frame 
			cv2.imshow('Tobii Pro Glasses 3 - Live Scene',frame)

			# Comando per avviare la calibrazione
			if cv2.waitKey(1) & 0xFF == ord('c'):
				calibrate()
				
			# Comando per stoppare lo streaming video
			elif cv2.waitKey(1) & 0xFF == ord('q'):
				break

			# Break per il loop
		else:
			break

	cap.release()
	cv2.destroyAllWindows()

def calibrate():

	url = "http://192.168.75.51/rest/calibrate!run"

	payload = "[]"
	headers = {
	'Content-Type': 'text/plain'
	}

	response = requests.request("POST", url, headers=headers, data=payload)

	print(response.text)

	