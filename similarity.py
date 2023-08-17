from collections import defaultdict
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def jaccard_similarity(G1, G2):
    intersection = defaultdict(lambda: 0)
    union = defaultdict(lambda: 0)
    
    # Calculate intersection and union of nodes
    for node in G1.nodes():
        if node in G2:
            for neighbor in G1.neighbors(node):
                if neighbor in G2[node]:
                    weight1 = G1[node][neighbor]['weight']
                    weight2 = G2[node][neighbor]['weight']
                    intersection[node] += min(weight1, weight2)
                    union[node] += max(weight1, weight2)
    
    # Calculate Jaccard similarity for each node
    similarity = []
    for node in intersection:
        if union[node] > 0:
            similarity.append(intersection[node] / union[node])
    
    # Return average similarity
    if len(similarity) > 0:
        return sum(similarity) / len(similarity)
    else:
        return 0

### real world
G = np.load("xxx1/best_adj_mx.npy")
print(G)
A=np.matrix(G)
graph_1 = nx.from_numpy_array(A)
print(graph_1)
nx.draw(graph_1, with_labels=True)
plt.show()


### cc
G2 = np.load("xxx2/best_adj_mx.npy")
print(G2)
A2=np.matrix(G2)
graph_cc = nx.from_numpy_array(A2)
print(graph_cc)
nx.draw(graph_cc, with_labels=True)
plt.show()

###od
G3 = np.load("xxx3/best_adj_mx.npy")
print(G3)
A3=np.matrix(G3)
graph_od = nx.from_numpy_array(A3)
print(graph_od)
nx.draw(graph_od, with_labels=True)
plt.show()


similarity = jaccard_similarity(graph_od, graph_cc)
print(similarity)

