from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QTextEdit, QPushButton
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
        
        # Layout de las rutas
        rutaLayout = QHBoxLayout()
        rutaContainer = QWidget()
        self.textoRutas = QTextEdit()
        rutaLayout.addWidget(self.textoRutas)

        # Se añaden las rutas
        rutaContainer.setLayout(rutaLayout)
        rutaLayout.addWidget(self.textoRutas)

        # Se añaden los layouts al principal
        self.layout.addWidget(mapContainer, 1)
        self.layout.addWidget(rutaContainer)

        # Boton de prueba
        boton = QPushButton("pulsa")
        boton.clicked.connect(lambda: self.showFileDialog())
        mapLayout.addWidget(boton)

    def showFileDialog(self):
        # Directorio inicial configurado para la carpeta del proyecto
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "",
                                                  "Text Files (*.txt)", options=options)
        if fileName:
            self.loadTextFromFile(fileName)

    def loadTextFromFile(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()  # Lee todas las líneas del archivo
                text = ''.join(lines[1:])  # Une todo excepto la primera línea
                self.textoRutas.setText(text)  # Establece el texto en el widget de texto
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
