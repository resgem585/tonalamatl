import json
from datetime import datetime
from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import (
    find_xiuhpohualli_day,
    find_nemontemi_day,
    encontrar_trecena_de_fecha,
    obtener_senor_de_la_noche,
    obtener_rumbo,        # ← nuevo import
)

DAY_SIGNS_MAP = {
    "CIPACTLI": 1, "EHECATL": 2, "CALLI": 3, "CUETZPALLI": 4, "COATL": 5,
    "MIQUIZTLI": 6, "MAZATL": 7, "TOCHTLI": 8, "ATL": 9, "ITZCUINTLI": 10,
    "OZOHMATLI": 11, "MALINALLI": 12, "ACATL": 13, "OCELOTL": 14, "CUAUHTLI": 15,
    "COZCACUAUHTLI": 16, "OLLIN": 17, "TECPATL": 18, "QUIAUITL": 19, "XOCHITL": 20,
}


def main():
    # 1) Cargar datos
    with open("xiuhmolpilli.json", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)
    with open("calendario_completo.json", encoding="utf-8") as f:
        calendario = json.load(f)

    # 2) Fecha de nacimiento
    birth_str = input("🗓️  Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("❌  Formato inválido, usa DD/MM/YYYY.")
        return

    # 3) Xiuhmolpilli
    año = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)
    if año:
        print(f"🌽  Año Xiuhmolpilli: {año[0]}  |  🌀 Tlalpilli: {año[1]}")
    else:
        print("⚠️  Sin Tlalpilli para tu fecha.")

    # 4) Día Tonalpohualli / Nemontemi
    if (birth_date.month, birth_date.day) in [(3, d) for d in range(7, 12)] and año:
        res = find_nemontemi_day(calendario, año[1], birth_date)
    else:
        res = find_xiuhpohualli_day(calendario, birth_date)

    if not res:
        print("❌  Día Tonalpohualli no encontrado.")
        return

    num_tonal, signo, veintena = res

    # 5) Rumbo
    if veintena != "NEMONTEMI":
        rumbo = obtener_rumbo(calendario, birth_date)
    else:  # Nemontemi ya lleva rumbo en el JSON
        rumbo = next(
            (d["rumbo"]
             for d in calendario["NEMONTEMI"][año[1]]
             if d["fecha"] == birth_date.strftime("%d/%m")),
            None,
        )

    # 6) Salida compacta del día
    linea_dia = f"🦅  {num_tonal} {signo}  |  🌿 {veintena}"
    if rumbo:
        linea_dia += f"  |  🧭 {rumbo}"
    print(linea_dia)

    # 7) Señor de la Noche
    senor = obtener_senor_de_la_noche(calendario, birth_date)
    if senor:
        print(f"🌙  Señor de la Noche: #{senor[0]} {senor[1]}")

    # 8) Trecena (solo en días regulares)
    if veintena != "NEMONTEMI":
        trecena = encontrar_trecena_de_fecha(birth_date, calendario)
        if trecena:
            idx, tonal_i, signo_i, veintena_i, fecha_i = trecena
            idx_ciclico = ((idx - 1) % 20) + 1
            print(f"📍  Trecena #{idx_ciclico}: inicia {tonal_i} {signo_i} ({fecha_i}) en {veintena_i}")

            # 8‑bis) Acompañantes de la trecena
            acomp_trecena = next(
                (x for x in calendario["ACOMPANANTES_TRESCENAS"] if x["numero"] == idx_ciclico),
                None,
            )
            if acomp_trecena:
                nombres = ", ".join(acomp_trecena["acompanantes"])
                print(f"✨  Acompañantes de la trecena: {nombres}")
    else:
        print("🌌  Días Nemontemi (fuera de la cuenta regular)")

    # 9) Acompañante diurno del signo
    num_signo = DAY_SIGNS_MAP.get(signo)
    acomp20 = next((x for x in calendario["ACOMPANANTES_20_DIAS"] if x["numero"] == num_signo), None)
    if acomp20:
        print(f"🔶  Acompañante diurno: {acomp20['acompanante_diurno']}")

    # 10) Acompañantes del número tonal
    acomp_tonal = next((x for x in calendario["ACOMPANANTES_TONALPOHUALLI"] if x["numero"] == num_tonal), None)
    if acomp_tonal:
        print(
            "🔹  Acompañantes tonal {0}: Diurno {1} • Volador {2} • Complementario {3}".format(
                num_tonal,
                acomp_tonal["acompanante_diurno"],
                acomp_tonal["acompanante_volador"],
                acomp_tonal["acompanante_complementario"],
            )
        )


if __name__ == "__main__":
    main()
