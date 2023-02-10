import streamlit as st
import time
# from streamlit_option_menu import option_menu

# import folium
# from streamlit_folium import st_folium

import pandas as pd
# import numpy as np

# import seaborn as sns
# import matplotlib.pyplot as plt

# import altair as alt
# from vega_datasets import data

st.set_page_config(
    page_title="Profile",
    page_icon="🧊",
    layout="wide",
)

@st.cache
def load_data(url):
    time.sleep(20)
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")

# @st.cache_data  
# def load_data(url):
#     df = pd.read_csv(url) 
#     return df

# df = load_data('pages/bird_migration (1).csv')
# st.dataframe(df)

# st.button("Rerun")

# import streamlit as st
# from streamlit_keplergl import keplergl_static
# from keplergl import KeplerGl
# import pandas as pd

# df_raw = pd.read_csv('pages/bird_migration (1).csv')

# df = pd.DataFrame(
#     {
#         "City": ["San Francisco", "San Jose", "Palo Alto"],
#         "Latitude": [37.77, 37.33, 37.44],
#         "Longitude": [-122.43, -121.89, -122.14],
#         "Latitude_2": [38.77, 38.33, 39.44],
#         "Longitude_2": [-121.43, -123.89, -124.14],
#     }
# )

# st.dataframe(df_raw.head())

# st.write("This is a kepler.gl map with data input in streamlit")

# # map_1 = KeplerGl(height=600)
# # map_1.add_data(
# #     data=df_raw, name="cities"
# # )  # Alternative: 

# map_1 = KeplerGl(height=400, data={"cities": df,
#                                    "seagul":df_raw})

# keplergl_static(map_1, center_map=True)




# from st_aggrid import JsCode, AgGrid, GridOptionsBuilder






# df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')

# gb = GridOptionsBuilder.from_dataframe(df)
# gb.configure_selection(selection_mode="multiple", use_checkbox=True)
# gridOptions = gb.build()
# dta = AgGrid(df, gridOptions=gridOptions,height=350, allow_unsafe_jscode=True, enable_enterprise_modules=True)

# st.write(dta['selected_rows'])
