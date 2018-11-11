#%%
import networkx as nx

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
                 node_color='red',
                 node_size=300,
                 with_labels=True)

#%%
