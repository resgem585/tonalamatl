import json
from datetime import datetime, timedelta

with open("calendario_base.json", encoding="utf-8") as f:
    base = json.load(f)


def generar_json_completo() -> dict:
    calendario = {}

    # ── 1) Veintenas (360 días) sin número_tonal ni rumbo ───────
    tonal_num = 1
    tonal_index = 0
    rumbo_index = 0

    signos = base["tonalpohualli_simbolos"]
    xiuh_meses = base["xiuhpohualli_meses"]
    rumbos = base["rumbos"]

    for mes, f_ini in xiuh_meses:
        dias = []
        fecha = datetime.strptime(f"{f_ini}/2024", "%d/%m/%Y")

        for d in range(1, 21):
            dias.append({"numero": d, "nombre": signos[tonal_index], "fecha": fecha.strftime("%d/%m")})

            fecha += timedelta(days=1)
            tonal_index = (tonal_index + 1) % 20
            if tonal_num == 13:
                tonal_num = 1
                rumbo_index = (rumbo_index + 1) % 4
            else:
                tonal_num += 1

        calendario[mes] = dias

    # ── 2) Nemontemi (5 días por tipo) sin número_tonal ni rumbo ─
    calendario["NEMONTEMI"] = {}
    fecha_base = datetime.strptime("07/03/2025", "%d/%m/%Y")
    for tipo, simbolos in base["nemontemi"].items():
        calendario["NEMONTEMI"][tipo] = [
            {
                "numero": i + 1,
                "nombre": simbolo,
                "fecha": (fecha_base + timedelta(days=i)).strftime("%d/%m"),
            }
            for i, simbolo in enumerate(simbolos)
        ]

    # ── 3) Acompañantes Tonalpohualli (13) ──────────────────────
    calendario["ACOMPANANTES_TONALPOHUALLI"] = [
        {"numero": n, **base["ACOMPANANTES_13"][str(n)]} for n in range(1, 14)
    ]

    # ── 4) Acompañantes de trecenas (20) ─────────────────────────
    calendario["ACOMPANANTES_TRESCENAS"] = [
        {"numero": t["trecena"], "acompanantes": t["acompanantes"]}
        for t in base["ACOMPANANTES_TRESCENAS"]
    ]

    # ── 5) Acompañantes de 20 signos & Señores de la Noche ──────
    calendario["ACOMPANANTES_20_DIAS"] = base["ACOMPANANTES_20_DIAS"]
    calendario["SENORES_9"] = base["SENORES_9"]

    # ── 6) Listas nombre‑valor de signos y números ───────────────
    calendario["TONALPOHUALLI_SIMBOLOS"] = [
        {"nombre": i + 1, "valor": s} for i, s in enumerate(signos)
    ]
    calendario["numeros"] = [
        {"nombre": i + 1, "valor": n} for i, n in enumerate(base["numeros"])
    ]

    return calendario


def guardar_json(data: dict, filename="calendario_completo.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    guardar_json(generar_json_completo())
    print("✅  JSON generado: ‘numero_tonal’ y ‘rumbo’ eliminados también de Nemontemi.")
