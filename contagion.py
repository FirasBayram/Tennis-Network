import networkx as nx
import matplotlib.pyplot as plt


def infect_nodes(graph):
    #   Define the a and b parameters
    pos = nx.circular_layout(graph)
    iter=0
    snap_graph(graph, pos, iter)
    a = 3
    b = 1
    # Find noncontagious nodes to be infected
    for node in graph.nodes():
        if not graph.nodes[node]['contagious']:
            # Count contagious neighbors
            contagious_neighbors = sum([graph.nodes[n]['contagious']
                                        for n in graph.neighbors(node)])
            q = b / (a + b)
            neighbors_count = len(list(nx.neighbors(graph, node)))
            if neighbors_count == 0:
                continue
            p = contagious_neighbors / neighbors_count
            if p > q:
                graph.node[node]['contagious'] = True
                iter += 1
                if not iter % 100:
                    snap_graph(graph, pos, iter)

def snap_graph(graph, pos, iter):
    plt.figure(figsize=(20, 20))
    #   Set the colors of the nodes
    node_color = ['navy' if graph.nodes[node]['contagious']
                  else 'red' for node in graph.nodes]
    #   Draw the network
    nx.draw_networkx(graph, pos=pos, with_labels=False,  node_color=node_color)
    plt.draw()
    #   Save the figure
    plt.savefig('./Contagion_Figures/' + str(iter) + '.png')
    plt.close()

