#!/usr/bin/env python
# -*- coding: utf-8 -*-
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt





##########################################
# Abrir archivos
##########################################

relation = pd.read_csv("data/relation5.csv", sep = ";") #user_id , rel

subrelation = relation.sample(n=10000)

G= nx.DiGraph()

for index, row in subrelation.iterrows():
    G.add_node(int(row["user_id"]))

for index, row in subrelation.iterrows():
    if isinstance(row["rel"],str):
        rels = row["rel"].split(" ")
        for x in rels:
            x = int(x)
            if(G.has_node(x)):
                G.add_edge(row["user_id"], x)

nx.draw(G)
plt.show()

#Comentario agregado
