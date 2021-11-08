import csv
from tkinter import Message
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import PySimpleGUI as sg
from kMean import *
from dbscan import *
from PIL import Image

#Funzione per stampare il file aoi.csv sulla console
def readFileAoi():
    csv_file = 'out/aoi.csv'
    data = pd.read_csv(csv_file)
    print(data)


def readAoiDbscan2(scene):
    df = pd.read_csv('out/fixation.csv')  # Salvo in un dataFrame i dati letti dal file
    X = df.iloc[:, [1, 3, 4]].values  # Salvo nella variabile X i valori che mi servono del dataFrame
    db = DBscan(NOISE=0, UNASSIGNED=0, core=-1, edge=-2)  # Creo un'istanza del dbscan

    time = [element for element in X[:, 0]]
    time2 = []
    smin = 0

    # Nuove liste vuote
    clusterList = []
    centerXList = []
    centerYList = []
    centerList = []
    medList = []
    numFixList = []
    numImgList = []
    stdevXList = []
    stdevYList = []
    ListTimelist = []
    # Loop per ogni scena che è stata trovata
    for z in range(0, len(scene) - 1):
        for t in time:
            if t <= scene[z + 1]:
                time2.append(t)  # Inserisco nella lista 'time2' tutti i valori minori della t-esima scena

        # Prendo i valori x e y da X che rientrano tra il tempo iniziale e il tempo finale
        x = [element for element in X[smin:len(time2), 1]]
        y = [element for element in X[smin:len(time2), 2]]
        time3 = [element for element in X[smin:len(time2),0]]
        help = np.array([x, y])  # Creo un array con i valori x e y
        res = help.transpose()  # e faccio la trasposizione
        c1, pointlabel, listTime = db.fit2(res, time3)  # Eseguo il dbscan
        ListTimelist.append(listTime)
        ops = []
        for i in range(len(ListTimelist)):
            for j in range(len(ListTimelist[i])):
                ops.append(ListTimelist[i][j])

        # Creazione del file aoi.csv
        numImg = []
        numC = db.getCluster(c1)
        center = db.compute_centroids(res, c1, pointlabel)
        centerX = []
        centerY = []
        numF = db.countFix(pointlabel)

        for i in range(len(numC)):
            numImg.append(z + 1)

        for i in range(len(center)):
            centerX.append(center[i][0])
            centerY.append(center[i][1])

        valX = []
        valY = []
        stdevX = []
        stdevY = []
        for i in range(len(numC)):
            for j in range(1, len(pointlabel)):
                if (pointlabel[j] == i + 1):
                    valX.append(res[j][0])
                    valY.append(res[j][1])
            x1 = np.std(valX)
            stdevX.append(x1)
            y1 = np.std(valY)
            stdevY.append(y1)
            valX.clear()
            valY.clear()

        # Creo liste annidate
        distPoint = db.distance_mean_point_to_point(res, c1, pointlabel)
        centerList.append(center)
        clusterList.append(numC)
        centerXList.append(centerX)
        centerYList.append(centerY)
        medList.append(distPoint)
        numFixList.append(numF)
        numImgList.append(numImg)
        stdevXList.append(stdevX)
        stdevYList.append(stdevY)

        # Svuoto le liste, e assegno il nuovo valore iniziale 'smin' per ogni valore x e y

        diff = len(time2) - smin
        smin = smin + diff
        x.clear()
        y.clear()
        time2.clear()

    # Trasformo le liste annidate in liste semplici
    nC1 = []
    for i in range(len(clusterList)):
        if i != None:
            for j in range(len(clusterList[i])):
                nC1.append(clusterList[i][j])

    nCX = []
    for i in range(len(centerXList)):
        if i != None:
            for j in range(len(centerXList[i])):
                nCX.append(centerXList[i][j])

    nCY = []
    for i in range(len(centerYList)):
        if i != None:
            for j in range(len(centerYList[i])):
                nCY.append(centerYList[i][j])

    m1 = []
    for i in range(len(medList)):
        if i != None:
            for j in range(len(medList[i])):
                m1.append(medList[i][j])

    nF1 = []
    for i in range(len(numFixList)):
        if numFixList[i] != [0]:
            for j in range(len(numFixList[i])):
                nF1.append(numFixList[i][j])
    nImg1 = []
    for i in range(len(numImgList)):
        if i != None:
            for j in range(len(numImgList[i])):
                nImg1.append(numImgList[i][j])

    sX = []
    for i in range(len(stdevXList)):
        if i != None:
            for j in range(len(stdevXList[i])):
                sX.append(stdevXList[i][j])

    sY = []
    for i in range(len(stdevYList)):
        if i != None:
            for j in range(len(stdevYList[i])):
                sY.append(stdevYList[i][j])

    fields = ['n_img', 'n_cluster', 'n_fixation', 'centerPointX', 'centerPointY', 'distMeanPoint', 'stdevX', 'stdevY']
    with open('out/aoi.csv', 'w', newline="") as cvs:
        w = csv.DictWriter(cvs, fieldnames=fields)
        w.writeheader()

        for nI, nC, nF, cX, cY, med, sX, sY in zip(nImg1, nC1, nF1, nCX, nCY, m1, sX, sY):
            d = {'n_img': nI, 'n_cluster': nC, 'n_fixation': nF, 'centerPointX': cX, 'centerPointY': cY,
                 'distMeanPoint': med,
                 'stdevX': sX, 'stdevY': sY}
            w.writerow(d)
    cvs.close()
    return ops


#Funzione per leggere il file fixation.csv ed eseguire il dbscan
def readAoiDbscan(scene):
    df = pd.read_csv('out/fixation.csv')                            # Salvo in un dataFrame i dati letti dal file
    X = df.iloc[: , [1,3,4]].values                                 # Salvo nella variabile X i valori che mi servono del dataFrame
    db = DBscan(NOISE = 0, UNASSIGNED = 0, core=-1, edge = -2)      # Creo un'istanza del dbscan

    
    time = [element for element in X[:, 0]]
    time2 = []
    smin = 0

    # Nuove liste vuote
    clusterList = []
    centerXList = []
    centerYList = []
    centerList = []
    medList = []
    numFixList = []
    numImgList = []
    stdevXList = []
    stdevYList = []

    # Loop per ogni scena che è stata trovata
    for z in range(0,len(scene)-1):
        for t in time:
            if t<=scene[z+1]:
                time2.append(t)                                 # Inserisco nella lista 'time2' tutti i valori minori della t-esima scena

        # Prendo i valori x e y da X che rientrano tra il tempo iniziale e il tempo finale
        x = [element for element in X[smin:len(time2), 1]]
        y = [element for element in X[smin:len(time2), 2]]
        #time3 = [element for element in X[smin:len(time2),0]]
        help = np.array([x,y])                                  # Creo un array con i valori x e y
        res = help.transpose()                                  # e faccio la trasposizione
        c1, pointlabel = db.fit(res)                            # Eseguo il dbscan


        #Creazione del file aoi.csv
        numImg = []
        numC = db.getCluster(c1)
        center = db.compute_centroids(res,c1, pointlabel)
        centerX = []
        centerY = []
        numF = db.countFix(pointlabel)

        for i in range(len(numC)):
            numImg.append(z+1)

        for i in range(len(center)):
            centerX.append(center[i][0])
            centerY.append(center[i][1])

        valX = []
        valY = []
        stdevX = []
        stdevY = []
        for i in range(len(numC)):
            for j in range(1, len(pointlabel)):
                if (pointlabel[j] == i + 1):
                    valX.append(res[j][0])
                    valY.append(res[j][1])
            x1 = np.std(valX)
            stdevX.append(x1)
            y1 = np.std(valY)
            stdevY.append(y1)
            valX.clear()
            valY.clear()

        # Creo liste annidate
        distPoint = db.distance_mean_point_to_point(res, c1, pointlabel)
        centerList.append(center)
        clusterList.append(numC)
        centerXList.append(centerX)
        centerYList.append(centerY)
        medList.append(distPoint)
        numFixList.append(numF)
        numImgList.append(numImg)
        stdevXList.append(stdevX)
        stdevYList.append(stdevY)

        #Svuoto le liste, e assegno il nuovo valore iniziale 'smin' per ogni valore x e y
        
        diff = len(time2) - smin
        smin = smin + diff
        x.clear()
        y.clear()
        time2.clear()

    # Trasformo le liste annidate in liste semplici
    nC1 = []
    for i in range(len(clusterList)):
        if i != None:
            for j in range(len(clusterList[i])):
                nC1.append(clusterList[i][j])

    nCX = []
    for i in range(len(centerXList)):
        if i != None:
            for j in range(len(centerXList[i])):
                nCX.append(centerXList[i][j])

    nCY = []
    for i in range(len(centerYList)):
        if i != None:
            for j in range(len(centerYList[i])):
                nCY.append(centerYList[i][j])

    m1 = []
    for i in range(len(medList)):
        if i != None:
            for j in range(len(medList[i])):
                m1.append(medList[i][j])

    nF1 = []
    for i in range(len(numFixList)):
        if numFixList[i] != [0]:
            for j in range(len(numFixList[i])):
                nF1.append(numFixList[i][j])
    nImg1 = []
    for i in range(len(numImgList)):
        if i != None:
            for j in range(len(numImgList[i])):
                nImg1.append(numImgList[i][j])

    sX = []
    for i in range(len(stdevXList)):
        if i != None:
            for j in range(len(stdevXList[i])):
                sX.append(stdevXList[i][j])

    sY = []
    for i in range(len(stdevYList)):
        if i != None:
            for j in range(len(stdevYList[i])):
                sY.append(stdevYList[i][j])

    fields = ['n_img','n_cluster', 'n_fixation', 'centerPointX', 'centerPointY', 'distMeanPoint','stdevX', 'stdevY']
    with open('out/aoi.csv', 'w', newline= "") as cvs:
        w = csv.DictWriter(cvs, fieldnames=fields)
        w.writeheader()

        for nI, nC, nF, cX, cY, med, sX, sY in zip(nImg1,nC1, nF1, nCX, nCY, m1, sX, sY):
            d = {'n_img': nI,'n_cluster': nC, 'n_fixation': nF, 'centerPointX': cX, 'centerPointY': cY, 'distMeanPoint': med,
                 'stdevX':sX, 'stdevY':sY}
            w.writerow(d)

    graficAoiDB(scene)
    readFileAoi()
    cvs.close()  # chiusura del file aoi.csv


# Funzione che mi restituisce, salva e visualizza il grafico delle aoi per l'algoritmo dbscan
def graficAoiDB(scene):
    df = pd.read_csv('out/fixation.csv')                        # Lettura del file e salvataggio nel dataFrame df
    X = df.iloc[:, [1, 3, 4]].values                            # Salvo in X i valori del dataFrame che mi servono
    db = DBscan(NOISE=0, UNASSIGNED=0, core=-1, edge=-2)        # Creo istanza di dbscan

    time = [element for element in X[:, 0]]
    time2 = []
    smin = 0
    w = 0

    # Loop per ogni scena, quindi per ogni immagine trovata
    for q in range(0, len(scene)-1):
        for t in time:
            if t <= scene[q+1]:
                time2.append(t)
        x = [element for element in X[smin:len(time2),1]]
        y = [element for element in X[smin:len(time2),2]]
        help = np.array([x,y])
        res = help.transpose()
        db.getFit(res, w)
        w += 1
        diff = len(time2) - smin
        smin = smin + diff
        x.clear()
        y.clear()
        time2.clear()

# Funzione per leggere i dati di fixation.csv ed eseguire il k-means clustening.
# Esso restituira il file aoi.csv e mostrera le/a scene/a per visualizzare i clustening trovati.

def readAoiKmeans(scene,k):
    df = pd.read_csv('out/fixation.csv')                # DataFrame del file .csv
    km = Kmeans(n_clusters=k, max_iter=100)             # Istanza di K-means
    X = df.iloc[:, [1,3,4]].values                      # Valori  del dataFrame
    time = [element for element in X[:, 0]]
    time2 = []
    smin = 0
    # Liste vuote
    clusterList = []
    centerXList = []
    centerYList = []
    centerList = []
    medList = []
    numFixList = []
    numImgList = []
    stdevXList = []
    stdevYList = []
    # Loop per ogni scena.
    # Genero le liste x e y aventi i valori compresi tra il tempo minimo e il tempo massimo di ogni scena.
    for z in range(0,len(scene)-1):
        for t in time:
            if t<=scene[z+1]:
                time2.append(t)

        x = [element for element in X[smin:len(time2),1]]
        y = [element for element in X[smin:len(time2),2]]
        
        # Se le liste sono vuote o comprendono meno di 3 valori. Essi verranno scartati perchè non
        # posso generare k cluster. Altrimenti eseguo il k-means clustening
        if x == [] or len(x)<k:
            diff = len(time2) - smin
            smin = smin + diff
            x.clear()
            y.clear()
            time2.clear()
        else:

            help = np.array([x,y])
            res = help.transpose()
            km.fit(res)
            centroids = km.centroids

            #Creazione del file aoi.csv
            numImg = []
            numC = []
            centroidX = []
            centroidY = []
            numF = km.countFix(len(centroids),km.labels)
            valX = []
            valY = []
            stdevX = []
            stdevY = []
            for i in range(km.n_clusters):
                for j in range(len(km.labels)):
                    if (km.labels[j] == i):
                        valX.append(res[j][0])
                        valY.append(res[j][1])
                x1 = np.std(valX)
                stdevX.append(x1)
                y1 = np.std(valY)
                stdevY.append(y1)
                valX.clear()
                valY.clear()

            for i in range(km.getCluster()):
                numImg.append(z+1)
            for i in range(km.getCluster()):
                numC.append(i+1)
            for i in range(len(centroids)):
                centroidX.append(centroids[i][0])
                centroidY.append(centroids[i][1])
            med = km.getMeanDist(res, km.labels, km.centroids)

            # Creo liste annidate
            centerList.append(centroids)
            clusterList.append(numC)
            centerXList.append(centroidX)
            centerYList.append(centroidY)
            medList.append(med)
            numFixList.append(numF)
            numImgList.append(numImg)
            stdevXList.append(stdevX)
            stdevYList.append(stdevY)

            # Svuoto le liste e calcolo smin che sarà il tempo iniziale per ogni nuova lista x e y
            diff = len(time2) - smin
            smin = smin + diff
            x.clear()
            y.clear()
            time2.clear()


    # Trasformo le liste annidate in liste semplici
    nC1 = []
    for i in range(len(clusterList)):
        for j in range(0,k):
            nC1.append(clusterList[i][j])
    nCX = []
    for i in range(len(centerXList)):
        for j in range(0,k):
            nCX.append(centerXList[i][j])
    nCY = []
    for i in range(len(centerYList)):
        for j in range(0,k):
            nCY.append(centerYList[i][j])
    m1 = []
    for i in range(len(medList)):
        for j in range(0,k):
            m1.append(medList[i][j])
    nF1 = []
    for i in range(len(numFixList)):
        for j in range(0,k):
            nF1.append(numFixList[i][j])
    nImg1 = []
    for i in range(len(numImgList)):
        for j in range(0,k):
            nImg1.append(numImgList[i][j])

    sX = []
    for i in range(len(stdevXList)):
        for j in range(0,k):
            sX.append(stdevXList[i][j])

    sY = []
    for i in range(len(stdevYList)):
        for j in range(0,k):
            sY.append(stdevYList[i][j])

    fields = ['n_img','n_cluster', 'n_fixation', 'centroX', 'centroY', 'mediaDistCentro','stdevX','stdevY']

    with open('out/aoi.csv', 'w', newline= "") as cvs:
        w = csv.DictWriter(cvs, fieldnames=fields)
        w.writeheader()

        for nI, nC, nF, cX, cY, med, sX, sY in zip(nImg1,nC1, nF1, nCX, nCY, m1, sX, sY):
            d = {'n_img': nI,'n_cluster': nC, 'n_fixation': nF, 'centroX': cX, 'centroY': cY, 'mediaDistCentro': med,
                 'stdevX': sX, 'stdevY': sY}
            w.writerow(d)

    readFileAoi()
    cvs.close()  # chiusura del file aoi.csv
    print(centerList)
    graficAoiKmeans(scene, centerList,k)
# Funzione per la visualizzazione grafica dei dati del file aoi.csv
def graficAoiKmeans(scene, centerList,k):

    # Lettura del file fixation.csv e esecuzione del k-means clustening
    df = pd.read_csv('out/fixation.csv')
    km = Kmeans(n_clusters=k, max_iter=100)
    X = df.iloc[:, [1, 3, 4]].values

    s=1
    time = [element for element in X[:, 0]]
    time2 = []
    smin = 0
    w=0
    
    # Loop per ogni scena
    # Mi serve per prendere l'immagine di ogni scena
    for q in range(0, len(scene)-1):
        img = mpimg.imread('image/img'+str(q)+'.png')
        width = img.shape[1]
        height = img.shape[0]

        for t in time:
            if t <= scene[s]:
                time2.append(t)
        
        # Genero liste a e y aventi valori compresi tra il tempo iniziale e tempo finale della q-esima scena
        x = [element for element in X[smin:len(time2),1]]
        y = [element for element in X[smin:len(time2),2]]
        
        # Se le liste hanno meno di 3 valori, non posso eseguire l'algoritmo.
        # Restituisco l'immagine con le fissazioni presenti ma che non fanno parte di un aoi
        # Altrimenti eseguo il k-means
        if x == [] or len(x)<k:
            fig, ax = plt.subplots(num='Aoi %d' %q,figsize=(16, 12))
            plt.imshow(img)
            for i in range(len(x)):
                plt.scatter((x[i]*width), (y[i]*height), c = 'yellow')
            s += 1
            diff = len(time2) - smin
            smin = smin + diff
            x.clear()
            y.clear()
            time2.clear()
            fig.set_size_inches(11, 6)
            fig.savefig('grafic/aoi' + str(w) + '.jpg')  # Creazione del file aoi.jpg
            plt.show()
        else:
            help = np.array([x,y])
            res = help.transpose()
            km.getFit(res,centerList[w])
            centroids = km.centroids
            colmap = {0:'green', 1:'blue',2:'red', 3:'orange', 4:'indigo', 5:'magenta', 6:'pink', 7:'grey'}
            fig, ax = plt.subplots(num='Aoi %d' %q, figsize = (16,12))
            plt.imshow(img)
            # Visualizzo i cerchi per ogni valore x e y dell'array X di tutte le fissazioni presenti nel primo cluster
            for i in range(len(centroids)):
                plt.scatter(res[km.labels == i,0] * width, res[km.labels == i,1] * height,
                            c=colmap[i], label='cluster %d'%(i+1))
            # Visualizzo i cerchi per ogni valore x e y dell'array X di tutte le fissazioni presenti nel secondo cluster
            #plt.scatter(res[km.labels == 1, 0] * width, res[km.labels == 1, 1] * height,
            #            c='blue', label='cluster 2')

            # Visualizzo i cerchi per ogni valore x e y dell'array X di tutte le fissazioni presenti nel terzo cluster
            #plt.scatter(res[km.labels == 2, 0] * width, res[km.labels == 2, 1] * height,
            #            c='red', label='cluster 3')


            # Loop per visualizzare i centroidi
            for i in range(len(centroids)):
                plt.scatter(centroids[i][0] * width, centroids[i][1] * height, marker='*', s=50,
                            c=colmap[i], label='centroid')

            plt.legend()  # Legenda della grafico
            plt.xlim([0, width])  # Scala dell'asse x
            plt.ylim([height, 0])  # Scala dell'asse y

            plt.xlabel('Posizione X')  # Nome dell'asse x
            plt.ylabel('Posizione Y')  # Nome dell'asse y
            plt.axis('off')
            plt.title('Visualizzazione delle Aree di Interesse\n  ( K-Means Clustering )')  # Titolo del grafico
            ax.set_aspect('equal')
            fig.set_size_inches(11,6)

            fig.savefig('grafic/aoi'+str(w)+'.jpg')  # Creazione del file aoi.jpg
            plt.show()  # Visualizzo il grafico
            w+= 1

            s += 1
            diff = len(time2) - smin
            smin = smin + diff
            x.clear()
            y.clear()
            time2.clear()

# Funzione utilizzata per scegliere il tipo di algoritmo che si vuole eseguire per trovare le Aoi
def chooseAlgo(scene,choose):
    while True:

        if choose == str(1):
            k = sg.popup_get_text(title="AOI",message='''
                Esecuzione del K-means
                Verranno mostrate le immagini acquisite dal video scelto. Saranno sovraimpresse le aree di interesse
                delle fissazioni catturate negli intervalli di tempo di ogni cambio scena. E' possibile che vengano mostrate immagini senza aree di interesse e di conseguenza
                fissazioni di colore giallo o senza fissazioni, ciò significherà che l'algoritmo non è stato eseguito in quanto il
                numero di fissazioni sono insufficienti. Il numero minimo di fissazioni per eseguire l'algoritmo è uguale al numero di cluster richiesti.\n
                Quanti cluster vuoi generare:''')
            
            readAoiKmeans(scene,int(k))
            
        elif choose == str(2):
            print('''
                Esecuzione del DBscan
                Verranno mostrate le immagini acquisite dal video scelto. Saranno sovraimpresse le aree di interesse
                delle fissazioni catturate negli intervalli di tempo di ogni cambio scena. E' possibile che vengano mostrate immagini senza aree di interesse e di conseguenza
                fissazioni di colore giallo o senza fissazioni. Il numero minimo di punti (fissazioni) e il raggio di ogni fissazione per creare un area di interesse
                è 3.''')
    
            readAoiDbscan(scene)
            imgConv = Image.open(r'grafic/aoi0.jpg')
            imgConv.save(r'grafic/aoi0.png')
            event, values = sg.Window('Dettagli grafico AOI', [[sg.Image(filename='grafic/aoi0.png')]]).read(close=True)
            break

        elif choose == str(3):
            break
        else:
            print("Numero o parola inserita non valida. ")
    return choose
