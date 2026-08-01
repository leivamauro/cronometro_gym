"""Reloj del sistema en tiempo real (24h)."""

from datetime import datetime
import flet as ft
from utils.helpers import border_all


def create_real_time_clock(on_swap: callable) -> tuple:
    """Retorna (control, refs) con el texto del reloj."""

    time_text = ft.Text(
        value="",
        size=26,
        weight=ft.FontWeight.W_500,
        color="#a1a1a6",
        style=ft.TextStyle(letter_spacing=2),
        text_align=ft.TextAlign.CENTER,
        no_wrap=True,
    )

    def format_time() -> str:
        now = datetime.now()
        return now.strftime("%H:%M:%S")

    time_text.value = format_time()

    control = ft.Container(
        content=time_text,
        bgcolor="#1c1c1e",
        border=border_all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
        border_radius=16,
        padding=ft.Padding(left=40, top=14, right=40, bottom=14),
        width=400,
        ink=True,
        on_click=lambda _: on_swap(),
        shadow=ft.BoxShadow(0, 20, ft.Colors.with_opacity(0.4, ft.Colors.BLACK), ft.Offset(0, 4)),
        alignment=ft.alignment.Alignment(0, 0),
    )

    return control, {"text": time_text, "container": control}
