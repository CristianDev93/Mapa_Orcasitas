# Proyecto Mapa Interactivo Comunidad Energética en Orcasitas 🗺️
Este proyecto tiene como objetivo la creación de un mapa interactivo que visualiza la superficie disponible en los tejados de los edificios en Orcasitas, Madrid. Además, se calcula la cantidad de paneles solares necesarios para cubrir el consumo energético de la comunidad, basado en la radiación solar y el área disponible en los tejados.

---
## Estructura de lproyecto 

## 1. **Generador de Mapa (`GeneradorMap`)**

Esta clase se encarga de la creación del mapa interactivo utilizando `folium`, tambien añade capas, como la de radiación solar y superficie de los tejados con su correspondiente pop-up 💭.

### **Librerías y Componentes Importados**

1. **`folium`**: Una biblioteca de Python para la visualización de datos geoespaciales en mapas interactivos.
2. **`json`**: Biblioteca estándar de Python para trabajar con datos en formato JSON.
3. **`folium.features`**: Módulo de Folium que proporciona funcionalidades para trabajar con GeoJSON y pop-ups.
4. **`folium.plugins`**: proporciona clases que nos permiten añadir plugins como:
  - **`MiniMap`**: Añade un minimapa.
  - **`Geocoder`**: Permite buscar direcciones.
  - **`MousePosition`**:  Muestra las cordenadas en las que se encuentra el puntero del raton.
5. **`estilos_map.estilos as st`**: Clase que proporciona metos para dar estilo a las capas e interfaz  web.
6. **`branca.element.Element`**:   Clase de la biblioteca Branca, que se utiliza para añadir elementos html al mapa.

## **Métodos:**


### `__init__(self, ruta_datos, ruta_salida)`
- **Descripción**: Constructor.
  - `ruta_datos`: Ruta del archivo GeoJSON que contiene la información sobre los tejados.
  - `ruta_salida`: Ruta donde se guardará el mapa generado.
  - `mapa`: genera un objeto de tipo folium map.

    ```python
    def __init__(self, ruta_datos, ruta_salida):
        """
        Constructor.
        param => ruta_datos: ruta del archivo json con los datos de edificios
        param => ruta_salida: ruta del archivo en el cual se va a almacenar el mapa.
        param => map: genera un objeto de tipo folium map.
        """
        self.ruta_datos = ruta_datos
        self.ruta_salida = ruta_salida
        
        self.mapa = folium.Map(location=[40.36989654728313, -3.715546018233464],
                            zoom_start=15,
                            max_zoom=18,
                            min_zoom=6,
                            width="100%",
                            height="92%")
    ```

### `cargar_datos(self)`
  - **Descripción**: Carga el archivo GeoJSON con los datos de los tejados de los edificios. Utiliza la librería `fiona` para leer los archivos.
  - **Salida**: devuelve un diccionario con los datos de los tejados.

    ```python
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
    ```
            

### `add_capas(self, datos)`
  - **Descripción**: Añade capas al mapa.
  - **Entrada**: `datos`: Diccionario con la información de los tejados.

1. **Añadimos dos capas**
```python
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
            name= "Irradiación solar anual CIEMAT",
            control= True,
            overlay= True,
            show= False,
        ).add_to(self.mapa)
```
   Haciendo uso del método `TileLayer` de la librería `foium` se añaden dos capas, una de Google satelite, y otra creada con QGIS a partir de los datos de radiación proporcionados por el CIEMAT la cual se sirve por http o https, esta segunda siendo una capa de teselas que se sirve según el zoom.

---
2. **Se añaden capa de superficie y pop-ups.**
```python
        poligono = folium.GeoJson(
            data= datos,
            style_function= st.superficie,
            name= "Superficie disponible m\u00B2",
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
```
   - **poligono**: Secrea un obgeto de tipo `GeoJSON`
   - **for**: En el bucle se recorre cada `feature` o propiedad del objeto y se almacenan en la propiedad `"datos"` de cada feature.
   - **poligono.add_chld**: Se vincula cada poligono con su pop-up correspondiente.
                                         
### `add_pluguins(self)`
- **Descripción**: Añade plugins interactivos al mapa, como `MiniMap`, `Geocoder` y `MousePosition` para mejorar la interactividad del mapa.
  - `MiniMap`: Muestra añade un mini mapa.
  - `Geocoder`: Permite buscar localizaciones 🔎.
  - `MousePosition`: Muestra las cordenadas donde se encuentra el puntero del raton 🖱️.

```python
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
```

#### `add_leyenda(self)`
- **Descripción**: Añade una leyenda al mapa que muestra información las diferentes capas de irradiación y superficie disponible de los tejado.
  - `leyenda_html`: contiene el texto html y css que formará la leyenda en el mapa.
  - `leyenda_elemento`: Se crea un elemento HTML a partir del bloque de código HTML `leyenda_html`. La clasae `Element` se utiliza para combertir el HTML en un objeto que puede ser insertado en el mapa.
  - ` self.mapa.get_root()`: se encarga de obtener la raiz del mapa.
  - `.html.add_child(leyenda_elemento)`: agrega el elemento a la raiz del mapa. 

```python
  def add_leyenda(self):
        """
        Añade una leyenda al mapa con los estilos definidos.
        """
        leyenda_html = '''
                <div style="
                position: fixed; 
                bottom: 50px; left: 50px; width: 320px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:12px;
                padding: 10px;">
                <h4> Leyendas </h4>
                
                <details>
                    <summary><b>Irradiación Solar CIEMAT</b></summary>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FE230A; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.750 - 2.020<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FF9A0B; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.500 - 1.750<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#F8DD1C; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.250 - 1.500<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#FFFF73; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        1.000 - 1.250<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#B4FD77; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        750 - 1.000<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#89F0CC; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        500 - 750<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#3ACEFE; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        250 - 500<br>
                    </div>
                    <div style="margin-bottom: 5px;">
                        <i style="background:#6B73FD; width: 20px; height: 20px; float: left; margin-right: 8px;"></i>
                        0 - 250<br>
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
```


### `guardar_mapa(self)` 
- **Descripción**: Genera las capas del mapa llamando a los metodos de esta misma clase, guarda el mapa generado en un archivo HTML en la ruta de salida especificada y finalmente lo edita para ñadir la cabecera, llamando al metodo `generar_cabezera ` que esta alojado en la clase `estilos_map`.
- **Salida**: Un archivo HTML con el mapa interactivo generado.
```python
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
```
---

## 2. **Estilos del Mapa (`estilos`)**

Esta clase define cómo se muestran visualmente los elementos del mapa, como la superficie de los tejados y los popups interactivos.
## **Librerías y Componentes Importados**

**1. `import html`**: La librería `html` proporciona funciones para manejar y manipular contenido HTML.
**2. `from bs4 import BeautifulSoup`**: `BeautifulSoup` se utiliza para analizar documentos `html`. 
**3. `from .manejo_datos import manejo_datos as md`**: Clase que es utilizada para generar graficos y devolverlos en base64.

### **Métodos:**

#### `superficie(feature)`
- **Descripción**: Define el estilo visual de los tejados según su superficie. Los tejados más grandes se muestran con un color más oscuro.
- **Entrada**: `feature`: Un diccionario que representa un tejado y sus propiedades.
- **Salida**: Retorna un diccionario con las propiedades de estilo para los tejados.
```python
    def superficie(feature):
        """Aplica un estilo según la superficie disponible o datos de irradiación."""
        superficie = feature['properties'].get('Tejado_Disponible_m2', 0)
        if superficie in range(0, 21):
            return {'fillColor': '#FFFFB2', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(20, 81):
            return {'fillColor': '#FECC5C', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(80, 401):
            return {'fillColor': '#FD8D3C', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(400, 801):
            return {'fillColor': '#F03B20', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        elif superficie in range(800, 1604):
            return {'fillColor': '#BD0026', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
        else:
            return {'fillColor': '#FFFFFF', 'color': '#000000', 'weight': 0.5, 'fillOpacity': 0.7}
```


#### `crear_contenido_popup(feature)`
- **Descripción**: Crea el contenido del popup que se mostrará al hacer clic en los tejados.
- **Entrada**: `feature`: Un dicionario que representa un poligono y sus propiedades.
- **Salida**: Devuelve una cadena de HTML que contiene la información sobre el tejado (referencia catastral, uso, irradiación solar, etc.) y sera utilizado en la clase `GeneradorMap` dentro del metodo `add_capas` en el bucle que recore cada objeto `GEOJSON` generando el contenido para cada pop-up.

```python
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
        radiacion_Anual = [feature["properties"]['Radiacion_kWh_m2_Anual']]
        energia_anual = [feature["properties"]["Energia_KWh_Anual"]]
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
                        <p><b id="resultado-calculo-{id}" style="margin-top: 10px;">El numero de paneles es:</b></p>
                        <p><b id="icono-estado-{id}"></b></p>
                    </div>
                </details>
            </div>
            """
        return html_popup

```

#### `generar_cabecera(pat_html)`
- **Descripción**: Genera la cabecera, que contiene los logos y el título del mapa, para ello se lee el archivo se utiliza `BeautifulSoup` de la libreia `bs4` para crear un objeto que permite guardar le contenido HTML y se guarda en `contenido`, se crea el contenido almacenado en `cabezera_html`, dentro de `contenido` se busca el `body` del HTML, añadimos la cabezera al inicio del HTML con el metodo ` body.insert(0, BeautifulSoup(cabezera_html, 'html.parser'))` y por ultimo escribimos el `contenido` modificado.
- **Entrada**: `pat_html`: El archivo HTML donde se incluirá la cabecera.
- **Salida**: Añade la cabecera al archivo HTML.

```python
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
                    <h1 class = "titulo">Mapa Comunidad solar en Orcasitas</h1>
                    <script src ="./calcular_paneles.js" defer></script>
                </div>
            '''
            body = contenido.find('body')
            body.insert(0, BeautifulSoup(cabezera_html, 'html.parser'))

            with open(pat_html, 'w', encoding='utf-8') as file:
                file.write(str(contenido))

        except FileNotFoundError:
            print('El archivo HTML no existe.')
```

---

## 3. **Generación de Gráficos y Transformación a Base64 (`manejo_datos`)**

Esta clase se encarga de generar los gráficos de irradiación y producción energética, y los combierte a base64, facilitando la inserción directamente en el HTM.

### **Importaciones**

1. **`import matplotlib.pyplot as plt`**: 
   - `matplotlib.pyplot` es una librería utilizada para crear gráficos en Python.
   
2. **`import base64`**:
   - `base64` es una librería estándar en Python que permite codificar y decodificar datos binarios en texto.

3. **`from io import BytesIO`**:
   - `BytesIO` es una clase de la librería `io` un buffer para, en este caso para guardar los graficos en memoria y no en disco.

### **Métodos:**

#### `generar_grafico(irradiacion)`

1. **Definir los Meses**
    ```python
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    ```
    Definimos una lista con los meses del año. Estos serán el eje X en el gráfico de barras.

2. **Crear la Figura y los Ejes**
    ```python
    fig, ax = plt.subplots()
    ```
    Se crea una figura `fig` y un conjunto de ejes `ax` usando `matplotlib`, que nos permite crear el gráfico.

3. **Generar el Gráfico de Barras**
    ```python
    ax.bar(meses, irradiacion)
    ```
    Generamos un gráfico de barras con `meses` como las etiquetas del eje X y los valores de `irradiacion` que se obtine como parameto, como las alturas de las barras. La irradiación se muestra en el eje Y.

4. **Configurar el Gráfico**
    ```python
    ax.set_title('Radiación solar mensual (kWh/m²)')
    ax.set_ylabel('Irradiación (KWh/m²)')
    ```
    - `set_title(...)`: Título del gráfico.
    - `set_ylabel(...)`: Titulo de lo que representan los valores del eje y.

5. **Crear un Buffer de Memoria**
    ```python
    buffer = BytesIO()
    ```
    Se crea un objeto `BytesIO` que es un buffer de memoria. El buffer se usar para guardar la imagen en memoria y no tener que guardarla en disco.

6. **Guardar la Imagen en el Buffer**
    ```python
    plt.savefig(buffer, format="png")
    ```
    El gráfico se guarda en el buffer en formato PNG.

7. **Rewind del Buffer**
    ```python
    buffer.seek(0)
    ```
    Se lleva el puntero del buffer al principio del archivo, para poder leerlo correctamente.

8. **Codificación Base64**
    ```python
    img_base64_ir = base64.b64encode(buffer.read()).decode("utf-8")
    ```
    - `buffer.read()`: Lee los datos del buffer.
    - `base64.b64encode(...)`: Codifica los datos binarios en base64.
    - `.decode("utf-8")`: Convierte la cadena base64 en una cadena de texto.

9. **Cerrar la Figura**
    ```python
    plt.close(fig)
    ```
    Se cierra la figura de `matplotlib` para liberar la memoria.
10. **Retornar la Imagen Codificada**
    ```python
    return img_base64_ir
    ```
    Finalmente, se retorna la cadena base64.

#### `generar_gra_energia(potencia)`

- **Descripción**: Genera un gráfico de barras con la producción de energía mensual, el codigo es exactamente igual que el anterior.
- **Entrada**: `potencia`: valor que se obtiene de un diccionario.
- **Salida**: Retorna el gráfico generado en formato base64.

---

## 4. **Script Principal (`main`)**

Este es el script principal. Carga los datos, genera el mapa interactivo, y lo guarda como un archivo HTML.

### **Método Principal:**

#### `main()`
- **Descripción**: La función principal que ejecuta todo el codigo anterior mente explicado.
  1. Carga los datos desde el archivo GeoJSON.
  3. Genera el mapa interactivo con las capas correspondientes.
  4. Guarda el mapa interactivo en un archivo HTML.

```python
from src.generador_map import GeneradorMap
import os
import traceback
def main():
    """
    Función principal para generar el mapa interactivo.
    """
    # Configuración de rutas
    ruta_datos = os.path.join("datos", "Edificios_Orcasitas.json")
    ruta_salida = os.path.join("public_html", "index_orcasitas.html")

    # Verifica si el archivo de datos existe
    if not os.path.exists(ruta_datos):
        print(f"Error: No se encontró el archivo de datos en {ruta_datos}")
        return

    print("Generando el mapa...")

    # Instancia de la clase GeneradorMap
    generador = GeneradorMap(ruta_datos, ruta_salida)

    
    # Genera el mapa
    try:
        generador.guardar_mapa()
        print(f"Mapa generado exitosamente: {ruta_salida}")
    except Exception as e:
        print(f"Ocurrió un error al generar el mapa: {e}")
        print(traceback.format_exc())
if __name__ == "__main__":
    main()
```

---

## 5. **Script que calcula el número de paneles 🧮**

- **Descripción**: 

Este script se ejecuta cuando se abre un pop-up en un mapa interactivo, permite calcular el número de paneles solares necesarios para generar una cantidad de energía concreta.

### 1. **Evento 'popupopen'**
Cuando se abre un pop-up en el mapa (`map_5630b37a0384eaa561c23f6c52c22886.on('popupopen', function(event)`), se extraen varios datos dinámicos del contenido del pop-up usando su `id`. los cuales son necesarios par que funcione correctamente.
```javascript
    const popup = event.popup;
    const popupContent = popup.getElement();
```

### 2. **Extracción de Información**
Se extraen los valores de:
- **ID`s dinámico** de cada elemento del pop-up.
- **Área del tejado disponible** para la instalación de paneles solares.
- **Valores del consumo anual** y **potencia del panel**: los cuales introduce el usuario.
```javascript
    const id = popupContent.querySelector('div[data-id]').getAttribute('data-id');

    // Seleccionas los elementos usando los IDs dinámicos
    const boton = popupContent.querySelector(`#btn-calcular-${id}`);
    const consumoAnualInput = popupContent.querySelector(`#consumo-anual-${id}`);
    const potenciaPanelSelect = popupContent.querySelector(`#potencia-panel-${id}`);
    const resultadoCalculo = popupContent.querySelector(`#resultado-calculo-${id}`);
    const iconoEstado = popupContent.querySelector(`#icono-estado-${id}`)
    const tejadoE = popupContent.querySelector(`#tejado-sup-${id}`);
    const tejado = parseFloat(tejadoE.textContent.replace('Tejado disponible:', '').trim());
```
### 3. **Cálculo de Paneles Solares**
Cuando se hace clic sobre el botón:
- Se calculan los paneles necesarios para generar el consumo anual según los datos proporcionados por el usuario y la irradiación solar anual (5.14 horas solares pico al día).
- Si los valores ingresados no son válidos, se muestra un mensaje de alerta.
```javascript
 if (boton) {
        boton.addEventListener('click', function () {
            console.log('Calculando número de paneles...');
            const consumoAnual = parseFloat(consumoAnualInput.value);
            const potenciaPanel = parseFloat(potenciaPanelSelect.value);
            const horasSolarPico = 5.14;
            let metrosPaneles = 0;
            if (isNaN(consumoAnual) || isNaN(potenciaPanel) || consumoAnual <= 0 || potenciaPanel <= 0) {
                alert('Por favor, ingresa valores válidos.');
                console.error('Valores no válidos:', { consumoAnual, potenciaPanel });
                return;
            }
```
### 4. **Verificación de Superficie Disponible**
- Dependiendo del tipo de panel (potencia 0.44 kw => 1.95 m2, 0.49 kw => 2.17 m2 o 0.59 kw => 2.58 m2), se calcula la superficie que ocuparían los paneles.
- Se compara el área que ocupan los paneles con la superficie disponible del tejado.
  - Si hay suficiente espacio, se indica el numero de paneles y que es viable instalar los paneles.
  - Si no hay suficiente espacio, se indica el numero depaneles y que no es posible.
```javascript 
 switch(potenciaPanel){
                
                case 0.44:
                    metrosPaneles = numPaneles * panelP;
                    if(tejado>= metrosPaneles){
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'Hay superficie de tejado para poner los paneles ✔️';
                    }else{
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = ' este No hay suficiente superficie de tejado para poner los paneles ❌';
                    }
                    break;
                case 0.49:
                    metrosPaneles = numPaneles * panelM;
                    if(tejado >= metrosPaneles){
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = 'este Hay superficie de tejado para poner los paneles ✔️';
                    }else{
                        resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                        iconoEstado.innerText = ' este No hay suficiente superficie de tejado para poner los paneles ❌';
                    }
                    break;
                case 0.59:
                        metrosPaneles = numPaneles * panelG;
                        if(tejado>= metrosPaneles){
                            resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                            iconoEstado.innerText = 'Hay superficie de tejado para poner los paneles ✔️';
                        }else{
                            resultadoCalculo.innerText = `Número de paneles necesarios: ${Math.ceil(numPaneles)}`;
                            iconoEstado.innerText = `No hay suficiente superficie de tejado para poner los paneles ❌}`;
                        }
                    break;    
            }
```
