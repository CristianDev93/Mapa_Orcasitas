import html
from bs4 import BeautifulSoup
from .manejo_datos import manejo_datos as md

""""""


class estilos:

    # Metodo que da color a los poligonos, segun la superficie disponible.
        
    def superficie(feature):
        """Aplica un estilo según la superficie disponible o datos de irradiación."""
        superficie = feature['properties'].get('Tejado_Disponible_m2', 0)
        if superficie in range(0, 21):
            return {'fillColor': '#FFFFB2', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(20, 81):
            return {'fillColor': '#FECC5C', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(80, 401):
            return {'fillColor': '#FD8D3C', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(400, 801):
            return {'fillColor': '#F03B20', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(800, 1604):
            return {'fillColor': '#BD0026', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        else:
            return {'fillColor': '#FFFFFF', 'weight': 2, 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}

    # Metodo que genera un texto HTML con datos de los edificios.
    def crear_contenido_popup(feature):
        """
        Genera el estilo del pop up y añade contenido extraido del un GeoJson.
        """
        id = feature['id']
        ref_catastral = feature['properties']['Referencia_Catastral']
        uso = html.escape(feature['properties']['Uso'])
        tejado_disp = feature['properties']['Tejado_Disponible_m2']
        irradiacion = [feature["properties"]
                       [f'Radiacion_kWh_m2_{i}'] for i in range(1, 13)]
        energia = [feature["properties"]
                   [f"Energia_KWh_{j}"] for j in range(1, 13)]
        radiacion_Anual = feature["properties"]['Radiacion_kWh_m2_Anual']
        energia_anual = feature["properties"]["Energia_KWh_Anual"]
        img_base_i =  md.generar_grafico(irradiacion)
        img_base_e = md.generar_gra_energia(energia)
        html_popup = f"""
        <link rel = "stylesheet" href= "./css/estilos_popup.css">
        <div id="pop-up-{id}" data-id="{id}">
            <div style="background-color: #194470;">
                <h4 style="color: white;">Información del edificio</h4>
            </div>
            <b>Referencia catastral: </b> {ref_catastral}</br>
            <b>Uso: </b> {uso} <br>
            <b id = "tejado-sup-{id}">Tejado disponible:{tejado_disp}</b></br>
            <b>Radiación kWh m2 Anual:</b> {radiacion_Anual}</br>
            <b>Energía KWh Anual:</b> {energia_anual}</br>
            <details>
                <summary>Grafico irradiación kWh m2 mensula</summary>
                <div>
                    <img id="grafico" src="data:image/png;base64,{img_base_i}">
                </div>
            </details>
            
             <details>
                <summary>Grafico energía KWh mensual</summary>
                <div>
                    <img id="grafico" src="data:image/png;base64,{img_base_e}">
                </div>
            </details>
            
            <details>
                <summary>Calculadora de paneles</summary>
                <div>
                    <p>Introduce los datos para calcular el número de paneles necesarios:</p>
                    <label><b>Consumo Anual (kWh):</b></label>
                    <input type="number" id="consumo-anual-{id}" step="any" placeholder="Ej. 5000"><br>
                    <b>Selecciona la potencia del panel:</b>
                    <select id="potencia-panel-{id}">
                        <option value="0.44">0.44 kW</option>
                        <option value="0.49">0.49 kW</option>
                        <option value="0.59">0.59 kW</option>
                    </select><br>
                    <button id="btn-calcular-{id}">Calcular</button>
                    <p><b id="resultado-calculo-{id}" style="margin-top: 10px;"></b></p>
                    <p><b id="icono-estado-{id}"></b></p>
                </div>
            </details>
        </div>
        """

        return html_popup

    # Genera una cabezera para añadir al archivo html.
    def generar_cabecera(pat_html):
        """
        Añade la cabecera al mapa ya creado.
        Args: archivo HTML al cual se le añade el la cabecera. 
        """
        try:
            with open(pat_html, 'r', encoding='utf-8') as file:
                contenido = BeautifulSoup(file, 'html.parser')

            cabezera_html = '''
                <link rel = "stylesheet" href= "./css/estilos_header.css">
            
                <div id="header">
                    <div>
                       <img src="./logos/ciemat.png" alt="Logo CIEMAT" class="colaborador-logo">
                        <img src="./logos/politecnica.png" alt="Logo Universidad politecnica" class="colaborador-logo">
                        <img src="./logos/logo_canaveral.png" alt="Logo cañaveral" class="colaborador-logo">
                    </div>
                    <h1 class = "titulo">Comunidad Energética en Orcasitas</h1>
                    <script src ="./calcular_paneles.js" defer></script>
                </div>
            '''
            body = contenido.find('body')
            body.insert(0, BeautifulSoup(cabezera_html, 'html.parser'))

            with open(pat_html, 'w', encoding='utf-8') as file:
                file.write(str(contenido))

        except FileNotFoundError:
            print('El archivo HTML no existe.')
    