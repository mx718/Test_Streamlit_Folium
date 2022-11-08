import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd 


#import data
df = pd.read_parquet("reducedfile.parquet.snappy", engine='pyarrow')

pd.set_option('display.max_columns',None)

df = df.rename(columns={'latitude' : 'lat' , 'longitude' : 'lon'})
df = df.dropna(subset=['lat', 'lon'])
df.info(verbose=True, null_counts=True)

df = df.drop(df.iloc[:30,72:94],axis=1)
df.reset_index()
df.info(verbose=True, null_counts=True)

df.adedpe202006_mean_class_estim_ges.unique()
classedpe = list(df.adedpe202006_mean_class_estim_ges.unique())

df = df.dropna(subset=['SURF_HAB_TOTAL'])




#Add filter

st.title('Test Master dataset')

#Filtres

dpe = ["A", "B","C", "D", "E", "F", "G", "N"]

dpeselect = st.multiselect('Classe dpe :', classedpe,dpe)

surfaces = st.slider('Sélectionner la surface',0.0,10000.00,(0.00,10000.00),step=200.00)

df2 = df[df["adedpe202006_mean_class_estim_ges"].isin(dpeselect)]
st.write(df2["adedpe202006_mean_class_estim_ges"])
df3 =  df2[df2["SURF_HAB_TOTAL"].isin(surfaces)]


bat_location = df3[["lat","lon","geombui"]]

# center on Aix 
m = folium.Map(location=[45.68422679091273, 5.909982061873071], zoom_start=7)



# add Google Tile
tile = folium.TileLayer(
        tiles = 'http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga',
        attr = 'Google',
        name = 'Google Hybrid',
        overlay = False,
        control = True
       ).add_to(m)


for index, location_info in bat_location.iterrows():
    m.add_child(folium.Marker([location_info["lat"], location_info["lon"]], popup=location_info["geombui"]))

# call to render Folium map in Streamlit
st_map = st_folium(m, width = 725)