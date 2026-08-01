"""Recoverfit - Cronómetro y Reloj (Flet)."""

import asyncio
import time
from datetime import datetime
import flet as ft

from components.header_logo import create_header_logo
from components.stopwatch_display import create_stopwatch_display
from components.real_time_clock import create_real_time_clock
from components.control_buttons import create_control_buttons
from components.lap_history import create_lap_history
from components.extra_settings import create_extra_settings
from components.time_select_modal import create_time_select_modal
from utils.audio import play_beep
from utils.helpers import border_all


FONT_MAP = {
    "handwritten": "Architects Daughter",
    "caveat": "Caveat",
    "comic": "Comic Neue",
}


async def main(page: ft.Page):
    # ── Page config ────────────────────────────────────────────────
    page.title = "Recoverfit - Cron\u00f3metro y Reloj"
    page.bgcolor = ft.Colors.BLACK
    page.padding = 0
    page.window.width = 520
    page.window.height = 900
    page.window.min_width = 400
    page.window.min_height = 720
    await page.window.center()

    page.fonts = {
        "Architects Daughter": "assets/fonts/ArchitectsDaughter-Regular.ttf",
        "Caveat": "assets/fonts/Caveat-Variable.ttf",
        "Comic Neue": "assets/fonts/ComicNeue-Regular.ttf",
        "Montserrat": "assets/fonts/Montserrat-Variable.ttf",
    }

    # ── Global shared state ────────────────────────────────────────
    S = {
        "status": "idle",
        "mode": "stopwatch",
        "elapsed_ms": 0,
        "target_ms": 0,
        "remaining_ms": 0,
        "font_style": "handwritten",
        "sound_enabled": True,
        "laps": [],
        "show_laps": False,
        "start_time": 0.0,
        "accumulated_ms": 0.0,
        "swapped": False,
    }

    # ── Build components ───────────────────────────────────────────
    header = create_header_logo()

    display, drefs = create_stopwatch_display(on_click=lambda: _open_modal())

    clock, clock_refs = create_real_time_clock(on_swap=lambda: _toggle_swap())

    btns, btn_refs = create_control_buttons(
        on_start=lambda: _handle_start(),
        on_pause=lambda: _handle_pause(),
        on_reset=lambda: _handle_reset(),
    )

    laps_panel, lap_refs = create_lap_history(
        on_add_lap=lambda: _handle_add_lap(),
        on_clear_laps=lambda: _handle_clear_laps(),
    )

    settings, settings_refs = create_extra_settings(
        on_font_change=lambda k: _handle_font_change(k),
        on_sound_toggle=lambda: _handle_sound_toggle(),
        on_laps_toggle=lambda: _handle_laps_toggle(),
        on_fullscreen=lambda: _toggle_fullscreen(),
    )

    # ── Swap clock / stopwatch display ─────────────────────────────
    def _toggle_swap():
        S["swapped"] = not S["swapped"]
        _update_display()
        page.update()

    # ── Layout ─────────────────────────────────────────────────────
    scrollable_col = ft.Column(
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    main_container = ft.Container(
        content=ft.Column(
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                header,
                ft.Container(height=8),
                display,
                ft.Container(height=12),
                clock,
                ft.Container(height=16),
                btns,
                laps_panel,
                settings,
            ],
        ),
        margin=ft.Margin(left=16, top=24, right=16, bottom=24),
    )

    laps_panel.visible = False

    scrollable_col.controls.append(main_container)
    page.add(scrollable_col)

    # ── Modal ──────────────────────────────────────────────────────
    def _open_modal():
        total_ms = S["target_ms"] if S["mode"] == "countdown" and S["target_ms"] > 0 else S["elapsed_ms"]
        total_secs = max(0, total_ms // 1000)
        ih = total_secs // 3600
        im = (total_secs % 3600) // 60
        is_ = total_secs % 60

        def _confirm(h, m, s):
            total = (h * 3600 + m * 60 + s) * 1000
            S["start_time"] = 0
            S["accumulated_ms"] = 0
            S["elapsed_ms"] = 0
            if total > 0:
                S["mode"] = "countdown"
                S["target_ms"] = total
                S["remaining_ms"] = total
            else:
                S["mode"] = "stopwatch"
                S["target_ms"] = 0
                S["remaining_ms"] = 0
            S["status"] = "idle"
            _update_display()
            _update_buttons()
            page.pop_dialog()
            page.update()

        def _cancel():
            page.pop_dialog()
            page.update()

        dialog = create_time_select_modal(ih, im, is_, S["font_style"], _confirm, _cancel)
        page.show_dialog(dialog)

    # ── Timer loop ──────────────────────────────────────────────────
    async def _timer_loop():
        while True:
            if S["status"] == "running" and S["start_time"] > 0:
                now = time.perf_counter()
                delta_ms = (now - S["start_time"]) * 1000
                total_ms = S["accumulated_ms"] + delta_ms

                if S["mode"] == "stopwatch":
                    S["elapsed_ms"] = int(total_ms)
                else:
                    remaining = S["target_ms"] - total_ms
                    if remaining <= 0:
                        S["remaining_ms"] = 0
                        S["elapsed_ms"] = 0
                        S["status"] = "idle"
                        S["mode"] = "stopwatch"
                        S["target_ms"] = 0
                        S["start_time"] = 0
                        S["accumulated_ms"] = 0
                        if S["sound_enabled"]:
                            play_beep("reset")
                    else:
                        S["remaining_ms"] = int(remaining)

            _update_display()
            _update_buttons()
            page.update()
            await asyncio.sleep(0.03)

    asyncio.create_task(_timer_loop())

    # ── Display / UI update helpers ────────────────────────────────
    def _get_active_ms():
        if S["mode"] == "countdown":
            return S["remaining_ms"]
        return S["elapsed_ms"]

    def _update_display():
        active_ms = _get_active_ms()
        total_secs = max(0, active_ms // 1000)
        h = str(total_secs // 3600).zfill(2)
        m = str((total_secs % 3600) // 60).zfill(2)
        s = str(total_secs % 60).zfill(2)

        now = datetime.now()
        ch = str(now.hour).zfill(2)
        cm = str(now.minute).zfill(2)
        cs = str(now.second).zfill(2)

        if S["swapped"]:
            drefs["hour"].value = ch
            drefs["min"].value = cm
            drefs["sec"].value = cs
            clock_refs["text"].value = f"{h}:{m}:{s}"
        else:
            drefs["hour"].value = h
            drefs["min"].value = m
            drefs["sec"].value = s
            clock_refs["text"].value = f"{ch}:{cm}:{cs}"

        is_cd = S["mode"] == "countdown"
        drefs["badge"].bgcolor = "#fef3c7" if is_cd else "#27272a"
        drefs["badge"].border = border_all(1, "#fbbf24" if is_cd else "#3f3f46")
        drefs["badge_text"].value = (
            "\u23f1\ufe0f Modo Cuenta Regresiva" if is_cd else "\u23f1\ufe0f Modo Cron\u00f3metro"
        )
        drefs["badge_text"].color = "#d97706" if is_cd else "#a1a1aa"

    def _update_buttons():
        is_running = S["status"] == "running"
        is_not_running = not is_running

        btn_refs["start"].opacity = 0.5 if is_running else 1.0
        btn_refs["start"].on_click = None if is_running else (lambda _: _handle_start())
        btn_refs["start"].border = (
            border_all(2, ft.Colors.with_opacity(0.5, ft.Colors.GREEN_400))
            if is_running
            else border_all(1, ft.Colors.with_opacity(0.05, ft.Colors.WHITE))
        )

        btn_refs["pause"].opacity = 0.4 if is_not_running else 1.0
        btn_refs["pause"].on_click = None if is_not_running else (lambda _: _handle_pause())

        btn_refs["start"].update()
        btn_refs["pause"].update()

    def _update_laps_panel():
        is_running = S["status"] == "running"
        laps = S["laps"]
        show = S["show_laps"]

        laps_panel.visible = show

        lap_refs["header_title"].value = f"Historial de Vueltas / Laps ({len(laps)})"

        lap_refs["header_right"].controls.clear()
        if is_running:
            lap_refs["header_right"].controls.append(lap_refs["add_lap_button"])
        if laps:
            lap_refs["header_right"].controls.append(lap_refs["clear_button"])

        lap_refs["list"].controls.clear()
        if not laps:
            msg = (
                "Haz clic en \"+ Registrar Vuelta\" durante la carrera."
                if is_running
                else "Inicia el cron\u00f3metro para marcar tiempos."
            )
            lap_refs["list"].controls.append(
                ft.Text(
                    f"No hay vueltas registradas. {msg}",
                    size=12, color="#737373", italic=True,
                    text_align=ft.TextAlign.CENTER,
                )
            )
        else:
            font = FONT_MAP.get(S["font_style"], "Architects Daughter")
            for lap in reversed(laps):
                lap_refs["list"].controls.append(
                    ft.Container(
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    f"Vuelta #{lap['id']}",
                                    size=12, color="#a1a1a6",
                                    font_family="monospace",
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    lap["formattedTime"],
                                    size=20, weight=ft.FontWeight.BOLD,
                                    color="#f3f4f6", font_family=font,
                                ),
                            ],
                        ),
                        bgcolor="#282f39", border_radius=12,
                        padding=ft.Padding(left=12, top=8, right=12, bottom=8),
                    )
                )

        laps_panel.update()
        if show:
            page.update()

    # ── Action handlers ────────────────────────────────────────────
    def _handle_start():
        if S["status"] == "running":
            return
        if S["sound_enabled"]:
            play_beep("start")
        if S["mode"] == "countdown" and S["remaining_ms"] <= 0 and S["target_ms"] > 0:
            S["accumulated_ms"] = 0
            S["remaining_ms"] = S["target_ms"]
        S["start_time"] = time.perf_counter()
        S["status"] = "running"
        _update_buttons()
        page.update()

    def _handle_pause():
        if S["status"] != "running":
            return
        if S["sound_enabled"]:
            play_beep("pause")
        now = time.perf_counter()
        S["accumulated_ms"] += (now - S["start_time"]) * 1000
        S["start_time"] = 0
        S["status"] = "paused"
        _update_display()
        _update_buttons()
        page.update()

    def _handle_reset():
        if S["sound_enabled"]:
            play_beep("reset")
        S["start_time"] = 0
        S["accumulated_ms"] = 0
        S["elapsed_ms"] = 0
        S["target_ms"] = 0
        S["remaining_ms"] = 0
        S["mode"] = "stopwatch"
        S["status"] = "idle"
        _update_display()
        _update_buttons()
        page.update()

    def _handle_add_lap():
        active_ms = _get_active_ms()
        if active_ms == 0:
            return
        if S["sound_enabled"]:
            play_beep("tick")
        total_secs = active_ms // 1000
        h = str(total_secs // 3600).zfill(2)
        m = str((total_secs % 3600) // 60).zfill(2)
        s = str(total_secs % 60).zfill(2)
        fmt = f"{h}:{m}:{s}"
        S["laps"].append({
            "id": len(S["laps"]) + 1,
            "time": active_ms,
            "formattedTime": fmt,
        })
        if not S["show_laps"]:
            S["show_laps"] = True
        _update_laps_panel()

    def _handle_clear_laps():
        S["laps"] = []
        _update_laps_panel()

    def _handle_font_change(key):
        S["font_style"] = key
        font = FONT_MAP[key]
        drefs["hour"].font_family = font
        drefs["min"].font_family = font
        drefs["sec"].font_family = font
        drefs["badge_text"].font_family = font
        clock_refs["text"].font_family = font
        drefs["container"].update()
        clock_refs["container"].update()
        for k, btn in settings_refs["font_buttons"].items():
            is_active = k == key
            btn.bgcolor = "#3b434f" if is_active else ft.Colors.TRANSPARENT
            btn.content.weight = ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL
            btn.content.color = ft.Colors.WHITE if is_active else "#d1d5db"
            btn.update()
        page.update()

    def _handle_sound_toggle():
        S["sound_enabled"] = not S["sound_enabled"]
        return S["sound_enabled"]

    def _handle_laps_toggle():
        S["show_laps"] = not S["show_laps"]
        _update_laps_panel()

    def _toggle_fullscreen():
        page.window.full_screen = not page.window.full_screen
        page.update()

    # ── Keyboard handler ───────────────────────────────────────────
    def _on_keyboard(e: ft.KeyboardEvent):
        key = e.key.lower()
        if key == " " or key == "space":
            if S["status"] == "running":
                _handle_pause()
            else:
                _handle_start()
        elif key == "r":
            _handle_reset()
        elif key == "l" and S["status"] == "running":
            _handle_add_lap()
        elif key == "m":
            _open_modal()

    page.on_keyboard_event = _on_keyboard

    # ── Responsive box sizing ──────────────────────────────────────
    def _update_box_sizes():
        win_w = page.window.width
        available = win_w - 32
        box_size = min(max(90, (available - 24) // 3), 500)
        text_size = int(box_size * 0.55)
        for box in drefs["boxes"]:
            box.width = box_size
            box.height = box_size
        for txt in drefs["texts"]:
            txt.size = text_size

    def _on_resize(e):
        _update_box_sizes()
        page.update()

    page.on_resize = _on_resize

    # ── Initial render ─────────────────────────────────────────────
    _update_box_sizes()
    _update_display()
    _update_buttons()
    _update_laps_panel()
    page.update()

if __name__ == "__main__":
    ft.run(main)
