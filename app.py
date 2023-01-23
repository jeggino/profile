import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Profile",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


page = option_menu(None,["Biography", "---","Ecology","Data Science","Photography","Music"], 
                 icons=["bi bi-info-lg","bi bi-tree-fill",
                        "bi bi-bar-chart-fill","bi bi-camera2",
                        ],
                 default_index=1, orientation="horizontal", menu_icon="cast",
                 )

st.title("My website")

  
  
