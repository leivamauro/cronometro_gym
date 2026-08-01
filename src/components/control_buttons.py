"""Botones principales: Iniciar, Pausar, Reiniciar."""

import flet as ft
from utils.helpers import border_all


def create_control_buttons(
    on_start: callable,
    on_pause: callable,
    on_reset: callable,
) -> tuple:
    """Retorna (control, refs) con referencias a los botones para actualizar estado."""

    start_btn = ft.Container(
        content=ft.Text("Iniciar", size=24, weight=ft.FontWeight.BOLD,
                         color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, no_wrap=True),
        bgcolor="#3a3a3c",
        border=border_all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
        border_radius=16,
        padding=ft.Padding(left=24, top=16, right=24, bottom=16),
        ink=True,
        on_click=lambda _: on_start(),
        shadow=ft.BoxShadow(0, 15, ft.Colors.with_opacity(0.4, ft.Colors.BLACK), ft.Offset(0, 4)),
        expand=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    pause_btn = ft.Container(
        content=ft.Text("Pausar", size=24, weight=ft.FontWeight.BOLD,
                         color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, no_wrap=True),
        bgcolor="#3a3a3c",
        border=border_all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
        border_radius=16,
        padding=ft.Padding(left=24, top=16, right=24, bottom=16),
        ink=True,
        on_click=lambda _: on_pause(),
        shadow=ft.BoxShadow(0, 15, ft.Colors.with_opacity(0.4, ft.Colors.BLACK), ft.Offset(0, 4)),
        expand=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    reset_btn = ft.Container(
        content=ft.Text("Reiniciar", size=24, weight=ft.FontWeight.BOLD,
                         color=ft.Colors.WHITE, text_align=ft.TextAlign.CENTER, no_wrap=True),
        bgcolor="#3a3a3c",
        border=border_all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
        border_radius=16,
        padding=ft.Padding(left=24, top=16, right=24, bottom=16),
        ink=True,
        on_click=lambda _: on_reset(),
        shadow=ft.BoxShadow(0, 15, ft.Colors.with_opacity(0.4, ft.Colors.BLACK), ft.Offset(0, 4)),
        expand=True,
        alignment=ft.alignment.Alignment(0, 0),
    )

    control = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=16,
        controls=[start_btn, pause_btn, reset_btn],
    )

    return control, {"start": start_btn, "pause": pause_btn, "reset": reset_btn}
