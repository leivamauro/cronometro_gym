"""Modal para configurar el tiempo de cuenta regresiva."""

import flet as ft
from utils.helpers import border_all


def _font_family(font_style: str) -> str:
    return {
        "handwritten": "Architects Daughter",
        "caveat": "Caveat",
        "comic": "Comic Neue",
    }.get(font_style, "Architects Daughter")


def create_time_select_modal(
    initial_hours: int,
    initial_minutes: int,
    initial_seconds: int,
    font_style: str,
    on_confirm: callable,
    on_cancel: callable,
    is_mobile: bool = False,
) -> ft.AlertDialog:
    font = _font_family(font_style)

    hours = [initial_hours]
    minutes = [initial_minutes]
    seconds = [initial_seconds]

    def _make_spinner(label: str, value_ref: list, min_val: int, max_val: int, highlighted: bool) -> ft.Control:
        border_color = "#38bdf8" if highlighted else ft.Colors.with_opacity(0.4, "#9ca3af")

        def increment(_):
            if value_ref[0] < max_val:
                value_ref[0] += 1
                txt.value = str(value_ref[0]).zfill(2)
                txt.update()

        def decrement(_):
            if value_ref[0] > min_val:
                value_ref[0] -= 1
                txt.value = str(value_ref[0]).zfill(2)
                txt.update()

        txt = ft.TextField(
            value=str(value_ref[0]).zfill(2),
            text_align=ft.TextAlign.CENTER,
            text_size=22,
            color=ft.Colors.WHITE,
            bgcolor="#3d4653",
            border=ft.InputBorder.NONE,
            border_radius=12,
            height=60,
            content_padding=ft.Padding(top=8, bottom=8),
            text_style=ft.TextStyle(font_family=font, weight=ft.FontWeight.BOLD),
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: _handle_input(e, value_ref, min_val, max_val, txt),
            expand=True,
        )

        return ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            expand=True,
            controls=[
                ft.Text(
                    label,
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#e5e7eb",
                    font_family=font,
                    no_wrap=True,
                ),
                ft.Container(
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            txt,
                        ] + ([ft.Column(
                            spacing=0,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.KEYBOARD_ARROW_UP,
                                    icon_size=16,
                                    icon_color="#d1d5db",
                                    on_click=increment,
                                    style=ft.ButtonStyle(padding=ft.Padding(left=0, top=0, right=0, bottom=0)),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.KEYBOARD_ARROW_DOWN,
                                    icon_size=16,
                                    icon_color="#d1d5db",
                                    on_click=decrement,
                                    style=ft.ButtonStyle(padding=ft.Padding(left=0, top=0, right=0, bottom=0)),
                                ),
                            ],
                        )] if not is_mobile else []),
                    ),
                    bgcolor="#3d4653",
                    border=border_all(2, border_color),
                    border_radius=12,
                    padding=ft.Padding(left=4, top=4, right=4, bottom=4),
                ),
                ft.Text(
                    f"({min_val}-{max_val})",
                    size=12,
                    color="#d1d5db",
                    font_family=font,
                    no_wrap=True,
                ),
            ],
        )

    def _handle_input(e, value_ref, min_val, max_val, text_field):
        try:
            val = int(e.control.value) if e.control.value else 0
        except ValueError:
            val = min_val
        val = max(min_val, min(max_val, val))
        value_ref[0] = val
        text_field.value = str(val).zfill(2)
        text_field.update()

    def on_accept_click(_):
        on_confirm(hours[0], minutes[0], seconds[0])

    return ft.AlertDialog(
        modal=True,
        bgcolor="#535e6c",
        shape=ft.RoundedRectangleBorder(radius=24),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8,
                    controls=[
                        _make_spinner("Horas", hours, 0, 99, True),
                        _make_spinner("Minutos", minutes, 0, 59, False),
                        _make_spinner("Segundos", seconds, 0, 59, False),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=12,
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "Aceptar",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#12161b",
                                font_family=font,
                                text_align=ft.TextAlign.CENTER,
                                no_wrap=True,
                            ),
                            bgcolor="#8b99aa",
                            border_radius=16,
                            border=border_all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            ink=True,
                            on_click=on_accept_click,
                            expand=True,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                        ft.Container(
                            content=ft.Text(
                                "Cancelar",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color="#12161b",
                                font_family=font,
                                text_align=ft.TextAlign.CENTER,
                                no_wrap=True,
                            ),
                            bgcolor="#8b99aa",
                            border_radius=16,
                            border=border_all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                            padding=ft.Padding(left=20, top=10, right=20, bottom=10),
                            ink=True,
                            on_click=lambda _: on_cancel(),
                            expand=True,
                            alignment=ft.alignment.Alignment(0, 0),
                        ),
                    ],
                ),
            ],
        ),
    )
