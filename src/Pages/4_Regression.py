import streamlit as st 

st.title("Regression Reliablity Model")
import pandas as pd
import numpy as np
import surpyval as surv
import numpy as np
from matplotlib import pyplot as plt


from surpyval import CoxPH

SurvivalColumn = st.text_input('SurvivalColumnName', 'Enter the name of the column that contains the survival data')
CensoringColumn = st.text_input('CensoringColumnName', 'Enter the name of the column that contains the Censoring data')

# Load the data
DataUpload = st.file_uploader('Upload your  data in csv file format ')
if DataUpload:
    df = pd.read_csv(DataUpload)
    print(df.head())
    # Create the CoxPH model
    feature_col = df.columns.drop([SurvivalColumn, CensoringColumn])
    model = CoxPH(x=df[SurvivalColumn], Z=feature_col, c=df[CensoringColumn])
    # Fit the model
    model.fit()
    # Print the results
    st.write(model.summary())
    # Plot the results
    model.plot()
    st.pyplot()
   