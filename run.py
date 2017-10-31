#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt





##########################################
# Abrir archivos
##########################################

relation = pd.read_csv("data/relation5.csv", sep = ";") #user_id , rel

relation = relation.sample(n=5000)

G= nx.DiGraph()

print("Archivo leido")
for index, row in relation.iterrows():
    x = int(row["user_id"])
    if( not G.has_node(x)):
        G.add_node(x)

print("Nodos creados")


i = 0
D = {}
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
            if ( i%1000 == 0 or i == 1):
                print("Se han agregado %s arcos" %(i))

print("Arcos creados")
#nx.draw(G)
#plt.show()


pr = nx.pagerank(G, alpha = 0.9)
sr = sorted(pr, key=pr.get, reverse=True)[:10]

i = 1
for a in sr:
    print("#%s. %s -> %s. Con %s seguidores." % (i,a,pr[a],D[a]))
    i+=1