from bs4 import BeautifulSoup, Comment
import re
import os


class MapsManager:
    _instance = None
    case_path = "None"
    @staticmethod
    def get_instance():
        if MapsManager._instance is None:
            MapsManager._instance = MapsManager()
        return MapsManager._instance
    
    def crearMapaAlCargar(mapaRoute, coordenadas):
       # Cargar el archivo HTML existente
        originalRoute = os.path.abspath("Mapas/mapaInteracciones.html")

        with open(originalRoute, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, "html.parser")

        # Encuentra todas las etiquetas de script
        script_tags = soup.find_all("script")

        # Generar el nuevo código JavaScript para añadir marcadores
        nuevo_js = "\n\n"
        for index, (lat, lon) in enumerate(coordenadas, start=0):
            nuevo_js += f"L.marker([{lat}, {lon}]).addTo(map_5499b0ea0329795cfd0970b133c0823b).bindPopup('Marcador {index}: Lat: {lat}, Lon: {lon}');\n"


        # Asumiendo que quieres añadir el código al final del último script
        if script_tags:
            # Añadir el nuevo código JS al contenido del último script
            script_tags[-1].string = (script_tags[-1].string or '') + nuevo_js

        # Guardar el archivo HTML modificado
        with open(mapaRoute, 'w', encoding='utf-8') as file_mod:
            file_mod.write(str(soup))

        print("HTML modificado guardado.")

    def actualizarMapa(mapaRoute, coordenadas):
    
        with open(mapaRoute, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, "html.parser")

                # Encuentra todas las etiquetas de script
                script_tags = soup.find_all("script")

                # Generar el nuevo código JavaScript para añadir marcadores
                nuevo_js = "\n\n"
                for lat, lon in coordenadas:                   
                    nuevo_js += f"L.marker([{lat}, {lon}]).addTo(map_5499b0ea0329795cfd0970b133c0823b).bindPopup('Lat: {lat}, Lon: {lon}');\n"

                # Asumiendo que quieres añadir el código al final del último script
                if script_tags:
                    # Añadir el nuevo código JS al contenido del último script
                    script_tags[-1].string = (script_tags[-1].string or '') + nuevo_js

                # Guardar el archivo HTML modificado
                with open(mapaRoute, 'w', encoding='utf-8') as file_mod:
                    file_mod.write(str(soup))

                print("HTML modificado guardado.")
    
    def dibujarRutas(mapaRoute, newMapaRoute, rutas):
        with open(mapaRoute, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, "html.parser")

            # Encuentra todas las etiquetas de script
            script_tags = soup.find_all("script")

            # Inicializamos una lista para almacenar los marcadores
            all_markers = []
            i = 0
            # Buscamos todos los marcadores en las etiquetas de script
            for tag in script_tags:
                if tag.string:
                    matches = re.findall(r"L\.marker\(\[(.*?)\]\)\.addTo", tag.string)
                    for match in matches:
                        lat, lon = map(float, match.split(","))
                        index_match = re.findall(r'Marcador (\d+):', tag.string)
                        if index_match:
                            index = i
                            i += 1
                            all_markers.append((index, lat, lon))

            # Ordenamos los marcadores por su índice
            all_markers.sort(key=lambda x: x[0])

            # Colores para las rutas
            colores = ['red', 'blue', 'green', 'yellow', 'purple', 'orange']
            ruta_lines = []
            
            # Recorremos cada una de las rutas
            for ruta_idx, ruta in enumerate(rutas):
                color = colores[ruta_idx % len(colores)]
                atributos = f"{{patterns: [{{offset: 25, repeat: 50, symbol: L.Symbol.arrowHead({{pixelSize: 10, polygon: false, pathOptions: {{stroke: true, color: '{color}'}}}})}}]}}"
                
                # Dibujamos cada segmento de la ruta
                for i in range(len(ruta) - 1):
                    marker_start = all_markers[ruta[i]]
                    marker_end = all_markers[ruta[i + 1]]
                    ruta_lines.append(f"var polyline{ruta_idx}_{i} = L.polyline([[{marker_start[1]}, {marker_start[2]}], [{marker_end[1]}, {marker_end[2]}]], {{color: '{color}'}}).addTo(map_5499b0ea0329795cfd0970b133c0823b);")
                    ruta_lines.append(f"var arrowDecorator{ruta_idx}_{i} = L.polylineDecorator(polyline{ruta_idx}_{i}, {atributos}).addTo(map_5499b0ea0329795cfd0970b133c0823b);")

            # Agregamos las líneas de ruta al final del último script
            if ruta_lines and script_tags:
                last_script_tag = script_tags[-1]
                last_script_tag.string += "\n" + "\n".join(ruta_lines)

            # Guardamos el mapa actualizado en el archivo HTML
            with open(newMapaRoute, 'w', encoding='utf-8') as file_mod:
                file_mod.write(str(soup))
            print("Mapa guardado")


    def extraerArraysSolucion(file_path):
        arrays = []
        with open(file_path, 'r') as file:
            for line in file:
                # Busca líneas que contienen un patrón de array
                match = re.search(r'\[(.*?)\]', line)
                if match:
                    # Extrae el contenido dentro de los corchetes y conviértelo a una lista de enteros
                    array = list(map(int, match.group(1).split(',')))
                    arrays.append(array)
        return arrays
    
    def setPath(self, path):
        self.case_path = path