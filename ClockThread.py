from PyQt5.QtCore import QThread
import time

class ClockThread(QThread):
    def __init__(self, interval, semaphore, window):
        QThread.__init__(self)
        #устанавливаем интервал для работы потока
        self.interval = interval
        self.semaphore = semaphore
        self.window = window
    def run(self):
        while True:
            #ждем семафора
            self.semaphore.acquire()
            #ждем пока в таблице обновятся данные
            time.sleep(self.interval)
            #отрисовываем график выбранных значений
            self.window.plotFromSelectedColumn()