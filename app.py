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
    # First, import the elements you need

    from streamlit_elements import elements, mui, html

    # Create a frame where Elements widgets will be displayed.
    #
    # Elements widgets will not render outside of this frame.
    # Native Streamlit widgets will not render inside this frame.
    #
    # elements() takes a key as parameter.
    # This key can't be reused by another frame or Streamlit widget.

    with elements("new_element"):

        # Let's create a Typography element with "Hello world" as children.
        # The first step is to check Typography's documentation on MUI:
        # https://mui.com/components/typography/
        #
        # Here is how you would write it in React JSX:
        #
        # <Typography>
        #   Hello world
        # </Typography>

        mui.Typography("Hello world")



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
    
    
    
elif page == "Photography":
    st.image("My project.png")
    
elif page == "Music":    
    st_player("https://youtu.be/-uLhBxPzbcM")

  
