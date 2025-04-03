import json
from datetime import datetime


def find_xiuhmolpilli(data, birth_date):
    """
    Dada una fecha de nacimiento (birth_date), localiza el 'name' y 'tlalpilli'
    en el JSON de Xiuhmolpilli. Se basa en la lógica:
      - Si la fecha >= 12 de marzo => usamos 'year1'
      - Si la fecha < 12 de marzo => usamos 'year2'
    Regresa una tupla: (name, tlalpilli), o None si no encuentra.
    """
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year

    # Decidir cuál "columna" (year1 o year2) corresponde,
    # siguiendo la lógica de la primera hoja:
    if (month > 3) or (month == 3 and day >= 12):
        # del 12 de marzo al 31 de diciembre => year1
        search_col = "year1"
    else:
        # del 1 de enero al 11 de marzo => year2
        search_col = "year2"

    # Recorrer todas las filas (row) de la lista
    for row_obj in data:
        # Revisar cada uno de los 4 "grupos": group1..group4
        for group_key in ["group1", "group2", "group3", "group4"]:
            group_data = row_obj[group_key]  # dict con 'tlalpilli', 'name', 'year1', 'year2', ...

            # Si en ese grupo coincide el año con la columna que nos interesa:
            if group_data[search_col] == year:
                # Retornar (name, tlalpilli)
                return (group_data["name"], group_data["tlalpilli"])

    # Si no se encontró nada, retornar None
    return None


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
        print(f"Para la fecha {birth_date.strftime('%d/%m/%Y')} = '{name}' ({tlalpilli})")


# ---------------------------------------
# Ejecutar si se llama directamente
# ---------------------------------------
if __name__ == "__main__":
    main()
