import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from copy import copy, deepcopy

now = datetime.now()
monday = (now - timedelta(days=now.weekday())).date()


st.set_page_config(
    page_title="Meal Planner",
    page_icon="🍱",
    initial_sidebar_state="collapsed",
)


def get_difficulty(df):
    sub_df = df.loc[df["meal"].isin(st.session_state.selected_meals)]
    return sub_df["difficulty"].mean() / 3


def get_taste(df):
    sub_df = df.loc[df["meal"].isin(st.session_state.selected_meals)]
    mean = ((sub_df["taste k"] + sub_df["taste n"]) / 2).mean()
    return mean / 5


def delete_all_selections():

    meals_to_button = st.session_state.selected_meals.copy()
    for i in meals_to_button:
        st.session_state.results[i].empty()
        st.session_state.selected_meals.remove(i)


@st.cache
def get_meals_from_google_sheet():
    sheet_url = "https://docs.google.com/spreadsheets/d/1lMotcgwA_8VoE3kGmjjh8DOnrL97eGQxLt4h6dDf8d4/export?format=csv&gid=0"
    df = pd.read_csv(sheet_url)
    meals = df["meal"].tolist()
    return df, meals


def uncached_get_meals():
    if "all_options" not in st.session_state:
        get_meals_from_google_sheet()
        st.session_state.all_options = all_meals
    st.session_state.current_options = random.sample(
        st.session_state.all_options, st.session_state.n_meals_gen
    )


@st.cache
def get_meals():
    if "all_options" not in st.session_state:
        get_meals_from_google_sheet()
    st.session_state.current_options = random.sample(
        st.session_state.all_options, st.session_state.n_meals_gen
    )


df, all_meals = get_meals_from_google_sheet()
st.session_state.all_options = all_meals

st.session_state.n_meals_gen = st.sidebar.number_input(
    "Number of random meals to generate",
    min_value=1,
    max_value=30,
    value=5,  # , on_change=uncached_get_meals
)
get_meals()
st.button("Generate Random Meals", on_click=uncached_get_meals)


if "selected_meals" not in st.session_state:
    st.session_state.selected_meals = []


# this isnt working still

with st.form(key="my_annotator"):

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

print(len(st.session_state.selected_meals))


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

st.write(f"Difficulty: {difficulty}")
st.write(f"Taste: {taste}")