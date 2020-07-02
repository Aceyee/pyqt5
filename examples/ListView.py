import sys
import qtpy.QtCore as QtCore
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets

Label = QtCore.Qt.DisplayRole
Section = QtCore.Qt.UserRole + 1

class ListModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(ListModel, self).__init__(parent)
        self.items = list()

    def data(self, index, role):
        item = self.items[index.row()]
        if role == Label:
            return item["label"]

        if role == Section:
            return item["section"]

    def append(self, item):
        """Append item to end of model"""
        self.beginInsertRows(QtCore.QModelIndex(),
                             self.rowCount(),
                             self.rowCount())

        self.items.append(item)
        self.endInsertRows()

    def rowCount(self, parent=None):
        return len(self.items)

if __name__ == '__main__':
    # Create a Qt application
    app = QtWidgets.QApplication(sys.argv)
    
    # Our main window will be a QListView
    list_view = QtWidgets.QListView()
    list_view.setWindowTitle('Example List View')
    # list_view.setMinimumSize(600, 400)
    list_view.setFlow(QtWidgets.QListView.LeftToRight)
    list_view.setWrapping(True)
    
    # Create an empty model for the list_view's data
    model = ListModel()
    
    data = [{"label": "Ben", "section": "Human"},
             {"label": "Steve", "section": "Human"},
             {"label": "Alpha12", "section": "Robot"},
             {"label": "Alpha12", "section": "Robot"},
             {"label": "Alpha12", "section": "Robot"},
             {"label": "Alpha12", "section": "Robot"},
             {"label": "Mike", "section": "Toaster"}]
    # Add some textual items
    for item in data:
        model.append(item)
    
    # Apply the model to the list_view view
    list_view.setModel(model)
        
    # Show the window and run the app
    list_view.show()
    app.exec_()
