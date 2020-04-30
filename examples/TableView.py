import operator
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets
import qtpy.QtGui as QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self, data_list):
        super(MyWindow, self).__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.winwidth = 775
        self.winheight = 500
        self.setMinimumSize(self.winwidth, self.winheight)
        self.setWindowTitle("Click on column title to sort")
        table_model = MyTableModel(self, data_list)
        
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(table_model)


        table_view = QtWidgets.QTableView()
        table_view.setModel(self.proxy_model)

        item_delegate = ItemDelegate(self)
        table_view.setItemDelegate(item_delegate)

        # set font
        font = QtGui.QFont("Courier New", 14)
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)
        # select rows
        table_view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.onTextChanged)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(line_edit)
        layout.addWidget(table_view)
        self.setLayout(layout)
    
    def onTextChanged(self, text):
        self.proxy_model.setFilterRegExp(str(text))


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        self.edited_indexes = dict()

    def createEditor(self, parent, option, index):
        print 'aaaaaa'

        editor = QtWidgets.QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(0)
        editor.setMaximum(100)
        return editor

    def setEditorData(self, spinBox, index):
        print 'bbbbb'

        value = index.model().data(index, QtCore.Qt.EditRole)

        spinBox.setValue(value)

    def setModelData(self, spinBox, model, index):
        print 'ccccc'

        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        print 'ddddd'

        editor.setGeometry(option.rect)
        
        
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist):
        super(MyTableModel, self).__init__()
        self.mylist = mylist
        self.__columns = [{'name': 'source_path', 'visible': True},
                    {'name': 'source_space', 'visible': True},
                    {'name': 'dest_path', 'visible': True},
                    {'name': 'dest_space', 'visible': True},
                    {'name': 'depth', 'visible': True},
                    {'name': 'orig_source', 'visible': False},
                    {'name': 'folder', 'visible': False},
                    ]
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        num_visible = len([col for col in self.__columns if col['visible']])
        return num_visible

    def data(self, index, role):
        if not index.isValid():
            return

        if role == QtCore.Qt.DisplayRole:
            return self.mylist[index.row()][self.__columns[index.column()]['name']]

        elif role == 'full':
            return self.mylist[index.row()]

        elif isinstance(role, str):
            return self.mylist[index.row()][role]

        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                result = " ".join([part.title() for part in self.__columns[col]['name'].split('_')]).replace(
                    'Source', 'In').replace('Dest', 'Out')
                return result

        else:
            return col

        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.layoutChanged.emit()

# use numbers for numeric data to sort properly
data_list = [
{'source_path': 'AOV_spec_dot_nc8.tif', 'dest_space': 'nc8', 'depth': 'uint8', 'source_space': 'nc8',
    'orig_source': 'AOV_spec_dot_nc8.tif', 'dest_path': 'AOV_spec_dot_nc8.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'dome_lnf.hdr', 'dest_space': 'lnf', 'depth': 'float', 'source_space': 'lnf',
    'orig_source': 'dome_lnf.hdr', 'dest_path': 'dome_lnf.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'iris_NRM_nc8.tif', 'dest_space': 'nc8', 'depth': 'uint8', 'source_space': 'nc8',
    'orig_source': 'iris_NRM_nc8.tif', 'dest_path': 'iris_NRM_nc8.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'chr_Body_A_Beard_Msk_nc8.1001.tif', 'dest_space': 'nc8', 'depth': 'uint8',
    'source_space': 'nc8', 'orig_source': 'chr_Body_A_Beard_Msk_nc8.1001.tif',
    'dest_path': 'chr_Body_A_Beard_Msk_nc8.1001.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures'},
{'source_path': 'chr_Body_A_Blush_msk_nc8.1001.tif', 'dest_space': 'nc8', 'depth': 'uint8',
    'source_space': 'nc8', 'orig_source': 'chr_Body_A_Blush_msk_nc8.1001.tif',
    'dest_path': 'chr_Body_A_Blush_msk_nc8.1001.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures'}
]
app = QtWidgets.QApplication([])
win = MyWindow(data_list)
win.show()
app.exec_()