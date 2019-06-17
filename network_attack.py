import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import itertools


#   Take a snapshot to the network state
def graph_snap(graph, pos, file_name):
    bluenodes = [node for node in graph.nodes() if graph.degree(node) > 0]
    orangenodes = [node for node in graph.nodes() if graph.degree(node) == 0]
    plt.figure(figsize=(20, 20))
    plt.axis('off')
    fig = plt.figure(1)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_nodes(graph, pos, nodelist=orangenodes, node_color='orange')
    nx.draw_networkx_nodes(graph, pos, nodelist=bluenodes, node_color='navy')
    plt.savefig(file_name, bbox_inches="tight")
    plt.close()
    del fig


#   Calculate the density change after attacking a centrality
def density_attack(graph, centrality_metric):
    iters = 0
    graph = graph.copy()
    density = []
    ranks = centrality_metric(graph)
    nodes = sorted(graph.nodes(), key=lambda n: ranks[n])
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        density.append(nx.density(graph))
        graph.remove_node(nodes.pop())
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return density


#   Calculate the diameter change after attacking a centrality
def diameter_attack(graph, centrality_metric):
    iters = 0
    graph = graph.copy()
    diameter = []
    ranks = centrality_metric(graph)
    nodes = sorted(graph.nodes(), key=lambda n: ranks[n])
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        diameter.append(nx.diameter(graph))
        graph.remove_node(nodes.pop())
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return diameter


#   Calculate the clustering coefficient change after attacking a centrality
def clu_coe_attack(graph, centrality_metric):
    iters = 0
    graph = graph.copy()
    clu_coe = []
    ranks = centrality_metric(graph)
    nodes = sorted(graph.nodes(), key=lambda n: ranks[n])
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        clu_coe.append(nx.average_clustering(graph))
        graph.remove_node(nodes.pop())
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return clu_coe


#   Calculate the size of GCC after attacking a centrality
def gcc_attack(graph, centrality_metric):
    iters = 0
    graph = graph.copy()
    n_gcc = []
    pos = nx.spring_layout(graph)
    ranks = centrality_metric(graph)
    nodes = sorted(graph.nodes(), key=lambda n: ranks[n])
    while nx.number_of_nodes(max(nx.connected_component_subgraphs(graph), key=len)) > 1\
            and not nx.is_empty(max(nx.connected_component_subgraphs(graph), key=len))\
            and nodes:
        file_name = './pics1/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
        node = nodes.pop()
        giant = max(nx.connected_component_subgraphs(graph), key=len)
        graph.remove_node(node)
        n_gcc.append(nx.number_of_nodes(giant))
        if node in giant:
            giant.remove_node(node)
    else:
        file_name = './pics1/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return n_gcc


#   Calculate the size of GCC after random failure
def rnd_gcc_attack(graph, n):
    iters = 0
    graph = graph.copy()
    n_gcc = []
    pos = nx.spring_layout(graph)
    nodes = graph.nodes()
    while nx.number_of_nodes(max(nx.connected_component_subgraphs(graph), key=len)) > 1\
            and not nx.is_empty(max(nx.connected_component_subgraphs(graph), key=len))\
            and nodes:
        file_name = './pics1/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
        sample = random.sample(nodes, min(len(nodes), n))
        giant = max(nx.connected_component_subgraphs(graph), key=len)
        graph.remove_nodes_from(sample)
        n_gcc.append(nx.number_of_nodes(giant))
        if sample in giant:
            giant.remove_nodes_from(sample)
    else:
        file_name = './pics1/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return n_gcc


#   Calculate the density change after random failure
def rand_den_attack(graph, n):
    iters = 0
    graph = graph.copy()
    density = []
    nodes = graph.nodes()
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        sample = random.sample(nodes, min(len(nodes), n))
        density.append(nx.density(graph))
        graph.remove_nodes_from(sample)
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return density


#   Calculate the diameter change after random failure
def rand_dia_attack(graph, n):
    iters = 0
    graph = graph.copy()
    diameter = []
    nodes = graph.nodes()
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        sample = random.sample(nodes, n)
        diameter.append(nx.diameter(graph))
        graph.remove_nodes_from(sample)
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return diameter


#   Calculate the clustering coefficient change after random failure
def rand_cleu_coe_attack(graph, n):
    iters = 0
    graph = graph.copy()
    clu_coe = []
    nodes = graph.nodes()
    pos = nx.spring_layout(graph)
    while nx.is_connected(graph) and not nx.is_empty(graph):
        sample = random.sample(nodes, n)
        clu_coe.append(nx.average_clustering(graph))
        graph.remove_nodes_from(sample)
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        iters += 1
    else:
        file_name = './pics/' + str(iters) + '.png'
        # graph_snap(graph, pos, file_name)
        return clu_coe


#   Plot the changes with respect to a centrality measure
def attack_measures_plot(measure, m1, m2, m3, m4):
    d = locals()
    d = dict(itertools.islice(d.items(), 4))
    col_map = {'m1': 'red', 'm2': 'orange', 'm3': 'green', 'm4': 'blue'}
    for key in d.keys():
        plt.plot([i / len(d[key]) for i in np.arange(0, len(d[key]))], d[key], color=col_map[key])
    red_patch = mpatches.Patch(color='red', label='Closeness Attack')
    orange_patch = mpatches.Patch(color='orange', label='PageRank Attack')
    green_patch = mpatches.Patch(color='green', label='Betweenness Attack')
    blue_patch = mpatches.Patch(color='blue', label='Random Failure')
    plt.xlim(0, 1)
    plt.legend(handles=[red_patch, orange_patch, green_patch, blue_patch])
    plt.xlabel("Critical Threshold f")
    plt.ylabel(measure)
    plt.show()
