import geopandas as gpd
shapefile_path = 'data/Ecologisch_beheer_1e_meter.shp'
gdf = gpd.read_file(shapefile_path)
print(gdf.head())