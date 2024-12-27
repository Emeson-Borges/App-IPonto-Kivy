from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class TelaLogs(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        titulo = Label(text="Logs do Sistema", font_size='24sp')
        layout.add_widget(titulo)

        # ScrollView para exibição dos logs
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.logs_container = GridLayout(cols=1, size_hint_y=None, padding=10, spacing=10)
        self.logs_container.bind(minimum_height=self.logs_container.setter('height'))
        self.scroll.add_widget(self.logs_container)
        layout.add_widget(self.scroll)

        # Botão para exportar
        botao_exportar = Button(text="Exportar Logs", size_hint=(1, 0.2), on_release=self.exportar_logs)
        layout.add_widget(botao_exportar)

        # Botão para voltar
        botao_voltar = Button(text="Voltar", size_hint=(1, 0.2), on_release=self.voltar_tela)
        layout.add_widget(botao_voltar)

        self.add_widget(layout)

        # Carregar logs iniciais
        self.carregar_logs()

    def carregar_logs(self):
        # Substituir pela lógica para carregar os logs do banco de dados
        logs = [
            "Log 1: Ponto registrado por João em 26/12/2024",
            "Log 2: Funcionário Maria cadastrado em 25/12/2024",
            "Log 3: Exportação de logs realizada em 24/12/2024"
        ]

        self.logs_container.clear_widgets()
        for log in logs:
            label_log = Label(text=log, size_hint_y=None, height=40)
            self.logs_container.add_widget(label_log)

    def exportar_logs(self, instancia):
        # Lógica para exportar os logs (substituir pelo código de exportação)
        print("Logs exportados com sucesso!")

    def voltar_tela(self, instancia):
        self.manager.current = 'tela_inicial'
