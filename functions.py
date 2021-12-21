import random
import pandas as pd
import streamlit as st


def get_difficulty(df):
    sub_df = df.loc[df["meal"].isin(st.session_state.selected_meals)]
    return sub_df["difficulty"].mean()


def get_taste(df):
    sub_df = df.loc[df["meal"].isin(st.session_state.selected_meals)]
    mean = ((sub_df["taste k"] + sub_df["taste n"]) / 2).mean()
    return mean


def delete_all_selections():
    meals_to_button = st.session_state.selected_meals.copy()
    for i in meals_to_button:
        st.session_state.results[i].empty()
        st.session_state.selected_meals.remove(i)


@st.cache
def get_meals_from_google_sheet():
    sheet_url = "https://docs.google.com/spreadsheets/d/1lMotcgwA_8VoE3kGmjjh8DOnrL97eGQxLt4h6dDf8d4/export?format=csv&gid=0"
    df = pd.read_csv(sheet_url)
    df["taste"] = (df["taste k"] + df["taste n"]) / 10
    df["difficulty"] = df["difficulty"] / 3
    meals = df["meal"].tolist()
    return df, meals


def uncached_get_meals():
    if "all_options" not in st.session_state:
        get_meals_from_google_sheet()
        st.session_state.all_options = st.session_state.all_options

    efficiency = -999
    while efficiency < 0.1:
        meal_candidates = random.sample(
            st.session_state.all_options, st.session_state.n_meals_gen
        )
        sub_df = st.session_state.df.loc[
            st.session_state.df["meal"].isin(meal_candidates)
        ]
        efficiency = (sub_df["taste"] - sub_df["difficulty"]).mean()
        print(efficiency)
    st.session_state.current_options = meal_candidates


@st.cache
def get_meals():
    uncached_get_meals()
