"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/tests/test_board.py".
"""

### Inicio del código.

## Inicio de imports.

import unittest
from core.board import Point, Board

## Fin de imports.

## Inicio de la clase «TestPoint».

class TestPoint(unittest.TestCase):
    """Pruebas unitarias para la clase Point."""

    def test_initialization_valid(self):
        """Prueba la inicialización con valores válidos."""
        point = Point('X', 3)
        self.assertEqual(point.__owner__, 'X')
        self.assertEqual(point.__count__, 3)

    def test_initialization_negative_count(self):
        """Prueba que la inicialización con un conteo negativo lanza ValueError."""
        with self.assertRaises(ValueError):
            Point('X', -1)

    def test_count_setter_valid(self):
        """Prueba el setter de __count__ con valores válidos."""
        point = Point('O', 2)
        point.__count__ = 5
        self.assertEqual(point.__count__, 5)

    def test_count_setter_negative(self):
        """Prueba que el setter de __count__ con valores negativos lanza ValueError."""
        point = Point('O', 2)
        with self.assertRaises(ValueError):
            point.__count__ = -1

    def test_repr_empty(self):
        """Prueba __repr__ para un punto vacío."""
        point = Point(None, 0)
        self.assertEqual(str(point), " . ")

    def test_repr_non_empty(self):
        """Prueba __repr__ para un punto con fichas."""
        point = Point('X', 4)
        self.assertEqual(str(point), "X4")

## Fin de la clase «TestPoint».

## Inicio de la clase «TestBoard».

class TestBoard(unittest.TestCase):
    """Pruebas unitarias para la clase Board."""

    def setUp(self):
        """Configura un tablero nuevo para cada prueba."""
        self.board = Board()

    def test_reset_to_standard(self):
        """Prueba la configuración inicial estándar del tablero."""
        expected_layout = [
            (0, 'X', 2), (11, 'X', 5), (16, 'X', 3), (18, 'X', 5),
            (23, 'O', 2), (12, 'O', 5), (7, 'O', 3), (5, 'O', 5)
        ]
        for idx, owner, count in expected_layout:
            point = self.board.get_point(idx)
            self.assertEqual(point.__owner__, owner)
            self.assertEqual(point.__count__, count)
        # Verificar que otros puntos estén vacíos.
        for i in range(24):
            if i not in [0, 5, 7, 11, 12, 16, 18, 23]:
                point = self.board.get_point(i)
                self.assertEqual(point.__owner__, None)
                self.assertEqual(point.__count__, 0)
        # Verificar barra y retiradas.
        self.assertEqual(self.board.get_bar('X'), 0)
        self.assertEqual(self.board.get_bar('O'), 0)
        self.assertEqual(self.board.get_off('X'), 0)
        self.assertEqual(self.board.get_off('O'), 0)

    def test_is_point_owned_by(self):
        """Prueba la verificación de propiedad de puntos."""
        self.assertTrue(self.board.__is_point_owned_by__(0, 'X'))
        self.assertFalse(self.board.__is_point_owned_by__(0, 'O'))
        self.assertFalse(self.board.__is_point_owned_by__(1, 'X'))  # Punto vacío.

    def test_can_bear_off_true(self):
        """Prueba __can_bear_off__ cuando todas las fichas están en el cuarto final."""
        # Mover todas las fichas de X al punto 18.
        for _ in range(2):  # Mover 2 fichas de 0 a 18.
            self.board.__apply_move__(0, 18, 'X')
        for _ in range(5):  # Mover 5 fichas de 11 a 18.
            self.board.__apply_move__(11, 18, 'X')
        for _ in range(3):  # Mover 3 fichas de 16 a 18.
            self.board.__apply_move__(16, 18, 'X')
        # Las 5 fichas ya están en 18.
        self.assertTrue(self.board.__can_bear_off__('X'))

    def test_can_bear_off_false_bar(self):
        """Prueba __can_bear_off__ con fichas en la barra."""
        # Mover una ficha de O a la barra.
        self.board.__apply_move__(0, 5, 'X')  # X golpea una ficha de O en 5.
        self.assertEqual(self.board.get_bar('O'), 1)
        self.assertFalse(self.board.__can_bear_off__('O'))

    def test_can_bear_off_false_outside_home(self):
        """Prueba __can_bear_off__ con fichas fuera del cuarto final."""
        # Punto 11 (fuera del cuarto final de X) tiene fichas.
        self.assertFalse(self.board.__can_bear_off__('X'))

    def test_apply_move_valid(self):
        """Prueba un movimiento válido entre puntos."""
        result = self.board.__apply_move__(0, 3, 'X')
        self.assertTrue(result)
        self.assertEqual(self.board.get_point(0).__count__, 1)
        self.assertEqual(self.board.get_point(3).__owner__, 'X')
        self.assertEqual(self.board.get_point(3).__count__, 1)

    def test_apply_move_from_bar(self):
        """Prueba un movimiento válido desde la barra."""
        # Simular una ficha en la barra golpeando una ficha de O.
        self.board.__apply_move__(0, 5, 'X')  # X golpea una ficha de O en 5.
        self.assertEqual(self.board.get_bar('O'), 1)
        result = self.board.__apply_move__(-1, 2, 'O')
        self.assertTrue(result)
        self.assertEqual(self.board.get_bar('O'), 0)
        self.assertEqual(self.board.get_point(2).__owner__, 'O')
        self.assertEqual(self.board.get_point(2).__count__, 1)

    def test_apply_move_bear_off(self):
        """Prueba el retiro de fichas desde el cuarto final."""
        # Mover todas las fichas de X al punto 20.
        for _ in range(2):
            self.board.__apply_move__(0, 20, 'X')
        for _ in range(5):
            self.board.__apply_move__(11, 20, 'X')
        for _ in range(3):
            self.board.__apply_move__(16, 20, 'X')
        for _ in range(5):
            self.board.__apply_move__(18, 20, 'X')
        result = self.board.__apply_move__(20, 24, 'X')
        self.assertTrue(result)
        self.assertEqual(self.board.get_off('X'), 1)
        self.assertEqual(self.board.get_point(20).__count__, 14)

    def test_apply_move_bar_priority(self):
        """Prueba que no se permitan movimientos desde el tablero con fichas en la barra."""
        # Simular una ficha en la barra.
        self.board.__apply_move__(23, 0, 'O')  # O golpea una ficha de X.
        self.assertEqual(self.board.get_bar('X'), 1)
        result = self.board.__apply_move__(11, 14, 'X')
        self.assertFalse(result)

    def test_apply_move_invalid_indices(self):
        """Prueba movimientos con índices inválidos."""
        self.assertFalse(self.board.__apply_move__(-2, 3, 'X'))  # src < -1.
        self.assertFalse(self.board.__apply_move__(0, 25, 'X'))  # dst > 24.

    def test_apply_move_wrong_owner(self):
        """Prueba movimientos desde un punto que no pertenece al jugador."""
        self.assertFalse(self.board.__apply_move__(0, 3, 'O'))  # Punto pertenece a X.

    def test_apply_move_invalid_direction(self):
        """Prueba movimientos en dirección incorrecta."""
        self.assertFalse(self.board.__apply_move__(0, 0, 'X'))  # X: dst <= src.
        self.assertFalse(self.board.__apply_move__(23, 23, 'O'))  # O: dst >= src.

    def test_apply_move_blocked_destination(self):
        """Prueba movimientos a un punto bloqueado (2+ fichas del oponente)."""
        self.board.__apply_move__(0, 3, 'X')  # Mover una ficha de X a 3.
        self.board.__apply_move__(11, 3, 'X')  # Mover otra ficha de X a 3.
        self.assertFalse(self.board.__apply_move__(23, 3, 'O'))  # O no puede mover a 3 (bloqueado).

    def test_apply_move_hit_opponent(self):
        """Prueba golpear una ficha solitaria del oponente."""
        self.board.__apply_move__(11, 5, 'X')  # Mover una ficha de X a 5, golpeando a O.
        self.assertEqual(self.board.get_bar('O'), 1)
        self.assertEqual(self.board.get_point(5).__owner__, 'X')
        self.assertEqual(self.board.get_point(5).__count__, 1)

    def test_get_point_invalid_index(self):
        """Prueba get_point con un índice inválido."""
        with self.assertRaises(IndexError):
            self.board.get_point(24)

## Fin de la clase «TestBoard».

if __name__ == '__main__':
    unittest.main()

### Fin del código.