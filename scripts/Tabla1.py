import json
from datetime import datetime, timedelta

with open("calendario_base.json", encoding="utf-8") as f:
    base = json.load(f)

def generar_json_completo():
    calendario = {}

    tonal_num = 1
    tonal_index = 0
    rumbo_index = 0

    tonalpohualli_simbolos = base["tonalpohualli_simbolos"]
    xiuhpohualli_meses = base["xiuhpohualli_meses"]
    rumbos = base["rumbos"]
    nemontemi = base["nemontemi"]
    NEMONTEMI_RUMBO = base["NEMONTEMI_RUMBO"]
    ACOMPANANTES_13 = base["ACOMPANANTES_13"]
    ACOMPANANTES_20_DIAS = base["ACOMPANANTES_20_DIAS"]
    SENORES_9 = base["SENORES_9"]

    # 1) Generar 360 días
    for nombre_mes, fecha_inicio_str in xiuhpohualli_meses:
        dias_mes = []
        fecha_actual = datetime.strptime(fecha_inicio_str + "/2024", "%d/%m/%Y")

        for dia_num in range(1, 21):
            simbolo_actual = tonalpohualli_simbolos[tonal_index]
            rumbo_actual = rumbos[rumbo_index]

            dias_mes.append({
                "numero": dia_num,
                "nombre": simbolo_actual,
                "fecha": fecha_actual.strftime("%d/%m"),
                "numero_tonal": tonal_num,
                "rumbo": rumbo_actual
            })

            fecha_actual += timedelta(days=1)
            tonal_index = (tonal_index + 1) % 20
            if tonal_num == 13:
                tonal_num = 1
                rumbo_index = (rumbo_index + 1) % 4
            else:
                tonal_num += 1

        calendario[nombre_mes] = dias_mes

    # 2) Nemontemi
    calendario["NEMONTEMI"] = {}
    fecha_nemontemi_inicio = datetime.strptime("07/03/2025", "%d/%m/%Y")
    for tipo_anio, simbolos in nemontemi.items():
        dias_nemontemi = []
        rumbo_fijo = NEMONTEMI_RUMBO[tipo_anio]
        for i, simbolo in enumerate(simbolos):
            fecha_dia = fecha_nemontemi_inicio + timedelta(days=i)
            dias_nemontemi.append({
                "numero": i + 1,
                "nombre": simbolo,
                "fecha": fecha_dia.strftime("%d/%m"),
                "numero_tonal": i + 1,
                "rumbo": rumbo_fijo
            })
        calendario["NEMONTEMI"][tipo_anio] = dias_nemontemi

    # 3) Acompañantes Tonalpohualli (13)
    acompanantes_13_lista = []
    for numero in range(1, 14):
        data_num = ACOMPANANTES_13.get(str(numero), {
            "acompanante_diurno": "Desconocido",
            "acompanante_volador": "Desconocido",
            "acompanante_complementario": "Desconocido"
        })
        acompanantes_13_lista.append({
            "numero": numero,
            "acompanante_diurno": data_num["acompanante_diurno"],
            "acompanante_volador": data_num["acompanante_volador"],
            "acompanante_complementario": data_num["acompanante_complementario"]
        })
    calendario["ACOMPANANTES_TONALPOHUALLI"] = acompanantes_13_lista

    # 4) Acompañantes de 20 días
    calendario["ACOMPANANTES_20_DIAS"] = ACOMPANANTES_20_DIAS

    # 5) Señores de la noche (9)
    calendario["SENORES_9"] = SENORES_9

    return calendario

def guardar_json(calendario, filename="calendario_completo.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(calendario, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    calendario_completo = generar_json_completo()
    guardar_json(calendario_completo)
    print("\nArchivo JSON generado correctamente.")
