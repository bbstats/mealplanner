import streamlit as st

def set_multiselect_color():
    st.markdown(
        """
    <style>
    span[data-baseweb="tag"] {
    background-color: green !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )