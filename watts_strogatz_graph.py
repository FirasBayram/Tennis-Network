import networkx as nx
import network_attack as na

graph = nx.watts_strogatz_graph(n=400, k=20, p=0.3)
print("the total number of edges:")
n_edges = nx.number_of_edges(graph)
print(n_edges)
print("the total number of nodes:")
n_nodes = nx.number_of_nodes(graph)
print(n_nodes)
n_cc = nx.number_connected_components(graph)
print("the total number of connected components:")
print(n_cc)
print("the density of the graph:")
print(nx.density(graph))
avg_deg = sum([d for (n, d) in nx.degree(graph)]) / float(graph.number_of_nodes())
print("the average degree is " + str(avg_deg))

closeness_centrality = nx.closeness_centrality
pagerank_centrality = nx.pagerank
betweenness_centrality = nx.betweenness_centrality

#   GCC ATTACK
clo_gcc_att = na.gcc_attack(graph, closeness_centrality)
pgr_gcc_att = na.gcc_attack(graph, pagerank_centrality)
bet_gcc_att = na.gcc_attack(graph, betweenness_centrality)
rnd_gcc = na.rnd_gcc_attack(graph, 1)
na.attack_measures_plot("THe Giant Connected Component Size", clo_gcc_att, pgr_gcc_att, bet_gcc_att, rnd_gcc)

#   Diameter ATTACK
clo_dia_att = na.diameter_attack(graph, closeness_centrality)
pgr_dia_att = na.diameter_attack(graph, pagerank_centrality)
bet_dia_att = na.diameter_attack(graph, betweenness_centrality)
rnd_dia = na.rand_dia_attack(graph, 1)
na.attack_measures_plot("Diameter", clo_dia_att, pgr_dia_att, bet_dia_att, rnd_dia)

#   Density ATTACK
clo_den_att = na.density_attack(graph, closeness_centrality)
pgr_den_att = na.density_attack(graph, pagerank_centrality)
bet_den_att = na.density_attack(graph, betweenness_centrality)
rnd_den = na.rand_den_attack(graph, 1)
na.attack_measures_plot("Density", clo_den_att, pgr_den_att, bet_den_att, rnd_den)

#   Clustering Coefficient ATTACK
clo_clu_att = na.clu_coe_attack(graph, closeness_centrality)
pgr_clu_att = na.clu_coe_attack(graph, pagerank_centrality)
bet_clu_att = na.clu_coe_attack(graph, betweenness_centrality)
rnd_clu = na.rand_cleu_coe_attack(graph, 1)
na.attack_measures_plot("Clustering Coefficient", clo_clu_att, pgr_clu_att, bet_clu_att, rnd_clu)
