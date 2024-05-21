import sys
import folium
from VehiclesWindow import VehicleWindow
from RoutesWindow import RoutesWindow
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QComboBox, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFile, QTextStream
import os
import tempfile
import crearYEntrenar
import cargarModelo
from MessageManager import MessageManager
from MapsManager import MapsManager
import threading 


#Clase de la ventana principal
class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('TFG Nicolás')  # Titulo de la ventana      
        self.show()  # Método para abrir la ventana
        self.vehicles_tab = VehicleWindow()
        self.routes_tab = RoutesWindow()
        self.initUI()   # Método con los parámetros de la ventana
        self.cargarModelo = cargarModelo
        self.messageManager = MessageManager()
        self.case_path = None
        self.mapsM = MapsManager()
 

    def initUI(self):
        
        # Tamaño inicial de la ventana
        self.resize(1000, 600)  # Ancho por Alto en píxeles
        
        # Tamaño mínimo de la ventana
        self.setMinimumSize(800, 450)  # Ancho por Alto en píxeles

        # Crear la barra de menú
        menuBar = self.menuBar()
        
        # Crear la pestaña de ajustes
        settingsMenu = menuBar.addMenu('Ajustes')

        # Crear las acciones del menú
        darkModeAction = QAction('Activar modo oscuro', self, triggered=self.activateDarkMode)
        lightModeAction = QAction('Quitar modo oscuro', self, triggered=self.deactivateDarkMode)

        # Añadir las acciones al menú de ajustes
        settingsMenu.addAction(darkModeAction)
        settingsMenu.addAction(lightModeAction)

        # Establece un estilo inicial (opcional)
        self.activateDarkMode()

        # Crea el QTabWidget y lo establece como el widget central de la ventana principal
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Crea el contenido para la primera pestaña
        main_tab = QWidget()
        self.setupMainTab(main_tab)

        # Instancia de la ventana secundaria para la segunda pestaña
        

        # Añade las pestañas al QTabWidget
        self.tab_widget.addTab(main_tab, "Mapa")
        self.tab_widget.addTab(self.vehicles_tab, "Caso")
        self.tab_widget.addTab(self.routes_tab, "Solución")
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        # Verificar si la pestaña seleccionada es la que contiene "Solución"
        if self.tab_widget.tabText(index) == "Solución":
            # Ejecutar el método que deseas cuando se selecciona esa pestaña
            try:
                self.routes_tab.getArrays()
            except:
                pass
    def setupMainTab(self, tab):

        # Layout para el mapa y botones
        contenedor = QWidget()
        map_layout = QVBoxLayout(contenedor)
        
        # Layout para los controles de entrada
        controls_layout = QVBoxLayout()

        # Layout principal que incluye tanto el mapa como los controles
        main_layout = QHBoxLayout(tab)

        # Crear un mapa usando Folium apuntando a Bilbao
        self.map = folium.Map(location=[43.2630, -2.9350], zoom_start=12)  # Coordenadas de Bilbao, España

        # Guardar el mapa en un archivo temporal
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.html')
        self.map.save(tmp_file.name)

        # Crea un QWebEngineView como contenedor del mapa de Folium
        self.web_view = QWebEngineView()
        self.web_view.load(QUrl.fromLocalFile(tmp_file.name))

        # Añade el mapa al layout del mapa
        map_layout.addWidget(self.web_view)

        # Textboxes y ComboBox
        self.txt_iteraciones = QLineEdit('Iteraciones (Default = 10)')
        self.txt_timesteps = QLineEdit('Timesteps (Múltiplos de 2048) (Default = 10.240)')
        self.nVehicles = QLineEdit('Vehiculos (Default = 7)')
        self.nNodos = QLineEdit('Nodos (Default = 20)')
        self.txt_nVehicles2 = QLineEdit('nVehiculos')
        self.txt_nNodes2 = QLineEdit('nNodos')
        self.combo_options = QComboBox()
        self.combo_options.setStyleSheet("QComboBox { background-color: white; font-size: 12px; }")
        self.combo_options.addItem("Seleccione el algoritmo")
        self.combo_options.addItems(["PPO", "A2C", "DQN"])  # ComboBox con los algoritmos disponibles

        # Botones
        self.btn_load_case = QPushButton('Cargar Caso')
        self.btn_load_case.clicked.connect(self.vehicles_tab.load_case)  # Conecta con el método load_case
        self.btn_train = QPushButton('Entrenar desde 0')
        self.btn_load_model = QPushButton('Cargar Modelo')
        self.btn_train.clicked.connect(lambda: self.train(self.txt_iteraciones.text(), self.txt_timesteps.text(), self.nVehicles.text(), self.nNodos.text()))
        self.btn_load_model.clicked.connect(lambda: self.load_model(self.txt_nVehicles2.text(), self.txt_nNodes2.text()))

        # Formato
        self.txt_iteraciones

        
        # Añade los controles al layout de controles
        controls_layout.addWidget(self.combo_options)
        controls_layout.addWidget(self.btn_train)
        controls_layout.addWidget(self.txt_iteraciones)
        controls_layout.addWidget(self.txt_timesteps)
        controls_layout.addWidget(self.nVehicles)
        controls_layout.addWidget(self.nNodos)
        controls_layout.addWidget(self.btn_load_model)
        controls_layout.addWidget(self.txt_nNodes2)
        controls_layout.addWidget(self.txt_nVehicles2)
        # Añade los botones al layout del mapa
        map_buttons_layout = QHBoxLayout()
        map_buttons_layout.addWidget(self.btn_load_case)
        map_layout.addLayout(map_buttons_layout)



        # Añade los layouts de mapa y controles al layout principal
        main_layout.addWidget(contenedor)
        main_layout.addLayout(controls_layout, 1)

        # Widget central para contener el layout principal


    #Funciones de los botones
    
    """Función del boton crear y entrenar desde 0"""
    def train(self, iteraciones, timesteps, nVehiculos, nNodos):
        if self.combo_options.currentText() == "Seleccione el algoritmo":
            MessageManager.show_warning("No hay algoritmo seleccionado")
            return
        initialPath = os.path.join("mapsApp/Models")
        # Abre el cuadro de diálogo para seleccionar una carpeta
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        folderPath = QFileDialog.getExistingDirectory(self, "Selecciona carpeta donde guardar el resultado", initialPath, options=options)
        logdir = folderPath + "log"

        # Procede a llamar a la clase crearYEntrenar
        gym = crearYEntrenar
        if iteraciones == 'Iteraciones (Default = 10)':
            iteraciones = 10
        else:
            iteraciones = int(iteraciones)
        if timesteps == 'Timesteps (Múltiplos de 2048) (Default = 10.240)':
            timesteps = 10240
        else:
            timesteps = int(timesteps)
        if nVehiculos == 'Vehiculos (Default = 7)':
            nVehiculos = 7
        else:
            nVehiculos = int(nVehiculos)
        if nNodos == 'Nodos (Default = 20)':
            nNodos = 20
        else:
            nNodos = int(nNodos)

        self.setEnabled(False)
        self.messageManager.show_loading_message()
        def _train():
            gym.entrenarDesdeCero(self.combo_options.currentText(), folderPath, logdir, iteraciones, timesteps, nVehiculos, nNodos)
            self.setEnabled(True)
            # Oculta el mensaje de espera
            self.messageManager.hide_loading_message()

        thread = threading.Thread(target=_train)
        thread.start()
        


    def load_model(self, nVehicles, nNodes):
        # Define la ruta inicial para el diálogo de apertura de archivos
        initialPath = os.path.abspath("mapsApp/Cases")
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.case_path = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Casos", initialPath, options=options)
        initialPath = os.path.abspath("mapsApp/Models")
        mapMang = MapsManager.get_instance()
        mapMang.case_path = self.case_path
        mapMang.setPath(self.case_path)
        # Abre el cuadro de diálogo para seleccionar un archivo .zip
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        models_path, _ = QFileDialog.getOpenFileName(self, "Cargar Modelo", initialPath, "Modelos (*.zip)", options=options)

        # Verifica si el usuario seleccionó un archivo
        if models_path:
            # Deshabilita la ventana principal mientras se carga el modelo
            self.setEnabled(False)
            # Muestra un mensaje de espera al usuario
            self.messageManager.show_loading_message()

            # Define una función interna para cargar el modelo en un hilo
            
            def _load_model():
                # Cargar el modelo
                
                self.cargarModelo.cargarModelo(models_path, nVehicles, nNodes, self.case_path)
                self.messageManager.hide_loading_message()
                # Una vez cargado, vuelve a habilitar la ventana principal
                self.setEnabled(True)
                # Oculta el mensaje de espera
                """except:
                    self.messageManager.hide_loading_message()
                    # Una vez cargado, vuelve a habilitar la ventana principal
                    self.setEnabled(True)
                    # Oculta el mensaje de espera
                    self.messageManager.show_warning("Error")
                    pass"""
                
            

            # Crea un hilo para cargar el modelo
            thread = threading.Thread(target=_load_model)

             # Inicia el hilo
            thread.start()

    """Métodos para la modificación de la interfaz"""

    def activateDarkMode(self):
        self.applyStyleSheet("Styles/blackStyle.qss")

    def deactivateDarkMode(self):
        self.applyStyleSheet("Styles/style.qss")

    def applyStyleSheet(self, styleSheetFile):
        # Asegura que la ruta sea relativa al directorio actual del script
        basePath = os.path.dirname(os.path.abspath(__file__))
        filePath = os.path.join(basePath, styleSheetFile)

        file = QFile(filePath)
        if not file.open(QFile.ReadOnly | QFile.Text):
            print(f"No se pudo abrir el archivo de estilos: {styleSheetFile}")
            return
        
        stream = QTextStream(file)
        self.setStyleSheet(stream.readAll())




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MapWindow()
    window.show()
    sys.exit(app.exec_())
