import networkx as nx
import contagion as cg

#   Define the Karate Club graph
graph = nx.karate_club_graph()

#   Set the attribute of all the nodes to False
nx.set_node_attributes(graph, dict((i, False) for i in range(0, len(graph))), 'contagious')

#   Set the initial contagious nodes
for i in [10, 20]:
    graph.nodes[i]['contagious'] = True

cg.infect_nodes(graph)