from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from telas.tela_inicial import TelaInicial
from telas.tela_registro_ponto import TelaRegistroPonto
from telas.tela_administracao import TelaAdministracao
from telas.tela_cadastro import TelaCadastro
from telas.tela_logs import TelaLogs

class GerenciadorTelas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TelaInicial(name='tela_inicial'))
        self.add_widget(TelaRegistroPonto(name='tela_registro_ponto'))
        self.add_widget(TelaAdministracao(name='tela_administracao'))
        self.add_widget(TelaCadastro(name='tela_cadastro'))
        self.add_widget(TelaLogs(name='tela_logs'))

class SistemaPontoApp(App):
    def build(self):
        return GerenciadorTelas()

if __name__ == "__main__":
    SistemaPontoApp().run()
