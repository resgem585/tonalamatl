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

# Acompañantes para cada número del 1 al 13
ACOMPANANTES_13 = {
    1: {
        "acompanante_diurno": "Xiuhtecuhtli",
        "acompanante_volador": "Xiuhuitzitzilli",
        "acompanante_complementario": "Tlahuizcalpantecuhtli"
    },
    2: {
        "acompanante_diurno": "Tlaltecuhtli",
        "acompanante_volador": "Quetzalhuitzitzilli",
        "acompanante_complementario": "Ixtlilton"
    },
    3: {
        "acompanante_diurno": "Chalchiuhtlicue",
        "acompanante_volador": "Tohtli",
        "acompanante_complementario": "Xochipilli"
    },
    4: {
        "acompanante_diurno": "Tonatiuh",
        "acompanante_volador": "Zollin",
        "acompanante_complementario": "Xipe Totec"
    },
    5: {
        "acompanante_diurno": "Tlazohteotl",
        "acompanante_volador": "Cacalotl",
        "acompanante_complementario": "Yaotl"
    },
    6: {
        "acompanante_diurno": "Mictlantecuhtli",
        "acompanante_volador": "Chicuauhtli",
        "acompanante_complementario": "Huahuantli"
    },
    7: {
        "acompanante_diurno": "Xochipilli",
        "acompanante_volador": "Tizapapalotl",
        "acompanante_complementario": "Xiuhtecuhtli"
    },
    8: {
        "acompanante_diurno": "Tlaloc",
        "acompanante_volador": "Itzcuauhtli",
        "acompanante_complementario": "Tlaloc"
    },
    9: {
        "acompanante_diurno": "Quetzalcoatl",
        "acompanante_volador": "Huexolotl",
        "acompanante_complementario": "Tlaloc"
    },
    10: {
        "acompanante_diurno": "Tezcatlipoca",
        "acompanante_volador": "Tecolotl",
        "acompanante_complementario": "Tezcatlipoca"
    },
    11: {
        "acompanante_diurno": "Chalmecatecuhtli",
        "acompanante_volador": "Alotl",
        "acompanante_complementario": "Xochipilli"
    },
    12: {
        "acompanante_diurno": "Tlahuizcalpantecuhtli",
        "acompanante_volador": "Quetzaltototl",
        "acompanante_complementario": "Centeotl"
    },
    13: {
        "acompanante_diurno": "Huehuecoyotl",
        "acompanante_volador": "Tlapalpacholli",
        "acompanante_complementario": "Huehuecoyotl"
    }
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

        # Ajusta el año base; se usará 2024 para todos por consistencia
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
    # 2) Generar Nemontemi (7/03 al 11/03/2025)
    #    Reiniciamos numero_tonal de 1 a 5, con rumbo fijo según tipo de año (Tochtli, Acatl, Tecpatl, Calli).
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
            # REINICIAMOS la cuenta del "numero_tonal" en 1..5
            dia_nem = {
                "numero": i + 1,  # 1..5 (posición en Nemontemi)
                "nombre": simbolo,
                "fecha": fecha_dia.strftime("%d/%m"),
                "numero_tonal": i + 1,
                "rumbo": rumbo_fijo
            }
            dias_nemontemi.append(dia_nem)

        calendario["NEMONTEMI"][tipo_anio] = dias_nemontemi

    #
    # 3) Añadir la información de acompañantes (1..13)
    #
    #    Creamos una sección especial donde guardaremos
    #    este bloque con la estructura que quieras:
    #
    acompanantes_lista = []
    for numero in range(1, 14):
        data_num = ACOMPANANTES_13[numero]
        acompanantes_lista.append({
            "numero": numero,
            "acompanante_diurno": data_num["acompanante_diurno"],
            "acompanante_volador": data_num["acompanante_volador"],
            "acompanante_complementario": data_num["acompanante_complementario"]
        })

    calendario["ACOMPANANTES_TONALPOHUALLI"] = acompanantes_lista

    return calendario


def guardar_json(calendario, filename="calendario_xiuhpohualli.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(calendario, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    calendario_completo = generar_json_completo()
    guardar_json(calendario_completo)
    print("Archivo JSON generado correctamente.")
