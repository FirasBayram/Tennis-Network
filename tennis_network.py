import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
import dzcnapy_plotlib as dzcnapy
from tabulate import tabulate
from collections import Counter
import network_attack as na

#   READING THE DATASET
df = pd.read_csv('ATP.csv', encoding="ISO-8859-1")
df = df[['winner_name', 'loser_name']]
df.to_csv("graph.csv", index=False, encoding='UTF-8')
df = pd.read_csv('graph.csv',  encoding='UTF-8')

#   CREATING THE GRAPH
# Define Direct Graph creating the edge from the winner to the loser name
# Create the directed graph
# directed = nx.DiGraph()
# G = nx.from_pandas_edgelist(df,'winner_name','loser_name', create_using=directed)

# Create the undirected graph
undirected = nx.Graph()
G = nx.from_pandas_edgelist(df, 'winner_name', 'loser_name', create_using=undirected)
G.remove_node('U Unknown')

#   THE NETWORK MEASURES
# Print the number of edges and nodes
print("the total number of edges:")
n_edges = nx.number_of_edges(G)
print(n_edges)
print("the total number of nodes:")
n_nodes = nx.number_of_nodes(G)
print(n_nodes)

# Print the density of the network
density = nx.density(G)
print("The density of the graph is: " + str(density))

# The mean clustering coefficient for all nodes
acc = nx.average_clustering(G)
print("the mean clustering coefficient is: " + str(acc))

# The transitivity measure of the network
cc = nx.transitivity(G)
print("the transitivity measure is: " + str(cc))

# Calculate the assortativity of the network
print(nx.degree_assortativity_coefficient(G))

# Print the average degree
avg_deg = sum([d for (n, d) in nx.degree(G)]) / float(G.number_of_nodes())
print("the average degree is " + str(avg_deg))

# Print the number of connected components of the network
n_cc = nx.number_connected_components(G)
print("The number of connected components of the graph is")
print(n_cc)

# Printing the nodes with the highest degree
h_degree = sorted(G.degree(), reverse=True, key=itemgetter(1))[:20]
hdg_text = "\n".join(map(lambda t: "{} {}".format(*reversed(t)), h_degree))
textfile = open('Highest Degree.txt', 'w')
textfile.write(hdg_text)
textfile.close()


#   CENTRALITY MEASURES
def centrality_measures(graph):
    # Calculate Degree Centrality
    dgr = nx.degree_centrality(graph)
    dgr_sorted = sorted(dgr.items(), key=itemgetter(1), reverse=True)
    dgr_text = tabulate(dgr_sorted, headers=['Node ID', 'Node Degree Centrality'])
    textfile = open('Degree Centrality.txt', 'w')
    textfile.write(dgr_text)
    textfile.close()
    # Calculate Node Closeness
    clo = nx.closeness_centrality(graph)
    clo_sorted = sorted(clo.items(), key=itemgetter(1), reverse=True)
    clo_text = tabulate(clo_sorted, headers=['Node ID', 'Node Closeness'])
    textfile = open('Closeness.txt', 'w')
    textfile.write(clo_text)
    textfile.close()
    # Calculate Node Betweenness
    bet = nx.betweenness_centrality(graph)
    bet_sorted = sorted(bet.items(), key=itemgetter(1), reverse=True)
    bet_text = tabulate(bet_sorted, headers=['Node ID', 'Node Betweenness'])
    textfile = open('Betweenness.txt', 'w')
    textfile.write(bet_text)
    textfile.close()
    # Calculate Node Page Rank
    pgr = nx.pagerank(graph)
    pgr_sorted = sorted(pgr.items(), key=itemgetter(1), reverse=True)
    pgr_text = tabulate(pgr_sorted, headers=['Node ID', 'Node Page Rank'])
    textfile = open('Page Rank.txt', 'w')
    textfile.write(pgr_text)
    textfile.close()
    # Calculate Node Eigenvector Centrality
    egv = nx.eigenvector_centrality(graph)
    egv_sorted = sorted(egv.items(), key=itemgetter(1), reverse=True)
    egv_text = tabulate(egv_sorted, headers=['Node ID', 'Node Eigenvector'])
    textfile = open('Eigenvector.txt', 'w')
    textfile.write(egv_text)
    textfile.close()
    # Calculate Node HITS Authority
    hits = nx.hits(graph)
    sorted_hits = sorted(hits[0].items(), key=itemgetter(1), reverse=True)
    hits_text = tabulate(sorted_hits, headers=['Node ID', 'Node Authority'])
    textfile = open('HITS Authority.txt', 'w')
    textfile.write(hits_text)
    textfile.close()
    # Define the centralities DataFrame
    centralities = pd.concat(
        [pd.Series(c) for c in (hits[1], egv, pgr, clo, hits[0], dgr, bet)], axis=1)
    centralities.columns = ("Authorities", "Eigenvector", "PageRank",
                            "Closeness", "Hubs", "Degree", "Betweenness")
    textfile = open('centralities.txt', 'w')
    textfile.write(tabulate(centralities, headers=["Node ID", "Authorities", "Eigenvector", "PageRank",
                                                   "Closeness", "Hubs", "Degree", "Betweenness"]))
    textfile.close()
    return centralities


centralities = centrality_measures(G)


# Calculate the correlation between the centralities
def correlations(centralities):
    c_df = centralities.corr()
    # Transform the correlation df to diagonal
    ll_triangle = np.tri(c_df.shape[0], k=-1)
    c_df *= ll_triangle
    c_series = c_df.stack().sort_values()
    corrs_text = str(c_series)
    textfile = open('Correlation.txt', 'w')
    textfile.write(corrs_text)
    textfile.close()
    return c_series


correlations = correlations(centralities)


# Plot some measures against another
def centrality_correlation_plot(centralities, cent1, cent2):
    X = cent1
    Y = cent2
    limits = pd.concat([centralities[[X, Y]].min(),
                        centralities[[X, Y]].max()], axis=1).values
    centralities.plot(kind="scatter", x=X, y=Y, xlim=limits[0], ylim=limits[1],
                      edgecolors='black', color='pink', s=75, alpha=0.6)
    plt.grid()
    dzcnapy.plot("centralities_comparison")


centrality_correlation_plot(centralities, "Betweenness", "Degree")


#   PROBABILITY DISTRIBUTION
# Plot the probability distribution of the network
def prob_dist_plot(graph):
    deg = dict(nx.degree(graph))
    x, y = zip(*Counter(deg.values()).items())
    plt.scatter(x, y, s=10, c="navy")
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Tennis players degree distribution -- log scale")
    plt.xlim(0.9, max(x) + 10)
    plt.ylim(0.9, max(y) + 10)
    plt.xlabel("log(Degree)")
    plt.ylabel("log(Frequency)")
    dzcnapy.plot("Tennis players degree distribution")


prob_dist_plot(G)


#   THE GIANT CONNECTED COMPONENT ANALYSIS
# Store the giant connected component sub graph
giant = max(nx.connected_component_subgraphs(G), key=len)
print("the total number of nodes of the GCC is " + str(nx.number_of_nodes(giant)))
gcc_text = str(list(giant))
textfile = open('Giant Connected Component Nodes.txt', 'w')
textfile.write(gcc_text)
textfile.close()

# Calculate the radius and the diameter of the giant connected component of the network
diameter = nx.diameter(giant)
print("The Diameter of the graph is:")
print(diameter)
radius = nx.radius(giant)
print("The Radius of the graph is:")
print(radius)

# Calculate the average of the shortest paths and assortativity lengths of the GCC
print("The average Shortest path length is:")
print(nx.average_shortest_path_length(giant))
print("the assortativity coefficient is:")
print(nx.degree_assortativity_coefficient(giant))

# Print the peripheral nodes of the GCC
print("The peripheral nodes are:")
print(nx.periphery(giant))


# Calculate the eccentricity of the GCC nodes
ec_gcc = nx.eccentricity(giant)
ec_gcc_sorted = sorted(ec_gcc.items(), key=itemgetter(1), reverse=True)
ec_gcc_text = tabulate(ec_gcc_sorted, headers=['Node ID', 'Node Eccentricity'])
textfile = open('GCC Eccentricity.txt', 'w')
textfile.write(ec_gcc_text)
textfile.close()


#   ATTACKING THE NETWORK
closeness_centrality = nx.closeness_centrality
pagerank_centrality = nx.pagerank
betweenness_centrality = nx.betweenness_centrality

#   GCC ATTACK
clo_gcc_att = na.gcc_attack(giant, closeness_centrality)
pgr_gcc_att = na.gcc_attack(giant, pagerank_centrality)
bet_gcc_att = na.gcc_attack(giant, betweenness_centrality)
rnd_gcc = na.rnd_gcc_attack(giant, 1)
na.attack_measures_plot("THe Giant Component Component Size",
                        clo_gcc_att, pgr_gcc_att, bet_gcc_att, rnd_gcc)

#   Diameter ATTACK
clo_dia_att = na.diameter_attack(giant, closeness_centrality)
pgr_dia_att = na.diameter_attack(giant, pagerank_centrality)
bet_dia_att = na.diameter_attack(giant, betweenness_centrality)
rnd_dia = na.rand_dia_attack(giant, 1)
na.attack_measures_plot("Diameter", clo_dia_att, pgr_dia_att, bet_dia_att, rnd_dia)

#   Density ATTACK
clo_den_att = na.density_attack(giant, closeness_centrality)
pgr_den_att = na.density_attack(giant, pagerank_centrality)
bet_den_att = na.density_attack(giant, betweenness_centrality)
rnd_den = na.rand_den_attack(giant, 1)
na.attack_measures_plot("Density", clo_den_att, pgr_den_att, bet_den_att, rnd_den)

#   Clustering Coefficient ATTACK
clo_clu_att = na.clu_coe_attack(giant, closeness_centrality)
pgr_clu_att = na.clu_coe_attack(giant, pagerank_centrality)
bet_clu_att = na.clu_coe_attack(giant, betweenness_centrality)
rnd_clu = na.rand_cleu_coe_attack(giant, 1)
na.attack_measures_plot("Clustering Coefficient", clo_clu_att, pgr_clu_att, bet_clu_att, rnd_clu)
