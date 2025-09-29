"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/dice.py".
"""

### Inicio del código.

## Inicio.

## Inicio de imports.

import random
from typing import List, Tuple
from board import Board

## Fin de imports.

## Inicio de la clase «Dice».

class Dice:
    """
    Representa los dados en un juego de Backgammon.
    - Maneja el lanzamiento de dos dados de 6 caras.
    - Valida movimientos basados en los valores de los dados.
    - Registra y consume los valores usados.
    """

    def __init__(self):
        """
        Inicializa los dados sin valores asignados.

        Args:
            None
        Returns:
            None
        """
        self.__dice__: List[int] = []  # Valores de los dados disponibles

## Fin de la clase «Dice».

## Fin.

### Fin del código.