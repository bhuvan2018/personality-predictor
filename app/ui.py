import flet as ft
import os
from app.model import predict_personality

# Enhanced color palette with hex codes
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

# Fix image paths for mobile compatibility
def get_asset_path(image_name):
    # This creates a path that works in both development and when packaged for mobile
    base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "assets")
    
    # For direct use in mobile app
    if os.path.exists(os.path.join("app", "assets", image_name)):
        return os.path.join("app", "assets", image_name)
    
    # For development environment
    elif os.path.exists(os.path.join(base_path, image_name)):
        return os.path.join(base_path, image_name)
    
    # Fallback
    else:
        return os.path.join("assets", image_name)

theme_images = {
    "Abstract": get_asset_path("abstract.png"),
    "Nature": get_asset_path("nature.png"),
    "People": get_asset_path("people.png"),
    "Tech": get_asset_path("tech.png")
}

def main_view(page: ft.Page):
    # Modern app setup
    page.title = "Visual Personality Predictor"
    page.padding = 25
    page.spacing = 20
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    
    # Responsive window sizing
    page.window_width = 500
    page.window_height = 750
    page.window_min_width = 350
    page.window_min_height = 600
    
    # State variables
    selected_color = ""
    selected_theme = ""
    prediction_complete = False

    # UI elements with enhanced styling
    title = ft.Text(
        "Visual Personality Predictor",
        size=28,
        color="#f5f5f5",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER
    )
    
    subtitle = ft.Text(
        "Choose your preferences to discover your personality type",
        size=16,
        color="#aaaaaa",
        italic=True,
        text_align=ft.TextAlign.CENTER
    )
    
    selections_text = ft.Text(
        "Make your selections below",
        size=16,
        weight=ft.FontWeight.W_600,
        color="#dddddd",
    )
    
    prediction_text = ft.Text(
        "",
        size=18,
        color="#00e676",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
        visible=False
    )
    
    color_section_title = ft.Text(
        "Select Your Favorite Color",
        size=20,
        weight=ft.FontWeight.W_600,
        color="#f5f5f5"
    )
    
    theme_section_title = ft.Text(
        "Select Your Favorite Theme",
        size=20,
        weight=ft.FontWeight.W_600,
        color="#f5f5f5"
    )

    # Create a stylish dialog
    dialog = ft.AlertDialog(
        modal=True,
    )
    page.dialog = dialog
    
    # Store controls for highlighting
    color_buttons = []
    theme_buttons = []

    def update_selection_display():
        color_status = f"• Color: {selected_color}" if selected_color else "• Color: Not selected"
        theme_status = f"• Theme: {selected_theme}" if selected_theme else "• Theme: Not selected"
        selections_text.value = f"{color_status}\n{theme_status}"
        
        # Show prediction text if both selections made
        prediction_text.visible = selected_color and selected_theme and prediction_complete
        page.update()

    def clear_highlights(control_type=None):
        if control_type != "color":
            for btn in color_buttons:
                btn.style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=20),
                    side=ft.BorderSide(1, "#555555")
                )
                
        if control_type != "theme":
            for img in theme_buttons:
                img.content.border = ft.border.all(1, "#555555")
                img.content.border_radius = ft.border_radius.all(15)
                
        page.update()

    def handle_color_click(e):
        nonlocal selected_color, prediction_complete
        if selected_color == e.control.data:
            # Deselect if clicking the same color
            selected_color = ""
            clear_highlights("color")
        else:
            selected_color = e.control.data
            clear_highlights("color")
            e.control.style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(3, ft.colors.WHITE)
            )
        
        prediction_complete = False
        update_selection_display()

    def handle_theme_click(e):
        nonlocal selected_theme, prediction_complete
        if selected_theme == e.control.data:
            # Deselect if clicking the same theme
            selected_theme = ""
            clear_highlights("theme")
        else:
            selected_theme = e.control.data
            clear_highlights("theme")
            e.control.content.border = ft.border.all(3, "#00e5ff")
            e.control.content.border_radius = ft.border_radius.all(15)
            
        prediction_complete = False
        update_selection_display()
        
        # Automatically predict when both selections are made
        if selected_color and selected_theme:
            show_prediction()

    def show_prediction():
        nonlocal prediction_complete
        prediction = predict_personality(selected_color, selected_theme)
        prediction_text.value = f"Your personality: {prediction}"
        prediction_complete = True
        prediction_text.visible = True
        
        # Create and show an animated dialog
        dialog.title = ft.Text("Personality Analysis", weight=ft.FontWeight.BOLD, size=20)
        
        dialog.content = ft.Column([
            ft.Container(
                content=ft.Icon(ft.icons.PSYCHOLOGY_ALT, size=50, color="#00e5ff"),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=10, bottom=20)
            ),
            ft.Text(
                f"Based on your preferences:",
                size=16,
                color="#dddddd"
            ),
            ft.Container(
                content=ft.Text(
                    f"Color: {selected_color}",
                    size=16,
                    color=color_map[selected_color]
                ),
                margin=ft.margin.only(top=5)
            ),
            ft.Container(
                content=ft.Text(f"Theme: {selected_theme}", size=16),
                margin=ft.margin.only(bottom=10)
            ),
            ft.Container(
                content=ft.Text(
                    f"Your personality type is:",
                    size=16,
                    color="#dddddd",
                    weight=ft.FontWeight.W_500
                ),
                margin=ft.margin.only(top=10, bottom=5)
            ),
            ft.Container(
                content=ft.Text(
                    prediction,
                    size=22,
                    color="#00e676",
                    weight=ft.FontWeight.BOLD
                ),
                margin=ft.margin.only(bottom=20)
            )
        ], spacing=5, alignment=ft.MainAxisAlignment.CENTER)
        
        dialog.actions = [
            ft.TextButton(
                "Try New Combination",
                on_click=lambda e: setattr(dialog, 'open', False)
            )
        ]
        
        dialog.open = True
        page.update()

    def reset_all(e):
        nonlocal selected_color, selected_theme, prediction_complete
        selected_color = ""
        selected_theme = ""
        prediction_complete = False
        prediction_text.visible = False
        clear_highlights()
        update_selection_display()

    # Create color buttons with enhanced styling
    color_grid = ft.GridView(
        runs_count=2,
        max_extent=150,
        spacing=10,
        run_spacing=10,
        expand=True
    )
    
    color_buttons = []
    for color in colors:
        btn = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.icons.CIRCLE, color=color_map[color], size=20),
                    ft.Text(
                        color,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="black" if color == "Yellow" else "white"
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=8
            ),
            bgcolor=color_map[color] + "99",  # Semi-transparent
            data=color,
            on_click=handle_color_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20),
                side=ft.BorderSide(1, "#555555"),
            ),
            height=60,
            width=140
        )
        color_buttons.append(btn)
        color_grid.controls.append(btn)

    # Create theme cards with enhanced styling and fallback for missing images
    theme_grid = ft.GridView(
        runs_count=2,
        max_extent=160,
        spacing=15,
        run_spacing=15,
        expand=True
    )
    
    theme_buttons = []
    for theme in themes:
        # Create a failsafe theme representation
        theme_content = ft.Column(
            [
                ft.Container(
                    content=create_theme_visual(theme),
                    padding=5
                ),
                ft.Text(
                    theme,
                    size=16,
                    weight=ft.FontWeight.W_500,
                    color="#f5f5f5",
                    text_align=ft.TextAlign.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        )
        
        theme_card = ft.GestureDetector(
            on_tap=handle_theme_click,
            data=theme,
            content=ft.Container(
                content=theme_content,
                border=ft.border.all(1, "#555555"),
                border_radius=15,
                padding=10,
                alignment=ft.alignment.center
            )
        )
        theme_buttons.append(theme_card)
        theme_grid.controls.append(theme_card)

    # Reset button with proper styling
    reset_button = ft.ElevatedButton(
        "Reset Selections",
        icon=ft.icons.REFRESH_ROUNDED,
        on_click=reset_all,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        bgcolor="#555555",
        color="#ffffff"
    )

    # Create responsive layout
    page.add(
        # App header
        ft.Container(
            content=ft.Column(
                [title, subtitle],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            margin=ft.margin.only(bottom=10),
            padding=10
        ),
        
        # Color selection section
        ft.Container(
            content=ft.Column(
                [
                    color_section_title,
                    ft.Container(
                        content=color_grid,
                        margin=ft.margin.only(top=10, bottom=15),
                        padding=10
                    )
                ],
                spacing=5
            ),
            border_radius=10,
            bgcolor="#1e1e1e",
            padding=15,
            margin=ft.margin.only(bottom=20)
        ),
        
        # Theme selection section
        ft.Container(
            content=ft.Column(
                [
                    theme_section_title,
                    ft.Container(
                        content=theme_grid,
                        margin=ft.margin.only(top=10, bottom=15),
                        padding=10
                    )
                ],
                spacing=5
            ),
            border_radius=10,
            bgcolor="#1e1e1e",
            padding=15,
            margin=ft.margin.only(bottom=20)
        ),
        
        # Selections and prediction area
        ft.Container(
            content=ft.Column(
                [
                    selections_text,
                    prediction_text
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            border_radius=10,
            bgcolor="#1e1e1e",
            padding=20,
            margin=ft.margin.only(bottom=20)
        ),
        
        # Bottom action buttons
        ft.Container(
            content=ft.Row(
                [reset_button],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            margin=ft.margin.only(bottom=20)
        )
    )
    
    # Initial setup
    update_selection_display()

def create_theme_visual(theme):
    """Create a visual representation for a theme with a fallback if image doesn't load"""
    try:
        # Try to use the image
        return ft.Image(
            src=theme_images[theme],
            width=120,
            height=120,
            fit=ft.ImageFit.COVER,
            border_radius=ft.border_radius.all(10),
            error_content=create_theme_placeholder(theme)
        )
    except Exception:
        # Fallback to placeholder
        return create_theme_placeholder(theme)

def create_theme_placeholder(theme):
    """Create a colored placeholder for theme with text"""
    theme_colors = {
        "Abstract": "#7e57c2",  # Purple
        "Nature": "#4caf50",    # Green
        "People": "#ff9800",    # Orange
        "Tech": "#2196f3"       # Blue
    }
    
    return ft.Container(
        content=ft.Column(
            [
                ft.Icon(
                    get_theme_icon(theme),
                    size=50,
                    color="white"
                ),
                ft.Text(
                    theme,
                    color="white",
                    weight=ft.FontWeight.BOLD,
                    size=16
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        ),
        width=120,
        height=120,
        bgcolor=theme_colors.get(theme, "#757575"),
        border_radius=10,
        alignment=ft.alignment.center
    )

def get_theme_icon(theme):
    """Get an appropriate icon for each theme"""
    theme_icons = {
        "Abstract": ft.icons.PALETTE,
        "Nature": ft.icons.FOREST,
        "People": ft.icons.PEOPLE,
        "Tech": ft.icons.COMPUTER
    }
    return theme_icons.get(theme, ft.icons.IMAGE)

def main():
    ft.app(target=main_view)