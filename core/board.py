"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/board.py".
"""

# Inicio del código.

## Inicio de imports.

from dataclasses import dataclass
from typing import Optional, List

## Fin de imports.

## Inicio de la clase «Point».

@dataclass
class Point:
    """Representa un punto (casilla) del tablero."""
    
    __owner__: Optional[str]
    __count__: int = 0
    """
    Atributos:
        __owner__: (Optional[str]): 'X', 'O' o None según quién tiene fichas en el punto.
        __count__: (int): Cantidad de fichas en el punto.
    """

    def __repr__(self) -> str:
        """
        Devuelve una representación en cadena del punto para depuración.

        Args:
            None
        Returns:
            str: Representación del punto (ej. 'X2' para 2 fichas de X, ' . ' si está vacío).
        """
        if self.__owner__ is None or self.__count__ == 0:
            return " . "
        return f"{self.__owner__}{self.__count__}"

## Fin de la clase «Point».

## Inicio de la clase «Board».

class Board:
    """
    Representa el tablero de Backgammon.
    - Contiene 24 puntos numerados (0 a 23).
    - Mantiene registro de fichas en la barra y fichas fuera.
    - Permite aplicar movimientos simples y reiniciar el tablero a la disposición inicial.
    """

    def __init__(self):
        """
        Inicializa un tablero vacío y lo coloca en la configuración estándar.

        Args:
            None
        Returns:
            None
        """
        self.__points__: List[Point] = [Point(None, 0) for _ in range(24)]
        self.__bar__ = {"X": 0, "O": 0}  ### Fichas en la barra.
        self.__off__ = {"X": 0, "O": 0}  ### Fichas retiradas del juego.
        self.__reset_to_standard__()

    def __reset_to_standard__(self):
        """
        Coloca las fichas en la configuración inicial estándar de Backgammon.

        Args:
            None
        Returns:
            None
        """
        layout = [
            (0, 'X', 2),  ### Punto 1 (index 0): 2 de X.
            (11, 'X', 5),
            (16, 'X', 3),
            (18, 'X', 5),
            (23, 'O', 2),
            (12, 'O', 5),
            (7, 'O', 3),
            (5, 'O', 5),
        ]
        ### Limpiar.
        for i in range(24):
            self.__points__[i] = Point(None, 0)
        ### Colocar según layout.
        for idx, owner, cnt in layout:
            self.__points__[idx].__owner__ = owner
            self.__points__[idx].__count__ = cnt

    def __is_point_owned_by__(self, index: int, player: str) -> bool:
        """
        Devuelve True si el punto pertenece al jugador indicado y posee fichas.

        Args:
            index (int): Índice del punto (0 a 23).
            player (str): Jugador ('X' o 'O').
        Returns:
            bool: True si el punto pertenece al jugador y tiene fichas, False en caso contrario.
        """
        p = self.__points__[index]
        return p.__owner__ == player and p.__count__ > 0

    def __apply_move__(self, src: int, dst: int, player: str) -> bool:
        """
        Aplica un movimiento simple de src → dst para el jugador.

        Args:
            src (int): Índice del punto de origen (0 a 23).
            dst (int): Índice del punto de destino (0 a 23).
            player (str): Jugador ('X' o 'O').

        Returns:
            bool: True si el movimiento fue exitoso, False si no es válido.

        Reglas básicas implementadas:
        - No permite mover desde un punto vacío o de otro jugador.
        - Bloquea mover a un punto con 2 o más fichas del oponente.
        - Si hay una ficha del oponente, la golpea (se envía a la barra).
        """
        if src < 0 or src >= 24 or dst < 0 or dst >= 24:
            return False
        if not self.__is_point_owned_by__(src, player):
            return False

        dest_point = self.__points__[dst]
        opponent = 'O' if player == 'X' else 'X'

        ### Comprobar bloqueo (punto con 2+ fichas del oponente).
        if dest_point.__owner__ == opponent and dest_point.__count__ >= 2:
            return False

        ### Remover ficha del punto origen.
        self.__points__[src].__count__ -= 1
        if self.__points__[src].__count__ == 0:
            self.__points__[src].__owner__ = None

        ### Resolver destino: golpe o movimiento normal.
        if dest_point.__owner__ == opponent and dest_point.__count__ == 1:
            ### Golpear ficha y mandarla a la barra.
            self.__bar__[opponent] += 1
            self.__points__[dst].__owner__ = player
            self.__points__[dst].__count__ = 1
        else:
            if dest_point.__count__ == 0:
                self.__points__[dst].__owner__ = player
                self.__points__[dst].__count__ = 1
            else:
                self.__points__[dst].__count__ += 1

        return True

## Fin de la clase «Board».

# Fin del código.