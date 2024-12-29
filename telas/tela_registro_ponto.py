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

DB_PATH = "banco_dados.db"
FACE_RECOG_TOLERANCE = 0.4

class TelaRegistroPonto(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Feed da câmera
        self.camera_feed = Image(size_hint=(1, 0.7))
        self.layout.add_widget(self.camera_feed)

        # Nome do funcionário reconhecido
        self.nome_label = Label(
            text="",
            font_size='20sp',
            size_hint=(1, 0.1),
            color=(0, 0, 0, 1),
            halign="center",
            valign="middle"
        )
        self.layout.add_widget(self.nome_label)

        # Botões
        self.button_layout = BoxLayout(size_hint=(1, 0.2), spacing=10)

        self.cancelar_button = Button(
            text="Cancelar",
            size_hint=(0.5, 1),
            background_color=(0.8, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)
        )
        self.cancelar_button.bind(on_press=self.voltar_tela)
        self.button_layout.add_widget(self.cancelar_button)

        self.continuar_button = Button(
            text="Registrar",
            size_hint=(0.5, 1),
            background_color=(0.2, 0.6, 0.8, 1),  # Azul
            color=(1, 1, 1, 1),
            disabled=True
        )
        self.continuar_button.bind(on_press=self.registrar_ponto)
        self.button_layout.add_widget(self.continuar_button)

        self.layout.add_widget(self.button_layout)

        self.add_widget(self.layout)

        # Variáveis de controle
        self.capture = None
        self.current_frame = None
        self.recognized_name = None

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.atualizar_camera, 1.0 / 30.0)

    def on_leave(self):
        if self.capture:
            self.capture.release()
        self.capture = None
        Clock.unschedule(self.atualizar_camera)

    def atualizar_camera(self, dt):
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

        # Verificar reconhecimento facial
        self.verificar_reconhecimento(frame_rgb)

    def verificar_reconhecimento(self, frame_rgb):
        locs = face_recognition.face_locations(frame_rgb)
        encodings = face_recognition.face_encodings(frame_rgb, locs)

        if not encodings:
            self._atualizar_borda((1, 0, 0, 1))  # Vermelho se nenhum rosto
            self.nome_label.text = "Nenhum rosto detectado."
            self.continuar_button.disabled = True
            return

        encoding = encodings[0]
        nome = self.verificar_rosto(encoding)

        if nome:
            self._atualizar_borda((1, 0.5, 0, 1))  # Laranja se reconhecido
            self.nome_label.text = f"Reconhecido: {nome}"
            self.recognized_name = nome
            self.continuar_button.disabled = False
        else:
            self._atualizar_borda((1, 0, 0, 1))  # Vermelho se não reconhecido
            self.nome_label.text = "Rosto não reconhecido."
            self.recognized_name = None
            self.continuar_button.disabled = True

    def _atualizar_borda(self, color):
        with self.camera_feed.canvas.after:
            self.camera_feed.canvas.after.clear()
            Color(*color)
            Line(circle=(self.camera_feed.center_x, self.camera_feed.center_y, 150), width=2)

    def verificar_rosto(self, encoding):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT matricula, encoding FROM dados_faciais")
        registros = c.fetchall()
        conn.close()

        for matricula, encoding_json in registros:
            encoding_registrado = json.loads(encoding_json)
            distancia = face_recognition.face_distance([encoding_registrado], encoding)[0]
            if distancia < FACE_RECOG_TOLERANCE:
                return matricula

        return None

    def registrar_ponto(self, instance):
        if not self.recognized_name:
            return

        agora = datetime.now()
        horario = agora.strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT nome FROM funcionarios WHERE matricula = ?", (self.recognized_name,))
        nome = c.fetchone()[0]

        c.execute("""
            INSERT INTO registros_ponto (nome, matricula, data_hora, tipo)
            VALUES (?, ?, ?, ?)
        """, (nome, self.recognized_name, horario, "Entrada"))

        conn.commit()
        conn.close()

        self.nome_label.text = f"Ponto registrado para {nome}!"
        self.continuar_button.disabled = True

    def voltar_tela(self, instance):
        self.manager.current = 'tela_inicial'
