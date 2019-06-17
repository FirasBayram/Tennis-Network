import networkx as nx
import pandas as pd
from operator import itemgetter
import contagion as cg


#   READING THE DATASET
df = pd.read_csv('ATP.csv', encoding="ISO-8859-1")
df = df[['winner_name', 'loser_name']]
df.to_csv("graph.csv", index=False, encoding='UTF-8')
df = pd.read_csv('graph.csv',  encoding='UTF-8')


# Create the undirected graph
undirected = nx.Graph()
graph = nx.from_pandas_edgelist(df, 'winner_name', 'loser_name', create_using=undirected)
graph.remove_node('U Unknown')


h_degree = sorted(graph.degree(), reverse=True, key=itemgetter(1))[:200]
hd_nodes = list(list(zip(*h_degree))[0])

#   Set the attribute of all the nodes to False
nx.set_node_attributes(graph, dict((i, False) for i in graph.nodes), 'contagious')

#   Set the initial contagious nodes
for i in hd_nodes:
    graph.nodes[i]['contagious'] = True

cg.infect_nodes(graph)

contagious_nodes = [node for node in graph.nodes if graph.nodes[node]['contagious']]
noncontagious_nodes = [node for node in graph.nodes if not graph.nodes[node]['contagious']]
print(len(contagious_nodes) / len(noncontagious_nodes))
