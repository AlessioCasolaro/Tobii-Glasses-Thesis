import csv as cs
import gzip
import json
import numpy
import pandas as pd
import matplotlib


from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def blinkDetect():
    # dati del file pupil.csv
    csv_file = 'out/pupil.csv'
    # Salvo in un dataFrame il file letto
    dataFrame = pd.read_csv(csv_file)
    # Salvo in un array i valori dei campi che dovrò utilizzare
    data = dataFrame.iloc[:, [0,1,2]].values
    times = [element for element in data[:, 0]]
    eyeLF = [element for element in data[:, 1]]
    eyeRG = [element for element in data[:, 2]]

    last_was_0=False
    zero_clusters=[]

    for i in range(len(eyeLF)):
        a=eyeLF[i]
        if eyeLF[i] == 0 and eyeRG[i] == 0:
            if last_was_0:
                zero_clusters[-1][-1]+=1
            else:
                zero_clusters.append([i, i])
        last_was_0 = a == 0

     # Apertura del file di nome pupil.csv in modalità append
    with open('out/blinkDetected.csv', 'w', newline="") as csvBlink:

        # fieldnames è una lista avente i nomi dei campi per l'append
        fieldnames = ['Blink Count','Time start','Time end']
        # writer è una dictionary con i campi della lista fieldnames
        writer = cs.DictWriter(csvBlink, fieldnames=fieldnames)
        writer.writeheader()
            
        #Loop per inserire i valori
        for i in range(len(zero_clusters)):
            # Inserisco i valori nei campi del dictionary
            writer.writerow({'Blink Count':i+1, 'Time start': times[zero_clusters[i][0]], 'Time end':times[zero_clusters[i][1]]})

    csvBlink.close()  # Chiusura del file


