import json
from datetime import datetime
from xiuhmolpilli import find_xiuhmolpilli


def main():
    # 1. Cargar el JSON (ajusta el nombre de tu archivo si es distinto)
    json_path = "xiuhmolpilli.json"
    with open(json_path, "r", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)

    # 2. Pedir fecha de nacimiento al usuario
    birth_str = input("Ingrese su fecha de nacimiento (DD/MM/YYYY): ").strip()

    # 3. Convertir a datetime.date
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("Formato inválido. Por favor use DD/MM/YYYY. Ej: 07/01/1989")
        return

    # 4. Localizar en la estructura JSON
    result = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)

    # 5. Mostrar resultado
    if result is None:
        print("No se encontró un Tlalpilli para ese año en el JSON.")
    else:
        name, tlalpilli = result
        print(f"Año de nacimiento: {birth_date.strftime('%d/%m/%Y')} = Año: '{name}' Tlalpilli: '{tlalpilli}'")


if __name__ == "__main__":
    main()
