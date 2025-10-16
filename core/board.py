"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/core/board.py".
"""

#### Inicio del código.

### Inicio de imports.

from dataclasses import dataclass
from typing import Optional, List

### Fin de imports.

### Inicio de la clase «Point».

@dataclass
class Point:
    """
    Representa un punto (casilla) del tablero de Backgammon.
    
    Cada punto puede contener fichas de un único jugador ('X' u 'O'), o estar vacío (None).
    La clase se encarga de mantener la coherencia del conteo y validar que no existan valores negativos.
    """
    
    __owner__: Optional[str]
    __count_internal__: int = 0
    """
    Atributos:
        __owner__ (Optional[str]): 'X', 'O' o None según quién tiene fichas en el punto.
        __count__ (int): Cantidad de fichas en el punto (no negativa).
    """

    ## Inicio de la propiedad «__count__».

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

    ## Fin de la propiedad «__count__».

    ## Inicio del método «__post_init__».

    def __post_init__(self):
        """
        Valida y establece el valor inicial de __count__.

        Raises:
            ValueError: Si el valor inicial de __count_internal__ es negativo.
        """
        self.__count__ = self.__count_internal__

    ## Fin del método «__post_init__».

    ## Inicio del método «__repr__».

    def __repr__(self) -> str:
        """
        Devuelve una representación en cadena del punto para depuración.

        Returns:
            str: Representación del punto (ej. 'X2' para 2 fichas de X, ' . ' si está vacío).
        """
        if self.__owner__ is None or self.__count__ == 0:
            return " . "
        return f"{self.__owner__}{self.__count__}"

    ## Fin del método «__repr__».

    ## Inicio del método «__to_dict__».

    def __to_dict__(self) -> dict:
        """
        Devuelve una representación serializable del punto.

        Returns:
            dict: Diccionario con las claves 'owner' y 'count'.
        """
        return {"owner": self.__owner__, "count": self.__count__}

    ## Fin del método «__to_dict__».

    ## Inicio del método «__is_empty__».

    def __is_empty__(self) -> bool:
        """
        Verifica si el punto está vacío.

        Returns:
            bool: True si el punto no contiene fichas.
        """
        return self.__owner__ is None or self.__count__ == 0

    ## Fin del método «__is_empty__».

### Fin de la clase «Point».

### Inicio de la clase «Board».

class Board:
    """
    Representa el tablero de Backgammon.

    Atributos:
        __points__ (List[Point]): Lista de 24 puntos del tablero (índices 0 a 23).
        __bar__ (dict): Fichas en la barra, por jugador.
        __off__ (dict): Fichas retiradas del juego (fuera del tablero).

    Responsabilidades:
        - Mantener la disposición del tablero y su estado general.
        - Validar y aplicar movimientos según las reglas del juego.
        - Gestionar fichas en la barra y retiradas.
        - Permitir exportar e importar el estado del tablero.
    """

    ## Inicio del método «__init__».

    def __init__(self):
        """Inicializa un tablero vacío y lo coloca en la configuración estándar."""
        self.__points__: List[Point] = [Point(None, 0) for _ in range(24)]
        self.__bar__ = {"X": 0, "O": 0}  # Fichas en la barra.
        self.__off__ = {"X": 0, "O": 0}  # Fichas retiradas del juego.
        self.__reset_to_standard__()

    ## Fin del método «__init__».

    ## Inicio del método «__reset_to_standard__».

    def __reset_to_standard__(self):
        """Coloca las fichas en la configuración inicial estándar de Backgammon.
        
        Esta configuración corresponde a la disposición tradicional:
        - 2 fichas de 'X' en el punto 1.
        - 5 fichas de 'X' en el punto 12.
        - 3 fichas de 'X' en el punto 17.
        - 5 fichas de 'X' en el punto 19.
        - 2 fichas de 'O' en el punto 24.
        - 5 fichas de 'O' en el punto 13.
        - 3 fichas de 'O' en el punto 8.
        - 5 fichas de 'O' en el punto 6.
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

    ## Fin del método «__reset_to_standard__».

    ## Inicio de los métodos utilitarios.

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
            bool: True si todas las fichas están en el cuarto final y no hay fichas en la barra, False en caso contrario.
        """
        home_board = range(18, 24) if player == 'X' else range(0, 6)
        for i in range(24):
            if i not in home_board and self.__is_point_owned_by__(i, player):
                return False
        return self.__bar__[player] == 0  # No debe haber fichas en la barra.

    def __get_point__(self, index: int) -> Point:
        """
        Obtiene el estado de un punto en el tablero.

        Args:
            index (int): Índice del punto (0 a 23).
        Returns:
            Point: Objeto Point en el índice especificado.
        Raises:
            IndexError: Si el índice está fuera de rango.
        """
        if index < 0 or index >= 24:
            raise IndexError("Índice de punto fuera de rango")
        return self.__points__[index]
    
    def __get_bar__(self, player: str) -> int:
        """
        Obtiene el número de fichas en la barra para el jugador.

        Args:
            player (str): Jugador ('X' o 'O').
        Returns:
            int: Número de fichas en la barra.
        """
        return self.__bar__[player]
    
    def __get_off__(self, player: str) -> int:
        """
        Obtiene el número de fichas retiradas para el jugador.

        Args:
            player (str): Jugador ('X' o 'O').
        Returns:
            int: Número de fichas retiradas.
        """
        return self.__off__[player]
    
    ## Fin de los métodos utilitarios.

    ## Inicio de métodos auxiliares.

    def __validate_move__(self, src: int, dst: int, player: str) -> bool:
        """
        Valida un movimiento antes de aplicarlo.

        Reglas validadas:
            - Rango de índices permitido.
            - Prioridad de fichas en la barra.
            - Bloqueo de puntos del oponente.
            - Dirección del movimiento según el jugador.

        Returns:
            bool: True si el movimiento es válido, False si infringe alguna regla.
        """
        if src < -1 or src >= 24 or dst < -1 or dst > 24:
            return False
        if self.__bar__[player] > 0 and src >= 0:
            return False

        opponent = 'O' if player == 'X' else 'X'

        if src == -1:
            if self.__bar__[player] == 0:
                return False
            dest_point = self.__points__[dst] if dst in range(24) else None
            if dest_point and dest_point.__owner__ == opponent and dest_point.__count__ >= 2:
                return False
        else:
            if not self.__is_point_owned_by__(src, player):
                return False
            if dst < 24 and player == 'X' and dst <= src:
                return False
            if dst >= 0 and player == 'O' and dst >= src:
                return False

        return True

    def __perform_bear_off__(self, src: int, player: str) -> bool:
        """
        Ejecuta el retiro de fichas del tablero (bear off) si las condiciones lo permiten.

        Args:
            src (int): Índice de origen o -1 si viene desde la barra.
            player (str): Jugador que intenta retirar la ficha.
        Returns:
            bool: True si el retiro fue exitoso, False en caso contrario.
        """
        if not self.__can_bear_off__(player):
            return False

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

    def __perform_hit_or_move__(self, src: int, dst: int, player: str) -> bool:
        """
        Aplica un movimiento estándar o golpe según el estado del punto destino.

        Args:
            src (int): Punto de origen (-1 si desde barra).
            dst (int): Punto de destino (0-23).
            player (str): Jugador que realiza la jugada.
        Returns:
            bool: True si la jugada fue válida y aplicada, False si no fue posible.
        """
        opponent = 'O' if player == 'X' else 'X'
        dest_point = self.__points__[dst]

        if dest_point.__owner__ == opponent and dest_point.__count__ >= 2:
            return False

        # Quitar ficha del origen.
        if src == -1:
            self.__bar__[player] -= 1
        else:
            try:
                self.__points__[src].__count__ -= 1
                if self.__points__[src].__count__ == 0:
                    self.__points__[src].__owner__ = None
            except ValueError:
                return False

        # Resolver el destino.
        if dest_point.__owner__ == opponent and dest_point.__count__ == 1:
            # Golpe: enviar ficha oponente a la barra.
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

    ## Fin de métodos auxiliares.

    ## Inicio de método «__apply_move__».

    def __apply_move__(self, src: int, dst: int, player: str) -> bool:
        """
        Aplica un movimiento de origen (src) a destino (dst) para el jugador indicado.

        Se contemplan:
            - Movimientos normales.
            - Movimientos desde la barra.
            - Golpes a fichas del oponente.
            - Retiro de fichas del tablero.

        Returns:
            bool: True si el movimiento fue ejecutado correctamente, False si no fue válido.
        """
        if not self.__validate_move__(src, dst, player):
            return False

        # Retiro de fichas (bear off).
        if (player == 'X' and dst == 24) or (player == 'O' and dst == -1):
            return self.__perform_bear_off__(src, player)

        # Movimiento normal o golpe.
        return self.__perform_hit_or_move__(src, dst, player)

    ## Fin del método «__apply_move__».

    ## Inicio de método «__check_victory__».

    def __check_victory__(self, player: str) -> bool:
        """
        Verifica si el jugador ha ganado (todas las fichas retiradas del tablero).

        Args:
            player (str): Jugador ('X' o 'O').
        Returns:
            bool: True si el jugador retiró sus 15 fichas.
        """
        return self.__off__[player] >= 15

    ## Fin de método «__check_victory__».

    ## Inicio del método «__get_state__».

    def __get_state__(self) -> dict:
        """
        Devuelve una descripción completa del estado del tablero.

        Returns:
            dict: Estructura serializable con puntos, barra y fichas retiradas.
        """
        return {
            "points": [p.__to_dict__() for p in self.__points__],
            "bar": self.__bar__.copy(),
            "off": self.__off__.copy(),
        }

    ## Fin del método «__get_state__».

    ## Inicio del método «__set_state__».

    def __set_state__(self, state: dict) -> None:
        """
        Restaura el estado del tablero desde un diccionario serializado.

        Args:
            state (dict): Estructura generada previamente por __get_state__().
        """
        for i, p_state in enumerate(state["points"]):
            self.__points__[i].__owner__ = p_state["owner"]
            self.__points__[i].__count__ = p_state["count"]
        self.__bar__ = state["bar"].copy()
        self.__off__ = state["off"].copy()

    ## Fin del método «__set_state__».

    ## Inicio de método «__str__».

    def __str__(self) -> str:
        """
        Devuelve una representación textual del tablero.

        Se usa para depuración y visualización en la Interfaz de línea de comandos.
        No imprime directamente, solo genera una cadena representativa del estado.
        """
        return " ".join(str(p) for p in self.__points__)

    ## Fin de método «__str__».

### Fin de la clase «Board».

#### Fin del código.