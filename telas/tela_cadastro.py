from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from layout.rounded_button import BotaoArredondado
import sqlite3

DB_PATH = "banco_dados.db"

class TelaCadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = RoundedRectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Título
        titulo = Label(
            text="Cadastro de Funcionário",
            font_size='24sp',
            bold=True,
            color=(0, 0, 0, 1)  # Preto
        )
        layout.add_widget(titulo)

        # Campos de entrada
        self.campo_nome = TextInput(
            hint_text="Nome",
            multiline=False,
            size_hint=(0.9, 0.1),
            pos_hint={"center_x": 0.5},
            background_color=(0.95, 0.95, 0.95, 1),  # Cinza claro
            foreground_color=(0, 0, 0, 1),  # Preto
            cursor_color=(0, 0, 1, 1)  # Azul
        )
        self.campo_cpf = TextInput(
            hint_text="CPF",
            multiline=False,
            size_hint=(0.9, 0.1),
            pos_hint={"center_x": 0.5},
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 1, 1)
        )
        self.campo_matricula = TextInput(
            hint_text="Matrícula",
            multiline=False,
            size_hint=(0.9, 0.1),
            pos_hint={"center_x": 0.5},
            background_color=(0.95, 0.95, 0.95, 1),
            foreground_color=(0, 0, 0, 1),
            cursor_color=(0, 0, 1, 1)
        )

        layout.add_widget(self.campo_nome)
        layout.add_widget(self.campo_cpf)
        layout.add_widget(self.campo_matricula)

        # Botão para salvar
        botao_salvar = BotaoArredondado(
            text="Salvar Cadastro",
            size_hint=(0.9, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            color=(1, 1, 1, 1)  # Texto branco
        )
        botao_salvar.bind(on_release=self.salvar_cadastro)
        layout.add_widget(botao_salvar)

        # Botão para voltar
        botao_voltar = BotaoArredondado(
            text="Voltar",
            size_hint=(0.9, 0.12),
            pos_hint={"center_x": 0.5},
            font_size="18sp",
            background_color=(0.8, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)  # Texto branco
        )
        botao_voltar.bind(on_release=self.voltar_tela)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

    def _atualizar_fundo(self, *args):
        """Atualiza o fundo da tela ao redimensionar."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def salvar_cadastro(self, instancia):
        nome = self.campo_nome.text
        cpf = self.campo_cpf.text
        matricula = self.campo_matricula.text

        if not nome or not cpf or not matricula:
            self.mostrar_feedback("Todos os campos são obrigatórios.", sucesso=False)
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO funcionarios (nome, cpf, matricula)
                VALUES (?, ?, ?)
            ''', (nome, cpf, matricula))
            conn.commit()
            conn.close()

            self.mostrar_feedback(f"Funcionário {nome} cadastrado com sucesso!", sucesso=True)
            self.campo_nome.text = ""
            self.campo_cpf.text = ""
            self.campo_matricula.text = ""
        except sqlite3.IntegrityError:
            self.mostrar_feedback("Erro: CPF ou Matrícula já cadastrado.", sucesso=False)
        except Exception as e:
            self.mostrar_feedback(f"Erro ao salvar: {str(e)}", sucesso=False)

    def mostrar_feedback(self, mensagem, sucesso=False):
        """Mostra feedback para o usuário."""
        cor = (0, 1, 0, 1) if sucesso else (1, 0, 0, 1)  # Verde para sucesso, vermelho para erro
        popup = Popup(
            title="Cadastro de Funcionário",
            content=Label(text=mensagem, color=cor),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def voltar_tela(self, instancia):
        """Volta para a tela de administração."""
        self.manager.current = 'tela_administracao'