import threading
import sqlite3
import psycopg2
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from layout.rounded_button import BotaoArredondado

# Configurações do banco PostgreSQL
PG_CONFIG = {
    "dbname": "seu_banco",
    "user": "seu_usuario",
    "password": "sua_senha",
    "host": "seu_host",
    "port": 5432,
}

DB_PATH = "banco_dados.db"  # Caminho do banco SQLite local


class TelaSincronizar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo branco
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._atualizar_fundo, pos=self._atualizar_fundo)

        # Layout principal
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Título
        titulo = Label(
            text="Sincronizar Pontos",
            font_size="24sp",
            color=(0, 0, 0, 1),  # Preto
            bold=True,
        )
        self.layout.add_widget(titulo)

        # ScrollView para listar registros
        self.scroll_view = ScrollView(size_hint=(1, 0.6))
        self.registros_layout = GridLayout(cols=1, size_hint_y=None, spacing=10)
        self.registros_layout.bind(minimum_height=self.registros_layout.setter("height"))
        self.scroll_view.add_widget(self.registros_layout)
        self.layout.add_widget(self.scroll_view)

        # Botão "Sincronizar"
        self.botao_sincronizar = BotaoArredondado(
            text="Sincronizar",
            size_hint=(1, 0.1),
            pos_hint={"center_x": 0.5},
            font_size="16sp",
        )
        self.botao_sincronizar.bind(on_release=self.sincronizar_pontos)
        self.layout.add_widget(self.botao_sincronizar)

        # Botão "Voltar"
        # botao_voltar = BotaoArredondado(
        #     text="Voltar",
        #     size_hint=(1, 0.1),
        #     pos_hint={"center_x": 0.5},
        #     font_size="16sp",
        # )
        # botao_voltar.bind(on_release=self.voltar_tela)
        # self.layout.add_widget(botao_voltar)

        # self.add_widget(self.layout)
        
        # Botão "Voltar" como link
        botao_voltar = Button(
            text="Voltar",
            size_hint=(None, None),  # Define tamanho automático baseado no texto
            pos_hint={"center_x": 0.5},
            font_size="16sp",
            background_color=(0, 0, 0, 0),  # Fundo totalmente transparente
            color=(0.1, 0.5, 0.8, 1),  # Cor do texto (azul claro)
            background_normal='',  # Remove qualquer imagem padrão
            background_down='',  # Remove estilo ao pressionar
        )
        botao_voltar.bind(on_release=self.voltar_tela)
        self.layout.add_widget(botao_voltar)

        self.add_widget(self.layout)
        
    def on_enter(self):
        """
        Atualiza os registros não sincronizados sempre que a tela for exibida.
        """
        self.carregar_registros_nao_sincronizados()

    def _atualizar_fundo(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def carregar_registros_nao_sincronizados(self):
        """
        Carrega os registros do banco SQLite local que ainda não foram sincronizados.
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, matricula, data_hora, tipo FROM registros_ponto WHERE sincronizado = 'N'")
            registros = cursor.fetchall()
            conn.close()

            def atualizar_ui(dt):
                self.registros_layout.clear_widgets()

                if registros:
                    for registro in registros:
                        id_registro, nome, matricula, data_hora, tipo = registro
                        texto = f"ID: {id_registro}, Nome: {nome}, Matrícula: {matricula}, Data: {data_hora}, Tipo: {tipo}"
                        self.registros_layout.add_widget(Label(text=texto, size_hint_y=None, height=40))
                else:
                    self._mostrar_popup("Nenhum registro para sincronizar.", sucesso=False)

            Clock.schedule_once(atualizar_ui)

        except Exception as e:
            self._mostrar_popup(f"Erro ao carregar registros: {str(e)}", sucesso=False)

    def sincronizar_pontos(self, instance):
        """
        Sincroniza os pontos registrados no banco de dados local com o banco PostgreSQL.
        """
        self.botao_sincronizar.text = "Sincronizando..."
        self.botao_sincronizar.disabled = True

        threading.Thread(target=self._executar_sincronizacao).start()

    def _executar_sincronizacao(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, matricula, data_hora, tipo FROM registros_ponto WHERE sincronizado = 'N'")
            registros = cursor.fetchall()

            if not registros:
                Clock.schedule_once(lambda dt: self._mostrar_popup("Nenhum registro para sincronizar.", sucesso=False))
                return

            conn_pg = psycopg2.connect(**PG_CONFIG)
            cursor_pg = conn_pg.cursor()

            for registro in registros:
                id_registro, nome, matricula, data_hora, tipo = registro

                cursor_pg.execute(
                    """
                    INSERT INTO registros_ponto (nome, matricula, data_hora, tipo)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    (nome, matricula, data_hora, tipo),
                )

                cursor.execute("UPDATE registros_ponto SET sincronizado = 'S' WHERE id = ?", (id_registro,))

            conn.commit()
            conn_pg.commit()
            conn.close()
            conn_pg.close()

            Clock.schedule_once(lambda dt: self._mostrar_popup("Sincronização realizada com sucesso!", sucesso=True))
            Clock.schedule_once(lambda dt: self.carregar_registros_nao_sincronizados())

        except Exception as e:
            Clock.schedule_once(lambda dt: self._mostrar_popup(f"Erro durante sincronização: {str(e)}", sucesso=False))

        finally:
            Clock.schedule_once(lambda dt: self._resetar_botao())

    def _resetar_botao(self):
        self.botao_sincronizar.text = "Sincronizar"
        self.botao_sincronizar.disabled = False

    def _mostrar_popup(self, mensagem, sucesso):
        popup = Popup(
            title="Sincronização",
            content=Label(text=mensagem, halign="center"),
            size_hint=(0.8, 0.4),
        )
        popup.open()

    def voltar_tela(self, instance):
        self.manager.current = "tela_administracao"
