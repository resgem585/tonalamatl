import json
from datetime import datetime
from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import (
    find_xiuhpohualli_day,
    find_nemontemi_day,
    encontrar_trecena_de_fecha
)

# Mapa de signos (CIPACTLI..XOCHITL) a número 1..20
DAY_SIGNS_MAP = {
    "CIPACTLI": 1, "EHECATL": 2, "CALLI": 3, "CUETZPALLI": 4, "COATL": 5,
    "MIQUIZTLI": 6, "MAZATL": 7, "TOCHTLI": 8, "ATL": 9, "ITZCUINTLI": 10,
    "OZOHMATLI": 11, "MALINALLI": 12, "ACATL": 13, "OCELOTL": 14, "CUAUHTLI": 15,
    "COZCACUAUHTLI": 16, "OLLIN": 17, "TECPATL": 18, "QUIAUITL": 19, "XOCHITL": 20
}

def main():
    # 1) Cargar archivos JSON
    with open("xiuhmolpilli.json", "r", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)

    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_data = json.load(f)

    # 2) Solicitar fecha al usuario
    birth_str = input("🗓️ Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido. Usa DD/MM/YYYY.")
        return

    # 3) Encontrar año Xiuhmolpilli
    year_result = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)
    if year_result:
        name, tlalpilli = year_result
        print(f"🌽 Año Xiuhmolpilli: {name} | 🌀 Tlalpilli: {tlalpilli}")
    else:
        print("⚠️ No se encontró Tlalpilli para tu fecha.")
        tlalpilli = None

    # 4) Determinar día Tonalpohualli (o Nemontemi)
    day_result = None
    rumbo = None  # inicializamos rumbo

    if birth_date.month == 3 and 7 <= birth_date.day <= 11 and tlalpilli:
        day_result = find_nemontemi_day(calendario_data, tlalpilli, birth_date)
        if day_result:
            print("🌌 ¡Has nacido en días Nemontemi!")
            numero_tonal, nombre_signo, nombre_mes = day_result
            rumbo = calendario_data["NEMONTEMI"][tlalpilli][numero_tonal - 1]["rumbo"]
    else:
        day_result = find_xiuhpohualli_day(calendario_data, birth_date)
        if day_result:
            numero_tonal, nombre_signo, nombre_mes = day_result
            # Buscar rumbo (opcional si viene en JSON)
            for mes, dias in calendario_data.items():
                if mes == nombre_mes:
                    for dia in dias:
                        if dia["nombre"] == nombre_signo and dia["numero_tonal"] == numero_tonal:
                            rumbo = dia.get("rumbo", None)
                            break

    if not day_result:
        print("❌ No se encontró día Tonalpohualli para tu fecha.")
        return

    # Mostrar información del día
    print(f"🦅 Tu día Tonalpohualli: {numero_tonal} {nombre_signo}")
    print(f"🌿 Veintena (mes): {nombre_mes}")

    # Mostrar rumbo si disponible
    if rumbo:
        print(f"🧭 Rumbo asociado: {rumbo}")

    # 5) Mostrar la trecena si aplica
    if nombre_mes != "NEMONTEMI":
        trecena_info = encontrar_trecena_de_fecha(birth_date, calendario_data)
        if trecena_info:
            idx, tonal_i, signo_i, veintena_i, fecha_inicio = trecena_info
            print(f"📍 Trecena #{idx}: inicia con {tonal_i} {signo_i}")
            print(f"📆 Fecha de inicio: {fecha_inicio}")
            print(f"🌿 Veintena donde inicia: {veintena_i}")
    else:
        print("🌌 (Días Nemontemi fuera de la cuenta regular).")

    # 6) Mostrar acompañante diurno del signo (1-20)
    signo_normalizado = nombre_signo.strip().upper()
    numero_20 = DAY_SIGNS_MAP.get(signo_normalizado, None)

    if numero_20:
        acompanantes_20 = calendario_data.get("ACOMPANANTES_20_DIAS", [])
        data_signo = next(
            (item for item in acompanantes_20 if item["numero"] == numero_20),
            None
        )
        if data_signo:
            print("\n🔶 Acompañante diurno de tu signo:")
            print(f"   {data_signo['acompanante_diurno']}")
        else:
            print("\nℹ️ Sin datos de acompañante diurno para este signo.")
    else:
        print(f"\nℹ️ No tenemos mapeo para el signo {nombre_signo}.")

    # 7) Mostrar los tres acompañantes del número tonal (1-13)
    acompanantes_tonal = calendario_data.get("ACOMPANANTES_TONALPOHUALLI", [])
    data_tonal = next(
        (item for item in acompanantes_tonal if item["numero"] == numero_tonal),
        None
    )

    if data_tonal:
        print(f"\n🔹 Acompañantes para tu número tonal ({numero_tonal}):")
        print(f"   • Diurno: {data_tonal['acompanante_diurno']}")
        print(f"   • Volador: {data_tonal['acompanante_volador']}")
        print(f"   • Complementario: {data_tonal['acompanante_complementario']}")
    else:
        print(f"\nℹ️ Sin datos de acompañantes para el número tonal {numero_tonal}.")


if __name__ == "__main__":
    main()
