import json
from datetime import datetime, timedelta

# Tonalpohualli símbolos (20 días)
tonalpohualli_simbolos = [
    "CIPACTLI", "EHECATL", "CALLI", "CUETZPALLI", "COATL",
    "MIQUIZTLI", "MAZATL", "TOCHTLI", "ATL", "ITZCUINTLI",
    "OZOHMATLI", "MALINALLI", "ACATL", "OCELOTL", "CUAUHTLI",
    "COZCACUAUHTLI", "OLLIN", "TECPATL", "QUIAUITL", "XOCHITL"
]

xiuhpohualli_meses = [
    ("ATLACAHUALO", "12/03"), ("TLACAXIPEHUALIZTLI", "01/04"), ("TOZOZTONTLI", "21/04"),
    ("UEY TOTZOZTLI", "11/05"), ("TOXCATL", "31/05"), ("ETZALQUALIZTLI", "20/06"),
    ("TECUILHUITONTLI", "10/07"), ("UEYTECUILHUITL", "30/07"), ("TLAXOCHIMACO", "19/08"),
    ("XOCOLHUETZI", "08/09"), ("OCHPANIZTLI", "28/09"), ("TEOTLECO", "18/10"),
    ("TEPEILHUITL", "07/11"), ("QUECHOLLI", "27/11"), ("PANQUETZALIZTLI", "17/12"),
    ("ATEMOZTLI", "06/01"), ("TITIL", "26/01"), ("IZCALLI", "15/02")
]

nemontemi = {
    "Tochtli": ["CIPACTLI", "EHECATL", "CALLI", "CUETZPALLI", "COATL"],
    "Acatl":   ["MIQUIZTLI", "MAZATL", "TOCHTLI", "ATL", "ITZCUINTLI"],
    "Tecpatl": ["OZOMATLI", "MALINALLI", "ACATL", "OCELOTL", "CUAUHTLI"],
    "Calli":   ["COZCACUAUHTLI", "OLLIN", "TECPATL", "QUIAUITL", "XOCHITL"]
}

rumbos = ["Tlahuiztlampa", "Huitztlampa", "Cihuatlampa", "Mictlampa"]

NEMONTEMI_RUMBO = {
    "Tochtli": "Tlahuiztlampa",
    "Acatl":   "Huitztlampa",
    "Tecpatl": "Cihuatlampa",
    "Calli":   "Mictlampa"
}

# Acompañantes de 13 numeros (si ya lo tenías)
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
# NUEVA SECCION: acompañantes de 20 días
ACOMPANANTES_20_DIAS = [
    {
        "numero": 1,
        "signo": "CIPACTLI",
        "acompanante_diurno": "Tonacacihuatl y Tonacatecuhtli"
    },
    {
        "numero": 2,
        "signo": "EHECATL",
        "acompanante_diurno": "Quetzalcóatl"
    },
    {
        "numero": 3,
        "signo": "CALLI",
        "acompanante_diurno": "Tepeyólohtli"
    },
    {
        "numero": 4,
        "signo": "CUETZPALLI",
        "acompanante_diurno": "Huehuecóyotl"
    },
    {
        "numero": 5,
        "signo": "COATL",
        "acompanante_diurno": "Chalchiuhtlicue"
    },
    {
        "numero": 6,
        "signo": "MIQUIZTLI",
        "acompanante_diurno": "Tecuziztecatl"
    },
    {
        "numero": 7,
        "signo": "MAZATL",
        "acompanante_diurno": "Tlaloc"
    },
    {
        "numero": 8,
        "signo": "TOCHTLI",
        "acompanante_diurno": "Meyahual"
    },
    {
        "numero": 9,
        "signo": "ATL",
        "acompanante_diurno": "Xiuhtecuhtli"
    },
    {
        "numero": 10,
        "signo": "ITZCUINTLI",
        "acompanante_diurno": "Mictlantecuhtli"
    },
    {
        "numero": 11,
        "signo": "OZOHMATLI",
        "acompanante_diurno": "Xochipilli"
    },
    {
        "numero": 12,
        "signo": "MALINALLI",
        "acompanante_diurno": "Patecatl"
    },
    {
        "numero": 13,
        "signo": "ACATL",
        "acompanante_diurno": "Tezcatlipoca Ixquimilli"
    },
    {
        "numero": 14,
        "signo": "OCELOTL",
        "acompanante_diurno": "Tlazolteotl"
    },
    {
        "numero": 15,
        "signo": "CUAUHTLI",
        "acompanante_diurno": "Xipe Tótec"
    },
    {
        "numero": 16,
        "signo": "COZCACUAUHTLI",
        "acompanante_diurno": "Itzpapalotl"
    },
    {
        "numero": 17,
        "signo": "OLLIN",
        "acompanante_diurno": "Xólotl"
    },
    {
        "numero": 18,
        "signo": "TECPATL",
        "acompanante_diurno": "Chalchiuhtotolin"
    },
    {
        "numero": 19,
        "signo": "QUIAUITL",
        "acompanante_diurno": "Tonahtiuh"
    },
    {
        "numero": 20,
        "signo": "XOCHITL",
        "acompanante_diurno": "Xochiquetzalli"
    }
]


def generar_json_completo():
    calendario = {}

    tonal_num = 1
    tonal_index = 0
    rumbo_index = 0

    # 1) Generar 360 días de las 18 veintenas
    for nombre_mes, fecha_inicio_str in xiuhpohualli_meses:
        dias_mes = []
        fecha_actual = datetime.strptime(fecha_inicio_str + "/2024", "%d/%m/%Y")

        for dia_num in range(1, 21):
            simbolo_actual = tonalpohualli_simbolos[tonal_index]
            rumbo_actual = rumbos[rumbo_index]

            dia_entrada = {
                "numero": dia_num,
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

    # 2) Generar Nemontemi
    calendario["NEMONTEMI"] = {}
    fecha_nemontemi_inicio = datetime.strptime("07/03/2025", "%d/%m/%Y")

    for tipo_anio, simbolos in nemontemi.items():
        dias_nemontemi = []
        rumbo_fijo = NEMONTEMI_RUMBO[tipo_anio]
        for i, simbolo in enumerate(simbolos):
            fecha_dia = fecha_nemontemi_inicio + timedelta(days=i)
            dia_nem = {
                "numero": i + 1,
                "nombre": simbolo,
                "fecha": fecha_dia.strftime("%d/%m"),
                "numero_tonal": i + 1,
                "rumbo": rumbo_fijo
            }
            dias_nemontemi.append(dia_nem)
        calendario["NEMONTEMI"][tipo_anio] = dias_nemontemi

    # 3) Acompañantes 13 (opcional)
    acompanantes_13_lista = []
    for numero in range(1, 14):
        data_num = ACOMPANANTES_13.get(numero, {
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

    return calendario


def guardar_json(calendario, filename="calendario_xiuhpohualli.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(calendario, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    calendario_completo = generar_json_completo()
    guardar_json(calendario_completo)
    print("\nArchivo JSON generado correctamente.")
