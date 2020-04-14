import sys
from PyQt5.QtCore import QSemaphore, QRect
from PyQt5 import QtWidgets, QtGui, QtCore
from uiMainWindow import Ui_MainWindow
from TableModel import TableModel
from DelegateComboBox import DelegateComboBox
from ClockThread import ClockThread

class Window(QtWidgets.QMainWindow):
    #семафор для работы потока
    sem = QSemaphore()
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #создаем и привязываем свою модель к представлению
        self.model = TableModel()
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.resizeColumnsToContents()

        # создаем и устанавливаем в представление в столбец 1 делегат для выпадающего списка
        self.delegate = DelegateComboBox(self.ui.tableView, 1)
        self.ui.tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked |
                                          QtWidgets.QAbstractItemView.CurrentChanged |
                                          QtWidgets.QAbstractItemView.SelectedClicked)
        self.ui.tableView.setItemDelegateForColumn(1, self.delegate)

        #обработка сигнала от кнопки Random
        self.ui.btRandomNumbers.clicked.connect(self.autoFillTable)
        #обработка сигнала от кнопки Resize
        self.ui.btResizeTable.clicked.connect(self.resizeTableView)
        #обработка выбора столбцов в таблице
        #self.ui.tableView.model().dataChanged.connect(self.currentChangedInTableView)
        #self.ui.tableView.model().dataChanged.connect(self.plotFromSelectedColumn)

        #добавляем действия в меню для загрузки данных из файла
        #HDF
        self.openFileHdf = QtWidgets.QAction('Open from hdf', self)
        self.openFileHdf.setStatusTip('Open file')
        self.ui.menuHdf.addAction(self.openFileHdf)
        #TXT
        self.openFileTxt = QtWidgets.QAction('Open from txt', self)
        self.openFileTxt.setStatusTip('Open file')
        self.ui.menuTxt.addAction(self.openFileTxt)

        #добавляем действия в менб для загрузки данных в файл
        #HDF
        self.saveFileHdf = QtWidgets.QAction('Save as hdf', self)
        self.saveFileHdf.setStatusTip('Save to file')
        self.ui.menuHdf.addAction(self.saveFileHdf)
        #TXT
        self.saveFileTxt = QtWidgets.QAction('Save as txt', self)
        self.saveFileTxt.setStatusTip('Save to file')
        self.ui.menuTxt.addAction(self.saveFileTxt)

        #добавляем обработчики событий
        self.openFileHdf.triggered.connect(self.loadData)
        self.openFileTxt.triggered.connect(self.loadData)
        self.saveFileHdf.triggered.connect(self.saveData)
        self.saveFileTxt.triggered.connect(self.saveData)

        #создаем timer с инетрвалом 1с чтобы он вызывал функцию рисования графика через некоторое время после выбора столбцов
        #так как у меня основной поток не вовремя вызывает обработчик сигнала (данные о выборе не успевают обновлятся)
        self.t = QtCore.QTimer(self)
        self.t.timeout.connect(self.plotFromSelectedColumn)
        self.t.start(1000)

        # создаем поток с интервалом 1с чтобы он вызывал функцию рисования графика через некоторое время после выбора столбцов
        # self.t = ClockThread(1, self.sem)
        # self.t.timeout.connect(self.plotFromSelectedColumn)
        # self.t.start()

    #вызывается при измении размеров окна
    def resizeEvent(self, a0: QtGui.QResizeEvent):
        winHeight = self.height()
        winWidth = self.width()
        #изменяем размеры таблицы-представления
        self.ui.tableView.resize(winWidth - 200, int(winHeight*0.6))
        #изменяем размеры виджета-графика
        self.ui.graphWidget.setGeometry(0, int(winHeight*0.6) + 3, winWidth, int(winHeight*0.4) - 25)
        #изменяем положение кнопок и надписей
        self.ui.groupBox.setGeometry(QRect(winWidth - 200, 0, 200, self.ui.tableView.height()))

    #вызывается при нажатии на кнопку автозаполнения
    def autoFillTable(self):
        self.ui.tableView.model().autoFill()

    #вызывается при нажатии на кнопку измения размера таблицы
    def resizeTableView(self):
        #вызываем у модели метод изменения ее размеров
        self.ui.tableView.model().resize(int(self.ui.spBoxRows.text()), int(self.ui.spBoxColumns.text()))

    #вызывается при изменении выделения в представлении
    #для разблокировки потока
    def currentChangedInTableView(self):
        #разблокировываем поток
        self.sem.release()

    #метод для рисования графика
    def plotFromSelectedColumn(self):
        #очищаем холст
        self.ui.graphWidget.clear()
        columns = set()
        for a in self.ui.tableView.selectedIndexes():
            columns.add(a.column())
        #если выделено 2 столбца
        if len(columns) == 2:
            #получаем значения из модели
            values = zip(self.ui.tableView.model().columnValues(columns.pop()), self.ui.tableView.model().columnValues(columns.pop()))
            #сортируем
            x, y = list(zip(*sorted(values)))
            #отрисовываем график
            self.ui.graphWidget.plot(x, y)

    #вызывается при нажатии на кнопку сохранения
    def saveData(self):
        try:
            if self.sender().text() == 'Save as txt':
                #получаем путь к файлу
                fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '/data.txt',
                                                            'Текстовые документы (*.txt)')
                #передаем название файла модели
                self.ui.tableView.model().saveAsTxt(fname)
            else:
                # получаем путь к файлу
                fname, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '/data.hdf5',
                                                             'HDF (*.hdf5)')
                # передаем название файла модели
                self.ui.tableView.model().saveAsHdf(fname)
        except Exception:
            QtWidgets.QMessageBox.about(self, ' ', 'Error')

    #вызывается при нажатии на кнопку загрузки
    def loadData(self):
        try:
            if self.sender().text() == 'Open from txt':
                # получаем путь к файлу
                fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/data.txt',
                                                             'Текстовые документы (*.txt)')
                # передаем название файла модели
                self.ui.tableView.model().loadFromTxt(fname)
            else:
                # получаем путь к файлу
                fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/data.hdf5',
                                                             'HDF (*.hdf5)')
                # передаем название файла модели
                self.ui.tableView.model().loadFromHdf(fname)

            self.ui.tableView.resizeColumnsToContents()
        except Exception:
            QtWidgets.QMessageBox.about(self, ' ', 'Error')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())