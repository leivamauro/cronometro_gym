"""Logo Recoverfit."""

import flet as ft


def create_header_logo() -> tuple:
    """Retorna (control, refs) con el logo responsive."""
    logo_img = ft.Image(
        src="images/recoverfit_logo_recortado.png",
        fit=ft.BoxFit.CONTAIN,
    )

    control = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        controls=[logo_img],
    )

    return control, {"image": logo_img}
