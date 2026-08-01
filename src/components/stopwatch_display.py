"""Display del cronómetro: 3 cajas cuadradas (hr, min, seg) cliqueables."""

import flet as ft
from utils.helpers import border_all


def create_stopwatch_display(on_click: callable) -> tuple:
    """Retorna (control, refs) donde refs contiene los textos y cajas dinámicos."""
    font = "Architects Daughter"

    hour_text = ft.Text(
        "00", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
        font_family=font, text_align=ft.TextAlign.CENTER, no_wrap=True,
    )
    min_text = ft.Text(
        "00", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
        font_family=font, text_align=ft.TextAlign.CENTER, no_wrap=True,
    )
    sec_text = ft.Text(
        "00", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE,
        font_family=font, text_align=ft.TextAlign.CENTER, no_wrap=True,
    )

    badge_text = ft.Text(
        "\u23f1\ufe0f Modo Cron\u00f3metro",
        size=12, weight=ft.FontWeight.W_600, color="#a1a1aa",
        style=ft.TextStyle(letter_spacing=1), no_wrap=True,
    )
    badge = ft.Container(
        content=badge_text,
        bgcolor="#27272a", border_radius=999,
        padding=ft.Padding(left=12, top=4, right=12, bottom=4),
        border=border_all(1, "#3f3f46"),
    )

    def _box(text_ctrl, label: str) -> ft.Container:
        box = ft.Container(
            content=ft.Stack([
                ft.Container(content=text_ctrl, alignment=ft.alignment.Alignment(0, 0), expand=True),
                ft.Container(
                    content=ft.Text(
                        label, size=14, color="#888888", font_family=font,
                        no_wrap=True,
                    ),
                    alignment=ft.alignment.Alignment(1, -1),
                    padding=ft.Padding(top=8, right=10),
                ),
            ]),
            bgcolor="#1c1c1e",
            border=border_all(1, ft.Colors.with_opacity(0.1, ft.Colors.WHITE)),
            border_radius=20,
            ink=True,
            on_click=lambda _: on_click(),
            shadow=ft.BoxShadow(0, 30, ft.Colors.with_opacity(0.6, ft.Colors.BLACK), ft.Offset(0, 10)),
        )
        return box

    box_h = _box(hour_text, "hr")
    box_m = _box(min_text, "min")
    box_s = _box(sec_text, "seg")

    control = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
        controls=[
            badge,
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8,
                controls=[box_h, box_m, box_s],
            ),
        ],
    )

    refs = {
        "hour": hour_text,
        "min": min_text,
        "sec": sec_text,
        "badge": badge,
        "badge_text": badge_text,
        "container": control,
        "boxes": [box_h, box_m, box_s],
        "texts": [hour_text, min_text, sec_text],
    }

    return control, refs
