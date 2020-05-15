import qtpy.QtCore as QtCore
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets

class Button(object):
    def __init__(self, name):
        self.name = name

class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        self.parent = parent
        image_path = r'D:\pipeline\zihany\dev\git_repo\tool_panel_maya_anm\src\tool_panel_maya_anm\animate\anim_rec\anim_rec.png'
        self.image = QtGui.QImage(image_path)
        self.width = 0
        self.height = 0
        self.button_width = 50
        self.button_height = 50
        self.height_list = [0 for i in range(2)]

    def paint(self, painter, option, index):
        if index.data(QtCore.Qt.UserRole):
            QtWidgets.QStyledItemDelegate.paint(self, painter, option, index)
        else:
            geometry = self.parent.geometry()
            self.width = geometry.width()
            width = geometry.width()
            rect = option.rect
            height = self.button_height

            button_list = index.data()

            x = rect.x() + 0
            y = rect.y() + 0
            lineHeight = 0
            
            spaceX = 0
            spaceY = 0
            for button in button_list:
                next_x = x + self.button_width + spaceX
                if next_x - spaceX > width and lineHeight > 0:
                    x = rect.x()
                    y = y + lineHeight + spaceY
                    next_x = x + self.button_width + spaceX
                    lineHeight = 0

                draw_rect = QtCore.QRect(x, y, self.button_width, self.button_height)
                painter.drawImage(draw_rect, self.image)
                x = next_x
                lineHeight = max(lineHeight, self.button_height)

            row = index.row()
            h =  y + lineHeight - rect.y()
            if self.height_list[row] != h:
                index.model().setData(index, QtCore.QSize(20, h), QtCore.Qt.SizeHintRole)
                self.height_list[row] = h


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
            return self.itemData
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
        self.rootItem = TreeItem("header", True, None)
        self.setupModelData(data, self.rootItem)
        self.size = QtCore.QSize(20,50)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == QtCore.Qt.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())
        
        if role == QtCore.Qt.UserRole:
            item = index.internalPointer()
            return item.is_header

        if role == QtCore.Qt.SizeHintRole:
            item = index.internalPointer()
            if not item.is_header:
                return self.size

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        if role == QtCore.Qt.SizeHintRole:
            self.size = value
            self.dataChanged.emit(index, index)
            return True
        return False

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
        buttons2 = data['buttons']

        header_item = TreeItem(header, True, parent)
        content_item = TreeItem(buttons, False, header_item)
        header_item.appendChild(content_item)

        header_item2 = TreeItem(header, True, parent)
        content_item2 = TreeItem(buttons2, False, header_item2)
        header_item2.appendChild(content_item2)

        parent.appendChild(header_item)
        parent.appendChild(header_item2)
        

if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    data = {
        'header':'camera',
        'buttons': [Button('shake'), Button('aaa'), Button('ccc'), Button('sha'), Button('lll'), Button('ppp')]
    }
    model = TreeModel(data)
    view = QtWidgets.QTreeView()
    view.setIndentation(0)
    item_delegate = ItemDelegate(view)
    view.setItemDelegate(item_delegate)
    
    view.setRootIsDecorated(False)

    view.setHeaderHidden(True)

    view.setModel(model)
    view.setWindowTitle("MVTree")
    view.show()
    sys.exit(app.exec_())