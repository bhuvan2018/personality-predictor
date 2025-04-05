import flet as ft
from app.model import predict_personality

colors = ["Red", "Blue", "Yellow", "Black", "Green", "Purple", "Orange", "Grey"]
themes = ["Abstract", "Nature", "People", "Tech"]

color_map = {
    "Red": "#ff4d4d",
    "Blue": "#4d79ff",
    "Yellow": "#ffff66",
    "Black": "#333333",
    "Green": "#66cc66",
    "Purple": "#cc66ff",
    "Orange": "#ff9933",
    "Grey": "#999999"
}

theme_images = {
    "Abstract": "app/assets/abstract.png",
    "Nature": "app/assets/nature.png",
    "People": "app/assets/people.png",
    "Tech": "app/assets/tech.png"
}

def main_view(page: ft.Page):
    page.title = "Visual Personality Predictor"
    page.window_width = 500
    page.window_height = 700
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK

    selected_color = ""
    selected_theme = ""

    prediction_text = ft.Text("", size=16, color="green", weight=ft.FontWeight.BOLD)
    selections_text = ft.Text("Current Selections:\n", size=14, weight=ft.FontWeight.W_600)

    dialog = ft.AlertDialog(modal=True)
    page.dialog = dialog

    # Store controls for highlighting
    color_buttons = []
    theme_buttons = []

    def update_selection_display():
        selections_text.value = f"Current Selections:\n{selected_color}\n{selected_theme}"
        page.update()

    def clear_highlights():
        for btn in color_buttons:
            btn.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20), side=None)
        for img in theme_buttons:
            img.content.border = None

    def handle_color_click(e):
        nonlocal selected_color
        selected_color = e.control.data
        clear_highlights()
        e.control.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20),
                                         side=ft.BorderSide(2, ft.colors.WHITE))
        update_selection_display()

    def handle_theme_click(e):
        nonlocal selected_theme
        selected_theme = e.control.data
        clear_highlights()
        e.control.content.border = ft.border.all(3, ft.colors.CYAN)
        update_selection_display()

        if selected_color and selected_theme:
            prediction = predict_personality(selected_color, selected_theme)
            prediction_text.value = f"Prediction: {prediction}"
            dialog.title = ft.Text("Personality Prediction", weight=ft.FontWeight.BOLD, size=18)
            dialog.content = ft.Text(f"Your personality is: {prediction}", size=16)
            dialog.actions = [ft.TextButton("OK", on_click=lambda e: setattr(dialog, 'open', False))]
            dialog.open = True
            page.update()

    def reset_all(e):
        nonlocal selected_color, selected_theme
        selected_color = ""
        selected_theme = ""
        prediction_text.value = ""
        selections_text.value = "Current Selections:\n"
        clear_highlights()
        page.update()

    # Buttons
    color_buttons = [
        ft.ElevatedButton(
            text=color,
            bgcolor=color_map[color],
            color="black" if color == "Yellow" else "white",
            data=color,
            on_click=handle_color_click,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20))
        ) for color in colors
    ]

    # Image options
    theme_buttons = [
        ft.GestureDetector(
            on_tap=handle_theme_click,
            data=theme,
            content=ft.Image(
                src=theme_images[theme],
                width=100,
                height=100,
                fit=ft.ImageFit.COVER,
                border_radius=10
            )
        ) for theme in themes
    ]

    # Layout
    page.add(
        ft.Text("Select Your Favorite Color", size=18, weight=ft.FontWeight.W_600),
        ft.ResponsiveRow(controls=color_buttons, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20),
        ft.Text("Select Your Favorite Theme", size=18, weight=ft.FontWeight.W_600),
        ft.Row(theme_buttons, spacing=10, alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20),
        selections_text,
        prediction_text,
        ft.ElevatedButton("Try Again", icon=ft.icons.REFRESH, on_click=reset_all, bgcolor="grey")
    )

def main():
    ft.app(target=main_view)