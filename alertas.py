import csv
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

topico = os.environ["NTFY_TOPIC"]
url = f"https://ntfy.sh/{topico}"
hoy = datetime.now(ZoneInfo("America/Lima")).date()
DIAS_AVISO = 3

def enviar(titulo, mensaje, prioridad="default", tags="bell"):
    r = requests.post(
        url,
        data=mensaje.encode("utf-8"),
        headers={
            "Title": titulo.encode("utf-8"),
            "Priority": prioridad,
            "Tags": tags,
        },
        timeout=15,
    )
    r.raise_for_status()

errores = 0
with open("tareas.csv", encoding="utf-8") as f:
    for n, fila in enumerate(csv.DictReader(f), start=2):
        try:
            limite = datetime.strptime(fila["fecha_limite"].strip(), "%Y-%m-%d").date()
        except ValueError:
            print(f"Fila {n}: fecha inválida {fila['fecha_limite']!r}")
            errores += 1
            continue

        dias = (limite - hoy).days
        if dias > DIAS_AVISO:
            continue

        if dias < 0:
            titulo, prio, tags = f"VENCIDA: {fila['tarea']}", "urgent", "rotating_light"
        elif dias == 0:
            titulo, prio, tags = f"Vence HOY: {fila['tarea']}", "high", "warning"
        else:
            titulo, prio, tags = f"Vence en {dias} d: {fila['tarea']}", "default", "hourglass"

        cuerpo = f"Responsable: {fila['responsable']}\nVencimiento: {limite:%d/%m/%Y}"
        enviar(titulo, cuerpo, prio, tags)

sys.exit(1 if errores else 0)
