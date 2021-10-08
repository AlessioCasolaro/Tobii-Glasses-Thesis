import csv as cs
import gzip
import json
import numpy as np
import pandas as pd
import matplotlib
from pandas.core.frame import DataFrame


from fixatDetection import *
from fixColor import *
from pupil import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import PySimpleGUI as sg

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

def blinkGrafics(min, sup):
    DataFrame = pd.read_csv('out/blinkDetected.csv')   # Lettura del file .csv e salvataggio del dataframe
    data = DataFrame.iloc[:, [0,1,2]].values             # Prendo i valori che mi servono dal dataframe

    blinkCount = [element for element in data[:, 0]]    # Lista dei blink
    startTime = [element for element in data[:, 1]]        # Lista dei tempi di iniziono blink
    endTime = [element for element in data[:, 2]]       # Lista dei tempi di fine blink
    blinkList = []
    startList = []
    endList = []
    durList = []
    counter = 0

    for count, start, end in zip(blinkCount, startTime, endTime):
        if (end >= int(min) and end <= int(sup)):
            counter+=1
            blinkList.append(count)
            startList.append(start)
            endList.append(end)
            durList.append(end-start)

    fig, ax = plt.subplots(num='grafico Blink', figsize=(12,8)) # Creo una figura con dimensione 1.200 e 800

    numBar = np.arange(len(blinkList))
    bar_plot = plt.bar(blinkList,endList,width=0.5)
    print("numbar %s" %numBar)
    plt.xticks([r for r in blinkList],np.round(blinkList,2), rotation=90)

    # Funzione per generare le label sulle bar
    def autolabel(rects):
        for idx,rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 0.5*height,
                    round(endList[idx],4),
                    ha='center', va='bottom', rotation=90)
    autolabel(bar_plot)

    # Dettagli del grafico
    plt.subplots_adjust(bottom= 0.2, top = 0.98)# Regola i margini
    plt.ylabel('End time',fontweight='bold', fontsize=15)
    plt.xlabel('Intervallo fissazione',fontweight='bold', fontsize=15)
    fig.savefig('grafic/graficBlinkDuration.png')
    plt.grid()

    event, values = sg.Window('Dettagli grafico', [[sg.Image(filename='grafic/graficBlinkDuration.png')]]).read(close=True)
    plt.show()