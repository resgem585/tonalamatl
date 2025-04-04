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
