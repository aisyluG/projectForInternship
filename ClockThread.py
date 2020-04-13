from PyQt5.QtCore import QThread, pyqtSignal
import time

class ClockThread(QThread):
    timeout = pyqtSignal()
    def __init__(self, interval, semaphore):
        QThread.__init__(self)
        #устанавливаем интервал для работы потока
        self.interval = interval
        self.semaphore = semaphore
    def run(self):
        while True:
            #ждем семафор
            self.semaphore.acquire()
            #ждем пока в таблице обновятся данные
            time.sleep(self.interval)
            #отрисовываем график выбранных значений
            self.timeout.emit()
            #self.window.plotFromSelectedColumn()
