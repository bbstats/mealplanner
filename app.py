import streamlit as st
import random
import pandas as pd
df = pd.read_csv('meal finder - Sheet1.csv')
data = df['meal'].tolist()

if st.button('Generate'):
    st.write(random.sample(data,5))
