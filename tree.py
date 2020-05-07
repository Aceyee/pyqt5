import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets

class Button(object):
    def __init__(self, name):
        self.name = name

class TreeItem(object):
    def __init__(self, data, is_header=False, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.is_header = is_header
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            if self.is_header:
                return self.itemData
            else:
                return self.itemData.name
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)
        self.rootItem = TreeItem("", True, None)
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, column, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(column)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, data, parent):
        header = data['header']
        buttons = data['buttons']
        header_item = TreeItem(header, True, parent)
        for button in buttons:
            button_item = TreeItem(button, False, header_item)
            header_item.appendChild(button_item)
        parent.appendChild(header_item)
        

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    data = {
        'header':'camera',
        'buttons': [Button('shake'), Button('aaa'), Button('ccc')]
    }
    model = TreeModel(data)
    view = QtWidgets.QTreeView()
    view.setModel(model)
    view.setWindowTitle("MVTree")
    view.show()
    sys.exit(app.exec_())