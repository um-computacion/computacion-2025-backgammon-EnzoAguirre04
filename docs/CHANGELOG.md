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

## [Unreleased] - Segundo Sprint

### Añadido:
- Añadido el enlace del [CHANGELOG.md] en este mismo archivo.

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

[board.py]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/core/board.py
[CONSIGNA.md]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/docs/CONSIGNA.md
[CHANGELOG.md]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/blob/main/docs/CHANGELOG.md

[Unreleased]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/um-computacion/computacion-2025-backgammon-EnzoAguirre04/releases/tag/v0.1.0