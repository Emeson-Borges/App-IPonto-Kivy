from kivymd.theming import ThemeManager
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp




class AppTheme:
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Blue"  # Paleta principal
    theme_cls.accent_palette = "Amber"  # Paleta de destaque
    theme_cls.theme_style = "Light"  # Estilo: 'Light' ou 'Dark'
    theme_cls.primary_hue = "500"  # Intensidade da cor

    # Cores personalizadas
    custom_colors = {
        "primary": [0.1, 0.6, 0.8, 1],  # Azul customizado
        "accent": [1, 0.8, 0.2, 1],  # Âmbar customizado
        "background": [1, 1, 1, 1],  # Branco
        "error": [0.9, 0.3, 0.3, 1],  # Vermelho para erros
    }

    # Botões arredondados personalizados
    @staticmethod
    def rounded_button(text, on_release, color=None, size_hint=(1, None), height=dp(48)):
        return MDRaisedButton(
            text=text,
            size_hint=size_hint,
            height=height,
            md_bg_color=color or AppTheme.custom_colors["primary"],
            text_color=[1, 1, 1, 1],
            radius=[24],  # Torna o botão arredondado
            on_release=on_release,
        )

    # Campos de texto personalizados
    @staticmethod
    def text_field(hint_text, password=False):
        return MDTextField(
            hint_text=hint_text,
            size_hint=(1, None),
            height=dp(48),
            mode="rectangle",
            password=password,
        )
