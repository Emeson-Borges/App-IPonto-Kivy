from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from layout.rounded_button import BotaoArredondado


# Classe para a tela de administração
class TelaAdministracao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[0])
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Título
        titulo = Label(
            text="Administração do Sistema",
            font_size='24sp',
            color=(0, 0, 0, 1),  # Preto
            bold=True
        )
        self.layout.add_widget(titulo)

        # Botão "Cadastrar Funcionário"
        botao_cadastro = BotaoArredondado(
            text="Cadastrar Funcionário",
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            color=(1, 1, 1, 1),  # Texto branco
        )
        botao_cadastro.bind(on_release=self.ir_para_cadastro)
        self.layout.add_widget(botao_cadastro)

        # Botão "Prova de Vida"
        botao_prova_vida = BotaoArredondado(
            text="Prova de Vida",
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            color=(1, 1, 1, 1),  # Texto branco
        )
        botao_prova_vida.bind(on_release=self.ir_para_prova_vida)
        self.layout.add_widget(botao_prova_vida)

        # Botão "Sincronizar Pontos"
        botao_sincronizar = BotaoArredondado(
            text="Sincronizar Pontos",
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            color=(1, 1, 1, 1),  # Texto branco
        )
        botao_sincronizar.bind(on_release=self.ir_para_sincronizar)
        self.layout.add_widget(botao_sincronizar)

        # Botão "Voltar"
        botao_voltar = BotaoArredondado(
            text="Voltar",
            size_hint=(0.8, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            color=(1, 1, 1, 1),  # Texto branco
        )
        botao_voltar.bind(on_release=self.voltar_tela)
        self.layout.add_widget(botao_voltar)

        self.add_widget(self.layout)

    def _atualizar_fundo(self, *args):
        """Atualiza o fundo da tela ao redimensionar."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def ir_para_cadastro(self, instancia):
        """Navega para a tela de cadastro."""
        self.manager.current = 'tela_cadastro'

    def ir_para_prova_vida(self, instancia):
        """Navega para a tela de prova de vida."""
        self.manager.current = 'tela_prova_vida'

    def ir_para_sincronizar(self, instancia):
        """Navega para a tela de sincronização."""
        self.manager.current = 'tela_sincronizar'

    def voltar_tela(self, instancia):
        """Volta para a tela inicial."""
        self.manager.current = 'tela_inicial'
