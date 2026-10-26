import csv
import requests
from datetime import datetime, date

topico_ntfy = "mis_alertas"
url = f"https://ntfy.sh/{topico_ntfy}"

with open("tareas.csv", mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        tarea = fila["tarea"]
        responsable = fila["responsable"]
        fecha_limite_str = fila["fecha_limite"]

        fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        hoy = date.today()
        dias_restantes = (fecha_limite - hoy).days

        # El mensaje sí puede tener emojis sin problema
        mensaje = f"""👤 Responsable: {responsable}
📅 Vencimiento: {fecha_limite.strftime("%d/%m/%Y")}
⏳ Días restantes: {dias_restantes} días"""

        # En el Title QUITAMOS el emoji para evitar el error de codificación
        headers = {
            "Title": f"Tarea: {tarea}",  
            "Priority": "high",
            "Tags": "bell"
        }

        requests.post(url, data=mensaje.encode("utf-8"), headers=headers)
