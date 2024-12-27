from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="[b]Cadastro de Funcionário[/b]", font_size='24sp', markup=True)
        layout.add_widget(titulo)

        # Campos de entrada
        self.campo_nome = TextInput(hint_text="Nome", multiline=False, size_hint=(1, 0.1))
        self.campo_cpf = TextInput(hint_text="CPF", multiline=False, size_hint=(1, 0.1))
        self.campo_matricula = TextInput(hint_text="Matrícula", multiline=False, size_hint=(1, 0.1))

        layout.add_widget(self.campo_nome)
        layout.add_widget(self.campo_cpf)
        layout.add_widget(self.campo_matricula)

        # Botão para salvar
        botao_salvar = Button(text="Salvar Cadastro", size_hint=(1, 0.2), on_release=self.salvar_cadastro)
        layout.add_widget(botao_salvar)

        # Botão para voltar
        botao_voltar = Button(text="Voltar", size_hint=(1, 0.2), on_release=self.voltar_tela)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

    def salvar_cadastro(self, instancia):
        nome = self.campo_nome.text
        cpf = self.campo_cpf.text
        matricula = self.campo_matricula.text

        # Lógica para salvar no banco de dados (substituir pelo código do banco)
        print(f"Funcionário cadastrado: Nome={nome}, CPF={cpf}, Matrícula={matricula}")

    def voltar_tela(self, instancia):
        self.manager.current = 'tela_administracao'
