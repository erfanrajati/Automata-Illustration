import api
import random
import prewirtten as pw

from kivy.config import Config
# Config.set('graphics', 'resizable', '0')  
Config.set('graphics', 'height', '600')
Config.set('graphics', 'width', '800')

import kivy
from kivy.app import App
# from kivy.uix.label import Label
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen


class MainWindow(Screen):
    def submit(self, instance):
       userIn = self.ids.expression_input.text
       api.regex_analysis(userIn)

    def samples(self, instance):
        userIn = random.choice(pw.expressions)
        api.regex_analysis(userIn)


class SecondWindow(Screen):
    def submit(self, instance):
       pass

    def samples(self, instance):
        api.extract_automaton_by_sample()


class WindowManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        # return MyGridLayout()
        return WindowManager()
    

if __name__ == '__main__':
    MyApp().run()

