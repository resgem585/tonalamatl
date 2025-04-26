import json
from datetime import datetime, date
from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import find_nemontemi_day

# ─────────────────────────────
#  Parámetros y tablas fijas
# ─────────────────────────────
ANCHOR = date(1987, 3, 12)        # 1 Cipactli “histórico”
DIAS_XIUH = 360                   # 18 veintenas
MOD_TONAL = 13
EXTRAS = {
    "NEMONTEMI",
    "ACOMPANANTES_TONALPOHUALLI",
    "ACOMPANANTES_20_DIAS",
    "ACOMPANANTES_TRESCENAS",
    "SENORES_9",
    "RUMBOS_TONAL",
    "TONALPOHUALLI_SIMBOLOS",
    "numeros",
}

# Rumbo asociado al tlalpilli del año
TLALPILLI_RUMBO = {
    "Tochtli": "Tlahuiztlampa (Oriente)",
    "Acatl":   "Mictlampa (Norte)",
    "Tecpatl": "Cihuatlampa (Poniente)",
    "Calli":   "Huitztlampa (Sur)",
}


def _build_regular_days(cal):
    days, idx = [], {}
    for veintena, lst in cal.items():
        if veintena in EXTRAS or not isinstance(lst, list):
            continue
        for d in lst:
            days.append(
                {"i": len(days), "veintena": veintena,
                 "signo": d["nombre"].upper(), "fecha": d["fecha"]}
            )
            idx[d["fecha"]] = days[-1]["i"]
    return days, idx


# ─────────────────────────────
#  MAIN
# ─────────────────────────────
def main() -> None:
    with open("xiuhmolpilli.json", encoding="utf-8") as f:
        xiuhmolpilli = json.load(f)
    with open("calendario_completo.json", encoding="utf-8") as f:
        cal = json.load(f)

    días, fecha2i = _build_regular_days(cal)
    rumbos_trecena = cal.get("RUMBOS_TONAL", [])

    # ── Fecha de entrada ────────────────────────────
    raw = input("🗓️ Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        born = datetime.strptime(raw, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido.")
        return

    # ── Año Xiuhmolpilli (1-52) y tlalpilli ─────────
    año_nom, tlalpilli = find_xiuhmolpilli(xiuhmolpilli, born) or (None, None)
    if año_nom:
        # localizar número 1-52
        num52 = None
        for fila in xiuhmolpilli:                       # anio 1-13
            for col, g in enumerate(("group1", "group2", "group3", "group4"), 1):
                if fila[g]["name"] == año_nom:
                    num52 = (col - 1) * 13 + fila["anio"]
                    break
            if num52:
                break
        rumbo_año = TLALPILLI_RUMBO.get(tlalpilli, "¿?")
        print(f"🌽 Año Xiuhmolpilli: {año_nom} (#{num52}/52)  |  🌀 Tlalpilli: {tlalpilli}  |  🧭 Rumbo: {rumbo_año}")
    else:
        print("⚠️ Sin Tlalpilli para tu fecha.")

    # ── ¿Nemontemi? ─────────────────────────────────
    if (born.month, born.day) in [(3, d) for d in range(7, 12)] and año_nom:
        num_tonal, signo, veintena = find_nemontemi_day(cal, tlalpilli, born)
        rumbo = next(
            (d["rumbo"] for d in cal["NEMONTEMI"][tlalpilli]
             if d["fecha"] == born.strftime("%d/%m")),
            None,
        )
        trecena_cíc = None
    else:
        # Día regular
        key = born.strftime("%d/%m")
        if key not in fecha2i:
            print("❌ Día Tonalpohualli no encontrado.")
            return
        i = fecha2i[key]
        ciclos = born.year - ANCHOR.year
        if (born.month, born.day) < (3, 12):
            ciclos -= 1
        total = ciclos * DIAS_XIUH + i

        num_tonal = (total % MOD_TONAL) + 1
        signo = días[i]["signo"]
        veintena = días[i]["veintena"]

        trec_abs = total // 13
        trecena_cíc = trec_abs % 20 + 1
        rumbo = rumbos_trecena[trec_abs % len(rumbos_trecena)] if rumbos_trecena else None

        # comienzo de la trecena
        ini = días[(trec_abs * 13) % DIAS_XIUH]

    # ── Salida del día ──────────────────────────────
    out = f"🦅 {num_tonal} {signo}  |  🌿 {veintena}"
    if rumbo:
        out += f"  |  🧭 {rumbo}"
    print(out)

    # ── Info de trecena (si aplica) ─────────────────
    if trecena_cíc:
        print(f"📍 Trecena #{trecena_cíc}: inicia 1 {ini['signo']} ({ini['fecha']}) en {ini['veintena']}")
        acomp_tr = next((x for x in cal["ACOMPANANTES_TRESCENAS"]
                         if x["numero"] == trecena_cíc), None)
        if acomp_tr:
            print(f"✨ Acompañantes: {', '.join(acomp_tr['acompanantes'])}")
    else:
        print("🌌 Días Nemontemi (fuera de la cuenta regular)")

    # ── Acompañantes varios ─────────────────────────
    acomp20 = next((x for x in cal["ACOMPANANTES_20_DIAS"]
                    if x["signo"] == signo), None)
    if acomp20:
        print(f"🔶 Acompañante diurno: {acomp20['acompanante_diurno']}")

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
