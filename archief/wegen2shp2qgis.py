import requests
from shapely.geometry import LineString
import geopandas as gpd
from qgis.core import QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
import os

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
        if line_coords:
            print(f"Way ID: {way['id']} - Line Coordinates: {line_coords}")  
            lines.append(LineString(line_coords))
        else:
            print(f"Geen coördinaten gevonden voor weg ID: {way['id']}") 
    return lines

def create_shp_file(way_name, shp_output_dir):
    lines = fetch_way_coordinates(way_name)
    if lines:
        print(f"Er zijn {len(lines)} lijnen gevonden.")
    else:
        print("Er zijn geen lijnen gevonden voor deze wegnaam.")
    def create_shp_from_lines(lines, file_path):
        gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")
        gdf.to_file(file_path, driver='ESRI Shapefile')
    output_file_path = shp_output_dir
    create_shp_from_lines(lines, output_file_path)

def gather_all_files(dir_path):
    file_paths = []
    for filename in os.listdir(dir_path):
        if filename.endswith('.shp'):
            file_path = dir_path + filename
            file_paths.append(file_path)
    return file_paths

def add_layers_from_files(file_paths):
    for path in file_paths:
        layer = QgsVectorLayer(path, os.path.basename(path), 'ogr')
        if layer.isValid():
            layer.setCrs(crs)
            QgsProject.instance().addMapLayer(layer)
            print(f'Layer {os.path.basename(path)} added successfully.')
        else:
            print(f'Layer {os.path.basename(path)} failed to load!')

shp_output_dir = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data'
shp_read_dir = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data\\'
crs = QgsCoordinateReferenceSystem('EPSG:4326')
way_name = 'A10'
create_shp_file(way_name, shp_output_dir)
file_paths = gather_all_files(shp_read_dir)
add_layers_from_files(file_paths)
iface.mapCanvas().refreshAllLayers()
