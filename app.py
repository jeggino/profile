import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from streamlit_player import st_player

st.set_page_config(
    page_title="Profile",
    page_icon="🧊",
    layout="wide",
)


page = option_menu(None,["Biography", "Ecology","Data Science","Photography","Music"], 
                 icons=["bi bi-info-lg","bi bi-tree-fill",
                        "bi bi-bar-chart-fill","bi bi-camera2",
                        ],
                 default_index=1, orientation="horizontal", menu_icon="cast",
                 )

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])


from streamlit_elements import elements, mui, html,dashboard, media

with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 2, 2),
        dashboard.Item("second_item", 2, 0, 2, 2),
        dashboard.Item("third_item", 0, 2, 1, 1),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        mui.Paper("First item", key="first_item")
#         mui.Paper("Second item", key="second_item")
        st.map(df,key="third_item")

        media.Player(url="https://www.youtube.com/watch?v=iik25wqIuFo", controls=True, key="second_item")

   
