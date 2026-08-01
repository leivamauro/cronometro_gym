"""Panel colapsable de historial de vueltas."""

import flet as ft
from utils.helpers import border_all


def create_lap_history(
    on_add_lap: callable,
    on_clear_laps: callable,
) -> tuple:
    """Retorna (control, refs). El panel se reconstruye al cambiar laps."""

    lap_list = ft.ListView(spacing=4, height=192, padding=ft.Padding(right=4), expand=True)
    header_title = ft.Text(
        "Historial de Vueltas / Laps (0)", size=13,
        weight=ft.FontWeight.W_600, color="#d1d5db", style=ft.TextStyle(letter_spacing=0.5),
    )

    add_lap_button = ft.Container(
        content=ft.Text("+ Registrar Vuelta", size=11, weight=ft.FontWeight.W_500,
                         color=ft.Colors.WHITE, no_wrap=True),
        bgcolor="#3a4452", border_radius=8,
        padding=ft.Padding(left=10, top=4, right=10, bottom=4),
        ink=True, on_click=lambda _: on_add_lap(),
    )
    clear_button = ft.IconButton(
        icon=ft.Icons.DELETE, icon_size=14, icon_color="#a1a1a6",
        on_click=lambda _: on_clear_laps(),
    )

    header_right = ft.Row(spacing=8, controls=[])

    header = ft.Container(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(spacing=8, controls=[
                    ft.Icon(ft.Icons.FLAG, size=14, color="#a1a1a6"),
                    header_title,
                ]),
                header_right,
            ],
        ),
        padding=ft.Padding(bottom=8),
        border=ft.Border(bottom=ft.BorderSide(1, "#374151")),
    )

    control = ft.Container(
        content=ft.Column(spacing=8, controls=[header, lap_list]),
        bgcolor="#1e232a",
        border=border_all(1, "#2d343f"),
        border_radius=16,
        padding=ft.Padding(left=16, top=16, right=16, bottom=16),
        shadow=ft.BoxShadow(0, 20, ft.Colors.with_opacity(0.6, ft.Colors.BLACK), ft.Offset(0, 8)),
    )

    refs = {
        "panel": control,
        "list": lap_list,
        "header_title": header_title,
        "header_right": header_right,
        "add_lap_button": add_lap_button,
        "clear_button": clear_button,
    }

    return control, refs
