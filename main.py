import json
from datetime import datetime, date, timedelta

# ──────────────────────────────────────────────
#  Constantes del calendario
# ──────────────────────────────────────────────
BASE_YEAR = 1975                     # 12-mar-1975 = Ce Tochtli = #1
BASE_DAY = date(1987, 3, 12)        # 1 Cipactli “histórico” (para el día)
DIAS_XIUH = 360                      # 18 × 20
MOD_TONAL = 13

TLALPILLI_SEQ = ["Tochtli", "Acatl", "Tecpatl", "Calli"]
RUMBO_TLALPILLI = {
    "Tochtli": "Tlahuiztlampa (Oriente)",
    "Acatl":   "Mictlampa (Norte)",
    "Tecpatl": "Cihuatlampa (Poniente)",
    "Calli":   "Huitztlampa (Sur)",
}

# Claves “extras” en el JSON de calendario
EXTRAS = {
    "NEMONTEMI", "ACOMPANANTES_TONALPOHUALLI", "ACOMPANANTES_20_DIAS",
    "ACOMPANANTES_TRESCENAS", "SENORES_9", "RUMBOS_TONAL",
    "TONALPOHUALLI_SIMBOLOS", "numeros",
}


# ──────────────────────────────────────────────
#  Utilidades de precálculo
# ──────────────────────────────────────────────
def cargar_calendario():
    with open("calendario_completo.json", encoding="utf-8") as f:
        cal = json.load(f)

    # 360 días regulares
    dias, mapa = [], {}
    for veintena, lst in cal.items():
        if veintena in EXTRAS or not isinstance(lst, list):
            continue
        for d in lst:
            dias.append(
                {"i": len(dias), "veintena": veintena,
                 "signo": d["nombre"].upper(), "fecha": d["fecha"]}
            )
            mapa[d["fecha"]] = dias[-1]["i"]

    # nombres nahuas CE-OME-YEI… (1-13)
    numeros = [n["valor"] for n in cal["numeros"]]

    return cal, dias, mapa, numeros, cal["RUMBOS_TONAL"]


# ──────────────────────────────────────────────
#  Año Xiuhmolpilli algorítmico
# ──────────────────────────────────────────────
def info_xiuhmolpilli(fecha: date, numeros):
    """
    Devuelve (nombre_completo, tlalpilli, num_1_52).
    • El año ‘azteca’ inicia cada 12 de marzo.
    • 12-mar-1975 ≡ #1  (Ce Tochtli).
    """
    # año azteca al que pertenece la fecha:
    az_year = fecha.year if fecha >= date(fecha.year, 3, 12) else fecha.year - 1
    offset = az_year - BASE_YEAR            # puede ser negativo
    idx52 = offset % 52                     # 0-51
    num52 = idx52 + 1

    tlalpilli = TLALPILLI_SEQ[idx52 // 13]          # bloque de 13 años
    idx13 = idx52 % 13                              # 0-12
    nombre = f"{numeros[idx13]} {tlalpilli.upper()}"

    rumbo_año = RUMBO_TLALPILLI[tlalpilli]
    return nombre, tlalpilli, num52, rumbo_año


# ──────────────────────────────────────────────
#  Cálculo diario (Tonalpohualli)
# ──────────────────────────────────────────────
def info_dia(fecha: date, dias, mapa, rumbos_trecena):
    # ¿Nemontemi?
    if (fecha.month, fecha.day) in [(3, d) for d in range(7, 12)]:
        return None   # se tratarán aparte en main()

    key = fecha.strftime("%d/%m")
    idx = mapa[key]                       # 0-359

    ciclos = fecha.year - BASE_DAY.year
    if (fecha.month, fecha.day) < (3, 12):
        ciclos -= 1
    total = ciclos * DIAS_XIUH + idx

    num_tonal = (total % MOD_TONAL) + 1
    signo = dias[idx]["signo"]
    veintena = dias[idx]["veintena"]

    trec_abs = total // 13
    trec_cic = trec_abs % 20 + 1
    rumbo = rumbos_trecena[trec_abs % len(rumbos_trecena)]

    # inicio de la trecena
    ini = dias[(trec_abs * 13) % DIAS_XIUH]
    return num_tonal, signo, veintena, trec_cic, rumbo, ini


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    cal, dias, mapa, numeros, rumbos_trecena = cargar_calendario()

    raw = input("🗓️  Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        born = datetime.strptime(raw, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido.")
        return

    # —— Año Xiuhmolpilli ————————————————————
    nombre_año, tlalpilli, num52, rumbo_año = info_xiuhmolpilli(born, numeros)
    print(f"🌽 Año Xiuhmolpilli: {nombre_año} (#{num52}/52)  |  🌀 Tlalpilli: {tlalpilli}  |  🧭 Rumbo: {rumbo_año}")

    # —— Nemontemi ————————————————————————————
    if (born.month, born.day) in [(3, d) for d in range(7, 12)]:
        nem = cal["NEMONTEMI"][tlalpilli]
        dato = next(d for d in nem if d["fecha"] == born.strftime("%d/%m"))
        print(f"🌌 Día Nemontemi: {dato['numero']} {dato['nombre']}  |  🧭 Rumbo: {dato['rumbo']}")
        return

    # —— Día regular ————————————————————————
    num_tonal, signo, veintena, trec_cic, rumbo, ini = info_dia(
        born, dias, mapa, rumbos_trecena
    )

    print(f"🦅 {num_tonal} {signo}  |  🌿 {veintena}  |  🧭 {rumbo}")

    # —— Trecena con rumbo ————————————————————
    print(f"📍 Trecena #{trec_cic} (Rumbo {rumbo}): inicia 1 {ini['signo']} ({ini['fecha']}) en {ini['veintena']}")

    acomp_tr = next((x for x in cal["ACOMPANANTES_TRESCENAS"]
                     if x["numero"] == trec_cic), None)
    if acomp_tr:
        print(f"✨ Acompañantes trecena: {', '.join(acomp_tr['acompanantes'])}")

    # —— Acompañantes del signo y número ——————
    acomp20 = next((x for x in cal["ACOMPANANTES_20_DIAS"]
                    if x["signo"] == signo), None)
    if acomp20:
        print(f"🔶 Acompañante diurno del signo: {acomp20['acompanante_diurno']}")

    acomp_tonal = next((x for x in cal["ACOMPANANTES_TONALPOHUALLI"]
                        if x["numero"] == num_tonal), None)
    if acomp_tonal:
        print("🔹 Acompañantes tonal {0}: Diurno {1} • Volador {2} • Comp. {3}"
              .format(num_tonal,
                      acomp_tonal["acompanante_diurno"],
                      acomp_tonal["acompanante_volador"],
                      acomp_tonal["acompanante_complementario"]))


if __name__ == "__main__":
    main()
