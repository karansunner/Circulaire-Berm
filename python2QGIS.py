"""
DIT RUN JE BINNEN DE PYTHON CONSOLE VAN QGIS
"""

from qgis.core import QgsVectorLayer, QgsProject
import os

def add_layers_from_files(file_paths):
    for path in file_paths:
        layer = QgsVectorLayer(path, os.path.basename(path), 'ogr')
        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            print(f'layer {os.path.basename(path)} added')
        else:
            print(f'layer {os.path.basename(path)} failed')

# voor nu lokaal, straks willen we refereren naar of cosmos db of de blob storage.
file_paths = [
    r'C:\Users\singh\Documents\INMINDAEN-Python-Code\db2qgis\data\Ecologisch_beheer_1e_meter.shp'
]

add_layers_from_files(file_paths)
iface.mapCanvas().refreshAllLayers()