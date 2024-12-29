from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class TelaProvaVida(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Título
        titulo = Label(
            text="Prova de Vida",
            font_size='24sp',
            color=(0, 0, 0, 1),  # Preto
            bold=True
        )
        layout.add_widget(titulo)

        # Mensagem de instrução
        instrucao = Label(
            text="Apresente seu rosto para realizar a prova de vida.",
            font_size='18sp',
            color=(0.3, 0.3, 0.3, 1),  # Cinza escuro
        )
        layout.add_widget(instrucao)

        # Botão "Voltar"
        botao_voltar = Button(
            text="Voltar",
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5},
            background_color=(0.1, 0.5, 0.8, 1),  # Azul claro
            color=(1, 1, 1, 1),  # Branco
        )
        botao_voltar.bind(on_release=self.voltar_tela)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

    def _atualizar_fundo(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def voltar_tela(self, instance):
        self.manager.current = 'tela_administracao'
