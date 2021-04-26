import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim

#helper function to turn addresses into coordinates
def geolocate(v,geo): 
    if v =="N/A":
        return
    return geo.geocode(v)

#reads in a dataframe, finds coordinates, and makes an interactive .html map
def make_map(df):
    geolocator = Nominatim(user_agent="sample app")
    df['loc'] = df['location'].apply(geolocate, args = (geolocator,))
    df["point"]= df['loc'].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['lat', 'lon', 'altitude']] = pd.DataFrame(df['point'].to_list(), index=df.index)
    print(df)

    # center to the mean of all points
    m = folium.Map(location=df[["lat", "lon"]].mean().to_list(), zoom_start=2)

    # if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    # draw the markers and assign popup and hover texts
    # add the markers the the cluster layers so that they are automatically clustered
    for i,r in df.iterrows():
        if r["location"] != "N/A":
            location = (r["lat"], r["lon"])
            folium.Marker(location=location,
                        popup = r['log'],
                        tooltip=r['log'])\
            .add_to(marker_cluster)

    # display the map
    m


    # dave to a file
    m.save("interactive_map.html")

#example program call
#d = {'log': ["20-1", "20-12", "20-13"], 'location': ["MAIN ST, Massachusetts, 01267", "HARWOOD ST, Massachusetts, 01267", "N/A"]}
#df = pd.DataFrame(data=d)
#make_map(df)