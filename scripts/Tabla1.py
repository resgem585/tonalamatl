import json
from datetime import datetime, timedelta

with open("calendario_base.json", encoding="utf-8") as f:
    base = json.load(f)


def generar_json_completo() -> dict:
    calendario = {}

    # ── Datos base ──────────────────────────────────────────────
    signos = base["tonalpohualli_simbolos"]
    numeros_nahuas = base["NUMEROS"]
    xiuh_meses = base["xiuhpohualli_meses"]          # lista [mes, dd/mm]
    rumbos = base["RUMBOS_TONAL"]
    nemontemi = base["nemontemi"]
    acomp13 = base["ACOMPANANTES_13"]
    acomp20 = base["ACOMPANANTES_20_DIAS"]
    senores9 = base["SENORES_9"]
    acomp_trecenas = base["ACOMPANANTES_TRESCENAS"]

    # ── 1) Veintenas (360 días) ────────────────────────────────
    tonal_idx = 0
    for mes, f_ini in xiuh_meses:
        dias = []
        # ► FECHA FICTICIA 2023 (no bisiesto → febrero = 28 días)
        fecha = datetime.strptime(f"{f_ini}/2023", "%d/%m/%Y")
        for n_dia in range(1, 21):
            dias.append(
                {
                    "numero": n_dia,
                    "nombre": signos[tonal_idx],
                    "fecha": fecha.strftime("%d/%m"),
                }
            )
            fecha += timedelta(days=1)
            tonal_idx = (tonal_idx + 1) % 20
        calendario[mes] = dias

    # ── 2) Nemontemi (7‑11 de marzo) ───────────────────────────
    calendario["NEMONTEMI"] = {
        col: [
            {
                "nombre": simbolo,
                "fecha": f"{7 + i:02d}/03"           # 07‑11 de marzo
            }
            for i, simbolo in enumerate(simbolos)
        ]
        for col, simbolos in nemontemi.items()
    }

    # ── 3) Acompañantes Tonalpohualli (13) ─────────────────────
    calendario["ACOMPANANTES_TONALPOHUALLI"] = [
        {"numero": n, **acomp13[str(n)]} for n in range(1, 14)
    ]

    # ── 4) Acompañantes de trecenas (20) ───────────────────────
    calendario["ACOMPANANTES_TRESCENAS"] = [
        {"numero": t["trecena"], "acompanantes": t["acompanantes"]}
        for t in acomp_trecenas
    ]

    # ── 5) Acompañantes de 20 signos + Señores de la Noche ─────
    calendario["ACOMPANANTES_20_DIAS"] = acomp20
    calendario["SENORES_9"] = senores9

    # ── 6) Listas clave‑valor de signos y números ──────────────
    calendario["TONALPOHUALLI_SIMBOLOS"] = [
        {"clave": i + 1, "valor": s} for i, s in enumerate(signos)
    ]
    calendario["numeros"] = [
        {"clave": i + 1, "valor": n} for i, n in enumerate(numeros_nahuas)
    ]

    # ── 7) RUMBOS_TONAL ────────────────────────────────────────
    calendario["RUMBOS_TONAL"] = rumbos

    return calendario


def guardar_json(data: dict, filename="calendario_completo.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    guardar_json(generar_json_completo())
    print("✅  calendario_completo.json generado con 360 días (último: 06‑03).")
