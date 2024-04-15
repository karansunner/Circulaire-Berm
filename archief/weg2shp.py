import geopandas as gpd
import osmnx as ox
 
def get_street_geometry(address):
    try:
        street_graph = ox.graph_from_address(address, network_type='drive')
        street_edges = ox.utils_graph.graph_to_gdfs(street_graph, nodes=False, edges=True)
        street_name = address.split()[0]
        street_geometry = street_edges[street_edges['name'] == street_name]['geometry'].unary_union
        return street_geometry
    except Exception as e:
        print("Er is een fout opgetreden bij het verkrijgen van de straatgeometrie:", e)
        return None
 

address = 'Kantershof Amsterdam'
street_geometry = get_street_geometry(address)
street_gdf = gpd.GeoDataFrame(geometry=[street_geometry])
output_shapefile = "street_geometry.shp"
street_gdf.to_file(output_shapefile)