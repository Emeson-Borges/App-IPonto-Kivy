from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Line
import cv2
import face_recognition
import sqlite3
import json
from datetime import datetime

DB_PATH = "faces.db"
FACE_RECOG_TOLERANCE = 0.4  # Tolerância para reconhecimento facial

class TelaRegistroPonto(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Feed da câmera
        self.camera_feed = Image(size_hint=(1, 0.8))
        with self.camera_feed.canvas.before:
            Color(1, 0, 0, 1)  # Cor vermelha
            self.camera_border = Line(rectangle=(0, 0, 100, 100), width=3)
        self.layout.add_widget(self.camera_feed)

        # Botões
        self.button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10, padding=[20, 10, 20, 10])

        self.cancelar_button = Button(
            text="Cancelar",
            size_hint=(0.5, 1),
            background_color=(0.8, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)
        )
        self.cancelar_button.bind(on_press=self.voltar_tela)
        self.button_layout.add_widget(self.cancelar_button)

        self.continuar_button = Button(
            text="Continuar",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.6, 0.8, 1),  # Azul
            color=(1, 1, 1, 1)
        )
        self.continuar_button.bind(on_press=self.registrar_ponto)
        self.button_layout.add_widget(self.continuar_button)

        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)

        # Variáveis para controle da câmera
        self.capture = None
        self.current_frame = None

    def on_enter(self):
        """Abre a câmera ao entrar na tela."""
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.atualizar_camera, 1.0 / 30.0)

    def on_leave(self):
        """Libera a câmera ao sair da tela."""
        if self.capture:
            self.capture.release()
        self.capture = None
        Clock.unschedule(self.atualizar_camera)

    def atualizar_camera(self, dt):
        """Atualiza o feed da câmera."""
        ret, frame = self.capture.read()
        if not ret:
            return

        self.current_frame = frame.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        buf = frame_rgb.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        self.camera_feed.texture = texture

        # Atualizar borda da câmera
        self.camera_border.rectangle = (self.camera_feed.x, self.camera_feed.y, self.camera_feed.width, self.camera_feed.height)

    def registrar_ponto(self, instance):
        """Registra o ponto se o rosto for reconhecido."""
        if self.current_frame is None:
            return

        frame_rgb = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        locs = face_recognition.face_locations(frame_rgb)
        encodings = face_recognition.face_encodings(frame_rgb, locs)

        if not encodings:
            self.mostrar_feedback("Nenhum rosto detectado.")
            return

        encoding = encodings[0]
        nome = self.verificar_rosto(encoding)

        if nome:
            self.salvar_log(nome)
            self.mostrar_feedback(f"Ponto registrado para {nome}!", sucesso=True)
        else:
            self.mostrar_feedback("Rosto não reconhecido.")

    def verificar_rosto(self, encoding):
        """Verifica se o rosto é conhecido com base no banco de dados."""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name, encoding FROM face_encodings")
        registros = c.fetchall()
        conn.close()

        for nome, encoding_json in registros:
            encoding_registrado = json.loads(encoding_json)
            distancia = face_recognition.face_distance([encoding_registrado], encoding)[0]
            if distancia < FACE_RECOG_TOLERANCE:
                return nome

        return None

    def salvar_log(self, nome):
        """Salva o log de ponto no banco de dados."""
        agora = datetime.now()
        horario = agora.strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM face_logs WHERE name = ? AND date(date_time) = date('now')", (nome,))
        registros_hoje = c.fetchone()[0]
        tipo = "Entrada" if registros_hoje % 2 == 0 else "Saída"

        c.execute("INSERT INTO face_logs (name, date_time, log_type) VALUES (?, ?, ?)", (nome, horario, tipo))
        conn.commit()
        conn.close()

    def mostrar_feedback(self, mensagem, sucesso=False):
        """Mostra feedback para o usuário."""
        cor = (0, 1, 0, 1) if sucesso else (1, 0, 0, 1)  # Verde para sucesso, vermelho para erro
        popup = Popup(
            title="Registro de Ponto",
            content=Label(text=mensagem, color=cor),
            size_hint=(0.8, 0.4)
        )
        popup.open()

    def voltar_tela(self, instance):
        """Volta para a tela inicial."""
        self.manager.current = 'tela_inicial'
