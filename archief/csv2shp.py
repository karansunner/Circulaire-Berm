from shapely.geometry import LineString  # Import LineString from shapely
import geopandas as gpd

df = gpd.read_file('coordinaten/coordinaten.csv')

df['geometry'] = gpd.GeoSeries(LineString(zip(df['Start_X'], df['Start_Y'])))  # Use GeoSeries

df.crs = 'EPSG:28992'

df.to_file("coordinaten/sotaweg.shp")
