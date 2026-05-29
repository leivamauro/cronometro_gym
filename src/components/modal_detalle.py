# python
import flet as ft
# locales
from constants import *


def crear_modal_detalles(nombre_miembro: str, page: ft.Page):
    is_mobile = page.width is not None and page.width < 600

    # --- Header del modal (unificado con modal_pago) ---
    header = ft.Container(
        content=ft.Text(
            f"Detalles del Miembro - {nombre_miembro}",
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
        modal_detalles.open = False
        page.update()

    cancelar_btn = ft.OutlinedButton(
        content=ft.Text("Cancelar"),
        style=ft.ButtonStyle(
            color=THEME_TEXT_PRIMARY,
            side=ft.BorderSide(1, THEME_BORDER_COLOR),
            mouse_cursor=ft.MouseCursor.CLICK,
        ),
        on_click=cerrar_modal,
    )

    # --- Columna Izquierda: Información Detallada ---
    columna_izquierda = ft.Column(
        controls=[
            ft.Text("Información Detallada", size=18, color=THEME_TEXT_PRIMARY),
            ft.Container(height=5),
            ft.Text(f"Nombre: {nombre_miembro}", color=THEME_TEXT_PRIMARY),
            ft.Text("Fecha Registro: 10/01/2026", color=THEME_TEXT_PRIMARY),
            ft.Text("Último Pago: 15/03/2026 ($3000)", color=THEME_TEXT_PRIMARY),
            ft.Text("Estado actual: Vencido (Rojo)", color=THEME_TEXT_PRIMARY),
            ft.Text("Debe 2 meses ($6000)", color=THEME_TEXT_PRIMARY),
            ft.Text("Vencido hace 45 días", color=THEME_TEXT_PRIMARY),
        ],
        spacing=8,
    )

    # --- Columna Derecha: Historial de Pagos ---
    tabla_cabecera = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Fecha", weight="bold", color=THEME_TEXT_PRIMARY, width=80, text_align="center"),
                ft.Text("|", color=THEME_BORDER_COLOR),
                ft.Text("Monto", weight="bold", color=THEME_TEXT_PRIMARY, width=60, text_align="center"),
                ft.Text("|", color=THEME_BORDER_COLOR),
                ft.Text("Meses", weight="bold", color=THEME_TEXT_PRIMARY, width=50, text_align="center"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border=ft.Border.only(bottom=ft.BorderSide(1, THEME_BORDER_COLOR)),
        padding=ft.Padding.only(bottom=10),
    )

    datos_historial = [
        {"fecha": "15/03/2026", "monto": "$3000", "meses": "1 mes"},
        {"fecha": "15/02/2026", "monto": "$3000", "meses": "1 mes"},
        {"fecha": "15/02/2026", "monto": "$3000", "meses": "1 mes"},
        {"fecha": "15/03/2026", "monto": "$3000", "meses": "1 mes"},
    ]

    filas_historial = []
    for pago in datos_historial:
        fila = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(pago["fecha"], color=THEME_TEXT_PRIMARY, width=80, text_align="center"),
                    ft.Text("|", color=THEME_BORDER_COLOR),
                    ft.Text(pago["monto"], color=THEME_TEXT_PRIMARY, width=60, text_align="center"),
                    ft.Text("|", color=THEME_BORDER_COLOR),
                    ft.Text(pago["meses"], color=THEME_TEXT_PRIMARY, width=50, text_align="center"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            border=ft.Border.only(bottom=ft.BorderSide(1, THEME_BORDER_COLOR)),
            padding=ft.Padding.symmetric(vertical=10),
        )
        filas_historial.append(fila)

    if is_mobile:
        # Mobile: información arriba, historial abajo, cancelar al fondo
        columna_derecha = ft.Column(
            controls=[
                ft.Text("Historial de Pagos", size=18, color=THEME_TEXT_PRIMARY),
                ft.Container(height=5),
                tabla_cabecera,
                ft.Column(controls=filas_historial, scroll=ft.ScrollMode.AUTO, spacing=0),
                ft.Container(expand=True),
                ft.Row(controls=[ft.Container(expand=True), cancelar_btn]),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=8,
        )

        ancho_modal = page.width * 0.9 if page.width else None

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
                ft.Text("Historial de Pagos", size=18, color=THEME_TEXT_PRIMARY),
                ft.Container(height=5),
                tabla_cabecera,
                ft.Column(controls=filas_historial, scroll=ft.ScrollMode.AUTO, expand=True, spacing=0),
                ft.Row(
                    controls=[ft.Container(expand=True), cancelar_btn],
                ),
            ],
            spacing=8,
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
                            ft.VerticalDivider(width=1, color=THEME_BORDER_COLOR),
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

    modal_detalles = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        shape=ft.RoundedRectangleBorder(radius=12),
        content=ft.Container(
            content=contenido,
            width=ancho_modal if is_mobile else 700,
            height=None if is_mobile else 380,
        ),
        content_padding=ft.Padding.all(0),
    )

    return modal_detalles
