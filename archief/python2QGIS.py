"""
DIT RUN JE BINNEN DE PYTHON CONSOLE VAN QGIS
"""

from qgis.core import QgsVectorLayer, QgsProject
import os

# hierin zitten alle .shp files
dir_path = r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data\\'

# voegt alle .shp files toe aan een lijst
file_paths = []
for filename in os.listdir(dir_path):
    if filename.endswith('.shp'):
        file_path = dir_path + filename
        file_paths.append(file_path)

# per file maakt die een laag en voegt deze toe aan het project
def add_layers_from_files(file_paths):
    for path in file_paths:
        layer = QgsVectorLayer(path, os.path.basename(path), 'ogr')
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            print(f'Layer {os.path.basename(path)} added successfully.')
        else:
            print(f'Layer {os.path.basename(path)} failed to load!')

add_layers_from_files(file_paths)

iface.mapCanvas().refreshAllLayers()
