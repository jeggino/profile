import streamlit as st
from streamlit_option_menu import option_menu

st.title("My website")

with st.sidebar:
  page = option_menu("ciao", ["Biography", 
                              "Ecology",
                              "Data Science",
                              "Photography", 
                              "Music"], 
                     icons=["bi bi-info-lg","bi bi-tree-fill",
                            "bi bi-bar-chart-fill","bi bi-camera2",
                            "bi bi-file-earmark-music-fill"],
                     default_index=5, orientation="vertical",
                     menu_icon="cast")
  
