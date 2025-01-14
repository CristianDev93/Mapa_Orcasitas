import folium
import json
import folium.features
from folium.plugins import MiniMap, Geocoder, MousePosition
from .estilos_map import estilos as st 
from branca.element import Element

class GeneradorMap:
    
    def __init__(self, ruta_datos, ruta_salida):
        """
        Constructor.
        param => ruta_datos: ruta del archivo json con los datos de edificios
        param => ruta_salida: tura del archivo en el cual se va a almacenar el mapa.
        param => map: genera un objeto de tipo folium map.
        """
        self.ruta_datos = ruta_datos
        self.ruta_sallida = ruta_salida
        
        self.mapa = folium.Map(location=[40.36989654728313, -3.715546018233464],
                                zoom_start=15,
                                max_zoom=18,
                                min_zoom=6,
                                width= "100%",
                                height="92%")

    def cargar_datos(self):
        """
        Carga los datos contenidos en los archivos GeoJson.
        """
        try:
            with open(self.ruta_datos, "r", encoding= "utf-8") as file:
                return json.load(file)
        except FileExistsError:
            raise FileNotFoundError("El archivo JSON no se encontró.")
        except json.JSONDecodeError:
            
            raise ValueError("El archivo JSON no tiene un formato válido.")

    def add_capas(self, datos):
        """
        Añade las capas al mapa.
        parametros: datos => Datos cargados del archivo GeoJSON.
        """
        #Capa de google satelite
        folium.TileLayer(
            tiles= "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satelite",
            name= "Google Satelite",
            overlay=True,
            control= True,
            show= False
        ).add_to(self.mapa)
        # Capa irradiación solar CIEMAT
        folium.TileLayer(
            tiles= "http://localhost:8000/datos/teselas_irradiacion_6_20/{z}/{x}/{y}.png",
            attr= "Irradiación solar CIEMAT",
            name= "Irradiación solar anual",
            control= True,
            overlay= True,
            show= False,
        ).add_to(self.mapa)
        
        poligono = folium.GeoJson(
            data= datos,
            style_function= st.superficie,
            name= "Superficie disponible m\u00B2 y datos de los edificios CIEMAT",
            show=True,
            control= True
        )
        
        # TODO: se itera sobre cada elemento del objeto polígono y se genera el contenido para cada pop-up.
        for feature in poligono.data['features']:
            
            feature["properties"]["datos"] = st.crear_contenido_popup(feature)
        
        # TODO: se añade un pop-up para cada poligono que se extrae de la propiedad "datos", y se añaden al mapa      
        poligono.add_child(
            folium.features.GeoJsonPopup(
                fields=["datos"],
                parse_html = True,
                labels= False,
                localize= True,
                popup_options = {"autoPan" : True,
                                 "offset": [0, -50],
                                 "outoPanPadding": [10, 10]})).add_to(self.mapa)
    
    def add_pluguins(self):
        """
        Añadi plugins al mapa
        """
        MiniMap(
            toggle_display = True,
            width= 150,
            height= 150
        ).add_to(self.mapa)
        Geocoder().add_to(self.mapa)
        MousePosition().add_to(self.mapa)
        folium.LayerControl().add_to(self.mapa)
    
    def add_leyenda(self):
        """
        Añade una leyenda al mapa con los estilos definidos.
        """
        leyenda_html = '''
                <div style="
                position: fixed; 
                bottom: 50px; left: 50px; width: 290px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:12px;
                padding: 10px;">
                <h4> Leyendas </h4>
                
                <details>
                    <summary><b>Irradiación Solar</b></summary>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FE230A; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.750 - 2.020 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FF9A0B; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.500 - 1.750 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#F8DD1C; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.250 - 1.500 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FFFF73; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.000 - 1.250 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#B4FD77; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        750 - 1.000 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#89F0CC; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        500 - 750 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#3ACEFE; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        250 - 500 kWh m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#6B73FD; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        0 - 250 kWh m²<br>
                    </div>
                </details>
                
                <details>
                    <summary><b>Superficie Disponible</b></summary>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FFFFB2; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        0 - 20 m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FECC5C; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        20 - 80 m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FD8D3C; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        80 - 400 m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#F03B20; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        400 - 800 m²<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#BD0026; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        800 - 1600 m²<br>
                    </div>
                </details>
            </div>
        '''
        leyenda_elemento = Element(leyenda_html)
        self.mapa.get_root().html.add_child(leyenda_elemento)
        
    def guardar_mapa(self):
        """ 
        Guarda el mapa en un archivo HTML.
        """
        file = self.cargar_datos()
        self.add_capas(file)
        self.add_pluguins()
        self.add_leyenda()
        self.mapa.save(self.ruta_sallida)
        st.generar_cabecera(".\public_html\index_orcasitas.html")
        