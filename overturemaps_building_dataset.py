import pydeck as pdk
import geopandas as gpd

# Load GeoPackage data (adjust path and layer name as needed)
gpkg_data = gpd.read_file(r"buildings.gpkg", layer="buildings_building")
gpkg_data = gpkg_data.to_crs("EPSG:4326")  # Ensure CRS is in WGS84
gpkg_data['lat'] = gpkg_data['geometry'].centroid.y
gpkg_data['lon'] = gpkg_data['geometry'].centroid.x

# Check data integrity
print(gpkg_data[['id', 'lon', 'lat']].head())

# Data for visualization (latitude, longitude, and height of buildings)
data = gpkg_data[['id', 'lon', 'lat']]  # Corrected syntax error (removed extra comma)

# Check if data has valid height values
print(gpkg_data['height'].describe())

deck_map = pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=24.7136,
        longitude=46.6753,
        zoom=12,
        pitch=0,  # No tilt
        bearing=0
    ),
    layers=[ 
        pdk.Layer(
            "ScatterplotLayer",  # Use ScatterplotLayer for points (no elevation)
            data=data,
            get_position='[lon, lat]',  # Position based on lat and lon
            get_radius=10,  # Set the size of the points
            get_fill_color='[255, 255, 0, 100]',  # Red color with transparency
            pickable=True,  # Enable picking for interactivity
            tooltip={  # Tooltip for interaction
                "html": "<b>Building ID:</b> {id}<br>",  # Just showing building ID now
                "style": {"color": "white", "font-size": "12px"}  # Tooltip styling
            }
        ),
    ],
    map_style="dark",  # Use a built-in dark style from PyDeck
)

# Save the map as an HTML file
deck_map.to_html("riyadh_buildings.html")
