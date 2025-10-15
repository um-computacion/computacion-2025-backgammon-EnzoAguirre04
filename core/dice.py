"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/dice.py".
"""

### Inicio del código.

## Inicio de imports.

import random
from typing import List
from core.board import Board

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
        self.__dice__: List[int] = []  # Valores de los dados disponibles.

    def __roll__(self) -> None:
        """
        Lanza dos dados de 6 caras, asignando valores disponibles.
        Si los dados son iguales (dobles), se asignan cuatro movimientos.

        Args:
            None
        Returns:
            None
        """
        die1, die2 = random.randint(1, 6), random.randint(1, 6)
        self.__dice__ = [die1, die2]
        if die1 == die2:
            self.__dice__ = [die1] * 4  # Dobles: Cuatro movimientos.

    def __get_available_dice__(self) -> List[int]:
        """
        Obtiene los valores de los dados disponibles.

        Returns:
            List[int]: Lista de valores de dados disponibles.
        """
        return self.__dice__.copy()
    
    def __can_move__(self, src: int, dst: int, player: str, board: Board) -> bool:
        """
        Verifica si un movimiento es válido según los valores de los dados disponibles.

        Args:
            src (int): Índice del punto de origen (-1 para barra, 0 a 23 para puntos).
            dst (int): Índice del punto de destino (-1 para retiro de O, 0 a 23 para puntos, 24 para retiro de X).
            player (str): Jugador ('X' o 'O').
            board (Board): Instancia del tablero para validar el estado.

        Returns:
            bool: True si el movimiento es válido según los dados, False en caso contrario.

        Reglas implementadas:
        - Para movimientos normales: abs(dst - src) debe coincidir con un dado disponible.
        - Para movimientos desde la barra: dst = die_value - 1 (para X) o dst = 24 - die_value (para O).
        - Para retiro: el dado debe corresponder al punto exacto o al punto más alto disponible.
        """
        if not self.__dice__:
            return False  # No hay dados disponibles.

        # Movimiento desde la barra.
        if src == -1:
            expected_dst = self.__dice__[0] - 1 if player == 'X' else 24 - self.__dice__[0]
            return dst == expected_dst and board.__apply_move__(src, dst, player)

        # Retiro de las fichas.
        if (player == 'X' and dst == 24) or (player == 'O' and dst == -1):
            if not board.__can_bear_off__(player):
                return False
            home_board = range(18, 24) if player == 'X' else range(0, 6)
            if src not in home_board:
                return False
            # Verificar si el dado corresponde al punto exacto o uno más alto.
            exact_die = 24 - src if player == 'X' else src + 1
            if exact_die in self.__dice__:
                return board.__apply_move__(src, dst, player)
            # Retiro flexible: Usar el punto más alto si el exacto está vacío.
            for die in self.__dice__:
                if die > exact_die:
                    for i in home_board:
                        if i > src if player == 'X' else i < src:
                            if board.__is_point_owned_by__(i, player):
                                return False  # Hay un punto más alto con fichas.
                    return board.__apply_move__(src, dst, player)
            return False

        # Movimiento normal.
        distance = abs(dst - src)
        if distance in self.__dice__:
            return board.__apply_move__(src, dst, player)
        return False
    
    def __use_die__(self, src: int, dst: int, player: str) -> bool:
        """
        Consume un dado usado en un movimiento válido.

        Args:
            src (int): Índice del punto de origen.
            dst (int): Índice del punto de destino.
            player (str): Jugador ('X' o 'O').
        Returns:
            bool: True si el dado fue consumido, False si no es válido.
        """
        if not self.__dice__:
            return False

        # Movimiento desde la barra.
        if src == -1:
            expected_dst = self.__dice__[0] - 1 if player == 'X' else 24 - self.__dice__[0]
            if dst == expected_dst:
                self.__dice__.pop(0)
                return True
            return False

        # Retiro de fichas.
        if (player == 'X' and dst == 24) or (player == 'O' and dst == -1):
            exact_die = 24 - src if player == 'X' else src + 1
            if exact_die in self.__dice__:
                self.__dice__.remove(exact_die)
                return True
            # Retiro flexible: Usa el dado más grande disponible.
            max_die = max(self.__dice__)
            if max_die > exact_die:
                self.__dice__.remove(max_die)
                return True
            return False

        # Movimiento normal.
        distance = abs(dst - src)
        if distance in self.__dice__:
            self.__dice__.remove(distance)
            return True
        return False

## Fin de la clase «Dice».

### Fin del código.