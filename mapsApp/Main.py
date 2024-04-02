import sys
import folium
from VehiclesWindow import VehicleWindow
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLineEdit, QComboBox, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFile, QTextStream
import os
import tempfile
import crearYEntrenar


#Clase de la ventana principal
class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('TFG Nicolás')  # Titulo de la ventana      
        self.show()  # Método para abrir la ventana
        self.vehicles_tab = VehicleWindow()
        self.initUI()   # Método con los parámetros de la ventana
 

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
        self.txt_iteraciones = QLineEdit('n_iteraciones')
        self.txt_timesteps = QLineEdit('n_timesteps')
        self.txt_modelname_load_model = QLineEdit('model_name')
        self.txt_episodes = QLineEdit('episodes')
        self.combo_options = QComboBox()
        self.combo_options.setStyleSheet("QComboBox { background-color: white; font-size: 12px; }")
        self.combo_options.addItem("Seleccione el algoritmo")
        self.combo_options.addItems(["PPO", "A2C", "DQN"])  # ComboBox con los algoritmos disponibles

        # Botones
        self.btn_load_case = QPushButton('Cargar Caso')
        self.btn_load_case.clicked.connect(self.vehicles_tab.load_case)  # Conecta con el método load_case
        self.btn_train = QPushButton('Entrenar desde 0')
        self.btn_load_model = QPushButton('Cargar Modelo')
        self.btn_train.clicked.connect(lambda: self.train(self.txt_iteraciones.text(), self.txt_timesteps.text(), self.txt_modelname_train.text()))
        self.btn_load_model.clicked.connect(lambda: self.load_model(self.txt_modelname_load_model.text(), self.txt_episodes.text()))

        # Formato
        self.txt_iteraciones

        
        # Añade los controles al layout de controles
        controls_layout.addWidget(self.combo_options)
        controls_layout.addWidget(self.btn_train)
        controls_layout.addWidget(self.txt_iteraciones)
        controls_layout.addWidget(self.txt_timesteps)
        controls_layout.addWidget(self.btn_load_model)
        controls_layout.addWidget(self.txt_modelname_load_model)
        controls_layout.addWidget(self.txt_episodes)

        # Añade los botones al layout del mapa
        map_buttons_layout = QHBoxLayout()
        map_buttons_layout.addWidget(self.btn_load_case)
        map_layout.addLayout(map_buttons_layout)



        # Añade los layouts de mapa y controles al layout principal
        main_layout.addWidget(contenedor)
        main_layout.addLayout(map_layout, 3)
        main_layout.addLayout(controls_layout, 1)

        # Widget central para contener el layout principal


    #Funciones de los botones
    
    """Función del boton crear y entrenar desde 0"""
    def train(self, iteraciones, timesteps, modelname, nVehiculos, nNodos):
        
        initialPath = os.path.join("mapsApp/Cases")
        # Abre el cuadro de diálogo para seleccionar una carpeta
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        folderPath = QFileDialog.getExistingDirectory(self, "Selecciona carpeta donde guardar el resultado", initialPath, options=options)
        logdir = folderPath + "/log"

        # Procede a llamar a la clase crearYEntrenar
        gym = crearYEntrenar
        gym.entrenarDesdeCero(self.combo_options.currentText(), folderPath, logdir, iteraciones, timesteps, nVehiculos, nNodos)

    def load_model(self, modeldir, modelname, episodes):
        # Lógica para cargar el modelo
        print(modeldir, modelname, episodes)

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
