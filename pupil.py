#Informazioni:
#Dimensioni medie pupille occhio destro e sinistro combinati
#Dimensioni medie pupilla occhio destro totale
#Dimensioni medie pupilla occhio sinistro totale
#Dimenesione medie occhio destro e sinistro totale
#Dimensione massima occhio sinistro e occhio destro
#Dimensione minima occhio sinistro e occhio destro
#Cacolo Velocità media dilatazione

#Dimensioni medie pupille occhio destro e sinistro combinati
def averageLeftAndRight(diameterLF,diameterRG):
    average = (diameterLF + diameterRG)/2
    return average

#Dimensioni medie pupilla occhio sinistro totale
#Dimensioni medie pupilla occhio destro totale
def averangeTotal(diameterEye):
    return sum(diameterEye)/len(diameterEye)
   
#Dimenesione medie occhio destro e sinistro totale
def averangeLFRGTotal(averageTotalLF,averageTotalLFRG):
    average = (averageTotalLF+averageTotalLFRG)/2
    return average


#Dimensione massima occhio sinistro e occhio destro
#Dimensione minima occhio sinistro e occhio destro
def minmaxLeftAndRight(diameterLF,diameterRG):
    minDiameterLF = min([value for value in diameterLF if value!=0])
    minDiameterRG = min([value for value in diameterRG if value!=0])
    maxDiameterLF = max(diameterLF)
    maxDiameterRG = max(diameterRG)

    return minDiameterLF,minDiameterRG,maxDiameterLF,maxDiameterRG


#Cacolo Velocità media dilatazione
def avgDilatationSpeed(initialDil,finalDil,initialT,finalT):
    return (finalDil-initialDil)/(finalT-initialT)
