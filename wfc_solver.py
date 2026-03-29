import numpy as np

def apply_wfc_constraints(qrc_output_sequence: list[float], level_width: int, level_height: int) -> list[list[int]]:
    """
    Applies simplified Wave Function Collapse (WFC) inspired constraints
    to a QRC output sequence to generate a coherent level layout.
    This is a placeholder for a more complex WFC implementation.

    Args:
        qrc_output_sequence: A sequence of floats (0 to 1) from QRC, representing tile probabilities.
        level_width: The desired width of the level grid.
        level_height: The desired height of the level grid.

    Returns:
        A 2D list representing the generated level grid with integer tile types.
    """
    # For demonstration, we'll simplify: QRC output directly influences tile types.
    # A real WFC would iteratively collapse states based on local constraints.

    level_grid = [[0 for _ in range(level_width)] for _ in range(level_height)]
    sequence_idx = 0

    for r in range(level_height):
        for c in range(level_width):
            if sequence_idx < len(qrc_output_sequence):
                # Map QRC float output to a simple tile type (e.g., 0, 1, 2)
                # This is a very basic mapping for MVP demonstration.
                tile_value = qrc_output_sequence[sequence_idx]
                if tile_value < 0.33:
                    level_grid[r][c] = 0  # Empty space
                elif tile_value < 0.66:
                    level_grid[r][c] = 1  # Platform
                else:
                    level_grid[r][c] = 2  # Hazard
                sequence_idx += 1
            else:
                # If QRC sequence runs out, fill with default or repeat pattern
                level_grid[r][c] = 0

    # Apply a very basic connectivity constraint: ensure no floating platforms
    for r in range(level_height - 2, -1, -1): # Iterate from second to last row upwards
        for c in range(level_width):
            if level_grid[r][c] == 1 and level_grid[r+1][c] == 0: # Platform with empty space below
                # Try to place a support or change to empty space
                if c > 0 and level_grid[r+1][c-1] != 0:
                    level_grid[r+1][c] = 1 # Extend platform below
                elif c < level_width - 1 and level_grid[r+1][c+1] != 0:
                    level_grid[r+1][c] = 1 # Extend platform below
                else:
                    level_grid[r][c] = 0 # Remove floating platform

    return level_grid

def ensure_playability(level_grid: list[list[int]]) -> list[list[int]]:
    """
    A placeholder function to ensure basic playability (e.g., start/end points, paths).
    For MVP, this can be a simple check or a minor adjustment.
    """
    # For demonstration, ensure there's at least one 'platform' tile.
    has_platform = any(1 in row for row in level_grid)
    if not has_platform:
        level_grid[len(level_grid) - 1][len(level_grid[0]) // 2] = 1 # Place a platform at bottom center
    return level_grid
