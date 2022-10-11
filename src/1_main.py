import numpy as np
import surpyval as surv

import networkx as nx
import matplotlib.pyplot as plt
from surpyval.parametric import Parametric
from typing import Callable, List 
import numpy as np
from loader import Loader
from Calculation import *
from Graph import *
import streamlit as st 
from PIL import Image

st.set_page_config(page_title="Series-Parellel System Models",layout="wide")

image1 = Image.open('Screen1.jpg')
image2 = Image.open('Screen2.jpg')
image3 = Image.open('Screen3.jpg')
st.title("Reliability System Analysis - Block based Simulation")

st.write("This app uses equipment/assets physical time to fail data to create time to fail model, then create relationship between equipment/assets to create a system reliability model")
st.write("The system reliability model is then used to calculate the system reliability and failure rate")  


#plot reliability vs time
st.image(image1)
TTF_file = st.file_uploader('Upload your failure data in csv file format in [Equipment],[Time to Failure(Days)] columns ')

st.image(image2)
item_config= st.file_uploader('Upload your item configuration in csv file format in [Equipment],[Model],[Parameter a],[Parameter b] ')
st.image(image3)
item_rel = st.file_uploader('Upload your item relationship in csv file format in [Equipment],[Linked Equipment 1],[Linked Equipment 2]... ')






if (item_config and item_rel) is not None: 

    loaderObject = Loader(use_fitted_params=True)

    loaderObject.load(TTF_file.name,item_config.name,item_rel.name)
    object_dict = getattr(loaderObject,"object_dict")
    parameter_list= getattr(loaderObject,"parameter_list")
    max_T = np.asanyarray(parameter_list).max()
    graph = create_graph(object_dict)
    system_reliablity_time_values,system_cdf_time_values,system_hf_time_values = generate_reliablity_time_values(graph,max_T)
    _,_,_,importance_dict = Calculate_Network_Reliablity(graph,"Start",1)
   
    fig1,ax1 = plt.subplots()
    fig1 = nx.draw(graph, with_labels=True)
    ax1.set_title("System Reliability Graph")
    st.pyplot(fig1)
    fig2,ax2 = plt.subplots()
    ax2.plot(system_reliablity_time_values)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Reliability")
    ax2.set_title("Reliability vs Time")

    st.pyplot(fig2)
    fig3,ax3 = plt.subplots()
    ax3.plot(system_cdf_time_values)
    ax3.set_xlabel("Time")
    ax3.set_ylabel("CDF")
    ax3.set_title("CDF vs Time")
    st.pyplot(fig3)

    fig4,ax4 = plt.subplots()
    ax4.plot(system_hf_time_values)
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Failure Rate")
    ax4.set_title("Failure Rate vs Time")
    st.pyplot(fig4)

    fig5,ax5 = plt.subplots()
    ax5.bar(importance_dict.keys(),importance_dict.values())
    ax5.set_xlabel("Equipment")
    ax5.set_ylabel("Importance")
    ax5.set_title("Importance of Equipment")
    st.pyplot(fig5)
 

    st.write(f"<h1>average life of system is {find_nearest(system_reliablity_time_values,0.5)} days</h1>",unsafe_allow_html=True)
    st.write(f"<h1>Average failure rate of system over lifetime is {int(np.mean(system_hf_time_values))} failure per day</h1>",unsafe_allow_html=True)
   
