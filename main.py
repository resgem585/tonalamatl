import json
from datetime import datetime, date

# ──────────────────────────────────────────────
#  Ancla histórica
# ──────────────────────────────────────────────
BASE_DAY = date(1974, 3, 12)          # 1 Cipactli  |  CE TOCHTLI
DIAS_XIUH = 360
MOD_TONAL = 13

TLALPILLI_SEQ = ["Tochtli", "Acatl", "Tecpatl", "Calli"]
RUMBO_TL = {
    "Tochtli": "Tlahuiztlampa (Oriente)",
    "Acatl":   "Huitztlampa (Sur)",
    "Tecpatl": "Cihuatlampa (Poniente)",
    "Calli":   "Mictlampa (Norte)",
}

EXTRAS = {
    "NEMONTEMI", "ACOMPANANTES_TONALPOHUALLI", "ACOMPANANTES_20_DIAS",
    "ACOMPANANTES_TRESCENAS", "SENORES_9", "RUMBOS_TONAL",
    "TONALPOHUALLI_SIMBOLOS", "numeros",
}

# ──────────────────────────────────────────────
#  Carga calendario
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
#  Año Xiuhmolpilli
# ──────────────────────────────────────────────
def info_xiuhmolpilli(fecha: date, nums):
    az_year = fecha.year if fecha >= date(fecha.year, 3, 12) else fecha.year - 1
    idx52   = (az_year - BASE_DAY.year) % 52
    n52     = idx52 + 1

    tl_col  = TLALPILLI_SEQ[idx52 // 13]
    rumbo   = RUMBO_TL[tl_col]

    idx13   = idx52 % 13 + 1
    tl_nom  = TLALPILLI_SEQ[idx52 % 4]
    nombre  = f"{nums[idx13-1]} {tl_nom.upper()}"

    return nombre, tl_col, idx13, n52, rumbo

# ──────────────────────────────────────────────
#  Día regular (Tonalpohualli)
# ──────────────────────────────────────────────
def info_dia(fecha, dias, mapa, rumbos):
    idx = mapa[fecha.strftime("%d/%m")]
    ciclos = fecha.year - BASE_DAY.year - (1 if (fecha.month, fecha.day) < (3, 12) else 0)
    total  = ciclos * DIAS_XIUH + idx

    num   = (total % MOD_TONAL) + 1
    signo = dias[idx]["signo"]
    veint = dias[idx]["veintena"]

    trec_abs = total // 13
    trec     = trec_abs % 20 + 1
    rumbo    = rumbos[trec_abs % len(rumbos)]
    ini      = dias[(trec_abs * 13) % DIAS_XIUH]
    return num, signo, veint, trec, rumbo, ini, total

# ──────────────────────────────────────────────
#  Señor de la Noche (1‑9)
# ──────────────────────────────────────────────
def senor_noche(cal, total_dias):
    num = (total_dias % 9) + 1
    nom = next(x["nombre"] for x in cal["SENORES_9"] if x["numero"] == num)
    return num, nom

# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    cal, dias, mapa, numeros, rumbros = cargar_calendario()

    raw = input("🗓️ Ingresa la fecha (DD/MM/YYYY): ").strip()
    try:
        born = datetime.strptime(raw, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido.")
        return

    # — Año Xiuhmolpilli —
    nom_a, tl_col, idx13, n52, rumbo_a = info_xiuhmolpilli(born, numeros)
    print(f"🌽 {nom_a} (#{n52}/52) | 🌀 {tl_col} | 🧭 {rumbo_a}")

    # — Nemontemi (7‑11 de marzo) —
    if (born.month, born.day) in [(3, d) for d in range(7, 12)]:
        i = born.day - 7                                    # 0‑4
        signo = cal["NEMONTEMI"][tl_col][i]["nombre"].upper()

        start = ((idx13 - 1) * 5) % 13 + 1                 # número que abre 7‑mar
        num   = ((start - 1 + i) % 13) + 1

        print(f"🌌 Nemontemi: {num} {signo}")

        # — Acompañantes —
        acomp20 = next((x for x in cal["ACOMPANANTES_20_DIAS"] if x["signo"] == signo), None)
        if acomp20:
            print(f"🔶 Acompañante diurno del signo: {acomp20['acompanante_diurno']}")

        acomp13 = next((x for x in cal["ACOMPANANTES_TONALPOHUALLI"] if x["numero"] == num), None)
        if acomp13:
            print("🔹 Acompañantes tonal {0}: Diurno {1} • Volador {2} • Comp. {3}"
                  .format(num,
                          acomp13["acompanante_diurno"],
                          acomp13["acompanante_volador"],
                          acomp13["acompanante_complementario"]))
        return

    # — Día regular —
    num, signo, veint, trec, rumbo, ini, total = info_dia(born, dias, mapa, rumbros)
    print(f"🦅 {num} {signo} | 🌿 {veint} | 🧭 {rumbo}")

    print(f"📍 Trecena #{trec} (rumbo {rumbo}): inicia "
          f"1 {ini['signo']} ({ini['fecha']}) en {ini['veintena']}")

    acomp_tr = next((x for x in cal["ACOMPANANTES_TRESCENAS"] if x["numero"] == trec), None)
    if acomp_tr:
        print(f"✨ Acompañantes trecena: {', '.join(acomp_tr['acompanantes'])}")

    acomp20 = next((x for x in cal["ACOMPANANTES_20_DIAS"] if x["signo"] == signo), None)
    if acomp20:
        print(f"🔶 Acompañante diurno del signo: {acomp20['acompanante_diurno']}")

    acomp13 = next((x for x in cal["ACOMPANANTES_TONALPOHUALLI"] if x["numero"] == num), None)
    if acomp13:
        print("🔹 Acompañantes tonal {0}: Diurno {1} • Volador {2} • Comp. {3}"
              .format(num,
                      acomp13["acompanante_diurno"],
                      acomp13["acompanante_volador"],
                      acomp13["acompanante_complementario"]))

    # — Señor de la Noche (sólo días regulares) —
    num_s, nom_s = senor_noche(cal, total)
    print(f"🌙 Señor de la Noche: #{num_s} {nom_s}")


if __name__ == "__main__":
    main()
