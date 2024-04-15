from bs4 import BeautifulSoup, Comment
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