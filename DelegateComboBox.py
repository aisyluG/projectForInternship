from PyQt5.QtWidgets import QAbstractItemDelegate, QComboBox, \
    QStyleOptionComboBox, QStyle, QApplication

#класс делегата для использования ComboBox в представлении
class DelegateComboBox(QAbstractItemDelegate):
    def __init__(self, parent, column):
        QAbstractItemDelegate.__init__(self, parent)
        #номер столбца, в котором будет использован комбобокс
        self.column = column

    #метод для созданию виджета-редактора
    def createEditor(self, parent, option, index):
        if index.column() == self.column:
            self.comboBox = QComboBox(parent)
            items = [str(i) for i in range(1, 6)]
            self.comboBox.addItems(items)
            return self.comboBox
        else:
            return QAbstractItemDelegate.createEditor(self, parent, option, index)

    #метод для копирования данных из модели в редактор
    def setEditorData(self, editor, index):
        if index.column() == self.column and index.isValid():
            value = str(index.data())
            editor.setCurrentText(value)
        else:
            QAbstractItemDelegate.setEditorData(self, editor, index)

    #метод для сохранения отредактированного значения в модель
    def setModelData(self, editor, model, index):
        if index.column() == self.column:
            value = editor.currentText()
            model.setData(index, int(value))
        else:
            QAbstractItemDelegate.setModelData(self, editor, model, index)

    #метод для управления геометрией редактора
    def updateEditorGeometry(self, editor, option, index):
        if index.column() == self.column:
            editor.setGeometry(option.rect)
        else:
            QAbstractItemDelegate.updateEditorGeometry(self, editor, option, index)

    #метод для отрисовки виджета-редактора
    def paint(self, painter, option, index):
        value = index.data()
        if index.column() == self.column:
            if option.state:
                opt = QStyleOptionComboBox()
                opt.currentText = str(value)
                opt.rect = option.rect
                QApplication.style().drawControl(QStyle.CE_ComboBoxLabel, opt, painter)
        else:
            QAbstractItemDelegate.paint(self, painter, option, index)