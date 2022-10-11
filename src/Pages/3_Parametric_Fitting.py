import streamlit as st 
import pandas as pd 
import numpy as np
import surpyval as surv
from matplotlib import pyplot as plt

st.title("Parametric Estimation fitting data to model")
type_of_parametric_model = st.selectbox(
    'Select type of parametric estimation',
    ('Weibull', 'Normal','Lognormal','Exponential'))

TTF_file = st.file_uploader('Upload your  data in csv file format in [TIME TO FAILURE]')
if TTF_file is not None:
    if type_of_parametric_model == "Weibull":
        if TTF_file is not None:
            df = pd.read_csv(TTF_file)
            print(df.head())
            x = df['TIME TO FAILURE']
            # Weibull's measurements are cumulative so we need to tranasform them
            n = np.concatenate([[x[0]], np.diff(x)])
            prob_variable = surv.Weibull.fit(x, n=n)
            plt.figure(figsize=(10, 7))
            plt.ylabel('Survival Probability')
            plt.xlabel('Variable')
            plt.title('Survival Probability vs Variable')
            plt.step(prob_variable.x, prob_variable.R)
            st.pyplot()
    elif type_of_parametric_model == "Normal":
        if TTF_file is not None:
            df = pd.read_csv(TTF_file)
            print(df.head())
            x = df['TIME TO FAILURE']
            # Weibull's measurements are cumulative so we need to tranasform them
            n = np.concatenate([[x[0]], np.diff(x)])
            prob_variable = surv.Normal.fit(x, n=n)
            plt.figure(figsize=(10, 7))
            plt.ylabel('Survival Probability')
            plt.xlabel('Variable')
            plt.title('Survival Probability vs Variable')
            plt.step(prob_variable.x, prob_variable.R)
            st.pyplot()
    elif type_of_parametric_model == "Lognormal":
        if TTF_file is not None:
            df = pd.read_csv(TTF_file)
            print(df.head())
            x = df['TIME TO FAILURE']
            # Weibull's measurements are cumulative so we need to tranasform them
            n = np.concatenate([[x[0]], np.diff(x)])
            prob_variable = surv.Lognormal.fit(x, n=n)
            plt.figure(figsize=(10, 7))
            plt.ylabel('Survival Probability')
            plt.xlabel('Variable')
            plt.title('Survival Probability vs Variable')
            plt.step(prob_variable.x, prob_variable.R)
            st.pyplot()
    elif type_of_parametric_model == "Exponential":
        if TTF_file is not None:
            df = pd.read_csv(TTF_file)
            print(df.head())
            x = df['TIME TO FAILURE']
            # Weibull's measurements are cumulative so we need to tranasform them
            n = np.concatenate([[x[0]], np.diff(x)])
            prob_variable = surv.Exponential.fit(x, n=n)
            plt.figure(figsize=(10, 7))
            plt.ylabel('Survival Probability')
            plt.xlabel('Variable')
            plt.title('Survival Probability vs Variable')
            plt.step(prob_variable.x, prob_variable.R)
            st.pyplot()
    else:
        st.write('Please select a parametric model')   
else:
    st.write('Please upload your data')
