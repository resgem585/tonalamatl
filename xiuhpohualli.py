from datetime import datetime

def find_xiuhpohualli_day(calendario_data, birth_date):
    """
    Dada una fecha de nacimiento (birth_date), retorna (numero_tonal, nombre_signo, nombre_veintena)
    buscándolo en calendario_xiuhpohualli.json (las 18 veintenas).
    Retorna None si no encuentra.
    """
    fecha_str = birth_date.strftime("%d/%m")

    # Recorremos todas las veintenas en el JSON normal
    for nombre_veintena, dias_lista in calendario_data.items():
        for dia_info in dias_lista:
            if dia_info["fecha"] == fecha_str:
                return (dia_info["numero_tonal"], dia_info["nombre"], nombre_veintena)

    return None


def find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date):
    """
    Busca el día Nemontemi según el Tlalpilli (Acatl, Tochtli, Tecpatl o Calli),
    dentro de 'xiuhpohualli_nemontemi.json'.

    Retorna (numero_tonal, nombre_signo, "NEMONTEMI") si encuentra,
    o None si no hay coincidencia.
    """
    # Solo aplicable para 7/03 al 11/03, pero esa validación la hacemos desde main.py
    # Formateamos la fecha a 'DD/MM'
    fecha_str = birth_date.strftime("%d/%m")

    # La sección "NEMONTEMI" es la que contiene las claves "Acatl", "Calli", "Tecpatl", "Tochtli"
    # Checamos si Tlalpilli existe en ese dict
    nemontemi_dict = calendario_nemontemi_data.get("NEMONTEMI", {})
    if tlalpilli not in nemontemi_dict:
        # Si el Tlalpilli no está en la lista, regresamos None
        return None

    # Revisar la lista de días para ese Tlalpilli
    dias_lista = nemontemi_dict[tlalpilli]
    for dia_info in dias_lista:
        if dia_info["fecha"] == fecha_str:
            return dia_info["numero_tonal"], dia_info["nombre"], "NEMONTEMI"

    return None


def encontrar_inicios_de_trecenas(calendario_data):
    inicios = []
    for nombre_veintena, dias in calendario_data.items():
        # Ignorar "NEMONTEMI" y "ACOMPANANTES_TONALPOHUALLI"
        if nombre_veintena in ["NEMONTEMI", "ACOMPANANTES_TONALPOHUALLI"]:
            continue

        for i, dia in enumerate(dias):
            # Aquí ya asumimos que 'dia' sí tiene "numero_tonal"
            if (dia["numero_tonal"] == 1) or (i % 13 == 0):
                inicios.append(
                    (dia["numero_tonal"], dia["nombre"], nombre_veintena, dia["fecha"])
                )

    return inicios


def encontrar_trecena_de_fecha(birth_date, calendario_data):
    inicios = encontrar_inicios_de_trecenas(calendario_data)
    for i in range(len(inicios)):
        tonal, signo, veintena, fecha_inicio = inicios[i]
        fecha_inicio_dt = datetime.strptime(fecha_inicio + f"/{birth_date.year}", "%d/%m/%Y").date()

        if i + 1 < len(inicios):
            _, _, _, fecha_siguiente = inicios[i + 1]
            fecha_siguiente_dt = datetime.strptime(fecha_siguiente + f"/{birth_date.year}", "%d/%m/%Y").date()
        else:
            fecha_siguiente_dt = datetime(birth_date.year + 1, 1, 1).date()

        if fecha_inicio_dt <= birth_date < fecha_siguiente_dt:
            return i + 1, tonal, signo, veintena, fecha_inicio
    return None



