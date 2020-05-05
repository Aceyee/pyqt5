from QTreeItem import TreeItem
from qtpy.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt, QSortFilterProxyModel
from qtpy.QtWidgets import QApplication, QAbstractItemView, QTreeView, QTableView

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(("Title", "Summary", "ttt", "aaaa", "ccc"))
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
            {'source_path': 'chr_Body_A_Blush_msk_nc8.1001.tif', 'dest_role': 'nc8', 'depth': 'uint8',
                'source_role': 'nc8', 'orig_source': 'chr_Body_A_Blush_msk_nc8.1001.tif',
                'dest_path': 'chr_Body_A_Blush_msk_nc8.1001.tx',
                'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures'}
            ]
        self.setupModelData(data, self.rootItem)

    def setupModelData(self, lines, parent):
        for x in range(len(lines)):
            lineData = [lines[x][key] for key in lines[x].keys()]
            tree_item = TreeItem(lineData, parent)
            parent.appendChild(tree_item)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

class IconView(QTreeView):
    def __init__(self):
        super(IconView, self).__init__()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    f = QFile('default.txt')
    f.open(QIODevice.ReadOnly)
    model = TreeModel(f.readAll())
    f.close()

    view = IconView()
    proxy_model = QSortFilterProxyModel()
    proxy_model.setSourceModel(model)
    view.setModel(proxy_model)
    view.setWindowTitle("Simple Tree Model")
    view.setSortingEnabled(True)
    view.setSelectionMode(QAbstractItemView.ExtendedSelection)
    view.show()
    sys.exit(app.exec_())