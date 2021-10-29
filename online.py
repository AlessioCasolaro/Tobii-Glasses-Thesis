import cv2
import numpy as np
import requests


def streaming():
	cap = cv2.VideoCapture("rtsp://192.168.75.51:8554/live/all")

	#Controlla se lo streaming è stato aperto correttamente
	if (cap.isOpened()== False):
		print("Errore apertura streaming")

	url = "http://192.168.75.51/rest/"

	payload = ""
	headers = {}
	response = requests.request("POST", url, headers=headers, data=payload)
	print(response.text)

	# Leggi finche la streaming non è treminata
	while(cap.isOpened()):
		# Cattura frame per frame
		ret, frame = cap.read()
		if ret == True:
			# Mostra i frame 
			cv2.imshow('Tobii Pro Glasses 3 - Live Scene',frame)

			# Comando per stoppare lo streaming video
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

			# Break per il loop
		else:
			break

	cap.release()
	cv2.destroyAllWindows()