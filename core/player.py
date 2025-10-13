"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/player.py".
"""

### Inicio del código.

## Inicio de imports.

from typing import Optional
from board import Board
from dice import Dice

## Fin de imports.

## Inicio de la clase «Player».

class Player:
    """
    Representa un jugador en el juego de Backgammon.
    - Almacena el identificador del jugador ('X' o 'O') y un nombre opcional.
    - Interactúa con el tablero y los dados para realizar movimientos.
    - Consulta el estado del tablero para verificar condiciones de retiro o victoria.
    """

    def __init__(self, id: str, name: Optional[str] = None):
        """
        Inicializa un jugador con un identificador y un nombre opcional.

        Args:
            id (str): Identificador del jugador ('X' o 'O').
            name (Optional[str]): Nombre del jugador (opcional).
        Raises:
            ValueError: Si el identificador no es 'X' o 'O'.
        """
        if id not in ['X', 'O']:
            raise ValueError("El identificador debe ser 'X' o 'O'")
        self.__id__ = id
        self.__name__ = name if name else id

    @property
    def id(self) -> str:
        """
        Obtiene el identificador del jugador.

        Returns:
            str: Identificador del jugador ('X' o 'O').
        """
        return self.__id__

    @property
    def name(self) -> str:
        """
        Obtiene el nombre del jugador.

        Returns:
            str: Nombre del jugador (o identificador si no se proporcionó nombre).
        """
        return self.__name__

    def __can_bear_off__(self, board: Board) -> bool:
        """
        Verifica si el jugador puede retirar fichas.

        Args:
            board (Board): Instancia del tablero.
        Returns:
            bool: True si el jugador puede retirar fichas, False en caso contrario.
        """
        return board.__can_bear_off__(self.__id__)

    def __has_won__(self, board: Board) -> bool:
        """
        Verifica si el jugador ha ganado (todas las fichas retiradas).

        Args:
            board (Board): Instancia del tablero.
        Returns:
            bool: True si el jugador ha retirado todas sus fichas, False en caso contrario.
        """
        return board.__get_off__(self.__id__) == 15

    def __try_move__(self, src: int, dst: int, board: Board, dice: Dice) -> bool:
        """
        Intenta realizar un movimiento, validándolo con los dados y aplicándolo en el tablero.

        Args:
            src (int): Índice del punto de origen (-1 para barra, 0 a 23 para puntos).
            dst (int): Índice del punto de destino (-1 para retiro de O, 0 a 23 para puntos, 24 para retiro de X).
            board (Board): Instancia del tablero.
            dice (Dice): Instancia de los dados.
        Returns:
            bool: True si el movimiento fue exitoso y el dado consumido, False si no es válido.
        """
        if dice.__can_move__(src, dst, self.__id__, board):
            return dice.__use_die__(src, dst, self.__id__)
        return False

## Fin de la clase «Player».

### Fin del código.