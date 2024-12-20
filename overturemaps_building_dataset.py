import pydeck as pdk
import geopandas as gpd

# Load GeoPackage data (adjust path and layer name as needed)
gpkg_data = gpd.read_file(r"buildings.gpkg", layer="buildings_building")
gpkg_data = gpkg_data.to_crs("EPSG:4326")
gpkg_data['lat'] = gpkg_data['geometry'].centroid.y
gpkg_data['lon'] = gpkg_data['geometry'].centroid.x

# Check data integrity
print(gpkg_data[['id', 'lon', 'lat']].head())

# Data for visualization (latitude, longitude, and height of buildings)
data = gpkg_data[['id', 'lon', 'lat']]

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
            "ScatterplotLayer",
            data=data,
            get_position='[lon, lat]',
            get_radius=10,
            get_fill_color='[255, 255, 0, 100]',
            pickable=True,
            tooltip={ 
                "html": "<b>Building ID:</b> {id}<br>",
                "style": {"color": "white", "font-size": "12px"}
            }
        ),
    ],
    map_style="dark",
)

# Save the map as an HTML file
deck_map.to_html("riyadh_buildings.html")
