"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/tests/test_player.py".
"""

#### Los test dan errores, arreglarlos después.

### Inicio del código.

## Inicio de imports.

import unittest
from unittest.mock import patch
from core.player import Player
from core.board import Board, Point
from core.dice import Dice

## Fin de imports.

## Inicio de la clase «TestPlayer».

class TestPlayer(unittest.TestCase):
    """Pruebas unitarias para la clase Player."""

    def setUp(self):
        """Configura un jugador, tablero y dados para cada prueba."""
        self.player_x = Player('X', 'Jugador X')
        self.player_o = Player('O')
        self.board = Board()
        self.dice = Dice()

    def test_initialization_valid(self):
        """Prueba la inicialización con identificador y nombre válidos."""
        self.assertEqual(self.player_x.id, 'X')
        self.assertEqual(self.player_x.name, 'Jugador X')
        self.assertEqual(self.player_o.id, 'O')
        self.assertEqual(self.player_o.name, 'O')

    def test_initialization_invalid_id(self):
        """Prueba que un identificador inválido lanza ValueError."""
        with self.assertRaises(ValueError):
            Player('Z')

    def test_can_bear_off_true(self):
        """Prueba can_bear_off cuando todas las fichas están en el cuarto final."""
        # Mover todas las fichas de X al punto 18
        for _ in range(2):
            self.board.__apply_move__(0, 18, 'X')
        for _ in range(5):
            self.board.__apply_move__(11, 18, 'X')
        for _ in range(3):
            self.board.__apply_move__(16, 18, 'X')
        # Las 5 fichas ya están en 18
        self.assertTrue(self.player_x.__can_bear_off__(self.board))

    def test_can_bear_off_false(self):
        """Prueba can_bear_off con fichas fuera del cuarto final."""
        self.assertFalse(self.player_x.__can_bear_off__(self.board))  # Punto 11 está fuera

    def test_has_won_true(self):
        """Prueba has_won cuando todas las fichas están retiradas."""
        # Retirar todas las fichas de X
        for i in range(24):
            self.board.__points__[i] = Point(None, 0)
        self.board.__bar__['X'] = 0
        self.board.__off__['X'] = 15
        self.assertTrue(self.player_x.__has_won__(self.board))

    def test_has_won_false(self):
        """Prueba has_won cuando no todas las fichas están retiradas."""
        self.assertFalse(self.player_x.__has_won__(self.board))

    @patch('random.randint')
    def test_try_move_valid(self, mock_randint):
        """Prueba un movimiento válido con dados."""
        mock_randint.side_effect = [3, 5]
        self.dice.__roll__()
        result = self.player_x.__try_move__(0, 3, self.board, self.dice)
        self.assertTrue(result)
        self.assertEqual(self.board.__get_point__(0).__count__, 1)
        self.assertEqual(self.board.__get_point__(3).__owner__, 'X')
        self.assertEqual(self.board.__get_point__(3).__count__, 1)
        self.assertEqual(self.dice.__get_available_dice__(), [5])

    def test_try_move_invalid(self):
        """Prueba un movimiento inválido (punto no pertenece al jugador)."""
        self.dice.__dice__ = [3]
        result = self.player_o.__try_move__(0, 3, self.board, self.dice)
        self.assertFalse(result)
        self.assertEqual(self.dice.__get_available_dice__(), [3])

## Fin de la clase «TestPlayer».

if __name__ == '__main__':
    unittest.main()

### Fin del código.