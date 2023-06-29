from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp
import threading
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout

from kivy import platform
from Speechrecognizer import stt

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET, Permission.RECORD_AUDIO])


class FirstWindow(Screen):

    Builder.load_file('firstwindow.kv')

    def toggle_recording(self):

        if self.ids.rec.icon == 'record-circle-outline':
            self.ids.rec.icon = 'stop'
            threading.Thread(target=self.start_listening).start()

        else:
            self.ids.rec.icon = 'record-circle-outline'
            threading.Thread(target=self.stop_listening).start()

    def start_listening(self):
        if stt.listening:
            self.stop_listening()
            return

        self.ids.heard_speech.text = ''

        stt.start()

        Clock.schedule_interval(self.check_state, 1 / 5)

    def stop_listening(self):

        stt.stop()
        self.update()

        Clock.unschedule(self.check_state)

    def update(self):
        self.ids.heard_speech.text = '\n'.join(stt.results)

    def check_state(self, dt):
        # if the recognizer service stops, change UI
        if not stt.listening:
            self.stop_listening()


class WindowManager(ScreenManager):
    pass


class rawApp(MDApp):

    def build(self):

        return WindowManager()


if __name__ == '__main__':
    rawApp().run()
