"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/game.py".
"""

### Inicio del código.

## Inicio de imports.

from typing import Optional
from core.board import Board
from core.dice import Dice
from core.player import Player

## Fin de imports.

## Inicio de la clase «Game».

class Game:
    """
    Representa un juego de Backgammon.
    - Gestiona el tablero, los dados, y los jugadores.
    - Controla el flujo de los turnos y verifica condiciones de victoria.
    - Proporciona métodos para consultar el estado del juego.
    """

    def __init__(self, player_x_name: Optional[str] = None, player_o_name: Optional[str] = None):
        """
        Inicializa un nuevo juego con dos jugadores, un tablero, y dados.

        Args:
            player_x_name (Optional[str]): Nombre del jugador X (opcional).
            player_o_name (Optional[str]): Nombre del jugador O (opcional).
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__players__ = {
            'X': Player('X', player_x_name),
            'O': Player('O', player_o_name)
        }
        self.__current_player__ = 'X'  # X comienza.
        self.__dice_rolled__ = False

    def __get_board__(self) -> Board:
        """
        Obtiene la instancia del tablero.

        Returns:
            Board: Instancia del tablero.
        """
        return self.__board__

    def __get_current_player__(self) -> Player:
        """
        Obtiene el jugador actual.

        Returns:
            Player: Instancia del jugador actual.
        """
        return self.__players__[self.__current_player__]

    def __get_available_dice__(self) -> list[int]:
        """
        Obtiene los valores de los dados disponibles.

        Returns:
            list[int]: Lista de valores de dados disponibles.
        """
        return self.__dice__.__get_available_dice__()

    def __roll_dice__(self) -> None:
        """
        Lanza los dados para el turno del jugador actual.
        Solo permitido si los dados no han sido lanzados en este turno.

        Raises:
            RuntimeError: Si los dados ya fueron lanzados en este turno.
        """
        if self.__dice_rolled__:
            raise RuntimeError("Los dados ya fueron lanzados en este turno")
        self.__dice__.__roll__()
        self.__dice_rolled__ = True

    def __try_move__(self, src: int, dst: int) -> bool:
        """
        Intenta realizar un movimiento para el jugador actual.

        Args:
            src (int): Índice del punto de origen (-1 para barra, 0 a 23 para puntos).
            dst (int): Índice del punto de destino (-1 para retiro de O, 0 a 23 para puntos, 24 para retiro de X).
        Returns:
            bool: True si el movimiento fue exitoso, False si no es válido.
        Raises:
            RuntimeError: Si los dados no han sido lanzados.
        """
        if not self.__dice_rolled__:
            raise RuntimeError("Debes lanzar los dados antes de mover")
        player = self.__players__[self.__current_player__]
        result = player.__try_move__(src, dst, self.__board__, self.__dice__)
        if result and not self.__dice__.__get_available_dice__():
            self.__end_turn__()
        return result

    def __end_turn__(self) -> None:
        """
        Finaliza el turno del jugador actual, alternando al siguiente jugador.

        Args:
            None
        Returns:
            None
        """
        self.__current_player__ = 'O' if self.__current_player__ == 'X' else 'X'
        self.__dice_rolled__ = False

    def __get_winner__(self) -> Optional[Player]:
        """
        Verifica si hay un ganador (jugador que ha retirado todas sus fichas).

        Returns:
            Optional[Player]: Instancia del jugador ganador, o None si no hay ganador.
        """
        for player in self.__players__.values():
            if player.__has_won__(self.__board__):
                return player
        return None

## Fin de la clase «Game».

### Fin del código.