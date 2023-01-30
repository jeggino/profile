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

if page == "Biography":
    st.title("My website")



elif page == "Data Science":
    # import the raw data
    df_raw = pd.read_csv("HousingPrices-Amsterdam-August-2021 (1).csv").iloc[:,1:]
    
    # create the dataset
    df_model = df_raw[['Price', 'Area', 'Room']]
    fig = sns.pairplot(df_model[['Price', 'Area', 'Room']], diag_kind='auto',corner=True)
    sns.set_theme(style="white")
    st.pyplot(fig)
    
    # create the classes
    df_model['price_class'] = pd.cut(df_model.Price,
                                 bins=[df_model["Price"].min(),
                                       df_model["Price"].mean(),
                                       df_model["Price"].max()],
                                 include_lowest=True,
                                 labels=['low','high'])
    
    df_2 = df_model.groupby('price_class').mean().round(2)
    with st.expander("See code"):
        body = """
df_model['price_class'] = pd.cut(df_model.Price,
                                bins=[df_model["Price"].min(),
                                        df_model["Price"].mean(),
                                        df_model["Price"].max()],
                                include_lowest=True,
                                labels=['low','high'])

df_2 = df_model.groupby('price_class').mean().round(2)
"""
        st.code(body, language="python")
    st.dataframe(df_2)
    
    
    


    
    
elif page == "Ecology":
    # map
    m = folium.Map(location=[44.266308, 11.719301], zoom_start=3)
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False}).add_to(m)
    Fullscreen().add_to(m)
    LocateControl(auto_start=True).add_to(m)
    output = st_folium(m, returned_objects=["all_drawings"])
    
    
elif page == "Photography":
    st.image("My project.png")
    
elif page == "Music":    
    st_player("https://youtu.be/-uLhBxPzbcM")

  
