from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QTextEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import re
import pandas as pd
from MapsManager import MapsManager


class RoutesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mapsM = MapsManager()


    def initUI(self):
        self.layout = QHBoxLayout(self)
        # Layout del mapa
        mapLayout = QVBoxLayout()
        mapContainer = QWidget()
        mapContainer.setLayout(mapLayout)

        # Inicialización del mapa
        ruta_mapa = os.path.abspath("Mapas/mapabase.html")
        url = QUrl.fromLocalFile(ruta_mapa)
        # Crea un QWebEngineView como contenedor del mapa de Folium y se implementa al layout del mapa
        self.web_view = QWebEngineView()
        self.web_view.load(url)
        mapLayout.addWidget(self.web_view)
        
        # Layout de las rutas
        rutaLayout = QHBoxLayout()
        rutaContainer = QWidget()
        self.textoRutas = QTextEdit("No hay solución. Se necesita cargar un modelo")
        rutaLayout.addWidget(self.textoRutas)

        # Se añaden las rutas
        rutaContainer.setLayout(rutaLayout)
        rutaLayout.addWidget(self.textoRutas)

        # Se añaden los layouts al principal
        self.layout.addWidget(mapContainer, 1)
        self.layout.addWidget(rutaContainer)

    """Lee el fichero de texto con las rutas y las convierte en arrays"""
    def extract_arrays_from_file(self):
        self.textoRutas.append('Hola')
        maps = MapsManager.get_instance()
        ruta = maps.case_path + '/Reports/'
        archivos = os.listdir(ruta)
        for archivo in archivos:
            path = archivo
        file_path = ruta + path
        csv_path = os.path.dirname(os.path.dirname(file_path)) + '/nodes.csv'
        arrays = []
        with open(file_path, 'r') as file:
            for line in file:
                # Busca líneas que contienen un patrón de array
                match = re.search(r'\[(.*?)\]', line)
                if match:
                    # Extrae el contenido dentro de los corchetes y conviértelo a una lista de enteros
                    array = list(map(int, match.group(1).split(',')))
                    arrays.append(array)

        self.loadRoutes(arrays, csv_path, maps.case_path)

        return arrays
    
    def getArrays(self):
        print("Get Arrays")
        maps = MapsManager.get_instance()
        ruta = maps.case_path + '/Reports/'
        archivos = os.listdir(ruta)
        for archivo in archivos:
            path = archivo
        file_path = ruta + path
        csv_path = os.path.dirname(os.path.dirname(file_path)) + '/nodes.csv'
        arrays = []
        with open(file_path, 'r') as file:
            for line in file:
                # Busca líneas que contienen un patrón de array
                match = re.search(r'\[(.*?)\]', line)
                if match:
                    # Extrae el contenido dentro de los corchetes y conviértelo a una lista de enteros
                    array = list(map(int, match.group(1).split(',')))
                    arrays.append(array)

        self.loadRoutes(arrays, csv_path, maps.case_path)

        

    def loadRoutes(self, arrays, csv_path, file_path):
        df = pd.read_csv(csv_path)
        all_routes = []
        i = 1
        for array in arrays:
            route = self.generate_route_from_indices(df, array)
            texto = "Ruta "+ str(i) + ": " + route 
            all_routes.append(texto)
            i +=1
        self.actualizarVentana(all_routes, file_path)

    def generate_route_from_indices(self, dataframe, indices):
        route_places = [dataframe.iloc[idx, -1] for idx in indices]
        route = ' -> '.join(route_places)
        return route
    
    def actualizarVentana(self, routes, file_path):
        print("Actualizando rutas")
        for route in routes:
            self.textoRutas.append(route)
            
        self.actualizaMapa(file_path)


    def actualizaMapa(self, path):
        mapa_path = path + '/mapaRuta.html'
        print(mapa_path)
        url = QUrl.fromLocalFile(mapa_path)
        self.web_view.load(url)
        print("mapa rutas actualizado")        

    def si(self):
        self.textoRutas.append("Hola")
        
