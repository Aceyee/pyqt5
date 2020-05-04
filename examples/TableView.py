import operator
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets
import qtpy.QtGui as QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self, data_list):
        super(MyWindow, self).__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.winwidth = 1000
        self.winheight = 500
        self.setMinimumSize(self.winwidth, self.winheight)
        self.setWindowTitle("TX Converter")
        table_model = MyTableModel(self, data_list)
        
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(table_model)

        table_view = QtWidgets.QTableView()
        table_view.setModel(self.proxy_model)

        item_delegate = ItemDelegate(self)
        table_view.setItemDelegate(item_delegate)

        # latest version is setSectionResizeMode() however, qtpy is loading old version, so use setResizeMode()
        header_view = table_view.horizontalHeader()
        header_view.setResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header_view.setResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header_view.setResizeMode(4, QtWidgets.QHeaderView.Fixed)

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
        editor = None
        table_model = index.model().sourceModel()
        column = index.column()
        if column in [table_model.columnIndex('dest_path')]:
            editor = QtWidgets.QLineEdit(parent)

        elif column in [table_model.columnIndex('source_role'), table_model.columnIndex('dest_role')]:
            editor = QtWidgets.QComboBox(parent)

        return editor

    def setEditorData(self, editor, index):
        proxy_model = index.model()
        table_model = proxy_model.sourceModel()

        column = index.column()
        if column in [table_model.columnIndex('dest_path')]:
            editor.setText(proxy_model.data(index, QtCore.Qt.DisplayRole))

        elif column in [table_model.columnIndex('source_role'), table_model.columnIndex('dest_role')]:
            sorted_spaces = sorted(table_model.colorspace_mappings.keys())
            editor.addItems(sorted_spaces)
            editor.setCurrentIndex(sorted_spaces.index(proxy_model.data(index, QtCore.Qt.DisplayRole)))

        elif column == table_model.columnIndex['depth']:
            depths = sorted([item['depth'] for key, item in table_model.colorspace_mappings.iteritems()])
            editor.addItems(depths)
            editor.setCurrentIndex(depths.index(proxy_model.data(index)))

        else:
            return None

    def setModelData(self, editor, model, index):
        table_model = model.sourceModel()
        column = index.column()
        column_indexes = table_model.columnIndexes()
        table_index = model.mapToSource(index)
        if column in [column_indexes['source_path'], column_indexes['dest_path']]:
            value = editor.text()
            table_model.setData(table_index, value)
        elif column in [column_indexes['source_role'], column_indexes['dest_role']]:
            value = editor.currentText()
            table_model.setData(table_index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
        
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist):
        super(MyTableModel, self).__init__()
        self.mylist = mylist
        self.__columns = [{'name': 'source_path', 'visible': True},
                    {'name': 'source_role', 'visible': True},
                    {'name': 'dest_path', 'visible': True},
                    {'name': 'dest_role', 'visible': True},
                    {'name': 'depth', 'visible': True},
                    {'name': 'orig_source', 'visible': False},
                    {'name': 'folder', 'visible': False},
                    ]
        self.colorspace_mappings = {'nc8': {'space': 'nc8', 'format': 'uint8'},
                        'nc16': {'space': 'nc16', 'format': 'uint16'},
                        'ncf': {'space': 'ncf', 'format': 'float'},
                        'nch': {'space': 'nch', 'format': 'half'},
                        'dt8': {'space': 'lnh', 'format': 'half'},
                        'dt16': {'space': 'lnh', 'format': 'half'},
                        'dth': {'space': 'lnh', 'format': 'half'},
                        'dtf': {'space': 'lnf', 'format': 'float'},
                        'lnh': {'space': 'lnh', 'format': 'half'},
                        'lnf': {'space': 'lnf', 'format': 'float'},
                        'dtt': {'space': 'lnh', 'format': 'half'},
                        'srgb': {'space': 'lnh', 'format': 'half'},
                        'srgf': {'space': 'lnf', 'format': 'float'}
                        }

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        num_visible = len([col for col in self.__columns if col['visible']])
        return num_visible

    def columnIndex(self, name):
        for i, col in enumerate(self.__columns):
            if col['name'] == name:
                return i

    def columnIndexes(self):
        return {col['name']: i for i, col in enumerate(self.__columns)}

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

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False

        if role == QtCore.Qt.EditRole:
            self.mylist[index.row()][self.__columns[index.column()]['name']] = value
            return True

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                result = " ".join([part.title() for part in self.__columns[col]['name'].split('_')]).replace(
                    'Source', 'In').replace('Dest', 'Out')
                return result

        else:
            return col

        return None

# use numbers for numeric data to sort properly
data_list = [
{'source_path': 'AOV_spec_dot_nc8.tif', 'dest_role': 'nc8', 'depth': 'uint8', 'source_role': 'nc8',
    'orig_source': 'AOV_spec_dot_nc8.tif', 'dest_path': 'AOV_spec_dot_nc8.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'dome_lnf.hdr', 'dest_role': 'lnf', 'depth': 'float', 'source_role': 'lnf',
    'orig_source': 'dome_lnf.hdr', 'dest_path': 'dome_lnf.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'iris_NRM_nc8.tif', 'dest_role': 'nc8', 'depth': 'uint8', 'source_role': 'nc8',
    'orig_source': 'iris_NRM_nc8.tif', 'dest_path': 'iris_NRM_nc8.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures'},
{'source_path': 'chr_Body_A_Beard_Msk_nc8.1001.tif', 'dest_role': 'nc8', 'depth': 'uint8',
    'source_role': 'nc8', 'orig_source': 'chr_Body_A_Beard_Msk_nc8.1001.tif',
    'dest_path': 'chr_Body_A_Beard_Msk_nc8.1001.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures'},
{'source_path': 'chr_Body_A_Blush_msk_nc8.1001.tif', 'dest_role': 'nc8', 'depth': 'uint8',
    'source_role': 'nc8', 'orig_source': 'chr_Body_A_Blush_msk_nc8.1001.tif',
    'dest_path': 'chr_Body_A_Blush_msk_nc8.1001.tx',
    'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures'}
]
app = QtWidgets.QApplication([])
win = MyWindow(data_list)
win.show()
app.exec_()