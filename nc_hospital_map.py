import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Load shapefile and filter for NC
gdf = gpd.read_file("tl_2024_us_county.shp")
gdf = gdf[gdf["STATEFP"] == "37"]
gdf["NAME"] = gdf["NAME"].str.upper()

# Load and merge income data
income_df = pd.read_csv("median_income_by_county.csv")
income_df["NAME"] = income_df["NAME"].str.upper()
gdf = gdf.merge(income_df, on="NAME", how="left")

# Load hospitals
hospitals = pd.read_csv("NC_Hospitals.csv")
hospitals["COUNTY"] = hospitals["COUNTY"].str.upper()
counties_with_hospitals = set(hospitals["COUNTY"])
gdf["Has_Hospital"] = gdf["NAME"].isin(counties_with_hospitals)

# Set up base map
m = folium.Map(location=[35.5, -79.0], zoom_start=7, tiles="cartodbpositron")

# Define fill color
def county_color(row):
    if not row["Has_Hospital"]:
        return "black"
    income = row["Median_Household_Income"]
    if pd.isna(income):
        return "#2b2b2b"
    elif income < 40000:
        return "#bd0026"
    elif income < 50000:
        return "#f03b20"
    elif income < 60000:
        return "#fd8d3c"
    elif income < 70000:
        return "#fecc5c"
    else:
        return "#ffffb2"

# Add county layer
folium.GeoJson(
    gdf,
    style_function=lambda feature: {
        'fillColor': county_color(feature['properties']),
        'color': 'black',
        'weight': 0.3,
        'fillOpacity': 0.7,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NAME', 'Median_Household_Income'],
        aliases=['County:', 'Median Income:'],
        localize=True
    ),
    name='County Median Income'
).add_to(m)

# Add hospital markers
marker_cluster = MarkerCluster().add_to(m)
for _, row in hospitals.iterrows():
    try:
        folium.CircleMarker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            radius=5,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.9,
            popup=folium.Popup(
                f"<strong>{row['NAME']}</strong><br>{row['COUNTY']} County<br>Median Income: ${row['Median_Household_Income']:,.0f}",
                max_width=300
            )
        ).add_to(marker_cluster)
    except:
        continue

# Add updated legend
legend_html = '''
<div style="position: fixed; 
     bottom: 30px; left: 30px; width: 250px; height: 190px; 
     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
     padding: 10px;">
<b>Median Household Income</b><br>
&nbsp;<i style="background:black;width:12px;height:12px;float:left;margin-right:6px;"></i>No Hospital (Any Income)<br>
&nbsp;<i style="background:#bd0026;width:12px;height:12px;float:left;margin-right:6px;"></i>Under $40,000<br>
&nbsp;<i style="background:#f03b20;width:12px;height:12px;float:left;margin-right:6px;"></i>$40k–49k<br>
&nbsp;<i style="background:#fd8d3c;width:12px;height:12px;float:left;margin-right:6px;"></i>$50k–59k<br>
&nbsp;<i style="background:#fecc5c;width:12px;height:12px;float:left;margin-right:6px;"></i>$60k–69k<br>
&nbsp;<i style="background:#ffffb2;width:12px;height:12px;float:left;margin-right:6px;"></i>$70k+<br>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Save locally
m.save("nc_hospital_map_updated.html")
print("✅ Map saved as nc_hospital_map_updated.html")
