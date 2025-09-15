"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/board.py".
"""

### Inicio del código.

## Inicio de imports.

from dataclasses import dataclass
from typing import Optional, List

## Fin de imports.

## Inicio de la clase «Point».

@dataclass
class Point:
    """Representa un punto (casilla) del tablero."""
    
    __owner__: Optional[str]
    __count_internal__: int = 0
    """
    Atributos:
        __owner__: (Optional[str]): 'X', 'O' o None según quién tiene fichas en el punto.
        __count__: (int): Cantidad de fichas en el punto (no negativa).
    """
    @property
    def __count__(self) -> int:
        """
        Obtiene el valor de __count__.

        Returns:
            int: Cantidad de fichas en el punto.
        """
        return self.__count_internal__

    @__count__.setter
    def __count__(self, value: int) -> None:
        """
        Establece el valor de __count__, asegurando que no sea negativo.

        Args:
            value (int): Nueva cantidad de fichas.
        Raises:
            ValueError: Si el valor es negativo.
        """
        if value < 0:
            raise ValueError("El número de fichas no puede ser negativo")
        self.__count_internal__ = value

    def __post_init__(self):
        """
        Valida y establece el valor inicial de __count__.

        Raises:
            ValueError: Si el valor inicial de __count_internal__ es negativo.
        """
        # Se usa el setter para validar el valor inicial.
        self.__count__ = self.__count_internal__

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
    - Mantiene registro de fichas en la barra y fichas retiradas.
    - Permite aplicar movimientos simples, desde la barra, y retiro de fichas.
    - Valida reglas del tablero (índices, propiedad, dirección, bloqueo).
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
        self.__bar__ = {"X": 0, "O": 0}  # Fichas en la barra.
        self.__off__ = {"X": 0, "O": 0}  # Fichas retiradas del juego.
        self.__reset_to_standard__()

    def __reset_to_standard__(self):
        """
        Coloca las fichas en la configuración inicial estándar de Backgammon.

        Args:
            None
        Returns:
            None
        """
        # Limpiar el tablero.
        for i in range(24):
            self.__points__[i] = Point(None, 0)
        # Disposición estándar del tablero.
        layout = [
            (0, 'X', 2),  # Punto 1 (index 0): 2 de X.
            (11, 'X', 5),
            (16, 'X', 3),
            (18, 'X', 5),
            (23, 'O', 2),
            (12, 'O', 5),
            (7, 'O', 3),
            (5, 'O', 5),
        ]
        # Colocar según el layout.
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
    
    def __can_bear_off__(self, player: str) -> bool:
        """
        Verifica si el jugador puede retirar fichas (todas en el cuarto final).

        Args:
            player (str): Jugador ('X' o 'O').
        Returns:
            bool: True si todas las fichas están en el cuarto final, False en caso contrario.
        """
        home_board = range(18, 24) if player == 'X' else range(0, 6)
        for i in range(24):
            if i not in home_board and self.__is_point_owned_by__(i, player):
                return False
        return self.__bar__[player] == 0  # No debe haber fichas en la barra.

    def __apply_move__(self, src: int, dst: int, player: str) -> bool:
        """
        Aplica un movimiento simple de src → dst para el jugador.

        Args:
            src (int): Índice del punto de origen (0 a 23).
            dst (int): Índice del punto de destino (0 a 23).
            player (str): Jugador ('X' o 'O').

        Returns:
            bool: True si el movimiento fue exitoso, False si no es válido.

        Reglas implementadas:
        - Permite mover desde la barra (src = -1) al punto correcto según el jugador.
        - Permite retirar fichas (dst = 24 para X, dst = -1 para O) si todas están en el cuarto final.
        - No permite mover desde un punto vacío o de otro jugador.
        - Bloquea mover a un punto con 2+ fichas del oponente.
        - Si hay una ficha del oponente, la golpea (se envía a la barra).
        - Valida la dirección del movimiento (X: hacia puntos mayores, O: hacia puntos menores).
        """
        # Validación de índices.
        if src < -1 or src >= 24 or dst < -1 or dst > 24:
            return False
        
        # Validación de movimientos desde la barra (src = -1).
        if src == -1:
            if self.__bar__[player] == 0:
                return False  # No hay fichas en la barra.
            # El destino debe ser calculado externamente (en Dice), pero se valida que que no esté bloqueado.
            dest_point = self.__points__[dst] if dst in range(24) else None
            opponent = 'O' if player == 'X' else 'X'
            if dest_point and dest_point.__owner__ == opponent and dest_point.__count__ >= 2:
                return False  # Destino bloqueado.
        else:
            # Validar que el punto de origen pertenece al jugador.
            if not self.__is_point_owned_by__(src, player):
                return False
            # Validar la dirección del movimiento (no aplica para retiro).
            if dst < 24 and player == 'X' and dst <= src:
                return False
            if dst >= 0 and player == 'O' and dst >= src:
                return False
        
        # Validación del retiro de fichas.
        if (player == 'X' and dst == 24) or (player == 'O' and dst == -1):
            if not self.__can_bear_off__(player):
                return False  # No todas las fichas están en el cuarto final.
            # Retirar ficha.
            if src == -1:
                self.__bar__[player] -= 1
            else:
                try:
                    self.__points__[src].__count__ -= 1
                    if self.__points__[src].__count__ == 0:
                        self.__points__[src].__owner__ = None
                except ValueError:
                    return False
            self.__off__[player] += 1
            return True
        
        # Validación del destino (no bloqueado).
        dest_point = self.__points__[dst]
        opponent = 'O' if player == 'X' else 'X'
        if dest_point.__owner__ == opponent and dest_point.__count__ >= 2:
            return False

        # Remover ficha del origen.
        if src == -1:
            self.__bar__[player] -= 1
        else:
            try:
                self.__points__[src].__count__ -= 1
                if self.__points__[src].__count__ == 0:
                    self.__points__[src].__owner__ = None
            except ValueError:
                return False

        # Resolver destino: golpe o movimiento normal
        if dest_point.__owner__ == opponent and dest_point.__count__ == 1:
            # Golpear ficha y mandarla a la barra
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

### Fin del código.