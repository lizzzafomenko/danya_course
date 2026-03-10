#!/Users/macbook/anaconda3/bin/python
# https://networkx.org/documentation/stable/reference/readwrite/json_graph.html

import json
import networkx as nx
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file')     # start url
parser.add_argument('-o', '--out')     # start url
args = parser.parse_args()

with open(args.file) as f:
    data = json.load(f)

G = nx.DiGraph()

for node, links in data.items():
    for link in links:
        G.add_edge(node, link)

plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k=0.15)

nx.draw(
    G,
    pos,
    node_size=40,
    arrows=True,
    node_color='blue', 
    edge_color='gray', 
    linewidths=0.5, 
    font_size = 8
)

plt.savefig(f"{args.out}.png", dpi=300)
plt.show()