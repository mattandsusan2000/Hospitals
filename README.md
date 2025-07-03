# Hospitals
North Carolina Hospital Access & Income Map

Purpose
This project visualizes the relationship between hospital locations and median household income across North Carolina counties. The goal is to identify counties that may be at greater risk due to a lack of hospital infrastructure, especially in lower-income areas.

Included Files

nc_hospital_map.py – Python script that generates the interactive map

nc_hospital_map_updated.html – The completed interactive map (open in a browser)

NC_Hospitals.csv – A list of hospitals in North Carolina, including name, latitude, longitude, and county

median_income_by_county.csv – County-level median household income data

Shapefiles:

tl_2024_us_county.shp, .shx, .dbf, .prj, .cpg, etc. – TIGER/Line shapefile components from the U.S. Census Bureau

Map Features

Counties shaded by median household income:

Under $40,000 – dark red

$40k–49k – red-orange

$50k–59k – orange

$60k–69k – yellow

$70k and up – pale yellow

Counties with no hospital are shaded black, regardless of income level

Hospitals shown as blue markers

Marker clusters indicate hospital density

A legend explains all map elements

Data Sources

Hospital data manually compiled from a publicly available list of licensed NC facilities

Median household income from the U.S. Census American Community Survey (ACS 5-Year Estimates)

County boundary shapefiles from the U.S. Census Bureau’s TIGER/Line files

How to Run

Install required libraries: pandas, geopandas, folium

Ensure all files are in the same directory

Run the script with Python

Open the output HTML map in your browser

Deployment
The map can be hosted using GitHub Pages, Netlify, Vercel, or embedded on a school or research website.

