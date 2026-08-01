"""Helpers compatibles con Flet 0.86.5."""

import flet as ft


def border_all(width: float, color: str) -> ft.Border:
    side = ft.BorderSide(width, color)
    return ft.Border(top=side, left=side, right=side, bottom=side)
