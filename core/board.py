"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/board.py".
"""

# Incio del código.

## Incio de imports.

from dataclasses import dataclass
from typing import Optional

## Fin de imports.

## Incio de la clase «Point».

@dataclass
class Point:
    """Representa un punto (casilla) del tablero."""
    
    owner: Optional[str]
    count: int = 0
    """
    Atributos:
        owner (Optional[str]): 'X', 'O' o None según quién tiene fichas en el punto.
        count (int): cantidad de fichas en el punto.
    """

    def __repr__(self) -> str:
        """Devuelve una representación legible del punto para la depuración."""
        if self.owner is None or self.count == 0:
            return " . "
        return f"{self.owner}{self.count}"

## Fin de la clase «Point».

## Incio de la clase «Board».

## Fin de la clase «Board».

# Fin del código.