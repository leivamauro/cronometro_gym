# pyton
import flet as ft
# local
from constants import *

def crear_modal_pago(nombre_miembro: str):
    """
    Crea y retorna un componente AlertDialog con la interfaz de registro de pago.
    """

    # --- Columna Izquierda: Dropdown y Total ---
    opciones_meses = [
        ft.dropdown.Option("1 mes ($3000)"),
        ft.dropdown.Option("2 meses ($6000)"),
        ft.dropdown.Option("3 meses ($9000)"),
    ]

    columna_izquierda = ft.Column(
        controls=[
            ft.Dropdown(
                label="Meses a abonar",
                options=opciones_meses,
                value="1 mes ($3000)",  # Valor por defecto
                width=280,
                border_color=THEME_BORDER_COLOR,
                focused_border_color=THEME_TEAL,
                color=THEME_TEXT_PRIMARY,
            ),
            # El spacer empuja el total hacia el fondo para lograr el space-between
            ft.Container(expand=True),
            ft.Text("Total: $3000", size=32, weight="bold",
                    color=THEME_TEXT_PRIMARY),
        ],
        expand=1,  # Ocupa la mitad del espacio disponible en la fila
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # --- Columna Derecha: QR, Texto y Botones ---
    columna_derecha = ft.Column(
        controls=[
            # Placeholder del QR (Reemplazar por ft.Image cuando tengas el archivo)
            ft.Container(
                width=160,
                height=160,
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                alignment=ft.Alignment.CENTER,
                # Ejemplo de cómo poner la imagen real:
                # content=ft.Image(src="ruta/al/qr_mercadopago.png", fit=ft.ImageFit.CONTAIN)
                content=ft.Icon("qr_code_2", size=120, color=ft.Colors.BLACK)
            ),
            ft.Text(
                "Escaneá el código QR para abonar",
                size=14,
                color=THEME_TEXT_PRIMARY
            ),
            # Fila de botones
            ft.Row(
                controls=[
                    ft.FilledButton(
                        content=ft.Text("Confirmar Pago"),
                        bgcolor=THEME_TEAL,
                        color=THEME_TEAL_TEXT,
                        on_click=lambda e: None,  # Funcionalidad pendiente
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Cancelar"),
                        style=ft.ButtonStyle(
                            color=THEME_TEXT_PRIMARY,
                            side=ft.BorderSide(1, THEME_BORDER_COLOR),
                        ),
                        on_click=lambda e: None,  # Funcionalidad pendiente
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        expand=1,  # Ocupa la otra mitad del espacio
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15
    )

    # --- Ensamblado del Modal (AlertDialog) ---
    modal_pago = ft.AlertDialog(
        modal=True,
        bgcolor=THEME_CARD_BG,
        # Título en gris claro según tu requerimiento
        title=ft.Text(f"Registrar Pago - {nombre_miembro}", color="#E0E0E0", size=20),
        title_padding=ft.Padding.only(top=20, left=20, right=20, bottom=10),
        content_padding=ft.Padding.all(20),
        # Contenido principal estructurado en una fila de dos columnas
        content=ft.Container(
            width=650,
            height=300,
            content=ft.Row(
                controls=[columna_izquierda, columna_derecha],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
    )

    return modal_pago
