import json
from datetime import datetime
from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import (
    find_xiuhpohualli_day,
    find_nemontemi_day,
    encontrar_trecena_de_fecha
)


def main():
    # 1) Cargar los archivos JSON
    with open("xiuhmolpilli.json", "r", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)

    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_data = json.load(f)

    # para Nemontemi usamos el mismo JSON de calendario
    calendario_nemontemi_data = calendario_data

    # 2) Solicitar fecha al usuario
    birth_str = input("🗓️ Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido. Usa DD/MM/YYYY. Ejemplo: 07/01/1989")
        return

    # 3) Buscar el año Xiuhmolpilli (Tlalpilli)
    year_result = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)
    if year_result is None:
        print("⚠️ No se encontró el Tlalpilli correspondiente.")
        tlalpilli = None
    else:
        name, tlalpilli = year_result
        print(f"🌽 Año Xiuhmolpilli: {name} | 🌀 Tlalpilli: {tlalpilli}")

    # 4) Ver si la fecha cae en Nemontemi
    #    (sólo válido si es 7..11/03 y tenemos Tlalpilli)
    if birth_date.month == 3 and 7 <= birth_date.day <= 11 and tlalpilli:
        day_result = find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date)
        if day_result is not None:
            # day_result => (numero_tonal, nombre_signo, "NEMONTEMI")
            numero_tonal, nombre_signo, nombre_mes = day_result
            print("🌌 ¡Has nacido en días Nemontemi (fuera del tiempo sagrado)! 🌠")
        else:
            day_result = None
    else:
        # 5) Si no es Nemontemi, buscar en las 18 veintenas
        day_result = find_xiuhpohualli_day(calendario_data, birth_date)

    if not day_result:
        print("❌ No se encontró día Tonalpohualli para tu fecha.")
        return

    # day_result => (numero_tonal, nombre_signo, nombre_mes)
    numero_tonal, nombre_signo, nombre_mes = day_result

    print(f"🦅 Tu día Tonalpohualli: {numero_tonal} {nombre_signo}")
    print(f"🌿 Veintena (mes): {nombre_mes}")

    # 6) Si tu JSON tiene rumbo en cada día, podrías buscarlo igual que nombre, etc.
    #    (en tu find_xiuhpohualli_day devuelves 3 o 4 valores. Ajusta si quieres.)
    #    Ej: si devuelves 4 => day_result = (numero_tonal, nombre_signo, veintena, rumbo)
    #    if len(day_result) == 4: ... etc.

    # 7) Mostrar Trecena solo si no es Nemontemi
    if nombre_mes != "NEMONTEMI":
        trecena_info = encontrar_trecena_de_fecha(birth_date, calendario_data)
        if trecena_info:
            idx, tonal_i, signo_i, veintena_i, fecha_inicio = trecena_info
            print(f"📍 Trecena #{idx}: comienza con {tonal_i} {signo_i}")
            print(f"📆 Fecha de inicio: {fecha_inicio}")
            print(f"🌿 Veintena donde inicia: {veintena_i}")
    else:
        print("🌌 Los días Nemontemi no pertenecen a ninguna trecena ni veintena.")

    # 8) ======================
    #    BUSCAR ACOMPAÑANTES
    #  =======================
    # Suponiendo que calendario_data tiene un dict "ACOMPANANTES_TONALPOHUALLI" con la lista
    acompanantes = calendario_data.get("ACOMPANANTES_TONALPOHUALLI", [])
    # Buscar en esa lista el que tenga "numero" == numero_tonal
    data_acomp = next((item for item in acompanantes if item["numero"] == numero_tonal), None)

    if data_acomp:
        diurno = data_acomp["acompanante_diurno"]
        volador = data_acomp["acompanante_volador"]
        compl = data_acomp["acompanante_complementario"]

        print("\n🔶 Acompañantes Tonalpohualli para tu número:")
        print(f"   • Diurno: {diurno}")
        print(f"   • Volador: {volador}")
        print(f"   • Complementario: {compl}")
    else:
        print("\nℹ️ No hay datos de acompañantes para tu número_tonal.")


if __name__ == "__main__":
    main()
