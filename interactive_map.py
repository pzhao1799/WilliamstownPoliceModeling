import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from geopy.geocoders import Nominatim

#helper function to add state + zip for geolocating
def add_state_zip(v):
    if v == "N/A":
        return v 
    return v + ", Williamstown, 01267"

#helper function to turn addresses into coordinates
def geolocate(v,geo): 
    if v =="N/A":
        return None
    bracketindex = v.find("]")
    if bracketindex > 3:
        return geo.geocode(v[bracketindex+1:])
    return geo.geocode(v)

#reads in a dataframe, finds coordinates, and makes an interactive .html map
def get_coords(df):
    geolocator = Nominatim(user_agent="sample app")
    df['location'] = df['location'].apply(add_state_zip)
    df['loc'] = df['location'].apply(geolocate, args = (geolocator,))
    df["point"]= df['loc'].apply(lambda loc: tuple(loc.point) if loc else None)
    df[['lat', 'lon', 'altitude']] = pd.DataFrame(df['point'].to_list(), index=df.index)
    return df


def make_map(df):
    # center to the mean of all points
    m = folium.Map(location=df[["lat", "lon"]].mean().to_list(), zoom_start=12)

    # if the points are too close to each other, cluster them, create a cluster overlay with MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    # draw the markers and assign popup and hover texts
    # add the markers the the cluster layers so that they are automatically clustered
    for i,r in df.iterrows():
        if r["location"] != "N/A" and np.isnan(r["lat"]) != True:
            location = (r["lat"], r["lon"])
            picture = "info"
            col = "blue"
            if ("motor" in r["status"].lower() or "traffic" in r["status"].lower() or "parking" in r["status"].lower() or "vehicle" in r["status"].lower()):
                picture = "car"
                col = "purple"
            
            elif ("building" in r["status"].lower()):
                picture = "building"
                col = "black"

            elif ("animal" in r["status"].lower()):
                picture = "bug"
                col = "pink"

            elif ("fire" in r["status"].lower()):
                picture = "fire"
                col = "red"

            elif ("death" in r["status"].lower()):
                picture = "ambulance"
                col = "darkred"

            elif ("utility" in r["status"].lower()):
                picture = "wrench"
                col = "gray"

            folium.Marker(location=location,
                        popup = r["unit"] + ": " + r["narrative"],
                        tooltip=r['log'] + ": " + r['status'],
                        icon=folium.Icon(color = col,icon = picture, prefix = 'fa'))\
            .add_to(marker_cluster)

    # display the map
    m


    # dave to a file
    m.save("interactive_map.html")

#example program call
#d = {'log': ["20-1", "20-12", "20-13"], 'location': ["HARWOOD ST, Massachusetts, 01267", "SOUTHHWORTH ST, Massachusetts, 01267", "N/A"]}
#df = pd.DataFrame(data=d)
#make_map(df)