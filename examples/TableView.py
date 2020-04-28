import operator
import qtpy.QtCore as QtCore
import qtpy.QtWidgets as QtWidgets
import qtpy.QtGui as QtGui

class MyWindow(QtWidgets.QWidget):
    def __init__(self, data_list, header, *args):
        super(MyWindow, self).__init__()
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 200, 570, 450)
        self.setWindowTitle("Click on column title to sort")
        table_model = MyTableModel(self, data_list, header)
        
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setSourceModel(table_model)

        table_view = QtWidgets.QTableView()
        table_view.setModel(self.proxy_model)
        # set font
        font = QtGui.QFont("Courier New", 14)
        table_view.setFont(font)
        # set column width to fit contents (set font first!)
        table_view.resizeColumnsToContents()
        # enable sorting
        table_view.setSortingEnabled(True)

        line_edit = QtWidgets.QLineEdit()
        line_edit.textChanged.connect(self.onTextChanged)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(line_edit)
        layout.addWidget(table_view)
        self.setLayout(layout)
    
    def onTextChanged(self, text):
        self.proxy_model.setFilterRegExp(str(text))
        
class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, mylist, header, *args):
        super(MyTableModel, self).__init__()
        self.mylist = mylist
        self.header = header

    def rowCount(self, parent):
        return len(self.mylist)

    def columnCount(self, parent):
        return len(self.mylist[0])

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.mylist = sorted(self.mylist,
            key=operator.itemgetter(col))
        if order == QtCore.Qt.DescendingOrder:
            self.mylist.reverse()
        self.layoutChanged.emit()

# the solvent data ...
# header = ['Input File Path', 'Role', 'Output TX', 'Role', 'Depth']
header = ['source_path', 'source_space', 'dest_path', 'dest_space', 'depth', 'folder','orig_source']

# use numbers for numeric data to sort properly
data_list = [
('ACETIC ACID', 117.9, 16.7, 1.049, 5),
('ACETIC ANHYDRIDE', 140.1, -73.1, 1.087, 6),
('ACETONE', 56.3, -94.7, 0.791, 8)
]

data = [
(('AOV_spec_dot_nc8.tif'),'nc8', 'uint8',  'nc8',
    ('AOV_spec_dot_nc8.tif'),  ('AOV_spec_dot_nc8.tx'),
    ('Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures')),

(('dome_lnf.hdr'),'lnf', 'float',  'lnf',
    ('dome_lnf.hdr'),  ('dome_lnf.tx'),
    ('Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures')),

(('iris_NRM_nc8.tif'),'nc8', 'uint8',  'nc8',
    ('iris_NRM_nc8.tif'),  ('iris_NRM_nc8.tx'),
    ('Y:/APA/assets/gen_elems/Character_Elems/Eyes/textures')),
]
app = QtWidgets.QApplication([])
win = MyWindow(data, header)
win.show()
app.exec_()