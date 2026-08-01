"""Barra de configuraciones extra: fuente, sonido, pantalla completa, vueltas."""

import flet as ft
from utils.helpers import border_all


def create_extra_settings(
    on_font_change: callable,
    on_sound_toggle: callable,
    on_laps_toggle: callable,
    on_fullscreen: callable,
    is_mobile: bool = False,
) -> tuple:
    """Retorna (control, refs) con referencias a botones dinámicos."""

    font_buttons = {}
    for key, label in [("handwritten", "Architects"), ("caveat", "Caveat"), ("comic", "Comic")]:
        btn = ft.Container(
            content=ft.Text(label, size=11, no_wrap=True),
            border_radius=6,
            padding=ft.Padding(left=8, top=3, right=8, bottom=3),
            ink=True,
            data=key,
        )
        btn.on_click = lambda e, k=key: on_font_change(k)
        font_buttons[key] = btn

    laps_btn = ft.Container(
        content=ft.Row(spacing=4, controls=[
            ft.Icon(ft.Icons.LIST, size=13),
            ft.Text("Vueltas", size=11, no_wrap=True),
        ]),
        bgcolor="#1a1f26",
        border=border_all(1, "#374151"),
        border_radius=8,
        padding=ft.Padding(left=10, top=5, right=10, bottom=5),
        ink=True,
    )
    laps_btn.on_click = lambda _: on_laps_toggle()

    def _toggle_sound(e):
        new_sound_on = on_sound_toggle()
        sound_btn.icon = ft.Icons.VOLUME_UP if new_sound_on else ft.Icons.VOLUME_OFF
        sound_btn.update()

    sound_btn = ft.IconButton(
        icon=ft.Icons.VOLUME_UP, icon_size=13, icon_color="#a1a1a6",
        style=ft.ButtonStyle(
            bgcolor={"": "#1a1f26"},
            side={"": ft.BorderSide(1, "#374151")},
            shape={"": ft.RoundedRectangleBorder(radius=8)},
        ),
        on_click=_toggle_sound,
    )

    fullscreen_btn = ft.IconButton(
        icon=ft.Icons.FULLSCREEN, icon_size=13, icon_color="#a1a1a6",
        style=ft.ButtonStyle(
            bgcolor={"": "#1a1f26"},
            side={"": ft.BorderSide(1, "#374151")},
            shape={"": ft.RoundedRectangleBorder(radius=8)},
        ),
        on_click=lambda _: on_fullscreen(),
    )

    if is_mobile:
        inner = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            controls=[sound_btn, fullscreen_btn],
        )
    else:
        inner = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(spacing=6, controls=[
                    ft.Icon(ft.Icons.TITLE, size=13, color="#a1a1a6"),
                    ft.Text("Fuente:", size=11, color="#a1a1a6", no_wrap=True),
                    font_buttons["handwritten"],
                    font_buttons["caveat"],
                    font_buttons["comic"],
                ]),
                ft.Row(spacing=6, controls=[
                    laps_btn,
                    sound_btn,
                    fullscreen_btn,
                ]),
            ],
        )

    control = ft.Container(
        content=inner,
        padding=ft.Padding(top=16),
    )

    refs = {
        "font_buttons": font_buttons,
        "laps_btn": laps_btn,
        "sound_btn": sound_btn,
        "container": control,
    }

    return control, refs
