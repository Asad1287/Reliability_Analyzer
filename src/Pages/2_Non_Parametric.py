import streamlit as st 
import pandas as pd
import numpy as np
import surpyval as surv
from matplotlib import pyplot as plt
st.title("Non Parametric Estimation")
option = st.selectbox(
    'Select type of data',
    ('Not Censored', 'Right Censored', 'Left Censored'))

type_of_non_parametric = st.selectbox(
    'Select type of non parametric estimation',
    ('Kaplan-Meier', 'Nelson-Aalen'))

TF_file = st.file_uploader('Upload your  data in csv file format in [TIME TO FAILURE],[VARIABLE OF INTEREST - e.g. Stress] ,[Censoring],columns ')

if TF_file is not None:
    df = pd.read_csv(TF_file)
    print(df.head())
    x = df['TIME TO FAILURE']
    n =df['VARIABLE OF INTEREST']
    if option == 'Not Censored':
        c = np.zeros(len(x))
    elif option == 'Right Censored':
        c = df['Censoring']
    elif option == 'Left Censored':
        c = 1-df['Censoring']
    else:
        st.write("Error, please input data correctly")


    # Weibull's measurements are cumulative so we need to tranasform them
    n = np.concatenate([[n[0]], np.diff(n)])

    if type_of_non_parametric == "Kaplan-Meier":
        if option == "Not Censored":
            prob_variable = surv.KaplanMeier.fit(x, n=n)
        elif option == "Right Censored":
            prob_variable = surv.KaplanMeier.fit(x,c=c, n=n)
        elif option == "Left Censored":
            prob_variable = surv.KaplanMeier.fit(x,c=c, n=n)
    else:
        prob_variable = surv.NelsonAalen.fit(x, n=n)
       
    
    plt.figure(figsize=(10, 7))
    plt.ylabel('Survival Probability')
    plt.xlabel('Variable')
    plt.title('Survival Probability vs Variable')
    plt.step(prob_variable.x, prob_variable.R)
    
    st.pyplot()
    