from QTreeItem import TreeItem
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets
import qtpy.QtGui as QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.winwidth = 1000
        self.winheight = 500
        self.setMinimumSize(self.winwidth, self.winheight)
        self.setWindowTitle("TX Converter")

        model = TreeModel()
        view = IconView()
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(model)
        view.setModel(self.proxy_model)
        view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        view.show()

        # item_delegate = ItemDelegate(self)
        # view.setItemDelegate(item_delegate)

        # latest version is setSectionResizeMode() however, qtpy is loading old version, so use setResizeMode()
        # header_view = view.horizontalHeader()
        # header_view.setResizeMode(1, QtWidgets.QHeaderView.Fixed)
        # header_view.setResizeMode(3, QtWidgets.QHeaderView.Fixed)
        # header_view.setResizeMode(4, QtWidgets.QHeaderView.Fixed)

        # set font
        font = QtGui.QFont("Courier New", 14)
        view.setFont(font)
        # set column width to fit contents (set font first!)
        # view.resizeColumnsToContents()
        # enable sorting
        view.setSortingEnabled(True)
        # select rows
        view.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.onTextChanged)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(line_edit)
        layout.addWidget(view)
        self.setLayout(layout)
    
    def onTextChanged(self, text):
        self.proxy_model.setFilterRegExp(str(text))

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Root"))
        self.__columns = [{'name': 'source_path', 'visible': True},
            {'name': 'source_role', 'visible': True},
            {'name': 'dest_path', 'visible': True},
            {'name': 'dest_role', 'visible': True},
            {'name': 'depth', 'visible': True},
            {'name': 'orig_source', 'visible': False},
            {'name': 'folder', 'visible': False},
            ]
        data = [
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
            {'source_path': 'chr_Body_A_Blush_msk_nc8.<UDIM>.tif', 'dest_role': 'nc8', 'depth': 'uint8',
                'source_role': 'nc8', 'orig_source': 'chr_Body_A_Blush_msk_nc8.1001.tif',
                'dest_path': 'chr_Body_A_Blush_msk_nc8.1001.tx',
                'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures',
                'sublist': ['chr_Body_A_Blush_msk_nc8.1001.tif', 'chr_Body_A_Blush_msk_nc8.1002.tif', 'chr_Body_A_Blush_msk_nc8.1003.tif']}
            ]
        self.setupModelData(data, self.rootItem)

    def setupModelData(self, lines, parent):
        visible_columns = [item['name'] for item in self.__columns if item['visible']]

        for x in range(len(lines)):
            lineData = [lines[x][key] for key in visible_columns]
            tree_item = TreeItem(lineData, parent)
            if 'sublist' in lines[x]:
                for y in lines[x]['sublist']:
                    subitem = TreeItem([y], tree_item)
                    tree_item.appendChild(subitem)
            parent.appendChild(tree_item)

    def columnCount(self, parent):
        num_visible = len([col for col in self.__columns if col['visible']])
        return num_visible

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

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                result = " ".join([part.title() for part in self.__columns[col]['name'].split('_')]).replace(
                    'Source', 'In').replace('Dest', 'Out')
                return result

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

class IconView(QtWidgets.QTreeView):
    def __init__(self):
        super(IconView, self).__init__()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication([])
    win = MyWindow()
    win.show()
    app.exec_()
