from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal
from PyQt5 import QtCore, QtGui
import numpy as np
import h5py

#создаем класс собственной модели
class TableModel(QAbstractTableModel):
    #двумерный numpy массив для хранения данных
    table_data = np.empty((2, 5))
    #лист с названиями столбцов
    columnHeaderData = [''] * 5
    #номера  нередактируемых столбцов (пересчитываемый столбец и столбец с накопленными значениями)
    notEditableColumns = {2, 3}
    #номер столбца с выпадающим списком допустимых значений
    columnWithComboBox = 1
    #номер столбца с изменяющимся в зависимости от знака числа фоном
    columnWithBackgroundColor = 4
    #сигнал о том, что данные в 1ом столбце изменились
    dataChangedInFstColumn = pyqtSignal(int, int)

    def __init__(self):
        QAbstractTableModel.__init__(self)
        #подписываемся на сигнал об изменении данных в первом столбце
        self.dataChangedInFstColumn.connect(self.calculateTrdColumn)
        self.dataChangedInFstColumn.connect(self.calculateFourColumn)
        #заполняем массив данными
        for j in self.editableColumns():
            for i in range(0, self.rowCount()):
                self.setData(self.index(i, j), 1)
        #заполняем данные о названиях столбцов
        for j in range(0, self.columnCount()):
            if j == self.columnWithComboBox:
                self.setHeaderData(j, Qt.Horizontal, "Столбец с выпадающим списком")
            elif j == 2:
                self.setHeaderData(j, Qt.Horizontal, "Пересчитываемый столбец")
            elif j == 3:
                self.setHeaderData(j, Qt.Horizontal, "Накопленные значения")
            elif j == self.columnWithBackgroundColor:
                self.setHeaderData(j, Qt.Horizontal, "Столбец с фоном")
            else:
                self.setHeaderData(j, Qt.Horizontal, str(j+1))

    #метод, возвращающий номера редактируемых столбцов
    def editableColumns(self):
        columns = set(range(0, self.columnCount()))
        return list(columns.difference(self.notEditableColumns))

    #устанавливаем данные по заданному модельному индексу
    def setData(self, index, data, role=QtCore.Qt.EditRole):
        #если элемент не редактируем, то изменения не вносятся
        if role != QtCore.Qt.EditRole:
            return False
        #изменяем данные в массиве по заданному индексу заданным значением
        self.table_data[index.row()][index.column()] = data
        #посылаем сиогнал о том, данные изменились
        self.dataChanged.emit(index, index)
        #если первый столбец, то посылаем сигнал об изменении данных в первом столбце
        #и передаем номер строки и новое значение ячейки
        if index.column() == 0:
            self.dataChangedInFstColumn.emit(index.row(), data)
        return True

    #возвращаем число строк в данных в модели
    def rowCount(self, parent=QModelIndex()):
        return len(self.table_data)

    #возвращаем число столбцов в данных в модели
    def columnCount(self, parent=QModelIndex()):
        return int(self.table_data.size/len(self.table_data))

    #метод для передачи представлениям и делегатам информации о данных модели
    def data(self, index, role):
        column = index.column()
        row = index.row()
        dt = int(self.table_data[row][column])
        #если отображаемые или редактируемые данные
        if role == Qt.EditRole or role == Qt.DisplayRole:
            return dt
        #если цвет фона и столбец с изменяющимся в зависимости от знака числа фоном
        if role == Qt.BackgroundColorRole and column == self.columnWithBackgroundColor:
            if dt > 0:
                return QtGui.QBrush(QtGui.QColor('lightgreen'))
            else:
                return QtGui.QBrush(QtGui.QColor('red'))
        else:
            return QtCore.QVariant()

    #метод, возвращающийкомбинацию флагов, соответствующую каждому элементу
    def flags(self, index):
        column = index.column()
        #если элемент в столбце с пересчитываемыми значениями, то он нередактируем
        if column in self.notEditableColumns:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEditable |QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    #метод для заполнения таблицы рандомными значениями от -1000 до 1000
    def autoFill(self):
        #запоняем только те столбцы, где значения не пересчитываются
        for j in self.editableColumns():
            for i in range(0, self.rowCount()):
                self.setData(self.index(i, j), np.random.randint(-1000, 1000))
        #заполняем столбец с комбобоксом, так как там возможны значения только от 1 до 5
        for i in range(0, self.rowCount()):
            self.setData(self.index(i, self.columnWithComboBox), np.random.randint(1, 6))

    #метод для передачи представлениям и делегатам информации о заголовках в модели
    def headerData(self, p_int, Qt_Orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QtCore.QVariant()
        #если заголовки столбцов, то возвращаем данные из листа с названиями столбцов
        if Qt_Orientation == Qt.Horizontal:
            return self.columnHeaderData[p_int]
        #если заголовки строк, то возвращаем просто номер строки
        elif Qt_Orientation == Qt.Vertical:
            return str(p_int + 1)
        return QtCore.QVariant()

    #устанавливаем данные в заголовках в модели по заданному номеру и ориентации
    def setHeaderData(self, section, orientation, value, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return False
        if orientation == Qt.Horizontal:
            self.columnHeaderData[section] = value
            self.headerDataChanged.emit(orientation, section, section)
            return True
        else:
            return False

    #метод для добавления новых строк в модель
    def insertRows(self, row, count, parent):
        #уведомляем о том, что собираемся вставить новые строки
        self.beginInsertRows(parent, row, row + count - 1)
        r = np.zeros((count, self.columnCount()))
        self.table_data = np.vstack((self.table_data, r))
        for j in self.editableColumns():
            for i in range(row, row+count):
                self.setData(self.index(i, j), 1)
        #уведомляем о том, что количество строк изменилось
        self.endInsertRows()
        return True

    #метод для удаления строк из модели
    def removeRows(self, row, count, parent):
        #уведомляем о том, что собираемся удалить строки из модели
        self.beginRemoveRows(parent, row, row + count - 1)
        self.table_data = self.table_data[:row + 1]
        #уведомляем о том, что количество строк изменилось
        self.endRemoveRows()

    #метод для добавления новых столбцов в модель
    def insertColumns(self, column, count, parent):
        #уведомляем о том, что собираемся вставить новые столбцы
        self.beginInsertColumns(parent, column, column + count - 1)
        r = np.ones((self.rowCount(), count))
        self.table_data = np.hstack((self.table_data, r))
        #уведомляем о том, что количество столбцов изменилось
        self.endInsertColumns()
        return True

    #метод для удаления столбцов из модели
    def removeColumns(self, column, count, parent):
        #уведомляем о том, что собираемся удалить столбцы из модели
        self.beginRemoveColumns(parent, column, column + count - 1)
        self.table_data = self.table_data[:, :column + 1]
        #уведомляем о том, что количество столбцов изменилось
        self.endRemoveColumns()

    #метод для изменения размеров модели
    def resize(self, newrows, newcolumns):
        rows = self.rowCount()
        columns = self.columnCount()
        if newrows > rows:
            self.insertRows(rows, newrows - rows, QtCore.QModelIndex())
        else:
            self.removeRows(newrows, rows - newrows, QtCore.QModelIndex())

        if newcolumns > columns:
            self.insertColumns(columns, newcolumns - columns, QtCore.QModelIndex())
        else:
            self.removeColumns(newcolumns, columns - newcolumns, QtCore.QModelIndex())

    #метод для вычисления значений в столбце из значений другого столбца
    def calculateTrdColumn(self, row, data):
        self.setData(self.index(row, 2), data * 100)

    #метод для вычисления накопленных значений в столбце из значений другого столбца
    def calculateFourColumn(self, row, data):
        #вычисляем значение в ячейке пересчитываемого столбца в строке, в которой изменилось значение в другом столбце
        #если не первая строка, то = значение в ячейке предыдущей строки + новое значение из другого столбца
        #иначе просто = новому значению из другого столбца
        if row != 0:
            value = self.data(self.index(row-1, 3), role=Qt.EditRole) + data
        else:
            value = data
        #далее пересчитываем значения следующих строк в столбце
        for i in range(row, self.rowCount()):
            self.setData(self.index(i, 3), value)
            value = value + self.data(self.index(row, 0), role=Qt.EditRole)

    #метод для получения данных в определенном столбце
    def columnValues(self, column):
        return self.table_data[:,column]

    #метод для записи данных в файл в формате TXT
    def dataToTxt(self, file):
        #записываем размеры модели
        file.write('rows={};columns={};\n'.format(self.rowCount(), self.columnCount()))
        #записываем данные о заголовках столбцов
        for i in range(0, self.columnCount()):
            file.write(self.headerData(i, Qt_Orientation=Qt.Horizontal)+';')
        file.write('\n')
        #записываем данные в ячейках
        for i in range(0, self.rowCount()):
            for j in range(0, self.columnCount()):
                file.write(str(self.data(self.index(i, j), role=Qt.DisplayRole))+';')
            file.write('\n')

    #метод для сохранения данных в TXT файл
    def saveAsTxt(self, fname):
        with open(fname, 'w') as file:
            self.dataToTxt(file)

    # метод для записи загруженных данных в модель
    def dataFromTxt(self, file):
        str = file.readline().split(';')
        #считываем информацию о размерах модели
        rows = int(str[0][-1])
        columns = int(str[1][-1])
        #переопределяем массив с данными
        self.table_data = np.empty((rows, columns))
        str = file.readline().split(';')
        self.columnHeaderData = ['']*columns
        #устанавливаем данные о заголовках
        for i in range(0, columns):
            self.setHeaderData(i, Qt.Horizontal, str[i])
        #устанавливаем значения ячеек
        for i in range(0, rows):
            str = file.readline().split(';')
            for j in range(0, columns):
                self.setData(self.index(i, j), int(str[j]))

    # метод для загрузки данных из TXT файла
    def loadFromTxt(self, fname):
        with open(fname, 'r') as file:
            self.dataFromTxt(file)

    # метод для записи данных в файл в формате HDF
    def dataToHdf(self, file):
        #записываем данные в ячейках
        file.create_dataset('Data', data=self.table_data)
        # записываем данные о заголовках
        headerData = np.array(self.columnHeaderData, dtype=h5py.string_dtype(encoding='utf-8'))
        file.create_dataset('HeaderData', data=headerData, dtype=h5py.string_dtype(encoding='utf-8'))

    #метод для сохранения данных в HDF файл
    def saveAsHdf(self, fname):
        with h5py.File(fname, 'w') as file:
            self.dataToHdf(file)

    # метод для записи загруженных данных в модель
    def dataFromHdf(self, file):
        #считываем данные о значениях в ячейках
        data = file['Data']
        #вычисляем размеры модели
        rows = len(data)
        columns = int(data.size/rows)
        #переопределяем массив с данными
        self.table_data = np.empty((rows, columns))
        #устанавливаем значения ячеек
        for i in range(0, rows):
            for j in range(0, columns):
                self.setData(self.index(i, j), int(data[i][j]))
        #считываем данные о заголовках
        headerData = file['HeaderData']
        self.columnHeaderData = ['']*columns
        # устанавливаем данные о заголовках
        for i in range(0, columns):
            self.setHeaderData(i, Qt.Horizontal, headerData[i], role=Qt.DisplayRole)

    # метод для загрузки данных из HDF файла
    def loadFromHdf(self, fname):
        with h5py.File(fname, 'r') as file:
            self.dataFromHdf(file)