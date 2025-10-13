"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/tests/test_dice.py".
"""
#### Los test dan errores, arreglarlos después.

### Inicio del código.

## Inicio de imports.

import unittest
from unittest.mock import patch
from core.dice import Dice
from core.board import Board, Point

## Fin de imports.

## Inicio de la clase «TestDice».

class TestDice(unittest.TestCase):
    """Pruebas unitarias para la clase Dice."""

    def setUp(self):
        """Configura los dados y el tablero para cada prueba."""
        self.dice = Dice()
        self.board = Board()

    @patch('random.randint')
    def test_roll_normal(self, mock_randint):
        """Prueba el lanzamiento de dados no dobles."""
        mock_randint.side_effect = [3, 5]
        self.dice.__roll__()
        self.assertEqual(self.dice.__get_available_dice__(), [3, 5])

    @patch('random.randint')
    def test_roll_doubles(self, mock_randint):
        """Prueba el lanzamiento de dados dobles."""
        mock_randint.side_effect = [4, 4]
        self.dice.__roll__()
        self.assertEqual(self.dice.__get_available_dice__(), [4, 4, 4, 4])

    def test_can_move_normal(self):
        """Prueba un movimiento válido según los dados."""
        self.dice.__dice__ = [3, 5]
        result = self.dice.__can_move__(0, 3, 'X', self.board)
        self.assertTrue(result)
        self.assertEqual(self.board.__get_point__(0).__count__, 1)
        self.assertEqual(self.board.__get_point__(3).__owner__, 'X')
        self.assertEqual(self.board.__get_point__(3).__count__, 1)

    def test_can_move_from_bar(self):
        """Prueba un movimiento válido desde la barra."""
        self.dice.__dice__ = [3]
        self.board.__apply_move__(23, 0, 'O')  # O golpea una ficha de X.
        self.assertEqual(self.board.__get_bar__('X'), 1)
        result = self.dice.__can_move__(-1, 2, 'X', self.board)
        self.assertTrue(result)
        self.assertEqual(self.board.__get_bar__('X'), 0)
        self.assertEqual(self.board.__get_point__(2).__owner__, 'X')
        self.assertEqual(self.board.__get_point__(2).__count__, 1)

    def test_can_move_bear_off(self):
        """Prueba el retiro de fichas con un dado exacto."""
        self.dice.__dice__ = [4]
        for i in range(24):
            self.board.__points__[i] = Point(None, 0)
        self.board.__points__[20] = Point('X', 15)
        self.board.__bar__['X'] = 0
        result = self.dice.__can_move__(20, 24, 'X', self.board)
        self.assertTrue(result)
        self.assertEqual(self.board.__get_off__('X'), 1)
        self.assertEqual(self.board.__get_point__(20).__count__, 14)

    def test_can_move_bear_off_flexible(self):
        """Prueba el retiro flexible desde un punto más alto."""
        self.dice.__dice__ = [5]
        for i in range(24):
            self.board.__points__[i] = Point(None, 0)
        self.board.__points__[20] = Point('X', 15)  # Punto 21.
        self.board.__bar__['X'] = 0
        result = self.dice.__can_move__(20, 24, 'X', self.board)
        self.assertTrue(result)
        self.assertEqual(self.board.__get_off__('X'), 1)
        self.assertEqual(self.board.__get_point__(20).__count__, 14)

    def test_use_die_normal(self):
        """Prueba el consumo de un dado en un movimiento normal."""
        self.dice.__dice__ = [3, 5]
        self.dice.__can_move__(0, 3, 'X', self.board)
        result = self.dice.__use_die__(0, 3, 'X')
        self.assertTrue(result)
        self.assertEqual(self.dice.__get_available_dice__(), [5])

    def test_use_die_from_bar(self):
        """Prueba el consumo de un dado en un movimiento desde la barra."""
        self.dice.__dice__ = [3]
        self.board.__apply_move__(23, 0, 'O')  # O golpea una ficha de X.
        self.dice.__can_move__(-1, 2, 'X', self.board)
        result = self.dice.__use_die__(-1, 2, 'X')
        self.assertTrue(result)
        self.assertEqual(self.dice.__get_available_dice__(), [])

    def test_use_die_bear_off(self):
        """Prueba el consumo de un dado en un retiro."""
        self.dice.__dice__ = [4]
        for i in range(24):
            self.board.__points__[i] = Point(None, 0)
        self.board.__points__[20] = Point('X', 15)
        self.board.__bar__['X'] = 0
        self.dice.__can_move__(20, 24, 'X', self.board)
        result = self.dice.__use_die__(20, 24, 'X')
        self.assertTrue(result)
        self.assertEqual(self.dice.__get_available_dice__(), [])

## Fin de la clase «TestDice».

### Fin del código.

if __name__ == '__main__':
    unittest.main()