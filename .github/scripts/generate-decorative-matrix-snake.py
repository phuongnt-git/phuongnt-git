#!/usr/bin/env python3
"""Render a clearly labeled decorative Matrix snake over synthetic cells.

The animation is inspired by snake-and-commits (MIT); see the vendor folder
for the upstream source and license. No GitHub contribution data is queried.
"""

from pathlib import Path
import sys
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor" / "snake-and-commits"))
import generate as snake_renderer  # noqa: E402


def main():
    columns, rows = 53, 7
    grid = [
        [1 + ((column * 7 + row * 11 + column * row % 13) % 4) for row in range(rows)]
        for column in range(columns)
    ]
    counts = [[1 for _ in range(rows)] for _ in range(columns)]

    # A continuous boustrophedon route traverses every synthetic matrix cell.
    route = []
    for row in range(rows):
        column_order = range(columns) if row % 2 == 0 else range(columns - 1, -1, -1)
        route.extend((column, row) for column in column_order)

    simulated_cells = len(route)
    target_length = 48
    growth = list(range(target_length - snake_renderer.BASE_LEN))
    eats = [(step, cell) for step, cell in enumerate(route)]
    opts = SimpleNamespace(frame=True, counter=True)

    svg = snake_renderer.render(
        grid=grid,
        counts=counts,
        months=[],
        route=route,
        eats=eats,
        growth=growth,
        theme="matrix",
        opts=opts,
    )
    svg = svg.replace("$ commits eaten:", "Commits eaten:")
    svg = svg.replace(
        "</svg>",
        f"  <!-- Decorative simulation: {simulated_cells} synthetic cells; not GitHub activity. -->\n</svg>",
    )

    output = Path("assets/contribution-matrix-snake.svg")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(f"Rendered decorative simulation: {simulated_cells}/{simulated_cells} cells; snake length {target_length}.")


if __name__ == "__main__":
    main()
