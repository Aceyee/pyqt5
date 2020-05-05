from QTreeItem import TreeItem
from qtpy.QtCore import QAbstractItemModel, QFile, QIODevice, QModelIndex, Qt, QSortFilterProxyModel
from qtpy.QtWidgets import QApplication, QAbstractItemView, QTreeView, QTableView

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent=None):
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
            {'source_path': 'chr_Body_A_Blush_msk_nc8.1001.tif', 'dest_role': 'nc8', 'depth': 'uint8',
                'source_role': 'nc8', 'orig_source': 'chr_Body_A_Blush_msk_nc8.1001.tif',
                'dest_path': 'chr_Body_A_Blush_msk_nc8.1001.tx',
                'folder': 'Y:/APA/assets/gen_elems/Character_Elems/Skin/textures',
                'sublist': ['chr_Body_A_Blush_msk_nc8.1001.tif', 'chr_Body_A_Blush_msk_nc8.1002.tif', 'chr_Body_A_Blush_msk_nc8.1003.tif']}
            ]
        self.setupModelData(data, self.rootItem)

    def setupModelData(self, lines, parent):
        for x in range(len(lines)):
            lineData = [lines[x][key] for key in lines[x].keys() if key != 'sublist']
            tree_item = TreeItem(lineData, parent)
            if 'sublist' in lines[x]:
                # print lines[x]['sublist']
                for y in lines[x]['sublist']:
                    # print lines[x][y]
                    subitem = TreeItem(y, tree_item)
                    tree_item.appendChild(subitem)
            parent.appendChild(tree_item)

    def columnCount(self, parent):
        num_visible = len([col for col in self.__columns if col['visible']])
        return num_visible

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

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                result = " ".join([part.title() for part in self.__columns[col]['name'].split('_')]).replace(
                    'Source', 'In').replace('Dest', 'Out')
                return result

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