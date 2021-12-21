import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from copy import copy
now = datetime.now()
monday = (now - timedelta(days=now.weekday())).date()


@st.cache
def get_meals_from_google_sheet():
    sheet_url = "https://docs.google.com/spreadsheets/d/1lMotcgwA_8VoE3kGmjjh8DOnrL97eGQxLt4h6dDf8d4/export?format=csv&gid=0"
    df = pd.read_csv(sheet_url)
    meals = df["meal"].tolist()
    return meals


def uncached_get_meals(n=5):
    if "all_options" not in st.session_state:
        get_meals_from_google_sheet()
        st.session_state.all_options = all_meals
    st.session_state.current_options = random.sample(st.session_state.all_options, n)


def delete_session_state_results():
    if 'selected_meals' in st.session_state:
        del st.session_state.selected_meals
        st.session_state.selected_meals = []

@st.cache
def get_meals(n=5):
    if "all_options" not in st.session_state:
        get_meals_from_google_sheet()
    st.session_state.current_options = random.sample(st.session_state.all_options, n)


all_meals = get_meals_from_google_sheet()
st.session_state.all_options = all_meals

get_meals()
st.button("Generate Random Meals", on_click=uncached_get_meals)


if "selected_meals" not in st.session_state:
    st.session_state.selected_meals = []

# options = ["Small talk","Shopping ideas","Customer service"]
st.button('Start Over', delete_session_state_results)
with st.form(key="my_annotator"):

    selections = st.multiselect(
        "Select your meals",
        options=st.session_state.all_options,
        default=st.session_state.current_options,
    )

    accept_button = st.form_submit_button(label="Accept")
    

    if accept_button:
        st.session_state.selected_meals += selections
        st.session_state.selected_meals = list(set(st.session_state.selected_meals))

st.session_state.results={}

print(len(st.session_state.selected_meals))


meals_to_button = st.session_state.selected_meals.copy()
for i in meals_to_button:
    placeholder = st.empty()
    st.session_state.results[i]=placeholder
    isclick = st.session_state.results[i].button(i)
    if isclick:
        st.session_state.results[i].empty()
        st.session_state.selected_meals.remove(i)