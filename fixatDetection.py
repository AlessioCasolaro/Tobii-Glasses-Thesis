# This file is part of PyGaze - the open-source toolbox for eye tracking
# Funzione per creare le fissazioni, ha come parametri: valori x, valori y, valori z,
# tempo, distanza Massima e durata minim di ogni fissazione
def fixation(positionX, positionY, positionZ, time, maxDist=0.10, mindur=0.2):

    Sfix = []  # Lista di inizio fissazione
    Efix = []  # Lista di fine fissazione


    # Loop di tutte le coordinate di x e y
    si = 0
    fixStart = False
    count = 0
    numFix = 0
    for i in range(1, len(positionX)):
        # Controllo il valore i-esimo di x
        if positionX[i] != 0:


            # Calcolo della distanza quadratica della prima coordinata x e y con la successiva
            quadr_dist = ((positionX[si] - positionX[i]) ** 2 + (positionY[si] - positionY[i]) ** 2)
            dist = 0.0  # distanza iniziale della fissazione

            if quadr_dist > 0:
                dist = quadr_dist ** 0.5

            # Controllo se la distanza è minore della distanza massima
            if dist <= maxDist and not fixStart:
                # inizia nuova fissazione
                si = 0 + i
                fixStart = True
                Sfix.append([time[i]])
            # Controllo se la distanza è maggiore della distanza massima
            elif dist > maxDist and fixStart:
                # Termino la fissazione corrente
                fixStart = False
                si = 0 + i

                # Memorizzo la fissazione corrente solo se la durata minima è corretta
                if time[i - 1] - Sfix[-1][0] >= mindur:
                    # NUMERO DI FISSAZIONI, TEMPO DI INIZIO, DURATA, POSIZIONE X, POSIZIONE Y, POSIZIONE Z
                    # Aggiungo alla lista Efix il numero di fissazioni, tempo iniziale, la durata,
                    # valore x, valore y e valore z
                    numFix += 1
                    Efix.append([numFix, Sfix[-1][0], time[i - 1] - Sfix[-1][0], positionX[si], positionY[si],
                                 positionZ[si]])
                    count += 1
                # Elimino la la fissazione iniziale altrimenti
                else:
                    Sfix.pop(-1)
                si = 0 + i

            elif not fixStart:
                si += 1

    return Efix
