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
    temp = []
    temp2 = []
    Matrix = [[0 for x in range(20)] for y in range(20)] 
    timesStartBlink = []
    timesEndBlink = []
    count = 0
    h=0
  

    for i, lf in enumerate(eyeLF):
        if(eyeLF[i] == 0):
            Matrix[h][0]
        while eyeLF[i] == 0:
            i+=1
        Matrix[h][1] = i-1
        h+=1
        count+=1

    print("blink: %d\n", count)

    for i in range(0,count,1):
        print("inizio fine: %d\t%d\n", Matrix[i][0], Matrix[i][1])

    
    #for lf,rg,i in zip(eyeLF,eyeRG,range(0,len(times),1)):
    
        #if (lf == rg == 0):
            #timesStartBlink.append(times[i])

          #  while lf == rg == 0:
                #i+=1

           # timesEndBlink.append(times[i-1])

            

          #  count+=1
        
    

   # print("blink: %d\n", count)
  #  print("inizio fone: %d\t%d\n", timesStartBlink,timesEndBlink)






   
        #if(lf==rg==0 and numpy.arange(time,time*1,33)):
            #temp.append(time)
            #print(time)
        #else:
            #timesStartBlink.append(temp[0])
           # timesEndBlink.append(temp[len(temp)-1])
            #temp.clear()
           




     # Apertura del file di nome pupil.csv in modalità append
    with open('out/blinkDetected.csv', 'w', newline="") as csvBlink:

        # fieldnames è una lista avente i nomi dei campi per l'append
        fieldnames = ['Time start','Time end']
        # writer è una dictionary con i campi della lista fieldnames
        writer = cs.DictWriter(csvBlink, fieldnames=fieldnames)
        writer.writeheader()
            
        #Loop per inserire i valori
        for timeS,timeE in zip(timesStartBlink,timesEndBlink):
            # Inserisco i valori nei campi del dictionary
            writer.writerow({'Time start': timeS, 'Time end':timeE})

    csvBlink.close()  # Chiusura del file


