from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle, Rectangle

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


class TelaLoginAdministrativo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        self.layout = BoxLayout(orientation="vertical", spacing=10, padding=[20, 20, 20, 20])
        self.add_widget(self.layout)  # Adiciona o layout principal
        self.mostrar_tela_inicial()  # Chama a tela inicial

    def _atualizar_fundo(self, *args):
        """Atualiza o fundo da tela ao redimensionar."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def mostrar_tela_inicial(self):
        """Restaura a tela inicial com os botões 'Acessar' e 'Nova Conta'."""
        self.layout.clear_widgets()

        # Adicionar logo
        self.logo = Label(
            text="Administrativo",
            font_size="24sp",
            size_hint=(1, 0.3),
            halign="center",
            valign="middle",
            color=(0, 0, 0, 1),
        )
        self.layout.add_widget(self.logo)

        # Botão "Acessar"
        botao_acessar = RoundedButton(
            text="Acessar",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_acessar.bind(on_release=self.mostrar_tela_pin)
        self.layout.add_widget(botao_acessar)

        # Botão "Nova Conta"
        botao_nova_conta = RoundedButton(
            text="Nova Conta",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_nova_conta.bind(on_release=self.criar_nova_conta)
        self.layout.add_widget(botao_nova_conta)

    def mostrar_tela_pin(self, instancia):
        """Exibe a tela de inserção do PIN."""
        self.layout.clear_widgets()

        # Label "Insira a senha de acesso"
        label_instrucao = Label(
            text="Insira a senha de acesso",
            font_size="18sp",
            size_hint=(1, 0.2),
            color=(0.2, 0.2, 0.2, 1),
            halign="center",
            valign="middle",
        )
        label_instrucao.bind(size=label_instrucao.setter("text_size"))
        self.layout.add_widget(label_instrucao)

        # Layout para os dígitos da senha
        senha_grid = GridLayout(cols=6, spacing=10, size_hint=(1, 0.3))

        self.senha_inputs = []
        for _ in range(6):
            senha_input = TextInput(
                password=True,  # Oculta o texto digitado
                multiline=False,
                halign="center",
                size_hint=(None, None),
                size=(60, 60),  # Define o tamanho uniforme
                font_size="24sp",
                input_filter="int",
                background_color=(0.95, 0.95, 0.95, 1),
                foreground_color=(0, 0, 0, 1),
                cursor_color=(0, 0, 0, 1),
                padding=(15, 15),  # Ajusta o padding interno
            )
            senha_input.bind(text=self.limitar_caracter_e_mover_foco)
            self.senha_inputs.append(senha_input)
            senha_grid.add_widget(senha_input)

        self.layout.add_widget(senha_grid)

        # Botão "Confirmar"
        botao_confirmar = RoundedButton(
            text="Confirmar",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.1, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_confirmar.bind(on_release=self.verificar_pin)
        self.layout.add_widget(botao_confirmar)

        # Botão "Voltar"
        botao_voltar = RoundedButton(
            text="Voltar",
            size_hint=(1, 0.2),
            font_size="16sp",
            background_color=(0.9, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
            background_normal="",
            background_down="",
        )
        botao_voltar.bind(on_release=lambda _: self.mostrar_tela_inicial())
        self.layout.add_widget(botao_voltar)

    def limitar_caracter_e_mover_foco(self, instance, value):
        """Força o campo a conter apenas um caractere e move o foco automaticamente."""
        if len(value) > 1:
            instance.text = value[:1]
        if len(value) == 1:
            index = self.senha_inputs.index(instance)
            if index < len(self.senha_inputs) - 1:
                self.senha_inputs[index + 1].focus = True

    def verificar_pin(self, instancia):
        """Valida o PIN inserido e realiza o login."""
        senha = "".join([campo.text for campo in self.senha_inputs])
        if len(senha) == 6 and senha.isdigit():
            if senha == "123456":  # Substitua por uma consulta real ao banco
                if not self.manager.has_screen("tela_administracao"):
                    self.manager.add_widget(TelaAdministracao(name="tela_administracao"))
                self.manager.current = "tela_administracao"
            else:
                self.mostrar_erro("PIN incorreto ou não encontrado.")
        else:
            self.mostrar_erro("O PIN deve conter 6 dígitos numéricos.")

    def mostrar_erro(self, mensagem):
        """Exibe uma mensagem de erro."""
        popup = Popup(
            title="Erro",
            content=Label(text=mensagem),
            size_hint=(0.8, 0.4),
        )
        popup.open()

    def criar_nova_conta(self, instancia):
        """Redireciona para a tela de criação de nova conta."""
        print("Redirecionando para a tela de criação de nova conta.")
        self.manager.current = "tela_nova_conta"


class TelaAdministracao(Screen):
    """Tela para administração."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", spacing=20, padding=[20, 20, 20, 20])
        label = Label(
            text="Bem-vindo à Tela de Administração!",
            font_size="24sp",
            size_hint=(1, 0.2),
            halign="center",
            valign="middle",
        )
        layout.add_widget(label)
        self.add_widget(layout)
