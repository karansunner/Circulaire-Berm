import requests, os
from shapely.geometry import LineString
import geopandas as gpd
from qgis.core import QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem

# Haalt wegnamen op die als kaartlaag moeten worden toegevoegd
def read_highway_names(filename):
  highway_names = []
  try:
    with open(filename, "r") as f:
      for line in f:
        highway_names.append(line.rstrip())
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
  return highway_names

# o.b.v. naam van de weg de coordinaten ophalen
def fetch_way_coordinates(way_name):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json][timeout:25];
    area(3602323309)->.nederland;
    (
      way(area.nederland)["ref"="{way_name}"];
    );
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    response.raise_for_status()  
    data = response.json()
    nodes = {node['id']: (node['lon'], node['lat']) for node in data['elements'] if node['type'] == 'node'}
    ways = [element for element in data['elements'] if element['type'] == 'way']
    lines = []

    for way in ways:
        way_nodes = way['nodes']
        line_coords = [nodes[node_id] for node_id in way_nodes if node_id in nodes]
        lines.append(LineString(line_coords))

    gdf = gpd.GeoDataFrame(geometry=lines)
    gdf['wegnaam'] = way_name
    return gdf

# maakt shapefile 
def save_to_shapefile(gdf, output_path):
    gdf.to_file(output_path, driver='ESRI Shapefile', crs="EPSG:4326")
    print("Shapefile saved successfully.")

def gather_all_files(dir_path, processed_files):
    file_paths = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.shp'):
            file_path = os.path.join(dir_path, filename)
            if file_path not in processed_files:
                file_paths.append(file_path)
                processed_files.append(file_path)
    return file_paths, processed_files

# voegt shapefile toe als nieuwe laag binnen QGIS 
def add_layers_from_files(file_paths):
    for path in file_paths:
        layer_name = os.path.basename(path).split('.')[0]
        layer = QgsVectorLayer(path, layer_name, 'ogr')
        if layer.isValid():
            layer.setCrs(crs)
            QgsProject.instance().addMapLayer(layer)
            print(f'Layer {layer_name} added successfully.')
        else:
            print(f'Layer {layer_name} failed to load!')

shp_output_dir = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data'
shp_read_dir = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data\\'
way_names_file = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\highway_names.txt'
crs = QgsCoordinateReferenceSystem('EPSG:4326')


way_names = read_highway_names(way_names_file) 
processed_files = [] # houdt bij welke wegen al als laag zijn toegevoegd om duplicatie te voorkomen binnen QGIS 
for way_name in way_names:
    output_file_path = os.path.join(shp_output_dir, f"{way_name}.shp")
    gdf = fetch_way_coordinates(way_name)
    save_to_shapefile(gdf, output_file_path)
    file_paths, processed_files = gather_all_files(shp_read_dir, processed_files)
    add_layers_from_files(file_paths)
    iface.mapCanvas().refreshAllLayers()
    
