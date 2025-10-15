# Changelog

Todos los cambios notables realizados a este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## Nomenclatura de versiones:

**`[X.Y.Z]` - AAAA-MM-DD - Número de Sprint**

El proyecto utiliza un esquema adaptado de [SemVer](https://semver.org/) donde:
- **`X (major)`** representa la **etapa de desarrollo**:
    - 0 → Desarrollo inicial (Estructura base).
    - 1 → Interfaz de Consola (CLI para jugar al Backgammon).
    - 2 → Interfaz gráfica (Pygame).
    - 3 → Persistencia de partidas (Redis).
    - 4 → Optimización y refinamiento final.
- **`Y (minor)`** representa nuevas funcionalidades agregadas dentro de la misma etapa.
- **`Z (patch)`** representa correcciones de errores o mejoras menores.

## Fechas de Sprints:

- **Primer Sprint:** Del 2025-08-19 al 2025-09-03.
- **Segundo Sprint:** Del 2025-09-04 al 2025-09-17.
- **Tercer Sprint:** Del 2025-09-18 al 2025-10-01.
- **Cuarto Sprint:** Del 2025-10-01 al 2025-10-15.

## [Unreleased] - Cuarto Sprint

## [0.5.0] - 2025-10-14 - Cuarto Sprint

### Añadido:

- **Clase `Game` en [game.py]:**
    - Atributos:
        - `__board__`: Instancia de Board para el tablero.
        - `__dice__`: Instancia de Dice para los dados.
        - `__players__`: Diccionario con los jugadores (X y O).
        - `__current_player__`: Identificador del jugador actual (X o O).
        - `__dice_rolled__`: Bandera para rastrear si los dados fueron lanzados en el turno.
    - Métodos:
        - `__init__`: Inicializa el juego con dos jugadores, un tablero, y dados.
        - `__get_board__`: Devuelve el tablero.
        - `__get_current_player__`: Devuelve el jugador actual.
        - `__get_available_dice__`: Devuelve los dados disponibles.
        - `__roll_dice__`: Lanza los dados si no se han lanzado en el turno.
        - `__try_move__`: Intenta un movimiento, validándolo con Player.try_move y finalizando el turno si no quedan dados.
        - `__end_turn__`: Alterna el jugador y reinicia los dados.
        - `__get_winner__`: Verifica si hay un ganador.
    - Integración:
        - Usa métodos públicos de `Board` (`get_point`, `get_bar`, `get_off`, `apply_move`), `Dice` (`roll`, `get_available_dice`, `can_move`, `use_die`), y `Player` (`try_move`, `has_won`). `try_move` finaliza el turno automáticamente si no quedan dados, lo que simplifica la lógica para el CLI.

- **Pruebas en [test_game.py]**
    - Cobertura:
        - `test_initialization`: Verifica la creación del juego.
        - `test_roll_dice`: Prueba el lanzamiento de dados.
        - `test_roll_dice_already_rolled`: Asegura que no se pueda relanzar en el mismo turno.
        - `test_try_move_without_rolling`: Verifica que mover sin lanzar dados lanza un error.
        - `test_try_move_valid/invalid`: Prueba movimientos válidos e inválidos.
        - `test_end_turn`: Verifica el cambio de turno y reinicio de dados.
        - `test_get_winner/none`: Prueba la detección de ganador o su ausencia.

### Modificado:

- Añadido "core." a los imports dentro de los archivos de "core/".

## [0.4.0] - 2025-10-12 - Cuarto Sprint

### Añadido:

- **Clase Player en [player.py]:**
    - Atributos:
        - `__id__`: Identificador del jugador (X o O).
        - `__name__`: Nombre opcional (por defecto, igual al identificador).
    - Métodos:
        - `id y name`: Propiedades para acceder al identificador y nombre.
        - `can_bear_off`: Delega a `Board.__can_bear_off__` para verificar si el jugador puede retirar fichas.
        - `has_won`: Comprueba si el jugador ha retirado todas sus fichas (get_off(player) == 15).
        - `try_move`: Valida un movimiento con Dice.can_move y, si es válido, consume el dado con Dice.use_die.
    - Integración:
        - Usa métodos públicos de `Board` (`get_point`, `get_bar`, `get_off`, `__apply_move__`) y `Dice` (`can_move`, `use_die`).

- **Pruebas en [test_player.py]:**
    - Cobertura de tests:
        - `test_initialization_valid`: Verifica inicialización con y sin nombre.
        - `test_initialization_invalid_id`: Asegura que un identificador inválido lanza ValueError.
        - `test_can_bear_off_true/false`: Comprueba la capacidad de retirar fichas.
        - `test_has_won_true/false`: Verifica la condición de victoria.
        - `test_try_move_valid`: Prueba un movimiento válido, incluyendo consumo de dado.
        - `test_try_move_invalid`: Prueba un movimiento inválido (punto no pertenece al jugador).

## [0.3.0] - 2025-10-01 - Tercer Sprint

### Añadido:

- Fechas de los Sprints en este [CHANGELOG.md].
- **Implementación inicial de la clase `Dice` en [dice.py]**:
    - Representa los dados en Backgammon, manejando dos dados de 6 caras.
    - Añadido `__init__` para inicializar una lista vacía de valores de dados.
    - Añadido `__roll__` para simular el lanzamiento de dos dados, asignando cuatro movimientos en caso de dobles.
    - Añadido `__get_available_dice__` para devolver una copia de los valores de dados disponibles.
    - Añadido `__can_move__` para validar movimientos (normales, desde la barra, retiro) basados en los valores de los dados, integrándose con `board.__apply_move__`.
    - Añadido `__use_die__` para consumir un dado usado, soportando retiro flexible.
- **Documentación completa**:
    - Añadidos Docstrings para la clase `Dice` y todos sus métodos, detallando propósito, argumentos, valores de retorno y excepciones.
- **Pruebas unitarias**:
    - Añadido **[test_dice.py]** con pruebas unitarias completas para la clase `Dice` usando `unittest`.
    - Las pruebas cubren lanzamiento de dados (normales y dobles), validación de movimientos (normales, desde la barra, retiro exacto y flexible), y consumo de dados.
    - Uso de `unittest.mock.patch` para controlar los valores de los dados en las pruebas.

## [0.2.1] - 2025-09-28 - Segundo y Tercer Sprint

### Añadido:

- Añadido el enlace del [CHANGELOG.md] en este mismo archivo.
- En **[board.py]**:
    - Añadidos `get_point`, `get_bar`, `get_point` en la clase `Board`.
    - Añadida validación para la prioridad de la barra en `__apply_move__` dentro de la clase `Board`.
- Creación de **[test_board.py]** para realizar tests unitarios a **[board.py]**:
- Añadida la clase `TestPoint` en **[test_board.py]** con los siguientes tests para hacer a `Point`:
    - `test_initialization_valid`.
    - `test_initialization_negative_count`.
    - `test_count_setter_valid`.
    - `test_count_setter_negative`.
    - `test_repr_empty`.
    - `test_repr_non_empty`.
- Añadida la clase `TestBoard` en **[test_board.py]** con los siguientes tests para hacer a `Board`:
    - `setUp`.
    - `test_reset_to_standard`.
    - `test_is_point_owned_by`.
    - `test_can_bear_off_true`.
    - `test_can_bear_off_false_bar`.
    - `test_can_bear_off_false_outside_home`.
    - `test_apply_move_valid`.
    - `test_apply_move_from_bar`.
    - `test_apply_move_bear_off`.
    - `test_apply_move_bar_priority`.
    - `test_apply_move_invalid_indices`.
    - `test_apply_move_wrong_owner`.
    - `test_apply_move_invalid_direction`.
    - `test_apply_move_blocked_destination`.
    - `test_apply_move_hit_opponent`.
    - `test_get_point_invalid_index`.

### Arreglado:
- Enlances de [board.py] y [CONSIGNA.md] arreglados.

## [0.2.0] - 2025-09-15 - Segundo Sprint

### Añadido:
- Estructura del [CHANGELOG.md] con versiones [0.1.0], [0.2.0] y [Unreleased].
- En **[board.py]**:
    - Creación de la clase `Point` para representar un punto del tablero.
    - Creación de la clase `Board` con inicialización, disposición estándar, y movimientos básicos.
    - Adición de validaciones en `Board` (índices, propiedad, dirección, bloqueo, golpeo, no negativo).
    - Soporte para movimientos desde la barra (`src = -1`) y retiro de fichas (`dst = 24` para `X`, `dst = -1` para `O`).
    - Añadidos comentarios varios y docstrings según lo especificado en [CONSIGNA.md].

## [0.1.0] - 2025-09-03 - Primer Sprint

### Añadido:
- Carpetas y archivos varios vacíos.
- README.md simple con estructura básica del proyecto.
- Consigna del proyecto en formato Markdown.

[test_game.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/tests/test_game.py
[test_player.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/tests/test_player.py
[test_dice.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/tests/test_dice.py
[test_board.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/tests/test_board.py
[game.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/core/game.py
[player.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/core/player.py
[dice.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/core/dice.py
[board.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/core/board.py
[CONSIGNA.md]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/docs/CONSIGNA.md
[CHANGELOG.md]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/docs/CHANGELOG.md

[Unreleased]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/releases/tag/v0.1.0