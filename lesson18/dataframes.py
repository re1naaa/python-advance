import pandas as pd
import streamlit as st

st.header("Displaying dataframes")

data = pd.DataFrame({
    'Name' : ['Egzon', 'Melina', 'Liron', 'Sara', 'Anid', 'Reina'],
    'Age' : [17,17,18,18,16,15],
    'City' :  ['Fushe Kosove', 'Prishtine', 'Presheve', 'Obiliq', 'Prishtine', 'Prishtine']
})


st.dataframe(data)