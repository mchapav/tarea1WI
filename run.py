#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import sample


# Funcion que permite recuperar una cantidad determinada de nodos alrededor de un grupo de nodos.
def get_nodes_at_distance(G, L, level, leng):
    A = []
    A.append(list(L))
    for i in range(level):
        largo = len(A[i])
        A.append([])
        for x in range(largo):
            a = G.successors(A[i][x])
            b = G.predecessors(A[i][x])
            for y in b:
                A[i+1].append(y)
            for y in b:
                A[i+1].append(y)
        A[i] = sample(A[i],min(len(A[i]),leng[i]))
    r = []
    for i in range(level):
        r = r + A[i]
    return r


##########################################
# Abrir archivos
##########################################

relation = pd.read_csv("data/relation5.csv", sep = ";") #user_id , rel


#Se utilizan 5000 filas del archivo, por motivos computacionales
relation = relation.sample(n=5000)



##########################################
# Agregar Nodos
##########################################
G= nx.DiGraph()
Cantidad_Seguidores = {}
print("Archivo leido")
for index, row in relation.iterrows():
    x = int(row["user_id"])
    if(not G.has_node(x)):
        G.add_node(x)
        Cantidad_Seguidores[x]= 0


print("Nodos creados")


i = 0
###############################################################
# Agregar arcos
###############################################################
# Por cada nodo fila del archivo se agregan las relaciones y se agregan los nodos que faltan
for index, row in relation.iterrows():
    if isinstance(row["rel"],str):
        rels = row["rel"].split(" ")
        for x in rels:
            i+=1
            x = int(x)
            # Si existe el nodo en la cantidad de seguidores se le suma 1
            if (x in Cantidad_Seguidores):
                Cantidad_Seguidores[x] = Cantidad_Seguidores[x] + 1
            #Sino, se crea el elemento del diccionario con un valor inicial de 1
            else:
                Cantidad_Seguidores[x] = 1
            # Si ya existe el nodo, solo se agrega la relacion
            if(G.has_node(x)):
                G.add_edge(row["user_id"],x)
            # Si no existe el nodo, se agrega el nodo y la relacion
            else:
                G.add_node(x)
                G.add_edge(row["user_id"],x)
            # Cada 10000 arcos agregados se imprime.
            if ( i%10000 == 0 or i == 1):
                print("Se han agregado %s arcos" %(i))


N_NODOS = len(G.nodes())
print("Grafo listo, %s arcos y %s nodos agregados."%(i,N_NODOS))

##########################################
# Calcular PageRank
##########################################
#Se calcula el pagerank
pr = nx.pagerank(G, alpha = 0.9)

# Se ordenan las "keys" por valor del pagerank en orden decreciente y se capturan las 20 primeras
srt = sorted(pr, key=pr.get, reverse=True)[:20]




# Se ordenan las "keys" por valor del pagerank en orden creciente y se capturan las 20 primeras
sr = sorted(pr, key=pr.get, reverse=False)[:20]





##########################################
# Dibujar nodos alrededor de mejor pagerank
##########################################

#Se encuentran los nodos a distancia menor que 3 del usuario con mayor pagerank. Se samplea 1 de distancia 0, 20 de distancia 1 y 400 de distancia 2.
L =get_nodes_at_distance(G,srt[0:3],3, [3,40,1600])


#Se imprime el grafico solo mostrando dichos nodos
#nx.draw(G.subgraph(L))
#plt.show()



##########################################
# Comparación entre PageRank y Seguidores
##########################################

PRL =[]
SEGUIDORESL =[]
# Se ordenan de forma decreciente por pagerank
a = sorted(pr, key=pr.get, reverse=True)
for node in a:
    #Se agrega a la lista el pagerank y su cantidad de seguidores
    PRL.append(pr[node])
    SEGUIDORESL.append(Cantidad_Seguidores[node])


#Se transforman en arrays
nprl = np.array(PRL)
nsegl = np.array(SEGUIDORESL)

# Se encuentra una regresión lineal entre ambos
fit = np.polyfit(nprl, nsegl, 1)


# Se hace un scatterplot entre ambos valores
#plt.scatter(nprl, nsegl)
# Se plotea la linea del LM_fit
#plt.plot(nprl, fit[0]*nprl + fit[1], 'r-')
# Se definen ejes
#plt.axis([0, max(PRL)*1.05, 0, max(SEGUIDORESL)*1.05])

print("Los parametros ax+b de la regresión son:\n a: %s y b:%s" %(fit[0],fit[1]))
#plt.show()

###############################################################
# Diccionarios usuario con nombre, tweets, rtweets y menciones
###############################################################
tweets = pd.read_csv("data/tweets5.csv", sep = ";") #id	twitter_id	user_id	text
users = pd.read_csv("data/users5.csv", sep = ";") #twitter_id	name	screename	description	followerscount	createdat

# Número de tweets en el juego de datos.
# Número de retweets promedio.
# Respuestas y menciones.

class Usuarios():
    def __init__(self,id ,screename=""):
        self.id = id #Guarda el id
        self.user = "@"+screename #Guarda el nombre de usuario de twitter asociado al ID usuario
        self.ntwt = 0 #Guarda la cantidad de tweets asociados al ID usuario
        self.nrt = 0  #Guarda la cantidad de rtweets asociados al ID usuario
        self.nment = 0 #Guarda la cantidad de menciones asociados al ID usuario

Users = {}
screenameToId = {}

for index, row in users.iterrows():
    x = int(row["twitter_id"])
    screename = row["screename"]
    Users[x]= Usuarios(id= x, screename = screename)
    screenameToId[screename]=x


for index, row in tweets.iterrows():
    key = int(row["user_id"])
    if (not key in Users):
        Users[key]= Usuarios(id = key)
    user = Users[key]
    user.ntwt+= 1
    text = row["text"].split()
    if text[0] == "rt":
        screename =text[1][1:-1]
        try:
            Users[screenameToId[screename]].nrt += 1
        except:
            pass
    for word in text[2:]:
        if word[0]=="@":
            screename= word[1:]
            try:
                Users[screenameToId[screename]].nment +=1
            except:
                pass


###############################################################
# Se guardan metricas
###############################################################
with open("users.csv",'w') as file:
    file.write(";ID;SCREENAME;NTWT;NRT;NMENT\n")
    for key in Users:
        usuario = Users[key]
        file.write(";%s;%s;%s;%s;%s\n" % (usuario.id,usuario.user,usuario.ntwt,usuario.nrt,usuario.nment))




###############################################################
# Se imprimen PageRanks
###############################################################

# Se imprimen los 20 mayores pageranks
i = 1
for a in srt:
    try:
        screename = str(Users[a].user)
    except:
        screename = "NN"
    print("#%s. %s -> %s. Con %s seguidores. S_Name:%s" % (i, a, pr[a], Cantidad_Seguidores[a],screename))
    i+=1


# Se imprimen los ultimos 20 pageranks
i = 0
for a in sr:
    try:
        screename = str(Users[a].user)
    except:
        screename = "NN"
    print("#%s. %s -> %s. Con %s seguidores. S_Name:%s" % (N_NODOS - i, a, pr[a], Cantidad_Seguidores[a],screename))
    i+=1
