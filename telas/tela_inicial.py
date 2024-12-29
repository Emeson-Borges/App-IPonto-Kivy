from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button
import datetime

# Configurar tamanho de janela para simular um app menor
Window.size = (360, 640)  # Dimensões padrão para aplicativos móveis


class BotaoArredondado(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Remove o fundo padrão
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 1)  # Define a cor de fundo (azul claro)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])  # Define o raio do botão
        self.bind(size=self.atualizar_canvas, pos=self.atualizar_canvas)

    def atualizar_canvas(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configurar o fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=[20, 20, 20, 20])

        # Adicionar a logo
        self.logo = Image(
            source='assets/rh247_azul.png',
            size_hint=(1, 0.4),
            allow_stretch=True,
            keep_ratio=True
        )
        self.layout.add_widget(self.logo)

        # Saudação dinâmica, hora e data agrupados em um BoxLayout
        info_layout = BoxLayout(orientation='vertical', spacing=5, size_hint=(1, 0.2))

        # Saudação dinâmica
        self.saudacao = Label(
            text="",
            font_size='22sp',
            bold=True,
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1)  # Preto
        )
        info_layout.add_widget(self.saudacao)

        # Hora dinâmica
        self.horario = Label(
            text="",
            font_size='36sp',
            bold=True,
            halign="center",
            valign="middle",
            color=(0.1, 0.5, 0.8, 1)  # Azul claro
        )
        info_layout.add_widget(self.horario)

        # Data dinâmica
        self.data = Label(
            text="",
            font_size='18sp',
            halign="center",
            valign="middle",
            color=(0.4, 0.4, 0.4, 1)  # Cinza
        )
        info_layout.add_widget(self.data)

        self.layout.add_widget(info_layout)

        # Botão "Registrar Ponto"
        self.botao_continuar = BotaoArredondado(
            text="Registrar Ponto",
            size_hint=(1, 0.1),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            background_color=(0.1, 0.5, 0.8, 1),  # Azul claro
            color=(1, 1, 1, 1),  # Branco
            background_normal='',  # Remove o estilo padrão
            background_down='',
        )
        self.botao_continuar.bind(on_release=self.ir_para_registro_ponto)
        self.layout.add_widget(self.botao_continuar)

        # Botão "Administrativo"
        self.botao_administrativo = BotaoArredondado(
            text="Administrativo",
            size_hint=(1, 0.1),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            background_color=(0.1, 0.5, 0.8, 1),  # Azul claro
            color=(1, 1, 1, 1),  # Branco
            background_normal='',  # Remove o estilo padrão
            background_down='',
        )
        self.botao_administrativo.bind(on_release=self.ir_para_administrativo)
        self.layout.add_widget(self.botao_administrativo)

        # Adicionar layout principal à tela
        self.add_widget(self.layout)

        # Atualizar hora, data e saudação dinamicamente
        Clock.schedule_interval(self.atualizar_tempo, 1)

    def _atualizar_fundo(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def atualizar_tempo(self, *args):
        agora = datetime.datetime.now()

        # Atualizar saudação
        hora = agora.hour
        if hora < 12:
            self.saudacao.text = "Bom dia"
        elif 12 <= hora < 18:
            self.saudacao.text = "Boa tarde"
        else:
            self.saudacao.text = "Boa noite"

        # Atualizar horário e data
        self.horario.text = agora.strftime("%H:%M:%S")
        self.data.text = agora.strftime("%d de %B de %Y")

    def ir_para_registro_ponto(self, instancia):
        self.manager.current = 'tela_registro_ponto'

    # def ir_para_administrativo(self, instancia):
    #     self.manager.current = 'tela_administracao'


    def ir_para_administrativo(self, instancia):
        """Navega para a tela de login ao clicar em 'Administrativo'."""
        self.manager.current = 'tela_login'

