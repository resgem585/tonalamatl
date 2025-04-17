from datetime import datetime


def find_xiuhpohualli_day(calendario_data, birth_date):
    fecha_str = birth_date.strftime("%d/%m")

    for nombre_veintena, dias_lista in calendario_data.items():
        if nombre_veintena in ["NEMONTEMI", "ACOMPANANTES_TONALPOHUALLI", "ACOMPANANTES_20_DIAS"]:
            continue

        for dia_info in dias_lista:
            if dia_info["fecha"] == fecha_str:
                return (dia_info["numero_tonal"], dia_info["nombre"], nombre_veintena)

    return None


def find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date):
    fecha_str = birth_date.strftime("%d/%m")

    nemontemi_dict = calendario_nemontemi_data.get("NEMONTEMI", {})
    if tlalpilli not in nemontemi_dict:
        return None

    dias_lista = nemontemi_dict[tlalpilli]
    for dia_info in dias_lista:
        if dia_info["fecha"] == fecha_str:
            return (dia_info["numero_tonal"], dia_info["nombre"], "NEMONTEMI")

    return None


def encontrar_inicios_de_trecenas(calendario_data):
    """
    Encuentra los inicios reales de trecenas: cada 13 días continuos (rumbos).
    Retorna una lista de tuplas:
    (numero_tonal, nombre_signo, nombre_veintena, fecha_inicio)
    """
    inicios = []
    contador_dias = 0

    # Crear una lista lineal de todos los días válidos
    dias_lineales = []
    for nombre_veintena, dias in calendario_data.items():
        if nombre_veintena in {
            "NEMONTEMI",
            "ACOMPANANTES_TONALPOHUALLI",
            "ACOMPANANTES_20_DIAS",
            "SENORES_9",
        }:
            continue
        for dia in dias:
            dias_lineales.append((dia, nombre_veintena))

    for i, (dia, nombre_veintena) in enumerate(dias_lineales):
        if i % 13 == 0:
            inicios.append((
                dia["numero_tonal"],
                dia["nombre"],
                nombre_veintena,
                dia["fecha"]
            ))

    return inicios


def encontrar_trecena_de_fecha(birth_date, calendario_data):
    inicios = encontrar_inicios_de_trecenas(calendario_data)
    for i in range(len(inicios)):
        tonal_i, signo_i, veintena_i, fecha_inicio = inicios[i]
        fecha_inicio_dt = datetime.strptime(fecha_inicio + f"/{birth_date.year}", "%d/%m/%Y").date()

        if i + 1 < len(inicios):
            _, _, _, fecha_sig = inicios[i + 1]
            fecha_sig_dt = datetime.strptime(fecha_sig + f"/{birth_date.year}", "%d/%m/%Y").date()
        else:
            fecha_sig_dt = datetime(birth_date.year + 1, 1, 1).date()

        if fecha_inicio_dt <= birth_date < fecha_sig_dt:
            return (i + 1, tonal_i, signo_i, veintena_i, fecha_inicio)
    return None

def obtener_senor_de_la_noche(calendario_data, birth_date):
    """
    Devuelve (número, nombre) del Señor de la Noche que rige el día dado.
    • Se usan solo los 360 días “regulares”; los días Nemontemi quedan fuera.
    • Los Señores (1‑9) se repiten de forma cíclica cada 9 días.
    """
    fecha_str = birth_date.strftime("%d/%m")
    dia_absoluto = 0  # Día 0 corresponde al Señor 1 (Xiuhtecuhtli)

    for nombre_mes, dias in calendario_data.items():
        if nombre_mes in {
            "NEMONTEMI",
            "ACOMPANANTES_TONALPOHUALLI",
            "ACOMPANANTES_20_DIAS",
            "SENORES_9",
        }:
            continue  # Excluimos claves auxiliares

        for dia in dias:
            if dia["fecha"] == fecha_str:
                # Calculamos el Señor de la Noche en base al día absoluto
                num_senor = (dia_absoluto % 9) + 1
                lista_senores = calendario_data["SENORES_9"]
                senor = next(s for s in lista_senores if s["numero"] == num_senor)
                return num_senor, senor["nombre"]
            dia_absoluto += 1

    return None  # Si no se encuentra la fecha
