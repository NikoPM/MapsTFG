from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os

class RoutesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        


        # Se añaden los layouts al principal
        self.layout.addWidget(mapContainer, 1)
