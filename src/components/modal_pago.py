# python
import flet as ft
# local
from constants import *


def crear_modal_pago(nombre_miembro: str, page: ft.Page):
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal ---
    header = ft.Container(
        content=ft.Text(
            f"Registrar Pago - {nombre_miembro}",
            size=14,
            weight="bold",
            color=THEME_TEXT_PRIMARY,
            text_align=ft.TextAlign.CENTER,
        ),
        bgcolor=THEME_HEADER_BG,
        padding=ft.Padding(20, 14, 20, 14),
        alignment=ft.Alignment.CENTER,
    )

    # --- Columna Izquierda: Dropdown y Total ---
    opciones_meses = [
        ft.dropdown.Option("1 mes ($3000)"),
        ft.dropdown.Option("2 meses ($6000)"),
        ft.dropdown.Option("3 meses ($9000)"),
    ]

    dropdown = ft.Dropdown(
        label="Meses a abonar",
        options=opciones_meses,
        value="1 mes ($3000)",
        width=280,
        border_color=THEME_BORDER_COLOR,
        focused_border_color=THEME_TEAL,
        color=THEME_TEXT_PRIMARY,
    )

    total_text = ft.Text("Total: $3000", size=32, weight="bold",
                         color=THEME_TEXT_PRIMARY)

    columna_izquierda = ft.Column(
        controls=[
            dropdown,
            ft.Container(expand=True),
            total_text,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # --- QR, Texto y Botones ---
    def cerrar_modal(e):
        modal_pago.open = False
        page.update()

    confirmar_btn = ft.FilledButton(
        content=ft.Text("Confirmar Pago"),
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

    # Contenedor QR que ocupa ~80-90% del espacio disponible en la derecha
    qr_container = ft.Container(
        content=ft.Image(
            src="src/assets/qr_ejemplo.png",
            fit="contain",
            expand=True,
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        expand=True,
        alignment=ft.Alignment.CENTER,
    )

    if is_mobile:
        # Mobile: izquierda arriba, QR + botones abajo
        ancho_modal = page.width * 0.9 if page.width else None

        columna_derecha = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        src="src/assets/qr_ejemplo.png",
                        fit="contain",
                        expand=True,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=12,
                    height=180,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text("Escaneá el código QR para abonar",
                        size=14, color=THEME_TEXT_PRIMARY),
                ft.Row(
                    controls=[confirmar_btn, cancelar_btn],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        contenido = ft.Column(
            controls=[
                header,
                ft.Container(
                    content=columna_izquierda,
                    padding=ft.Padding(20, 20, 20, 10),
                ),
                ft.Container(
                    content=columna_derecha,
                    padding=ft.Padding(20, 10, 20, 20),
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    else:
        # Desktop: izquierda y derecha lado a lado
        columna_derecha = ft.Column(
            controls=[
                qr_container,
                ft.Text("Escaneá el código QR para abonar",
                        size=14, color=THEME_TEXT_PRIMARY),
                ft.Row(
                    controls=[confirmar_btn, cancelar_btn],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )

        contenido = ft.Column(
            controls=[
                header,
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=columna_izquierda,
                                padding=ft.Padding(20, 20, 20, 20),
                                expand=True,
                            ),
                            ft.VerticalDivider(width=1,
                                               color=THEME_BORDER_COLOR),
                            ft.Container(
                                content=columna_derecha,
                                padding=ft.Padding(20, 20, 20, 20),
                                expand=True,
                            ),
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
        )

    modal_pago = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido,
            width=ancho_modal if is_mobile else 650,
            height=None if is_mobile else 380,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_pago
