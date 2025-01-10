import matplotlib.pyplot as plt
import base64
import matplotlib.pyplot as plt
from io import BytesIO 



"""Clase donde se definen metodós para realizar operaciones sobre los archivos"""
class manejo_datos():
        
    #Metodo que crea un grafico y luego hace un buffer con una imagen base 64
    def generar_grafico(irradiacion):
        
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        fig, ax = plt.subplots()
        ax.bar(meses, irradiacion)
        ax.set_title('Radiación solar mensual (kWh/m²)')
        ax.set_ylabel('Irradiación (KWh/m²)')
        
        buffer = BytesIO()
        
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        img_base64_ir = base64.b64encode(buffer.read()).decode("utf-8")
        
        plt.close(fig)
        
        return img_base64_ir
    
    #Metodo que crea un grafico y luego hace un buffer con una imagen base 64
    def generar_gra_energia(potencia):
        
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        fig, ax = plt.subplots()
        ax.bar(meses, potencia)
        ax.set_title('Producción mensual de energía fotovoltaica (kWh)')
        ax.set_ylabel("Energia KWh")
        
        buffer = BytesIO()
        plt.savefig(buffer, format = "png")
        buffer.seek(0)
        img_base64_ener = base64.b64encode(buffer.read()).decode("utf-8")
        plt.close(fig)
        
        return img_base64_ener
        