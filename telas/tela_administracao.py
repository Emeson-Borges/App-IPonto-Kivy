from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class TelaAdministracao(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="Administração do Sistema", font_size='24sp')
        layout.add_widget(titulo)

        # Botão para cadastro
        botao_cadastro = Button(text="Cadastrar Funcionário", size_hint=(1, 0.2), on_release=self.ir_para_cadastro)
        layout.add_widget(botao_cadastro)

        # Botão para voltar
        botao_voltar = Button(text="Voltar", size_hint=(1, 0.2), on_release=self.voltar_tela)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

    def ir_para_cadastro(self, instancia):
        self.manager.current = 'tela_cadastro'

    def voltar_tela(self, instancia):
        self.manager.current = 'tela_inicial'
