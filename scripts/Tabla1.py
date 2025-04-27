import json
from datetime import datetime, timedelta

with open("calendario_base.json", encoding="utf-8") as f:
    base = json.load(f)


def generar_json_completo() -> dict:
    calendario = {}

    # ── Datos base ──────────────────────────────────────────────
    signos = base["tonalpohualli_simbolos"]
    numeros_nahuas = base["NUMEROS"]
    xiuh_meses = base["xiuhpohualli_meses"]
    rumbos = base["RUMBOS_TONAL"]  # ← 4 rumbos
    nemontemi = base["nemontemi"]
    acomp13 = base["ACOMPANANTES_13"]
    acomp20 = base["ACOMPANANTES_20_DIAS"]
    senores9 = base["SENORES_9"]
    acomp_trecenas = base["ACOMPANANTES_TRESCENAS"]

    # ── 1) Veintenas (360 días) ─────────────────────────────────
    tonal_num = 1
    tonal_idx = 0
    rumbo_idx = 0

    for mes, f_ini in xiuh_meses:
        dias = []
        fecha = datetime.strptime(f"{f_ini}/2024", "%d/%m/%Y")
        for d in range(1, 21):
            dias.append({"numero": d, "nombre": signos[tonal_idx], "fecha": fecha.strftime("%d/%m")})
            fecha += timedelta(days=1)
            tonal_idx = (tonal_idx + 1) % 20
            tonal_num = 1 if tonal_num == 13 else tonal_num + 1
            if tonal_num == 1:
                rumbo_idx = (rumbo_idx + 1) % 4
        calendario[mes] = dias

    # ── 2) Nemontemi (5 días por tipo) ─────────────────────────
    calendario["NEMONTEMI"] = {}
    fecha_base = datetime.strptime("07/03/2025", "%d/%m/%Y")
    for tipo, simbolos in nemontemi.items():
        calendario["NEMONTEMI"][tipo] = [
            {
                "numero": i + 1,
                "nombre": simbolo,
                "fecha": (fecha_base + timedelta(days=i)).strftime("%d/%m"),
            }
            for i, simbolo in enumerate(simbolos)
        ]

    # ── 3) Acompañantes Tonalpohualli (13) ─────────────────────
    calendario["ACOMPANANTES_TONALPOHUALLI"] = [
        {"numero": n, **acomp13[str(n)]} for n in range(1, 14)
    ]

    # ── 4) Acompañantes de trecenas (20) ───────────────────────
    calendario["ACOMPANANTES_TRESCENAS"] = [
        {"numero": t["trecena"], "acompanantes": t["acompanantes"]} for t in acomp_trecenas
    ]

    # ── 5) Acompañantes de 20 signos & Señores de la Noche ─────
    calendario["ACOMPANANTES_20_DIAS"] = acomp20
    calendario["SENORES_9"] = senores9

    # ── 6) Listas clave-valor de signos y números ──────────────
    calendario["TONALPOHUALLI_SIMBOLOS"] = [
        {"clave": i + 1, "valor": s} for i, s in enumerate(signos)
    ]
    calendario["numeros"] = [
        {"clave": i + 1, "valor": n} for i, n in enumerate(numeros_nahuas)
    ]

    # ── 7) **RUMBOS_TONAL** — los 4 rumbos en orden ─────────────
    calendario["RUMBOS_TONAL"] = rumbos      # ["Tlahuiztlampa", "Huitztlampa", "Cihuatlampa", "Mictlampa"]

    return calendario


def guardar_json(data: dict, filename="./calendario_completo.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    guardar_json(generar_json_completo())
    print("✅  JSON generado con el bloque 'RUMBOS_TONAL' incluido.")
