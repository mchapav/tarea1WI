#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt





##########################################
# Abrir archivos
##########################################

relation = pd.read_csv("data/relation5.csv", sep = ";") #user_id , rel

G= nx.DiGraph()

for index, row in relation.iterrows():
    G.add_node(int(row["user_id"]))

for index, row in relation.iterrows():
    if isinstance(row["rel"],str):
        rels = row["rel"].split(" ")
        for x in rels:
            x = int(x)
            if(G.has_node(x)):
                G.add_edge(row["user_id"], x)

#nx.draw(G.subgraph[0:1000])
#plt.show()


pr = nx.pagerank(G, alpha = 0.9)
sr = sorted(pr, key=pr.get, reverse=True)[:10]

i = 1
for a in sr:
    print("#%s. %s -> %s." % (i,a,pr[a]))
    i+=1