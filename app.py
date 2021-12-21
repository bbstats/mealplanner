from copy import copy, deepcopy
from datetime import datetime, timedelta

import streamlit as st

from functions import (
    delete_all_selections,
    get_difficulty,
    get_meals,
    get_meals_from_google_sheet,
    get_taste,
    uncached_get_meals,

)

from frontend import set_multiselect_color


st.set_page_config(
    page_title="Meal Brainstormer",
    page_icon="🍱",
    initial_sidebar_state="collapsed",
)
st.title("Meal Brainstormer")

df, all_meals = get_meals_from_google_sheet()
st.session_state.df = df
st.session_state.all_options = all_meals



get_meals()
st.button("🧠 Generate Random Meals", on_click=uncached_get_meals)
st.sidebar.title("Settings")
st.session_state.n_meals_gen = st.sidebar.number_input(
    "Number of random meals to generate",
    min_value=1,
    max_value=30,
    value=4,
    #on_change=uncached_get_meals,
)

selectiveness = st.sidebar.select_slider(
    "Selectiveness:",
    options=["None", "Somewhat", "Balanced", "High"],
    value="Balanced",
    #on_change=uncached_get_meals,
)

mapper = {"None": -999, "Somewhat": 0, "Balanced": 0.1, "High": 0.2}
st.session_state.selectiveness = mapper[selectiveness]
#uncached_get_meals()
if "selected_meals" not in st.session_state:
    st.session_state.selected_meals = []


with st.form(key="my_annotator"):

    set_multiselect_color()
    selections = st.multiselect(
        "Add meals to your brainstorm:",
        options=st.session_state.all_options,
        default=st.session_state.current_options,
    )

    accept_button = st.form_submit_button(label="✔️ Add to Brainstorm")
    clear_button = st.form_submit_button(label="🔄 Clear Brainstorm")

    if accept_button:
        st.session_state.selected_meals += selections
        st.session_state.selected_meals = list(set(st.session_state.selected_meals))

    if clear_button:
        
        delete_all_selections()
        

st.session_state.results = {}


st.markdown("# Current Brainstorm")
difficulty = get_difficulty(df)
taste = get_taste(df)

col1, col2 = st.columns(2)
if len(st.session_state.selected_meals) > 0:
    col1.metric("Difficulty", str(int(round(difficulty * 100, -1))) + "%")
    col2.metric("Taste", str(int(round(taste * 100, -1))) + "%")
else:
    col1.metric("Difficulty", "0%")
    col2.metric("Taste", "0%")


meals_to_button = st.session_state.selected_meals.copy()
for i in meals_to_button:
    placeholder = st.empty()
    st.session_state.results[i] = placeholder
    isclick = st.session_state.results[i].button(i)
    if isclick:
        st.session_state.results[i].empty()
        st.session_state.selected_meals.remove(i)
