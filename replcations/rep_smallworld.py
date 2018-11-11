#%%
import networkx as nx

def flip(p):
        return np.random.random() < p

def all_pairs(nodes):
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i>j:
                yield u, v

#%%
def adjacent_edges(nodes, halfk):
    n = len(nodes)
    for i, u in enumerate(nodes):
        for j in range(i+1, i+halfk+1):
            v = nodes[j % n]
            yield u, v

#%%
>>> nodes = range(3)
>>> for edge in adjacent_edges(nodes, 1):
...     print(edge)

def make_ring_lattice(n, k):
    G = nx.Graph()
    nodes = range(n)
    G.add_nodes_from(nodes)
    G.add_edges_from(adjacent_edges(nodes, k//2))
    return G

#%%
lattice = make_ring_lattice(10, 4)


#%%
nx.draw_circular(lattice,
                 node_color='cyan',
                 node_size=300,
                 with_labels=True)

#%%

def rewire(G, p):
    nodes = set(G)
    for u, v in G.edges():
        if flip(p):
            choices = nodes - {u} - set(G[u])
            new_v = np.random.choice(list(choices))
            G.remove_edge(u, v)
            G.add_edge(u, new_v)
    return G 
#%%
def node_clustering(G, u):
    neighbors = G[u]
    k = len(neighbors)
    if k < 2:
        return np.nan
    possible = k * (k-1) / 2
    exist = 0
    for v, w in all_pairs(neighbors):
        if G.has_edge(v, w):
            exist +=1
    return exist / possible


#%%
>>> lattice = make_ring_lattice(10, 4)
>>> node_clustering(lattice, 1)

#%%

import numpy as np

def clustering_coefficient(G):
    cu = [node_clustering(G, node) for node in G]
    return np.nanmean(cu)

#%%
clustering_coefficient(lattice)

#%%
def path_lengths(G):
    length_map = dict(nx.shortest_path_length(G))
    lengths = [length_map[u][v] for u, v in all_pairs(G)]
    return lengths

#%%
 def characteristic_path_length(G):
    return np.mean(path_lengths(G))

#%%
characteristic_path_length(lattice)

#%%
def gen_lattice(n, k, p):
    lattice = make_ring_lattice(n, k)
    rewire(lattice, p)
    return lattice

def move_by_rewiring_prob(n, k, p):    
    lattice_p = gen_lattice(n, k, p)
    lattice_0 = gen_lattice(n, k, 0)
    
    cr = clustering_coefficient(lattice_p) / clustering_coefficient(lattice_0)
    lr = characteristic_path_length(lattice_p) / characteristic_path_length(lattice_0)
    return cr, lr

#%%
move_by_rewiring_prob(1000, 10, 0.5)


#%%
res = [move_by_rewiring_prob(1000, 10, p) for p in np.linspace(10**(-4), 0, 10)]

#%%
import pandas as pd
import matplotlib.pyplot as plt 

res = pd.DataFrame(res)
res['p'] = np.linspace(10**(-4), 0, 10)
res.columns = ['cr', 'lr', 'p']

plt.plot( 'p', 'cr', data=res, linestyle='-', marker='o', color='blue')
plt.plot( 'p', 'cr', data=res, linestyle='-', marker='o', color='blue')
plt.show()