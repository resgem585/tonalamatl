import json
from datetime import datetime, date

# ──────────────────────────────────────────────
#  Ancla histórica
# ──────────────────────────────────────────────
# 12-mar-1975 ≡ 1 Cipactli  y  CE TOCHTLI  (#1/52)
BASE_DAY = date(1974, 3, 12)  # único ancla
DIAS_XIUH = 360  # 18 × 20
MOD_TONAL = 13
TLALPILLI_SEQ = ["Tochtli", "Acatl", "Tecpatl", "Calli"]
RUMBO_TLALPILLI = {
    "Tochtli": "Tlahuiztlampa (Oriente)",
    "Acatl": "Mictlampa (Norte)",
    "Tecpatl": "Cihuatlampa (Poniente)",
    "Calli": "Huitztlampa (Sur)",
}

EXTRAS = {
    "NEMONTEMI", "ACOMPANANTES_TONALPOHUALLI", "ACOMPANANTES_20_DIAS",
    "ACOMPANANTES_TRESCENAS", "SENORES_9", "RUMBOS_TONAL",
    "TONALPOHUALLI_SIMBOLOS", "numeros",
}


# ──────────────────────────────────────────────
#  Precarga calendario
# ──────────────────────────────────────────────
def cargar_calendario():
    with open("calendario_completo.json", encoding="utf-8") as f:
        cal = json.load(f)

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

    numeros = [n["valor"] for n in cal["numeros"]]
    return cal, dias, mapa, numeros, cal["RUMBOS_TONAL"]


# ──────────────────────────────────────────────
#  Año Xiuhmolpilli (ciclo de 52 años)
# ──────────────────────────────────────────────
def info_xiuhmolpilli(fecha: date, numeros):
    """
    Devuelve: (nombre_completo, tlalpilli_columna, nº_1-52, rumbo_del_año).

    • El año ‘azteca’ inicia cada 12-mar.
    • 12-mar-1975 = CE TOCHTLI (#1/52).
    • El tlalpilli del **nombre** rota Tochtli→Acatl→Tecpatl→Calli cada año.
    • El **rumbo** (y la columna) cambian cada 13 años.
    """
    az_year = fecha.year if fecha >= date(fecha.year, 3, 12) else fecha.year - 1
    idx52 = (az_year - BASE_DAY.year) % 52  # 0-51
    num52 = idx52 + 1

    # Bloque de 13 años ⇒ columna (rumbo fijo)
    tlalpilli_col = TLALPILLI_SEQ[idx52 // 13]  # Tochtli / Acatl / …
    rumbo = RUMBO_TLALPILLI[tlalpilli_col]

    # Tlalpilli que va en el NOMBRE (rota cada año)
    tlalpilli_nom = TLALPILLI_SEQ[idx52 % 4]

    nombre = f"{numeros[idx52 % 13]} {tlalpilli_nom.upper()}"
    return nombre, tlalpilli_col, num52, rumbo


# ──────────────────────────────────────────────
#  Información del día (Tonalpohualli)
# ──────────────────────────────────────────────
def info_dia(fecha: date, dias, mapa, rumbos_trecena):
    if (fecha.month, fecha.day) in [(3, d) for d in range(7, 12)]:
        return None  # Nemontemi; se maneja en main()

    idx = mapa[fecha.strftime("%d/%m")]  # 0-359
    ciclos = fecha.year - BASE_DAY.year - (1 if (fecha.month, fecha.day) < (3, 12) else 0)
    total = ciclos * DIAS_XIUH + idx

    num = (total % MOD_TONAL) + 1
    signo = dias[idx]["signo"]
    veint = dias[idx]["veintena"]

    trec_abs = total // 13
    trec_idx = trec_abs % 20 + 1
    rumbo = rumbos_trecena[trec_abs % len(rumbos_trecena)]

    ini = dias[(trec_abs * 13) % DIAS_XIUH]  # inicio trecena
    return num, signo, veint, trec_idx, rumbo, ini


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    cal, dias, mapa, numeros, rumbos_trecena = cargar_calendario()

    raw = input("🗓️  Ingresa la fecha (DD/MM/YYYY): ").strip()
    try:
        born = datetime.strptime(raw, "%d/%m/%Y").date()
    except ValueError:
        print("❌  Formato inválido.")
        return

    # —— Año Xiuhmolpilli ————————————————————
    nom_a, tl_col, n52, rumbo_a = info_xiuhmolpilli(born, numeros)
    print(f"🌽  {nom_a} (#{n52}/52)  |  🌀 {tl_col}  |  🧭 {rumbo_a}")

    # —— Nemontemi ————————————————————————————
    if (born.month, born.day) in [(3, d) for d in range(7, 12)]:
        nem = cal["NEMONTEMI"][tl_col]
        d = next(x for x in nem if x["fecha"] == born.strftime("%d/%m"))
        print(f"🌌  Nemontemi: {d['numero']} {d['nombre']}  |  🧭 {d['rumbo']}")
        return

    # —— Día regular ————————————————————————
    num, signo, veint, trec, rumbo, ini = info_dia(born, dias, mapa, rumbos_trecena)
    print(f"🦅  {num} {signo}  |  🌿 {veint}  |  🧭 {rumbo}")

    # —— Trecena ——————————————————————————————
    print(f"📍  Trecena #{trec} (rumbo {rumbo}): inicia "
          f"1 {ini['signo']} ({ini['fecha']}) en {ini['veintena']}")

    acomp_tr = next((x for x in cal["ACOMPANANTES_TRESCENAS"] if x["numero"] == trec), None)
    if acomp_tr:
        print(f"✨  Acompañantes trecena: {', '.join(acomp_tr['acompanantes'])}")

    # —— Acompañantes diarios ——————————————————
    acomp20 = next((x for x in cal["ACOMPANANTES_20_DIAS"] if x["signo"] == signo), None)
    if acomp20:
        print(f"🔶  Acompañante diurno del signo: {acomp20['acompanante_diurno']}")

    acomp_tonal = next((x for x in cal["ACOMPANANTES_TONALPOHUALLI"] if x["numero"] == num), None)
    if acomp_tonal:
        print("🔹  Acompañantes tonal {0}: Diurno {1} • Volador {2} • Comp. {3}"
              .format(num,
                      acomp_tonal["acompanante_diurno"],
                      acomp_tonal["acompanante_volador"],
                      acomp_tonal["acompanante_complementario"]))


if __name__ == "__main__":
    main()
