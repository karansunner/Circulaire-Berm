import requests
from shapely.geometry import LineString, Point
import geopandas as gpd


def fetch_way_coordinates(way_name):
    # Overpass API URL
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Overpass query to fetch the way by its name and associated nodes
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
    response.raise_for_status()  # Raise an error if the request failed
    data = response.json()

    # Verwerk de gegevens en maak de LineStrings
    nodes = {node['id']: (node['lon'], node['lat']) for node in data['elements'] if node['type'] == 'node'}
    ways = [element for element in data['elements'] if element['type'] == 'way']
    lines = []

    for way in ways:
        way_nodes = way['nodes']
        line_coords = [nodes[node_id] for node_id in way_nodes if node_id in nodes]
        if line_coords:  # Als er coördinaten zijn, maak dan een LineString
            print(f"Way ID: {way['id']} - Line Coordinates: {line_coords}")  # Print de coördinaten
            lines.append(LineString(line_coords))
        else:
            print(f"Geen coördinaten gevonden voor weg ID: {way['id']}")  # Print een foutmelding

    return lines


# Pas de variabele way_name aan naar de weg die moet worden geplot
# way_name = "N11"

def create_shp_file(way_name):
    # way_name = input('Voer weg naam in: ')
    lines = fetch_way_coordinates(way_name)
    if lines:
        print(f"Er zijn {len(lines)} lijnen gevonden.")
    else:
        print("Er zijn geen lijnen gevonden voor deze wegnaam.")
    def create_shp_from_lines(lines, file_path):
        # Create a GeoDataFrame from the LineStrings
        gdf = gpd.GeoDataFrame(geometry=lines, crs="EPSG:4326")
        gdf.to_file(file_path, driver='ESRI Shapefile')

    # Verander de onderstaande regel naar het pad waar je het bestand wilt opslaan, dit moet als .shp file
    output_file_path = "data/N11_weg.shp"
    create_shp_from_lines(lines, output_file_path)


def niks():
    return 1+1
