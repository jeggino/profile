import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd

st.set_page_config(
    page_title="Profile",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


page = option_menu(None,["Biography", "Ecology","Data Science","Photography","Music"], 
                 icons=["bi bi-info-lg","bi bi-tree-fill",
                        "bi bi-bar-chart-fill","bi bi-camera2",
                        ],
                 default_index=1, orientation="horizontal", menu_icon="cast",
                 )

st.title("My website")


if page == "Data Science":
    # import the raw data
    df_raw = pd.read_csv("HousingPrices-Amsterdam-August-2021 (1).csv").iloc[:,1:]
    st.dataframe(df_raw)
    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    output = st_folium(m, returned_objects=["all_drawings"],width=1200, height=600)

  
