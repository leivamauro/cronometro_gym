"""Logo Recoverfit."""

import flet as ft


def create_header_logo() -> ft.Control:
    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[
            ft.Image(
                src="images/recoverfit_logo_recortado.png",
                width=400,
                fit=ft.BoxFit.CONTAIN,
                expand=True,
            ),
        ],
    )
