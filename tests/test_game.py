"""
Computación I - Backgammon.
Nombre y Apellido: Enzo Agustín Aguirre Polenta.
Ciclo Lectivo: 2025.
Carrera: Ingeniería en Informática.
Ruta: "computacion-2025-backgammon-EnzoAguirre04/tests/test_game.py".
"""

### Inicio del código.

## Inicio.

## Inicio de imports.

import unittest
from unittest.mock import patch
from core.game import Game
from core.board import Board, Point
from core.player import Player

## Fin de imports.

## Inicio de la clase «TestGame».

class TestGame(unittest.TestCase):
    """Pruebas unitarias para la clase Game."""

    def setUp(self):
        """Configura un juego para cada prueba."""
        self.game = Game(player_x_name="Jugador X", player_o_name="Jugador O")

    def test_initialization(self):
        """Prueba la inicialización del juego."""
        self.assertIsInstance(self.game.__get_board__(), Board)
        self.assertIsInstance(self.game.__get_current_player__(), Player)
        self.assertEqual(self.game.__get_current_player__().__id__, 'X')
        self.assertEqual(self.game.__get_current_player__().name, "Jugador X")
        self.assertEqual(self.game.__get_available_dice__(), [])
        self.assertIsInstance(self.game.__get_board__(), Board)

    def test_roll_dice(self):
        """Prueba el lanzamiento de dados."""
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [3, 5]
            self.game.__roll_dice__()
            self.assertEqual(self.game.__get_available_dice__(), [3, 5])

    def test_roll_dice_already_rolled(self):
        """Prueba que lanzar dados dos veces en el mismo turno lanza RuntimeError."""
        self.game.__roll_dice__()
        with self.assertRaises(RuntimeError):
            self.game.__roll_dice__()

    def test_try_move_without_rolling(self):
        """Prueba que intentar mover sin lanzar dados lanza RuntimeError."""
        with self.assertRaises(RuntimeError):
            self.game.__try_move__(0, 3)

    @patch('random.randint')
    def test_try_move_valid(self, mock_randint):
        """Prueba un movimiento válido."""
        mock_randint.side_effect = [3, 5]
        self.game.__roll_dice__()
        result = self.game.__try_move__(0, 3)
        self.assertTrue(result)
        board = self.game.__get_board__()
        self.assertEqual(board.__get_point__(0).__count__, 1)
        self.assertEqual(board.__get_point__(3).__owner__, 'X')
        self.assertEqual(board.__get_point__(3).__count__, 1)
        self.assertEqual(self.game.__get_available_dice__(), [5])

    @patch('random.randint')
    def test_try_move_invalid(self, mock_randint):
        """Prueba un movimiento inválido."""
        mock_randint.side_effect = [3, 5]
        self.game.__roll_dice__()
        result = self.game.__try_move__(0, 4)  # No coincide con los dados.
        self.assertFalse(result)
        self.assertEqual(self.game.__get_available_dice__(), [3, 5])

    @patch('random.randint')
    def test_end_turn(self, mock_randint):
        """Prueba finalizar el turno y alternar jugadores."""
        mock_randint.side_effect = [3, 5]
        self.game.__roll_dice__()
        self.game.__try_move__(0, 3)  # Usa un dado.
        self.game.__end_turn__()
        self.assertEqual(self.game.__get_current_player__().id, 'O')
        self.assertEqual(self.game.__get_available_dice__(), [])
        self.game.__roll_dice__()
        self.assertEqual(self.game.__get_current_player__().id, 'O')

    def test_get_winner_none(self):
        """Prueba que no haya ganador al inicio."""
        self.assertIsNone(self.game.__get_winner__())

## Fin de la clase «TestGame».

if __name__ == '__main__':
    unittest.main()

### Fin del código.