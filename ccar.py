import pyautogui
import time
import _thread
import mouse
import sys
from pyautogui import press
from PyQt5.QtWidgets import *

# --- configure variables ---
cars = [{
    "races": 6,
    "x": 421,
    "y": 726
}]

menu_cars_x = 578
menu_cars_y = 98
close_race_x = 1344
close_race_y = 91

# ---------------------------

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)

        self._running_bot = False
        self._running__x = False

        cbutton = QCheckBox("Bot ativo")
        cbutton.setChecked(False)
        cbutton.toggled.connect(self.onClickedBot)
        layout.addWidget(cbutton, 0, 0)

        cbutton_position = QCheckBox("Exibir X, Y")
        cbutton_position.setChecked(False)
        cbutton_position.toggled.connect(self.onClickedPosition)
        layout.addWidget(cbutton_position, 10, 0)

        self.thread = None 

    def click(self, x, y):
        mouse.move(x, y, absolute=True, duration=0.1)
        mouse.click('left')
        self.sleep(5)

    def scroll(self, value):
        pyautogui.vscroll(value)

    def sleep(self, seconds):
        time.sleep(seconds)

    def write(self, text):
        press(text)
        self.sleep(2)

    def rotine(self):
        for car in cars:
            print("5 segundos página será atualizada")
            self.sleep(5)
            if not self._running_bot:
                return 

            press('f5')

            self.sleep(5)
            if not self._running_bot:
                return 

            # menu cars
            print("entrando no menu dos carros")
            self.click(menu_cars_x, menu_cars_y)
            if not self._running_bot:
                return 

            print("refuel")
            self.click(1253, 622)
            if not self._running_bot:
                return

            print("refuel - ok")
            self.click(1038, 154)
            if not self._running_bot:
                return

            # scroll final
            print("rolando página até o final")
            self.scroll(-3000)
            self.sleep(5)
            if not self._running_bot:
                return

            for race in range(1, car["races"]+1):
                print("iniciando a corrida", race)
                # start corrida
                self.click(car["x"], car["y"])
                if not self._running_bot:
                    return 

                ''' 
                print("quebrar captcha")
                captcha = self.captcha()
                self.sleep(5)
                if not self._running_bot:
                    return

                print("digitando captcha")
                self.write(captcha)
                if not self._running_bot:
                    return

                print("iniciar corrida")
                self.click(957,689)
                if not self._running_bot:
                    return
                '''

                print("digite o captcha")
                self.sleep(30)

                # aguarda corrida
                print("aguardando a corrida terminar")
                self.sleep(60)
                if not self._running_bot:
                    return 
                    
                # scroll final
                print("rolando página até o inicio")
                self.scroll(0)
                self.sleep(5)
                if not self._running_bot:
                    return

                # fecha janela
                self.click(close_race_x, close_race_y)
                if not self._running_bot:
                    return 

    def get_position(self):
        while self._running_position:
            x, y = pyautogui.position()
            print("x={},Y={}".format(x,y))
            time.sleep(1)

    def terminate_position(self):
        self._running_position = False

    def terminate_bot(self):
        self._running_bot = False

    def onClickedPosition(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            print("position on")
            self._running_position = True
            _thread.start_new_thread( self.get_position, ())
        else:
            print("position off")
            self.terminate_position()

    def onClickedBot(self):
        cbutton = self.sender()
        if cbutton.isChecked():
            print("bot on")
            self._running_bot = True
            _thread.start_new_thread( self.rotine, ())
        else:
            print("bot off")
            self.terminate_bot()
            

app = QApplication(sys.argv)
screen = Window()
screen.setWindowTitle("CCARS BOT")
screen.show()
sys.exit(app.exec_())
