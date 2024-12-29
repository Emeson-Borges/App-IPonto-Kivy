from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class BotaoArredondado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Remover o fundo padrão do botão
        with self.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Azul claro no formato RGBA
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[25])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
