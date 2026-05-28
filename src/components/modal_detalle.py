# python
import flet as ft
# locales
from constants import *

def crear_modal_detalles(nombre_miembro: str):
    """
    Crea y retorna un componente AlertDialog con los detalles y el historial del miembro.
    """

    # --- Cabecera del Modal (Título y Botón Cerrar) ---
    # Usamos un Row para poder poner la "X" del lado derecho
    cabecera = ft.Row(
        controls=[
            ft.Text(f"Detalles del Miembro - {nombre_miembro}", color=THEME_TEXT_PRIMARY, size=20),
            ft.IconButton(
                icon="close",
                icon_color=THEME_TEXT_PRIMARY,
                # Funcionalidad pendiente (debería cerrar el modal)
                on_click=lambda e: None
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # --- Columna Izquierda: Información Detallada ---
    columna_izquierda = ft.Column(
        controls=[
            ft.Text("Información Detallada", size=18,color=THEME_TEXT_PRIMARY),
            ft.Container(height=5),  # Espaciador ligero
            ft.Text(f"Nombre: {nombre_miembro}", color=THEME_TEXT_PRIMARY),
            ft.Text("Fecha Registro: 10/01/2026", color=THEME_TEXT_PRIMARY),
            ft.Text("Último Pago: 15/03/2026 ($3000)", color=THEME_TEXT_PRIMARY),
            ft.Text("Estado actual: Vencido (Rojo)", color=THEME_TEXT_PRIMARY),
            ft.Text("Debe 2 meses ($6000)", color=THEME_TEXT_PRIMARY),
            ft.Text("Vencido hace 45 días", color=THEME_TEXT_PRIMARY),
        ],
        expand=1,  # Ocupa la mitad del espacio disponible
        spacing=8,
    )

    # --- Columna Derecha: Historial de Pagos (Tabla con Scroll) ---
    # 1. Cabecera de la tabla
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
        padding=ft.Padding.only(bottom=10)
    )

    # 2. Filas de datos (Mock data basados en la imagen)
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
            padding=ft.Padding.symmetric(vertical=10)
        )
        filas_historial.append(fila)

    # 3. Ensamblaje de la columna derecha
    columna_derecha = ft.Column(
        controls=[
            ft.Text("Historial de Pagos", size=18, color=THEME_TEXT_PRIMARY),
            ft.Container(height=5),
            tabla_cabecera,
            # Contenedor con Scroll para las filas
            ft.Column(
                controls=filas_historial,
                scroll=ft.ScrollMode.AUTO,
                expand=True,  # Permite que crezca y active el scroll si es necesario
                spacing=0,
            )
        ],
        expand=1,  # Ocupa la otra mitad del espacio
    )

    # --- Ensamblado del Modal Final ---
    modal_detalles = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        title=cabecera,
        title_padding=ft.Padding.only(top=20, left=25, right=15, bottom=10),
        content_padding=ft.Padding.all(25),
        content=ft.Container(
            width=700,
            height=280,
            content=ft.Row(
                controls=[columna_izquierda, columna_derecha],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )
    )

    return modal_detalles
