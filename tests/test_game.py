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
        self.assertIsInstance(self.game.get_board(), Board)
        self.assertIsInstance(self.game.get_current_player(), Player)
        self.assertEqual(self.game.get_current_player().id, 'X')
        self.assertEqual(self.game.get_current_player().name, "Jugador X")
        self.assertEqual(self.game.get_available_dice(), [])
        self.assertIsInstance(self.game.get_board(), Board)

    def test_roll_dice(self):
        """Prueba el lanzamiento de dados."""
        with patch('random.randint') as mock_randint:
            mock_randint.side_effect = [3, 5]
            self.game.roll_dice()
            self.assertEqual(self.game.get_available_dice(), [3, 5])

    def test_roll_dice_already_rolled(self):
        """Prueba que lanzar dados dos veces en el mismo turno lanza RuntimeError."""
        self.game.roll_dice()
        with self.assertRaises(RuntimeError):
            self.game.roll_dice()

    def test_try_move_without_rolling(self):
        """Prueba que intentar mover sin lanzar dados lanza RuntimeError."""
        with self.assertRaises(RuntimeError):
            self.game.try_move(0, 3)

    @patch('random.randint')
    def test_try_move_valid(self, mock_randint):
        """Prueba un movimiento válido."""
        mock_randint.side_effect = [3, 5]
        self.game.roll_dice()
        result = self.game.try_move(0, 3)
        self.assertTrue(result)
        board = self.game.get_board()
        self.assertEqual(board.__get_point__(0).__count__, 1)
        self.assertEqual(board.__get_point__(3).__owner__, 'X')
        self.assertEqual(board.__get_point__(3).__count__, 1)
        self.assertEqual(self.game.get_available_dice(), [5])

    @patch('random.randint')
    def test_try_move_invalid(self, mock_randint):
        """Prueba un movimiento inválido."""
        mock_randint.side_effect = [3, 5]
        self.game.roll_dice()
        result = self.game.try_move(0, 4)  # No coincide con los dados
        self.assertFalse(result)
        self.assertEqual(self.game.get_available_dice(), [3, 5])

    @patch('random.randint')
    def test_end_turn(self, mock_randint):
        """Prueba finalizar el turno y alternar jugadores."""
        mock_randint.side_effect = [3, 5]
        self.game.roll_dice()
        self.game.try_move(0, 3)  # Usa un dado
        self.game.end_turn()
        self.assertEqual(self.game.get_current_player().id, 'O')
        self.assertEqual(self.game.get_available_dice(), [])
        self.game.roll_dice()
        self.assertEqual(self.game.get_current_player().id, 'O')

    def test_get_winner(self):
        """Prueba la detección de un ganador."""
        # Configurar el tablero para que X haya ganado
        board = self.game.get_board()
        for i in range(24):
            board.__points__[i] = Point(None, 0)
        board.__bar__['X'] = 0
        board.__off__['X'] = 15
        winner = self.game.get_winner()
        self.assertIsNotNone(winner)
        self.assertEqual(winner.id, 'X')

    def test_get_winner_none(self):
        """Prueba que no haya ganador al inicio."""
        self.assertIsNone(self.game.get_winner())

## Fin de la clase «TestGame».

if __name__ == '__main__':
    unittest.main()

### Fin del código.