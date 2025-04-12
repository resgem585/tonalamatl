import json
from datetime import datetime
from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import find_xiuhpohualli_day, find_nemontemi_day, encontrar_trecena_de_fecha


def main():
    # 1) Cargar los archivos JSON 📚
    with open("xiuhmolpilli.json", "r", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)

    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_data = json.load(f)

    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_nemontemi_data = json.load(f)

    # 2) Solicitar fecha al usuario 📆
    birth_str = input("🗓️ Ingresa tu fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("❌ Formato inválido. Usa DD/MM/YYYY. Ejemplo: 07/01/1989")
        return

    # 3) Buscar el año Xiuhmolpilli 🌾🔥
    year_result = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)
    if year_result is None:
        print("⚠️ No se encontró el Tlalpilli correspondiente.")
        tlalpilli = None
    else:
        name, tlalpilli = year_result
        print(f"🌽 Año Xiuhmolpilli: {name} | 🌀 Tlalpilli: {tlalpilli}")

    # 4) Buscar día Tonalpohualli 🐉🌞
    day_result = None
    if birth_date.month == 3 and 7 <= birth_date.day <= 11 and tlalpilli:
        day_result = find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date)
        if day_result is not None:
            print("🌌 ¡Has nacido en días Nemontemi (fuera del tiempo sagrado)! 🌠")
    else:
        day_result = find_xiuhpohualli_day(calendario_data, birth_date)

    # 5) Resultados Tonalpohualli 📜✨
    if day_result is None:
        print("❌ No se encontró día Tonalpohualli para tu fecha.")
    else:
        if len(day_result) == 4:
            numero_tonal, nombre_signo, nombre_mes, rumbo = day_result
        else:
            numero_tonal, nombre_signo, nombre_mes = day_result
            rumbo = None

        print(f"🦅 Tu día Tonalpohualli: {numero_tonal} {nombre_signo}")
        print(f"🌿 Veintena (mes): {nombre_mes}")

        if rumbo:
            print(f"🧭 Rumbo: {rumbo}")

        # 6) Mostrar la trecena solo si no es Nemontemi 🔮📅
        if nombre_mes != "NEMONTEMI":
            trecena_info = encontrar_trecena_de_fecha(birth_date, calendario_data)
            if trecena_info:
                idx, tonal, signo, veintena, fecha_inicio = trecena_info
                print(f"📍 Trecena {idx}: comienza con {tonal} {signo}")
                print(f"📆 Fecha de inicio: {fecha_inicio}")
                print(f"🌿 Veintena en la que inicia: {veintena}")
        else:
            print("🌌 Los días Nemontemi no pertenecen a ninguna trecena y veintena (tiempo fuera del calendario regular).")


if __name__ == "__main__":
    main()
