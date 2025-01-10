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
