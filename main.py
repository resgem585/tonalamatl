import json
from datetime import datetime

from xiuhmolpilli import find_xiuhmolpilli
from xiuhpohualli import find_xiuhpohualli_day, find_nemontemi_day

def main():
    # 1) Cargar el JSON de los Años Xiuhmolpilli
    with open("xiuhmolpilli.json", "r", encoding="utf-8") as f:
        xiuhmolpilli_data = json.load(f)

    # 2) Cargar el JSON del Tonalpohualli (días normales)
    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_data = json.load(f)

    # 3) Cargar el JSON especial para Nemontemi
    with open("calendario_xiuhpohualli.json", "r", encoding="utf-8") as f:
        calendario_nemontemi_data = json.load(f)

    # 4) Pedir fecha de nacimiento
    birth_str = input("Ingrese su fecha de nacimiento (DD/MM/YYYY): ").strip()
    try:
        birth_date = datetime.strptime(birth_str, "%d/%m/%Y").date()
    except ValueError:
        print("Formato inválido. Use DD/MM/YYYY. Ejemplo: 07/01/1989")
        return

    # 5) Determinar el Año Xiuhmolpilli y su Tlalpilli
    year_result = find_xiuhmolpilli(xiuhmolpilli_data, birth_date)
    if year_result is None:
        print("No se encontró el Tlalpilli en el JSON de Xiuhmolpilli.")
        # Si no hay año, de todos modos intentamos ver si hay día Tonalpohualli
        tlalpilli = None
    else:
        name, tlalpilli = year_result
        print(f"Tu año Xiuhmolpilli es: {name}, Tlalpilli: {tlalpilli}")

    # 6) Verificar si la fecha está en el rango Nemontemi: 7 a 11 de marzo
    #    Si sí, usamos el JSON especial (xiuhpohualli_nemontemi.json)
    #    buscando en la sección "NEMONTEMI" con la clave = Tlalpilli (si existe).
    day_result = None
    if birth_date.month == 3 and 7 <= birth_date.day <= 11 and tlalpilli:
        # Intentar obtener el día Nemontemi
        day_result = find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date)

        # Si no encontramos nada, day_result seguirá como None
        if day_result is not None:
            print("¡Estás en días Nemontemi!")
    else:
        # 7) Caso normal: usar calendario_xiuhpohualli.json
        day_result = find_xiuhpohualli_day(calendario_data, birth_date)

    # 8) Mostrar resultados del Tonalpohualli
    if day_result is None:
        print("No se encontró día Tonalpohualli para tu fecha en los archivos JSON.")
    else:
        numero_tonal, nombre_signo, nombre_mes = day_result
        print(f"Tu día Tonalpohualli es: {numero_tonal} {nombre_signo}")
        print(f"Nombre de la Veintena/Mes: {nombre_mes}")

if __name__ == "__main__":
    main()
