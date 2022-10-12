import numpy as np

import surpyval as surv

import networkx as nx
import matplotlib.pyplot as plt
from surpyval.parametric import Parametric
from typing import Any, Callable, List, Tuple 
import numpy as np
from loader import Loader
from Graph import *

loaderObject = Loader(use_fitted_params=True)

loaderObject.load("TTF.csv","item_config.csv","item_rel.csv")
object_dict = getattr(loaderObject,"object_dict")
parameter_list= getattr(loaderObject,"parameter_list")
graph = create_graph(object_dict)
nx.draw(graph, with_labels=True)
plt.show()
class Series_Calculator:

    def __init__(self, itemList:List[Parametric],times:float) -> None:
        self.itemList = itemList
        self.times = times
        self._df = None 
        self._hf = None

       
    def sf(self):
        x = np.atleast_1d(self.times)
        sf = np.vstack([np.log(D.sf(x)) for D in self.itemList])
        return np.exp(sf.sum(axis=0))
    def ff(self):
        x = np.atleast_1d(self.times)
        return 1 - self.sf(x,self.itemList)
    def Hf( self):
        x = np.atleast_1d(self.times)
        return -np.log(self.sf(x))
    def hf(self):
        x = np.atleast_1d(self.times)
        return np.gradient(self.Hf(x), x)
    def df(self):
        x = np.atleast_1d(self.times)
        return np.gradient(self.hf(x), x)

class Parellel_Calculator:
    def __init__(self, itemList:List[Parametric],times:float) -> None:
        self.itemList = itemList
        self.times = times
        self._df = None 
        self._hf = None

    
  
    def ff( self):
        x = np.atleast_1d(self.times)
        ff = np.vstack([np.log(D.ff(x)) for D in self.itemList])
        return np.exp(ff.sum(axis=0))

    def sf( self):
        x = np.atleast_1d(self.times)
        return 1 - self.ff()
    
    def Hf( self):
        x = np.atleast_1d(self.times)
        return -np.log(self.sf(x))
    def hf( self):
        x = np.atleast_1d(self.times)
        return np.gradient(self.Hf(x), x)
    def df( self):
        x = np.atleast_1d(self.times)
        return np.gradient(self.hf(x), x)
    

from networkx.classes.reportviews import NodeView

#import graph class object type from networkx
from networkx.classes.graph import Graph

from collections import deque

max_T = np.asanyarray(parameter_list).max()

def Calculate_Network_Reliablity(G:Graph, start:NodeView,T:int)->List[NodeView]:
    """Finds reachable nodes by BFS.
    
    G: graph
    start: node to start at
    
    returns: set of reachable nodes
    """
    parellel_node_reliability_list = []
    relaibility_calculated_list = []
    reliability_importance = {}
  
    #relaibility_calculated_list.append(object_dict[start]['model'].sf(T))
    seen = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        print(node)
        if node not in seen:
            seen.add(node)
            queue.extend(G.neighbors(node))
            if len(list(G.neighbors(node)))>2:
                for name in list(G.neighbors(node)):
                    if name != "Terminal":
                        parellel_node_reliability_list.append(object_dict[name]['model'])
                relaibility_calculated_list.append(Parellel_Calculator(parellel_node_reliability_list,T).sf())
                reliability_importance[node] = Parellel_Calculator(parellel_node_reliability_list,T).sf()
                
                parellel_node_reliability_list = []
            else:
                for name in list(G.neighbors(node)):
                    if name != "Terminal":
                        relaibility_calculated_list.append(object_dict[name]['model'].sf(T))
                        reliability_importance[node] = object_dict[name]['model'].sf(T)

   
                       
    del reliability_importance["Start"]        
    return np.prod(relaibility_calculated_list), 1-np.prod(relaibility_calculated_list),-np.log(np.prod(relaibility_calculated_list)),reliability_importance




def generate_reliablity_time_values(Graph:Graph,max_T:int) -> Tuple[List[float],List[float],List[float],Any]:
    system_reliablity_time_values = [] 
    system_cdf_time_values = []
    system_hf_time_values = []
    for time in range(1,int(max_T)*10):
        time = time/10
        reliability,cdf,failure_Rate,_ = Calculate_Network_Reliablity(Graph,"Start",time)
        
        system_reliablity_time_values.append(reliability)
        system_cdf_time_values.append(cdf)
        system_hf_time_values.append(failure_Rate)
    return system_reliablity_time_values,system_cdf_time_values,system_hf_time_values
import numpy as np
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

print(Calculate_Network_Reliablity(graph,"Start",1))
