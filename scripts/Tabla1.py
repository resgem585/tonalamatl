import json
from datetime import datetime, timedelta

# Tonalpohualli símbolos (20 días)
tonalpohualli_simbolos = [
    "CIPACTLI", "EHECATL", "CALLI", "CUETZPALLI", "COATL",
    "MIQUIZTLI", "MAZATL", "TOCHTLI", "ATL", "ITZCUINTLI",
    "OZOHMATLI", "MALINALLI", "ACATL", "OCELOTL", "CUAUHTLI",
    "COZCACUAUHTLI", "OLLIN", "TECPATL", "QUIAUITL", "XOCHITL"
]

# Xiuhpohualli meses con fecha de inicio
# (ejemplo: ATLACAHUALO 12/03/2024 hasta IZCALLI 06/03/2025)
xiuhpohualli_meses = [
    ("ATLACAHUALO", "12/03"), ("TLACAXIPEHUALIZTLI", "01/04"), ("TOZOZTONTLI", "21/04"),
    ("UEY TOTZOZTLI", "11/05"), ("TOXCATL", "31/05"), ("ETZALQUALIZTLI", "20/06"),
    ("TECUILHUITONTLI", "10/07"), ("UEYTECUILHUITL", "30/07"), ("TLAXOCHIMACO", "19/08"),
    ("XOCOLHUETZI", "08/09"), ("OCHPANIZTLI", "28/09"), ("TEOTLECO", "18/10"),
    ("TEPEILHUITL", "07/11"), ("QUECHOLLI", "27/11"), ("PANQUETZALIZTLI", "17/12"),
    ("ATEMOZTLI", "06/01"), ("TITIL", "26/01"), ("IZCALLI", "15/02")
]

# Nemontemi por tipo de año
nemontemi = {
    "Tochtli": ["CIPACTLI", "EHECATL", "CALLI", "CUETZPALLI", "COATL"],
    "Acatl":   ["MIQUIZTLI", "MAZATL", "TOCHTLI", "ATL", "ITZCUINTLI"],
    "Tecpatl": ["OZOMATLI", "MALINALLI", "ACATL", "OCELOTL", "CUAUHTLI"],
    "Calli":   ["COZCACUAUHTLI", "OLLIN", "TECPATL", "QUIAUITL", "XOCHITL"]
}

# Los 4 rumbos (en la secuencia normal de 13 días)
rumbos = ["Tlahuiztlampa", "Huitztlampa", "Cihuatlampa", "Mictlampa"]

# Rumbo FIJO para cada tipo de año en Nemontemi
NEMONTEMI_RUMBO = {
    "Tochtli": "Tlahuiztlampa",
    "Acatl":   "Huitztlampa",
    "Tecpatl": "Cihuatlampa",
    "Calli":   "Mictlampa"
}

def generar_json_completo():
    calendario = {}

    # Variables para la secuencia normal de 13 días
    tonal_num = 1       # 1..13
    tonal_index = 0     # índice para tonalpohualli_simbolos
    rumbo_index = 0     # índice en [Tlahuiztlampa, Huitztlampa, Cihuatlampa, Mictlampa]

    #
    # 1) Generar los 360 días (18 veintenas)
    #
    for nombre_mes, fecha_inicio_str in xiuhpohualli_meses:
        dias_mes = []

        # Aquí fijamos el año base a 2024 y dejamos que los meses vayan corriendo
        fecha_actual = datetime.strptime(fecha_inicio_str + "/2024", "%d/%m/%Y")

        for dia_num in range(1, 21):
            simbolo_actual = tonalpohualli_simbolos[tonal_index]
            rumbo_actual = rumbos[rumbo_index]

            # Crear el registro del día
            dia_entrada = {
                "numero": dia_num,                # 1..20 (dentro de la veintena)
                "nombre": simbolo_actual,
                "fecha": fecha_actual.strftime("%d/%m"),
                "numero_tonal": tonal_num,
                "rumbo": rumbo_actual
            }
            dias_mes.append(dia_entrada)

            # Incrementos
            fecha_actual += timedelta(days=1)
            tonal_index = (tonal_index + 1) % 20

            if tonal_num == 13:
                tonal_num = 1
                rumbo_index = (rumbo_index + 1) % 4
            else:
                tonal_num += 1

        calendario[nombre_mes] = dias_mes

    #
    # 2) Generar Nemontemi (7/03 al 11/03):
    #    Reiniciamos numero_tonal de 1 a 5, con rumbo fijo según tipo de año
    #
    calendario["NEMONTEMI"] = {}
    fecha_nemontemi_inicio = datetime.strptime("07/03/2025", "%d/%m/%Y")

    for tipo_anio, simbolos in nemontemi.items():
        dias_nemontemi = []
        # Rumbo único para estos 5 días
        rumbo_fijo = NEMONTEMI_RUMBO[tipo_anio]

        # Para cada uno de los 5 días en Nemontemi
        for i, simbolo in enumerate(simbolos):
            fecha_dia = fecha_nemontemi_inicio + timedelta(days=i)

            # Reiniciamos la cuenta del "numero_tonal" en 1..5
            dia_nem = {
                "numero": i + 1,                       # 1..5 (pos en Nemontemi)
                "nombre": simbolo,
                "fecha": fecha_dia.strftime("%d/%m"),
                "numero_tonal": i + 1,                 # REINICIO 1..5
                "rumbo": rumbo_fijo                    # Rumbo fijo
            }
            dias_nemontemi.append(dia_nem)

        calendario["NEMONTEMI"][tipo_anio] = dias_nemontemi

    return calendario

def guardar_json(calendario, filename="calendario_xiuhpohualli.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(calendario, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    calendario_completo = generar_json_completo()
    guardar_json(calendario_completo)
    print("\nArchivo JSON generado correctamente (Nemontemi con numero_tonal 1..5).")
