import queue
import collections
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from numpy.linalg import norm

class DBscan():


    # Costrutto della classe, ha come parametri i valori dei punti rumore = 0,
    # i valori dei punti non assegnati = 0, il valore dei punti centrali = -1 e
    # il valore dei punti bordi = -2
    def __init__(self, NOISE, UNASSIGNED, core, edge):
        self.NOISE = NOISE
        self.UNASSIGNED = UNASSIGNED
        self.core = core
        self.edge = edge

    # Funzione per calcolare la distanza (raggio) tra i punti e il
    # punto corrente
    # Se la distanza dei vari punti è minore del raggio allora li inserisco 
    # nella lista 'punti'
    def calculateNearby(self,dati, pointId, raggio):
        pointList = []
        for i in range(len(dati)):
            a = (np.linalg.norm(dati[i] - dati[pointId])) * 50

            if a <= raggio:
                pointList.append(i)

        return pointList

    # Funzione per computare l'algoritmo dbscan
    # Ha come paramentri i dati, il raggio e il numero minimo di punti per
    # generare un cluster

    def computedbscan(self, data, Eps, MinPt):

        # Liste vuote
        pointlabel = [self.UNASSIGNED] * len(data)
        pointcount = []
        corepoint = []
        noncore = []
        ListTime = []
        # Loop per contare quanti punti sono vicini
        for i in range(len(data)):
            pointcount.append(self.calculateNearby(data, i, Eps))

        # Loop per verificare se i punti vicini sono più di 3
        # In tal caso li aggiungo alla lista 'corepoint' (cioè il punto corrente è un punto centrale) e setto
        # all'i-esima posizione di pointlabel -1, altrimenti
        # nella lista 'noncore'
        for i in range(len(pointcount)):
            if (len(pointcount[i]) >= MinPt):
                pointlabel[i] = self.core
                corepoint.append(i)
            else:
                noncore.append(i)
        # Loop dei punti 'noncore'
        for i in noncore:
            # Loop dei punti vicini al i-esimo punto 'noncore'
            for j in pointcount[i]:
                # Se il j-esimo punto vicino è presenta nella lista 'corepoint'
                # allora setto all' i-esima posizione di pointlabel -2 (cioè il punto corrente è un punto bordo)
                # pointlabel rappresenta il valore che avrà l'etichetta
                if j in corepoint:
                    pointlabel[i] = self.edge
                    break
        c1 = 1

        for i in range(len(pointlabel)):
            # Genero una coda q
            q = queue.Queue()

            # Se l' i-esima etichetta ha valore -1, quindi il punto è centrale,
            # lo setto uguale a 1 (quindi fa parte del cluster)
            if (pointlabel[i] == self.core):
                pointlabel[i] = c1
                # Loop per ogni i-esimo pointcount
                # Se l'etichetta x ha valore -1 allora lo inserisco nella coda e
                # setto l'etichetta a 1 (quindi il punto fa parte del cluster)
                # Se l'etichetta x ha valore -2 allora setto solament
                # l'etichetta a 1 (quindi il punto fa parte del cluster)
                for x in pointcount[i]:
                    if (pointlabel[x] == self.core):
                        q.put(x)
                        pointlabel[x] = c1
                    elif (pointlabel[x] == self.edge):
                        pointlabel[x] = c1

                # Fin quando la coda non è vuota
                while not q.empty():
                    # Rimuovo e restituisco l'elemento della q
                    neightbors = pointcount[q.get()]

                    # Loop per i punti vicini
                    # Se l'etichetta y ha valore -1 lo setto uguale 1 e lo
                    # inserisco nella coda
                    # Se, invece, ha valore -2 lo setto uguale a 1
                    # (il punto farà parte del cluster)
                    for y in neightbors:
                        if (pointlabel[y] == self.core):
                            pointlabel[y] = c1
                            q.put(y)
                        if (pointlabel[y] == self.edge):
                            pointlabel[y] = c1

                c1 = c1 + 1
        return pointlabel, c1



    def computedbscan2(self, data, Eps, MinPt,time):

        # Liste vuote
        pointlabel = [self.UNASSIGNED] * len(data)
        pointcount = []
        corepoint = []
        noncore = []
        ListTime = []
        # Loop per contare quanti punti sono vicini
        for i in range(len(data)):
            pointcount.append(self.calculateNearby(data, i, Eps))

            ListTime.append(time[i])
        # Loop per verificare se i punti vicini sono più di 3
        # In tal caso li aggiungo alla lista 'corepoint' (cioè il punto corrente è un punto centrale) e setto 
        # all'i-esima posizione di pointlabel -1, altrimenti 
        # nella lista 'noncore'
        for i in range(len(pointcount)):
            if (len(pointcount[i]) >= MinPt):
                pointlabel[i] = self.core
                corepoint.append(i)
            else:
                noncore.append(i)
        # Loop dei punti 'noncore'
        for i in noncore:
            # Loop dei punti vicini al i-esimo punto 'noncore'
            for j in pointcount[i]:
                # Se il j-esimo punto vicino è presenta nella lista 'corepoint'
                # allora setto all' i-esima posizione di pointlabel -2 (cioè il punto corrente è un punto bordo)
                # pointlabel rappresenta il valore che avrà l'etichetta
                if j in corepoint:
                    pointlabel[i] = self.edge
                    break
        c1 = 1

        for i in range(len(pointlabel)):
            # Genero una coda q
            q = queue.Queue()
            
            # Se l' i-esima etichetta ha valore -1, quindi il punto è centrale,
            # lo setto uguale a 1 (quindi fa parte del cluster)
            if (pointlabel[i] == self.core):
                pointlabel[i] = c1
                # Loop per ogni i-esimo pointcount
                # Se l'etichetta x ha valore -1 allora lo inserisco nella coda e
                # setto l'etichetta a 1 (quindi il punto fa parte del cluster)
                # Se l'etichetta x ha valore -2 allora setto solament 
                # l'etichetta a 1 (quindi il punto fa parte del cluster)
                for x in pointcount[i]:
                    if (pointlabel[x] == self.core):
                        q.put(x)
                        pointlabel[x] = c1
                    elif (pointlabel[x] == self.edge):
                        pointlabel[x] = c1
                
                # Fin quando la coda non è vuota
                while not q.empty():
                    # Rimuovo e restituisco l'elemento della q
                    neightbors = pointcount[q.get()]
                    
                    # Loop per i punti vicini
                    # Se l'etichetta y ha valore -1 lo setto uguale 1 e lo
                    # inserisco nella coda
                    # Se, invece, ha valore -2 lo setto uguale a 1
                    # (il punto farà parte del cluster)
                    for y in neightbors:
                        if (pointlabel[y] == self.core):
                            pointlabel[y] = c1
                            q.put(y)
                        if (pointlabel[y] == self.edge):
                            pointlabel[y] = c1
                            
                c1 = c1 + 1
        return pointlabel, c1, ListTime
    
    
    # Funzione che mi restituisce il grafico del numero di cluster trovati
    # Ha come parametri: i dati, le etichette, il numero di cluster,
    # un carattere che corrisponde al numero del video e un numero q
    def plotRes(self, data, clusterRes, clusterNum, q):
        nPoints = len(data)
        scatterColors = ['green', 'blue', 'red', 'orange', 'brown', 'gray','yellow']
        fig, ax = plt.subplots(num='Aoi %d' %q, figsize=(11, 7))
        ax.autoscale(enable=True)
        img = mpimg.imread('image/img'+str(q)+'.png')
        # Utilizzati per moltiplicare gli elementi x e y per la dimensione dell immagine
        width = img.shape[1]
        height = img.shape[0]
        ax.set_aspect('equal')
        for i in range(clusterNum):
            if (i == 0):
                color = 'yellow'
            else:
                color = scatterColors[i % len(scatterColors)]

            x1 = []
            y1 = []
            for j in range(nPoints):
                if clusterRes[j] == i:
                    x1.append(data[j, 0] * width)
                    y1.append(data[j, 1] * height)

            plt.scatter(x1, y1, c=color, alpha=1)
        ax.imshow(img, aspect='auto')
        fig.set_size_inches(11, 6)
        plt.axis('off')
        plt.title('Visualizzazione delle Aree di Interesse\n  ( DBscan Clustering )')  # Titolo del grafico
        fig.savefig('grafic/aoi' + str(q) + '.jpg')  # Creazione del file aoi.jpg
        plt.show()

    # Funzione che esegue il dbScan. Ha come paramtri X, un array, che contiene valori di x e y
    def fit(self, X):
        listOut = []
        #epss indica il raggio che ogni punto avrà
        # minptss indica il numero minimo di punti per generare un cluster
        epss = [3 ]
        minptss = [3]
        
        # Loop per il raggio
        for eps in epss:
            # Loop per il numero minimo di punti
            for minpts in minptss:
                #print('Set eps = ' + str(eps) + ', Minpoints = ' + str(minpts))
                
                # Computo il dbscan e restituisco il numero delle etichette e
                # il numero di cluster (compreso il cluster che contiene le
                # fissazioni scartate
                pointlabel, c1 = self.computedbscan(X, eps, minpts)
                
                #print('number of cluster found: ' + str(c1 - 1))
                cluster = c1-1
                counter = collections.Counter(pointlabel)
                #print(counter)
                outliers = pointlabel.count(0)
                #print('numebers of outliers found: ' + str(outliers) + '\n')

        return cluster, pointlabel

    def fit2(self, X, time):
        listOut = []
        # epss indica il raggio che ogni punto avrà
        # minptss indica il numero minimo di punti per generare un cluster
        epss = [3]
        minptss = [3]

        # Loop per il raggio
        for eps in epss:
            # Loop per il numero minimo di punti
            for minpts in minptss:
                #print('Set eps = ' + str(eps) + ', Minpoints = ' + str(minpts))

                # Computo il dbscan e restituisco il numero delle etichette e
                # il numero di cluster (compreso il cluster che contiene le
                # fissazioni scartate
                pointlabel, c1, listTime = self.computedbscan2(X, eps, minpts, time)

                #print('number of cluster found: ' + str(c1 - 1))
                cluster = c1 - 1
                counter = collections.Counter(pointlabel)
                #print(counter)
                outliers = pointlabel.count(0)
                #print('numebers of outliers found: ' + str(outliers) + '\n')
                for x in range(cluster):
                    listOut.append([])
                    for y in range(len(pointlabel)):
                        if pointlabel[y] == x + 1:
                            listOut[x].append(listTime[y])

        return cluster, pointlabel, listOut
    # Funzione implementata per la riproduzione del grafico
    def getFit(self, data, q):
        epss = [3]
        minptss = [3]
        for eps in epss:
            for minpts in minptss:
                pointlabel, c1 = self.computedbscan(data, eps, minpts)
                self.plotRes(data, pointlabel, c1, q)

    # Funzione che restituisce il numero di cluster trovati
    def getCluster(self, cluster):
        nC = []
        for i in range(0, cluster):
            nC.append(i+1)
        return nC
    
    # Funzione che restituisce il numero di fissazioni presenti nel cluster
    def countFix(self,pointlabel):
        
        numF = []
        c = 0
        count = collections.Counter(pointlabel)
        # Loop per trovare il numero di fissazioni considerando quante etichette ci sono
        for i in range(len(pointlabel)):
            if pointlabel[i] !=0:
                c+= 1

        
        # Se le etichette sono maggiori di 0, quindi esistono punti di fissazione
        # mi trovo la media altrimenti setto la media a 0
        if len(pointlabel) > 0:
            mean = c/len(pointlabel)
        else:
            mean = 0.0
        # Se la media è diverso da 1 e 0.0 aggiungo nella lista nF il numero di fissazioni presenti nel cluster
        # Se la media è uguale a 0.0 aggiungo alla lista nF 0 fissazioni.
        if mean != 1 and mean != 0.0:
            for i in range(1,len(count)):
                numF.append(count[i])
        elif mean == 0.0:
            numF.append(0)
        else:
            numF.append(c)
        return numF

    # Funzione per computare il centro di ogni cluster
    # Ha come parametri i dati , i cluster e i punti delle etichette
    def compute_centroids(self, data, cluster, pointlabel):
        # Lista di nuovi centroidi
        centroids = np.zeros((cluster, data.shape[1]))
        help = []
        for i in range(cluster):

            for j in range(len(pointlabel)):
                if (pointlabel[j] == i + 1):
                    help.append(data[j])
            centroids[i, :] = np.mean(help, axis=0)
            help.clear()
        return centroids

    # Funzione per trovare la distanza media tra i punti
    # Ha come parametri: i dati, i cluster e i punti delle etichette
    def distance_mean_point_to_point(self, data, cluster, pointlabel):
        distances = []
        help = []
        j0 =0
        count = 0
        for i in range(cluster):

            for j in range(1, len(pointlabel)):
                data[j].sort()
                if(pointlabel[j] == i+1):
                    if pointlabel[j0] == i+1:
                        dist = norm(data[j] - data[j0], axis = 0)
                        dist_2 = np.square(dist)
                        help.append(dist_2)
                        count+=1
                    j0 = j
            distance = (np.sum(help, axis=0))/count
            distances.append(distance)
            count = 0
            help.clear()
        return distances

