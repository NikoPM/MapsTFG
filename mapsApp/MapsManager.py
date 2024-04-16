from bs4 import BeautifulSoup, Comment
import re
import os


class MapsManager:
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
    
    def dibujarRuta(mapaRoute, newMapaRoute, ruta):
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
                    # Buscamos todas las ocurrencias de marcadores en la etiqueta de script
                    matches = re.findall(r"L\.marker\(\[(.*?)\]\)\.addTo", tag.string)
                    for match in matches:
                        # Dividimos las coordenadas del marcador y extraemos el índice
                        lat, lon = map(float, match.split(","))
                        # Buscamos el índice del marcador en la etiqueta de script
                        index_match = re.findall(r'Marcador (\d+):', tag.string)
                        print(index_match)
                        if index_match:
                            index = i
                            i+=1
                            print(index)
                            all_markers.append((index, lat, lon))

            # Ordenamos los marcadores por su índice
            all_markers.sort(key=lambda x: x[0])

            # Creamos la ruta dinámicamente
            print(all_markers)
            ruta_lines = []
            atributos = "{patterns: [{offset: 25,repeat: 50,symbol: L.Symbol.arrowHead({pixelSize: 10,polygon: false,pathOptions: {stroke: true,color: 'red'}})}]}"
            indice = 0  
            for i in range(0, len(ruta) - 1):
                marker_start = all_markers[ruta[i]]
                marker_end = all_markers[ruta[i + 1]]
                print(marker_start)
                ruta_lines.append(f"var polyline{indice}= L.polyline([[{marker_start[1]}, {marker_start[2]}], [{marker_end[1]}, {marker_end[2]}]], {{color: 'red'}}).addTo(map_5499b0ea0329795cfd0970b133c0823b);")
                indice+=1
            indice = 0  
            for i in range(0, len(ruta) - 1):        
                ruta_lines.append(f"var arrowDecorator{indice} = L.polylineDecorator(polyline{indice}, {atributos});")
                ruta_lines.append(f"arrowDecorator{indice}.addTo(map_5499b0ea0329795cfd0970b133c0823b);")
                indice+=1
            # Agregamos las líneas de ruta al final del último script
            if ruta_lines:
                if script_tags:
                    last_script_tag = script_tags[-1]
                    last_script_tag.string += "\n" + "\n".join(ruta_lines)

            # Guardamos el mapa actualizado en el archivo HTML
            with open(newMapaRoute, 'w', encoding='utf-8') as file_mod:
                file_mod.write(str(soup))
            print("Mapa guardado")
