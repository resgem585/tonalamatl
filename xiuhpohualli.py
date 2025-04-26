from datetime import datetime
from typing import Optional, List, Tuple, Dict, Any

# Claves que no representan veintenas
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


# ──────────────────────────────
#  Ayudas internas
# ──────────────────────────────
def _numero_tonal(dia_abs: int) -> int:
    """Número tonal (1‑13) cíclico."""
    return (dia_abs % 13) + 1


def _rumbo_por_trecena(idx_trecena: int, rumbos: List[str]) -> str:
    """Rumbo asignado a la trecena (0‑based)."""
    return rumbos[idx_trecena % len(rumbos)]


def _es_lista_dias(item: Any) -> bool:
    """
    True si `item` es lista de diccionarios con claves típicas de un día.
    """
    return (
            isinstance(item, list)
            and item
            and isinstance(item[0], dict)
            and {"nombre", "fecha"}.issubset(item[0].keys())
    )


# ──────────────────────────────
#  Día Xiuhpohualli / Tonalpohualli
# ──────────────────────────────
def find_xiuhpohualli_day(
        calendario_data: Dict[str, Any],
        birth_date,
) -> Optional[Tuple[int, str, str]]:
    """
    Retorna (numero_tonal, signo, veintena) para la fecha dada.
    """
    fecha_str = birth_date.strftime("%d/%m")
    dia_abs = 0

    for veintena, dias in calendario_data.items():
        if veintena in EXTRAS or not _es_lista_dias(dias):
            continue

        for dia in dias:
            if dia["fecha"] == fecha_str:
                return _numero_tonal(dia_abs), dia["nombre"], veintena
            dia_abs += 1
    return None


# ──────────────────────────────
#  Nemontemi (sin cambios)
# ──────────────────────────────
def find_nemontemi_day(calendario_nemontemi_data, tlalpilli, birth_date):
    fecha_str = birth_date.strftime("%d/%m")
    nemontemi_dict = calendario_nemontemi_data.get("NEMONTEMI", {})
    if tlalpilli not in nemontemi_dict:
        return None

    for dia in nemontemi_dict[tlalpilli]:
        if dia["fecha"] == fecha_str:
            return dia["numero_tonal"], dia["nombre"], "NEMONTEMI"
    return None


# ──────────────────────────────
#  Inicios de trecena y búsqueda
# ──────────────────────────────
def encontrar_inicios_de_trecenas(
        calendario_data: Dict[str, Any]
) -> List[Tuple[int, str, str, str]]:
    """
    Devuelve lista de (numero_tonal, signo, veintena, fecha_dd/mm) para los 20
    inicios reales de trecena.
    """
    inicios = []
    dia_abs = 0

    for veintena, dias in calendario_data.items():
        if veintena in EXTRAS or not _es_lista_dias(dias):
            continue
        for dia in dias:
            if dia_abs % 13 == 0:
                inicios.append(
                    (_numero_tonal(dia_abs), dia["nombre"], veintena, dia["fecha"])
                )
            dia_abs += 1
    return inicios


def encontrar_trecena_de_fecha(
        birth_date, calendario_data: Dict[str, Any]
) -> Optional[Tuple[int, int, str, str, str]]:
    inicios = encontrar_inicios_de_trecenas(calendario_data)
    for i, (_, _, _, fecha_inicio) in enumerate(inicios):
        f_ini = datetime.strptime(
            fecha_inicio + f"/{birth_date.year}", "%d/%m/%Y"
        ).date()
        f_fin = (
            datetime.strptime(
                inicios[i + 1][3] + f"/{birth_date.year}", "%d/%m/%Y"
            ).date()
            if i + 1 < len(inicios)
            else datetime(birth_date.year + 1, 1, 1).date()
        )
        if f_ini <= birth_date < f_fin:
            tonal, signo, veintena, _ = inicios[i]
            return i + 1, tonal, signo, veintena, fecha_inicio
    return None


# ──────────────────────────────
#  Rumbo calculado para días regulares
# ──────────────────────────────
def obtener_rumbo(calendario_data: Dict[str, Any], birth_date) -> Optional[str]:
    """
    Devuelve rumbo según la trecena usando la lista RUMBOS_TONAL.
    """
    rumbos = calendario_data.get("RUMBOS_TONAL", [])
    if not rumbos:
        return None

    inicios = encontrar_inicios_de_trecenas(calendario_data)
    for idx, (_, _, _, fecha_inicio) in enumerate(inicios):
        f_ini = datetime.strptime(
            fecha_inicio + f"/{birth_date.year}", "%d/%m/%Y"
        ).date()
        f_fin = (
            datetime.strptime(
                inicios[idx + 1][3] + f"/{birth_date.year}", "%d/%m/%Y"
            ).date()
            if idx + 1 < len(inicios)
            else datetime(birth_date.year + 1, 1, 1).date()
        )
        if f_ini <= birth_date < f_fin:
            return _rumbo_por_trecena(idx, rumbos)
    return None


# ──────────────────────────────
#  Señores de la Noche (sin cambios)
# ──────────────────────────────
def obtener_senor_de_la_noche(calendario_data, birth_date):
    """
    Devuelve (número, nombre) del Señor de la Noche que rige el día dado.
    """
    fecha_str = birth_date.strftime("%d/%m")
    dia_abs = 0

    for veintena, dias in calendario_data.items():
        if veintena in EXTRAS or not _es_lista_dias(dias):
            continue
        for dia in dias:
            if dia["fecha"] == fecha_str:
                num_senor = (dia_abs % 9) + 1
                senor = next(
                    s for s in calendario_data["SENORES_9"] if s["numero"] == num_senor
                )
                return num_senor, senor["nombre"]
            dia_abs += 1
    return None
