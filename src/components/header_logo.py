"""Logo Recoverfit con emblema RF metálico y texto de marca."""

import flet as ft
import flet.canvas as cv


def create_header_logo() -> ft.Control:
    SILVER_METAL_COLORS = [
        "#FFFFFFFF",
        "#FFC0C0C0",
        "#FFE8E8E8",
        "#FF8A8A8A",
        "#FFDFDFDF",
    ]
    SILVER_METAL_STOPS = [0.0, 0.35, 0.50, 0.70, 1.0]

    SILVER_DARK_COLORS = [
        "#FF737373",
        "#FFD4D4D4",
        "#FFA3A3A3",
    ]
    SILVER_DARK_STOPS = [0.0, 0.50, 1.0]

    def _make_path(points, gradient_colors, gradient_stops, gradient_begin, gradient_end):
        elements = []
        for i, (x, y) in enumerate(points):
            if i == 0:
                elements.append(cv.Path.MoveTo(x, y))
            else:
                elements.append(cv.Path.LineTo(x, y))
        elements.append(cv.Path.Close())

        return cv.Path(
            elements=elements,
            paint=ft.Paint(
                gradient=ft.PaintLinearGradient(
                    begin=gradient_begin,
                    end=gradient_end,
                    colors=gradient_colors,
                    color_stops=gradient_stops,
                ),
                style=ft.PaintingStyle.FILL,
            ),
        )

    metal_begin = ft.alignment.Alignment(-1, -1)
    metal_end = ft.alignment.Alignment(1, 1)
    dark_begin = ft.alignment.Alignment(-1, 1)
    dark_end = ft.alignment.Alignment(1, -1)

    silver_metal = (SILVER_METAL_COLORS, SILVER_METAL_STOPS, metal_begin, metal_end)
    silver_dark = (SILVER_DARK_COLORS, SILVER_DARK_STOPS, dark_begin, dark_end)

    left_wing_1 = [(20, 20), (92, 20), (78, 45), (35, 45)]
    left_wing_2 = [(35, 45), (85, 45), (75, 62), (50, 62)]
    left_wing_3 = [(20, 20), (55, 62), (70, 62), (40, 20)]
    right_wing_1 = [(180, 20), (108, 20), (122, 45), (165, 45)]
    right_wing_2 = [(165, 45), (115, 45), (125, 62), (150, 62)]
    right_wing_3 = [(180, 20), (145, 62), (130, 62), (160, 20)]
    center_1 = [(75, 65), (125, 65), (100, 110)]
    center_2 = [(85, 68), (115, 68), (100, 98)]

    canvas = cv.Canvas(
        width=200,
        height=120,
        shapes=[
            _make_path(left_wing_1, *silver_metal),
            _make_path(left_wing_2, *silver_dark),
            _make_path(left_wing_3, *silver_metal),
            _make_path(right_wing_1, *silver_metal),
            _make_path(right_wing_2, *silver_dark),
            _make_path(right_wing_3, *silver_metal),
            _make_path(center_1, *silver_metal),
            _make_path(center_2, *silver_dark),
        ],
    )

    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2,
        controls=[
            ft.Container(
                content=canvas,
                width=96,
                height=64,
                alignment=ft.alignment.Alignment(0, 0),
                margin=ft.Margin(bottom=12),
            ),
            ft.Text(
                "RECOVERFIT",
                font_family="Montserrat",
                size=24,
                weight=ft.FontWeight.W_800,
                style=ft.TextStyle(letter_spacing=6),
                color=ft.Colors.WHITE,
                text_align=ft.TextAlign.CENTER,
                no_wrap=True,
            ),
            ft.Container(height=4),
            ft.Text(
                "RECUPERACI\u00d3N Y ENTRENAMIENTO",
                font_family="Montserrat",
                size=10,
                weight=ft.FontWeight.W_600,
                style=ft.TextStyle(letter_spacing=3),
                color="#71717a",
                text_align=ft.TextAlign.CENTER,
                no_wrap=True,
            ),
        ],
    )
