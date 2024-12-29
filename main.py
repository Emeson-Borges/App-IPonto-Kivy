from kivymd.app import MDApp  # Certifique-se de importar MDApp
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from telas.tela_inicial import TelaInicial
from telas.tela_registro_ponto import TelaRegistroPonto
from telas.tela_administracao import TelaAdministracao
from telas.tela_cadastro import TelaCadastro
from telas.tela_logs import TelaLogs
from utils.database import inicializar_banco
from telas.tela_prova_vida import TelaProvaVida
from telas.tela_sincronizar import TelaSincronizar
from telas.tela_login import TelaLoginAdministrativo

from layout.theme import AppTheme

# Inicializar o banco de dados
inicializar_banco()
class GerenciadorTelas(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TelaInicial(name='tela_inicial'))
        self.add_widget(TelaLoginAdministrativo(name="tela_login"))
        self.add_widget(TelaRegistroPonto(name='tela_registro_ponto'))
        self.add_widget(TelaAdministracao(name='tela_administracao'))
        self.add_widget(TelaCadastro(name='tela_cadastro'))
        self.add_widget(TelaLogs(name='tela_logs'))
        self.add_widget(TelaProvaVida(name='tela_prova_vida'))
        self.add_widget(TelaSincronizar(name='tela_sincronizar'))



# Inicializar o banco de dados
inicializar_banco()

class SistemaPontoApp(App):
    def build(self):
        self.title = "Sistema de Ponto RH247"
        return GerenciadorTelas()


# class SistemaPontoApp(MDApp):
#     def build(self):
#         # Aplica o tema global definido no AppTheme
#         # self.theme_cls = AppTheme.theme_cls
#         self.theme_cls = AppTheme()  # Gerenciador de tema
#         self.theme_cls.primary_palette = "Blue"  # Paleta principal
#         self.theme_cls.theme_style = "Light"  # Tema claro
#         return GerenciadorTelas()

if __name__ == "__main__":
    SistemaPontoApp().run()
