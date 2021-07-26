import gzip
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dbscan import *
from aoi import *


# Funzione creata per leggere i valori del file gazedata del video corrispondente
# Restituisce il numero di intervalli e la lista dei valori dell' intervallo di tempo
def openGazeData(char):

    with gzip.open('dataGaze/gazedata'+str(char)+'.gz') as f1:
        time = []
        for data in f1:
            d = json.loads(data)
            timestamp = d.get('timestamp')
            time.append(timestamp)
        listTime = []
        listTime.append(0)
        inter = []
        # L'utente deve scegliere quanti intervalli temporali vuole
        num = int(input("Quanti intervalli: "))
        for i in range(num):
            for j in time:
                maxTime = round(j, 1)
            print("Scegli tra %s e %s:" % (listTime[i], maxTime))
            if i == num - 1:
                helpTime = maxTime
            else:
                helpTime = float(input("Digita: "))
            numTime = (str(listTime[i]) + '-' + str(helpTime))
            listTime.append(helpTime)
            inter.append(numTime)
    return inter, listTime


# Funzione che restituisce il grafico della durata di ogni fissazione
def barGraphDurFix():
    dataFrame = pd.read_csv('out/fixation.csv')             # Lettura del file .csv e salvataggio del dataframe
    data = dataFrame.iloc[:, [0, 2]].values                 # Prendo i valori che mi serviranno dal dataframe
    fig, ax = plt.subplots(num='Durata Fissazioni', figsize=(12, 8))                 # Creo una figura con dimensione 1.200 e 800
    # Loop per creare liste 'dur' e 'nF': lista delle durate di ogni fissazione e lista del numero di fissazioni
    for i in range(len(data[1])):
        dur = [element for element in data[:, 1]]
        listForMaxDur = [element for element in data[: ,1]]
        numF = [element for element in data[:, 0]]
    listForMaxDur.sort()
    for j in range(len(listForMaxDur)):
        maxDur = listForMaxDur[j]
    # Loop per annotare il valore della durata per ogni fissazione

    for i in range(len(numF)):
        plt.bar(numF[i], dur[i])
    #plt.bar(numF, dur)
    # Dettagli del grafico
    plt.ylim(0, maxDur+2)
    plt.xlim(0, numF[i]+2)
    plt.ylabel('Durata (s)',fontweight='bold', fontsize=15)
    plt.xlabel('Fissazioni',fontweight='bold', fontsize=15)
    fig.savefig('grafic/graficDurFix.jpg')
    plt.show()

# Funzione che restituisce il grafico del numero delle fissazioni
# Parametri: inter = numero di intervalli di tempo; listTime = lista dei valori degli intervalli
def barGraphFix(inter,listTime):
    dataFrame = pd.read_csv('out/fixation.csv')                 # Dataframe del file .csv
    data = dataFrame.iloc[:, [0, 1, 3, 4]].values               # Prendo i valori che mi serviranno
    times = [element for element in data[:, 1]]
    time2 = []
    smin = 0
    numF = []

    # Loop per la dimensione della lista 'listTime'
    # Utilizzata per restituire una lista avente il numero di fissazioni per ogni intervallo
    for i in range(1, len(listTime)):
        for x in times:
            if x <= listTime[i]:
                time2.append(x)
                numFix = [int(element) for element in data[smin:len(time2), 1]]
        diff = len(time2) - smin
        smin = smin + diff
        numF.append(len(numFix))
        numFix.clear()
        time2.clear()

    # Dettagli del grafico
    fig, ax = plt.subplots(num='Conteggio Fissazioni',figsize=(12, 8))
    plt.bar(inter, numF, width=0.3)
    # Annotazioni per ogni barra che restituisce il numero di fissazioni
    for i in range(len(inter)):
        plt.annotate(numF[i], (-0.05 + i, numF[i]))
    plt.ylim([0, len(times)])
    plt.ylabel('Numero di Fissazioni',fontweight='bold', fontsize=15)
    plt.xlabel('Intervalli (s)',fontweight='bold', fontsize=15)
    plt.title('Grafico Numero di Fissazioni')
    fig.savefig('grafic/graficNumFissazioni.jpg')
    plt.show()

# Funzione che restituisce il grafico del numero di Aoi.
# Parametri: inter = numero di intervalli; listTime = lista dei valori temporali per ogni intervallo
def barGraphAoi(inter,listTime):
    df = pd.read_csv('out/fixation.csv')                                # Salvo in un dataframe il file .csv
    X = df.iloc[:, [1, 3, 4]].values                                    # Valori del dataframe che mi serviranno
    times = [element for element in X[:, 0]]
    db = DBscan(NOISE=0, UNASSIGNED=0, core=-1, edge=-2)                # Istanza del dbscan
    time2 = []
    smin = 0
    numC = []

    # Loop per la dimensione della lista
    # Trovo i valori x e y per ogni intervallo e eseguo il dbscan su questi valori
    # Mi restituisce una lista con il numero di aoi trovati per ogni intervallo
    for i in range(1, len(listTime)):
        for x in times:
            if x <= listTime[i]:
                time2.append(x)
                numCluX = [element for element in X[smin:len(time2), 1]]
                numCluY = [element for element in X[smin:len(time2), 2]]
        result = np.array([numCluX, numCluY])
        result2 = result.transpose()
        cluster, pl = db.fit(result2)
        numC.append(cluster)
        diff = len(time2) - smin
        smin = smin + diff
        numCluX.clear()
        numCluY.clear()
        time2.clear()

    # Dettagli del grafico
    fig, ax = plt.subplots(num='Conteggio Aoi',figsize=(12, 8))
    plt.bar(inter, numC, width=0.3)
    # Annotazione del numero di aoi per ogni intervallo
    for i in range(len(inter)):
        plt.annotate(numC[i], (-0.05 + i, numC[i]))
    plt.ylim([0, 5])
    plt.ylabel('Numero di Aree di Interesse',fontweight='bold', fontsize=15)
    plt.xlabel('Intervalli (s)',fontweight='bold', fontsize=15)
    plt.title('Grafico Aree di interesse')
    fig.savefig('grafic/graficAoi.jpg')
    plt.show()

# Funzione che mi restituisce un grafico con gli aoi dominanti per ogni intervallo
# Parametri: inter = numero di intervalli; listTime = lista avente i valori del tempo per ogni intervallo
def barGraphAoiDominant(listTime, timePoint):

    listTime2 = [val for val in listTime]
    listTime2.pop(0)
    count = 0
    count2 = 0
    numClust = []
    help1 = []
    for x in range(len(listTime) - 1):
        for i in range(len(timePoint)):
            for j in range(len(timePoint[i])):

                if timePoint[i][j] >= listTime[x] and timePoint[i][j] <= listTime[x + 1]:

                    count += 1
            if count != 0:
                numClust.append(count)
                count2 += 1
            count = 0

        help1.append(count2)
        count2 = 0

    help2 = []
    count3 = 0
    for x in range(len(help1)):
        help2.append([])
        for y in range(help1[x]):
            help2[x].append(numClust[count3])
            count3 += 1

    fig, ax = plt.subplots(num='Aoi Dominante', figsize=(12, 8))
    br1 = 0.1
    br2 = -0.92
    mapcolor = ['red', 'blue', 'green', 'yellow', 'black', 'orange', 'indigo', 'magenta', 'pink', 'grey', 'lime',
                'violet', 'cyan', 'fuchsia']
    count = 0
    maxCount = 0
    for i in range(len(help1)):
        if help1[i] >= 1:
            for j in range(help1[i]):
                br = [br2]
                plt.bar(br, help2[i][j], color=mapcolor[j], width=br1)
                plt.annotate(help2[i][j], (-0.05 + br2, help2[i][j]))
                count += 1
                if j < (help1[i]) - 1:
                    br2 += 0.1
                else:
                    br2 = 0
                    br2 = (1 * i) + 0.2

            if maxCount < count:
                maxCount = count
        else:
            br2 = (1 * (i + 1)) + 0.2
        count = 0
        # Altri dettagli del grafico
        plt.xlabel('Intervalli (s)', fontweight='bold', fontsize=15)
        plt.ylabel('Numero di fissazioni', fontweight='bold', fontsize=15)
        plt.xlim([-1, len(listTime)])
        plt.xticks([r + br1 for r in range(len(listTime2))], [listTime2[x] for x in range(len(listTime2))])  # CORRETTO

    for i in range(maxCount):
        plt.plot(i, label='cluster' + str(i + 1), c=mapcolor[i])
    plt.grid(axis='y')
    plt.legend()
    plt.title('Grafico Aoi Dominante\n(Dbscan)')
    fig.savefig('grafic/graficAOIDominante.jpg')
    plt.show()

# Funzione usata per scegliere il tipo di grafico che si vuole andare a creare e visualizzare
def chooseGraph(char,scene):
    while True:
        print('''Quale grafico vuoi creare e visualizzare?
        1. Grafico a barre per la durata delle fissazioni
        2. Grafico a barre per il numero di fissazioni nel tempo
        3. Grafico a barre per il numero di aree di interesse nel tempo
        4. Grafico a barre per l' AOI dominante nel tempo
        5. Torna al menu precedente
        ''')

        choose = input("Digita l'opzione scelta: ")
        if choose == str(1):
            print("Durata delle fissazioni")
            barGraphDurFix()
        elif choose == str(2):
            print("Numero di fissazioni nel tempo")
            inter, listTime = openGazeData(char)
            barGraphFix(inter,listTime)
        elif choose == str(3):
            print("Numero di aree di interesse nel tempo")
            inter, listTime = openGazeData(char)
            barGraphAoi(inter,listTime)
        elif choose == str(4):
            print("Aoi dominante nel tempo")
            timePoint = readAoiDbscan2(scene)
            inter, listTime = openGazeData(char)
            barGraphAoiDominant(listTime, timePoint)
        elif choose == str(5):
            break
        else:
            print("Numero o parola inserita non valida. ")