# python
import flet as ft
# local
from constants import *


def crear_modal_conf(page: ft.Page):
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal (unificado con modal_pago) ---
    header = ft.Container(
        content=ft.Text(
            "Configuración",
            size=14,
            weight="bold",
            color=THEME_TEXT_PRIMARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=THEME_HEADER_BG_MODAL,
        padding=ft.Padding(20, 14, 20, 14),
        alignment=ft.Alignment.CENTER,
        border_radius=ft.BorderRadius.only(top_left=12, top_right=12),
    )

    # --- Acción cerrar ---
    def cerrar_modal(e):
        modal_conf.open = False
        page.update()

    # --- Campos de entrada ---
    precio_field = ft.TextField(
        label="Precio mensual",
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    prueba_field = ft.TextField(
        label="Tiempo de prueba (días)",
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # --- Botones ---
    guardar_btn = ft.FilledButton(
        content=ft.Text("Guardar"),
        bgcolor=THEME_TEAL,
        color=THEME_TEAL_TEXT,
        on_click=lambda e: None,
    )

    cancelar_btn = ft.OutlinedButton(
        content=ft.Text("Cancelar"),
        style=ft.ButtonStyle(
            color=THEME_TEXT_PRIMARY,
            side=ft.BorderSide(1, THEME_BORDER_COLOR),
        ),
        on_click=cerrar_modal,
    )

    # --- Cuerpo del modal ---
    campos = ft.Column(
        controls=[
            precio_field,
            ft.Container(height=15),
            prueba_field,
            ft.Container(expand=True),
            ft.Row(
                controls=[guardar_btn, cancelar_btn],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ],
        expand=True,
    )

    contenido = ft.Column(
        controls=[
            header,
            ft.Container(
                content=campos,
                padding=ft.Padding(20, 20, 20, 20),
                expand=True,
            ),
        ],
    )

    modal_conf = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido,
            width=page.width * 0.9 if is_mobile else 450,
            height=None if is_mobile else 280,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_conf
