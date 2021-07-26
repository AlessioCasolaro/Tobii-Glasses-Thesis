import numpy as np
from numpy.linalg import norm

# Implementazione della classe Kmean
class Kmeans:

    # Costrutto della classe, ha come parametri il numero scelto di cluster, massimo numero di iterazioni
    # e
    def __init__(self, n_clusters, max_iter = 100, random_state=123):
        self.n_clusters = n_clusters                        # Numero di cluster
        self.max_iter = max_iter                            # Numero massimo di iterazioni
        self.random_state = random_state

    # Funzione per inizializzare i centroidi, ha come parametro i valori x e y di ogni fissazione.
    # Creo tot centroidi quanti sono i cluster e
    # assegno in modo random le coordinate x e y di ogni centroide
    def initializ_centroids(self, X):
        np.random.RandomState(self.random_state)
        random_idx = np.random.permutation(X.shape[0])
        centroids = X[random_idx[:self.n_clusters]]
        return centroids

    # Funzione per computare i centroidi, ha come parametri i valori x e y di ogni fissazione e le etichette
    # che corrispondono al numero di cluster.
    # Restituisco un array di nuovi centroidi
    def compute_centroids(self, X, labels):
        # Lista di nuovi centroidi
        centroids = np.zeros((self.n_clusters, X.shape[1]))
        # Loop per il numero di cluster
        for k in range(self.n_clusters):
            # Media aritmetica dei valori X per ogni etichetta lungo l'asse x
            centroids[k, :] = np.mean(X[labels == k, :], axis=0)
        return centroids

    # Funzione che prende in input X: valori x e y; e i centroidi
    # Restituisco la distanza di ogni valore X per ogni centroide
    def compute_distance(self, X, centroids):
        # Inizializzo un array con dimensione 0
        distance = np.zeros((X.shape[0], self.n_clusters))
        # Loop per ogni numero di cluster
        for k in range(self.n_clusters):
            # row_norm è una matrice i cui elementi sono le distanze tra il valore X con i centroidi lungo l'asse y
            row_norm = norm(X - centroids[k, :], axis =1)

            #distance è il quadrato dei termini row_norm
            distance[:, k] = np.square(row_norm)
        return distance

    # Funzione che restituisce l'argomento minimo dell' array distance
    def find_closest_cluster(self, distance):
        return np.argmin(distance, axis=1)

    # Funzione per prendere il k-means clustening una volta computato
    def getFit(self, X, centroids):
        self.centroids = centroids
        for i in range(self.max_iter):
            distance = self.compute_distance(X,centroids)
            self.labels = self.find_closest_cluster(distance)


    # Funzione per computare k-means clustening
    def fit(self, X):

        #Inizializzo i centroidi
        self.centroids = self.initializ_centroids(X)
        
        # Loop per computare i centroidi per max iterazioni
        for i in range(self.max_iter):

            old_centroids = self.centroids                              # Salvo in una variabile temporale i centroidi
            distance = self.compute_distance(X,old_centroids)           # Computo le distanze dei valori X per ogni centroide

            self.labels = self.find_closest_cluster(distance)           # Assegno la distanza minima ad una etichetta
            
            self.centroids = self.compute_centroids(X,self.labels)      # Computo i centroidi per le etichette restituendo nuovi centroidi

            # Confronto i vecchi centroidi con i nuovi, se sono uguali allora termino il ciclo perche ho trovato
            # i centroidi per ogni cluster
            if np.all(old_centroids == self.centroids):
                break

    # Funzione che restituisce il numero di cluster
    def getCluster(self):
        cluster = self.n_clusters
        return cluster

    # Funzione che restituisce i centroidi
    def getCentroid(self):
        centroide = self.centroids
        return centroide

    # Funzione che restituisce il numero di fissazioni per ogni etichetta
    def countFix(self,centroids, labels):
        
        nF = []
        count = 0
        for j in range(centroids):

            for i in labels:
                if i == j:
                    count+=1
            nF.append(count)
            count=0

        return nF




    # Funzione che restituisce la distanza media di ogni fissazione dal suo centroide
    def getMeanDist(self,X, labels, centroids):
        distance = np.zeros(X.shape[0])
        
        count = self.countFix(len(centroids),labels)
        
        med = []
        s = []
        m = []
        for k in range(self.n_clusters):
            s.append([])
            m.append([])
            distance[labels == k] = norm(X[labels == k] - centroids[k], axis =1)

            s[k] = np.sum(distance[labels == k])

            m[k]= s[k] /count[k]
            med.append(m[k])
        return med