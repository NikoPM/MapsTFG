from PyQt5.QtWidgets import QMessageBox


class MessageManager:
    # Funciones para mostrar mensajes por ventana
    def __init__(self):
        super().__init__()
        self.loading_message = None   
      
    def show_warning(self, text: str):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText(text)
        msgBox.setWindowTitle("Advertencia")
        msgBox.exec_()

    def show_loading_message(self):
        # Muestra un mensaje de carga al usuario
        self.loading_message = QMessageBox(None)
        self.loading_message.setWindowTitle("Cargando modelo")
        self.loading_message.setText("Por favor, espera mientras se carga el modelo...")
        self.loading_message.setStandardButtons(QMessageBox.Cancel)
        self.loading_message.show()

    def hide_loading_message(self):
        # Oculta el mensaje de carga
        if self.loading_message:
            self.loading_message.close()