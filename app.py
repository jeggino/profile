import streamlit as st
from streamlit_option_menu import option_menu

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

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
    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    output = st_folium(m, returned_objects=["all_drawings"], width=350, height=600)

  
  
