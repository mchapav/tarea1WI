#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import sample

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
    r = []
    for i in range(level):
        r = r + sample(A[i],min(len(A[i]),leng[i]))
    return r


##########################################
# Abrir archivos
##########################################

relation = pd.read_csv("data/relation5.csv", sep = ";") #user_id , rel

relation = relation.sample(n=5000)



##########################################
# Crear Grafo
##########################################
G= nx.DiGraph()
D = {}
print("Archivo leido")
for index, row in relation.iterrows():
    x = int(row["user_id"])
    if(not G.has_node(x)):
        G.add_node(x)
        D[x]= 0


print("Nodos creados")


i = 0

for index, row in relation.iterrows():
    if isinstance(row["rel"],str):
        rels = row["rel"].split(" ")
        for x in rels:
            i+=1
            x = int(x)
            if (x in D):
                D[x] = D[x] + 1
            else:
                D[x] = 1
            if(G.has_node(x)):
                G.add_edge(row["user_id"],x)
            else:
                G.add_node(x)
                G.add_edge(row["user_id"],x)
            if ( i%10000 == 0 or i == 1):
                print("Se han agregado %s arcos" %(i))

N_NODOS = len(G.nodes())
print("Grafo listo, %s arcos y %s nodos agregados."%(i,N_NODOS))

##########################################
# Calcular PageRank
##########################################
pr = nx.pagerank(G, alpha = 0.9)

srt = sorted(pr, key=pr.get, reverse=True)[:20]

i = 1
for a in srt:
    print("#%s. %s -> %s. Con %s seguidores." % (i,a,pr[a],D[a]))
    i+=1

sr = sorted(pr, key=pr.get, reverse=False)[:20]

i = 0
for a in sr:
    print("#%s. %s -> %s. Con %s seguidores." % (N_NODOS-i,a,pr[a],D[a]))
    i+=1



##########################################
# Dibujar nodos alrededor de mejor pagerank
##########################################
L =get_nodes_at_distance(G,srt[0:1],3, [1,20,400])

#nx.draw(G.subgraph(L))
#plt.show()

PRL =[]
SEGUIDORESL =[]
a = sorted(pr, key=pr.get, reverse=True)
for node in a:
    PRL.append(pr[node]*1000)
    SEGUIDORESL.append(D[node])

nprl = np.array(PRL)
nsegl = np.array(SEGUIDORESL)

fit = np.polyfit(nprl, nsegl, 1)

plt.scatter(nprl, nsegl)
plt.plot(nprl, fit[0]*nprl + fit[1], 'r-')
plt.show()