import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

from loader import Loader

loaderObject = Loader(use_fitted_params=True)

loaderObject.load("TTF.csv","item_config.csv","item_rel.csv")
object_dict = getattr(loaderObject,"object_dict")

def create_graph(object_dict:dict) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(object_dict.keys())
    graph.add_node("Start")
    graph.add_node("Terminal")
    for key in object_dict.keys():
        
        for relationship in object_dict[key]['relationship']:
            graph.add_edge(key,relationship)
    return graph
