from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from utils.functions import validar_e_formatar_cpf  # Importar a função de validação



class TelaLogin(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=[20, 20, 20, 20])

        # Adicionar logo
        self.logo = Image(
            source="assets/rh247_azul.png", size_hint=(1, 0.80), allow_stretch=True
        )
        self.layout.add_widget(self.logo)

        # Campo de CPF
        cpf_label = Label(
            text="CPF",
            font_size="16sp",
            size_hint=(1, 0.08),
            color=(0.3, 0.3, 0.3, 1),
            halign="left",
            valign="middle",
        )
        cpf_label.bind(size=cpf_label.setter("text_size"))
        self.layout.add_widget(cpf_label)

        # Campo CPF
        self.campo_cpf = TextInput(
            hint_text="Digite seu CPF",
            multiline=False,
            size_hint=(1, 0.2),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10],
            input_filter="int"  # Permitir apenas números
        )
        self.campo_cpf.bind(on_text_validate=self.validar_campo_cpf)
        self.layout.add_widget(self.campo_cpf)


        # Campo de Senha
        senha_label = Label(
            text="Senha",
            font_size="16sp",
            size_hint=(1, 0.08),
            color=(0.3, 0.3, 0.3, 1),
            halign="left",
            valign="middle",
        )
        senha_label.bind(size=senha_label.setter("text_size"))
        self.layout.add_widget(senha_label)

        self.campo_senha = TextInput(
            hint_text="Digite sua senha",
            password=True,
            multiline=False,
            size_hint=(1, 0.2),
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            padding=[10, 10, 10, 10],
        )
        self.layout.add_widget(self.campo_senha)

        # Botão "Acessar"
        botao_acessar = Button(
            text="Acessar",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_acessar.bind(on_release=self.fazer_login)
        self.layout.add_widget(botao_acessar)

        # Botão "Cancelar"
        botao_cancelar = Button(
            text="Cancelar",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.9, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_cancelar.bind(on_release=self.cancelar_login)
        self.layout.add_widget(botao_cancelar)

        # # Checkbox "Manter logado"
        # checkbox_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.1))
        # self.checkbox = CheckBox(size_hint=(0.1, 1))
        # checkbox_label = Label(
        #     text="Me manter logado.",
        #     font_size="14sp",
        #     color=(0.3, 0.3, 0.3, 1),
        # )
        # checkbox_layout.add_widget(self.checkbox)
        # checkbox_layout.add_widget(checkbox_label)
        # layout.add_widget(checkbox_layout)

        # Termos e políticas
        termos_label = Label(
            text="Ao se logar, você concorda com nossos\n[b]termos de uso[/b] e [b]política de privacidade[/b].",
            font_size="12sp",
            halign="center",
            markup=True,
            color=(0.4, 0.4, 0.4, 1),
        )
        termos_label.bind(size=termos_label.setter("text_size"))
        self.layout.add_widget(termos_label)

        # Link para recuperação de senha
        link_recuperacao = Button(
            text="Primeiro Acesso / Recuperação de Senha",
            size_hint=(1, 0.1),
            font_size="14sp",
            color=(0.1, 0.6, 0.8, 1),
            background_normal="",
            background_down="",
            background_color=(1, 1, 1, 0),
        )
        link_recuperacao.bind(on_release=self.recuperar_senha)
        self.layout.add_widget(link_recuperacao)

        self.add_widget(self.layout)

    def _atualizar_fundo(self, *args):
        """Atualiza o fundo da tela ao redimensionar."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def fazer_login(self, instancia):
        """Lógica de login."""
        cpf = self.campo_cpf.text
        senha = self.campo_senha.text
        print(f"Tentando login com CPF: {cpf} e Senha: {senha}")
        self.manager.current = "tela_configuracoes"  # Navega para configurações se login for bem-sucedido

    def cancelar_login(self, instancia):
        """Volta para a tela inicial."""
        self.manager.current = "tela_inicial"

    def recuperar_senha(self, instancia):
        """Lógica para recuperação de senha."""
        print("Redirecionando para recuperação de senha.")
    
    def validar_campo_cpf(self, instance):
        """
        Valida e formata o CPF digitado pelo usuário.
        """
        cpf_digitado = self.campo_cpf.text
        cpf_formatado = validar_e_formatar_cpf(cpf_digitado)

        if cpf_formatado:
            self.campo_cpf.text = cpf_formatado  # Atualiza o campo com o CPF formatado
        else:
            # Exibe um popup se o CPF for inválido
            popup = Popup(
                title="Erro de Validação",
                content=Label(text="CPF inválido. Certifique-se de que contém 11 dígitos numéricos."),
                size_hint=(0.8, 0.4)
            )
            popup.open()

