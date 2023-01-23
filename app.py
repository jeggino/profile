import streamlit as st
from streamlit_option_menu import option_menu

st.title("My website")

with st.sidebar:
  page = option_menu("ciao", ["Biography", 
                              "Ecology",
                              "Data Science",
                              "Photography", 
                              "Music"], 
#                      icons=["bi bi-info-circle","bi-calculator"],
                     default_index=1, orientation="vertical",
                     menu_icon="cast")
  
