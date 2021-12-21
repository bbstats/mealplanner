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

st.session_state.n_meals_gen = st.sidebar.number_input(
    "Number of random meals to generate",
    min_value=1,
    max_value=30,
    value=5,
)
get_meals()
st.button("Generate Random Meals", on_click=uncached_get_meals)


if "selected_meals" not in st.session_state:
    st.session_state.selected_meals = []


with st.form(key="my_annotator"):

    set_multiselect_color()
    selections = st.multiselect(
        "Select your meals",
        options=st.session_state.all_options,
        default=st.session_state.current_options,
    )

    accept_button = st.form_submit_button(label="Accept")
    clear_button = st.form_submit_button(label="Clear All")

    if accept_button:
        st.session_state.selected_meals += selections
        st.session_state.selected_meals = list(set(st.session_state.selected_meals))

    if clear_button:
        delete_all_selections()

st.session_state.results = {}


st.markdown("##")

meals_to_button = st.session_state.selected_meals.copy()
for i in meals_to_button:
    placeholder = st.empty()
    st.session_state.results[i] = placeholder
    isclick = st.session_state.results[i].button(i)
    if isclick:
        st.session_state.results[i].empty()
        st.session_state.selected_meals.remove(i)


difficulty = get_difficulty(df)
taste = get_taste(df)

st.write(f"Difficulty: {difficulty:.0%}")
st.write(f"Taste: {taste:.0%}")
