import sys
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets
import qtpy.QtCore as QtCore

class DictModel(QtCore.QAbstractListModel):
    def __init__(self, student_list=list()):
        super(DictModel, self).__init__()
        self.student_list = student_list
    
    def rowCount(self, parent):
        return len(self.student_list)

    def data(self, index, role):
        row = index.row()
        value = self.student_list[row]
        first_key = next(iter(value)) 
        if role == QtCore.Qt.DisplayRole:
            return str(first_key)
        if role == QtCore.Qt.UserRole:
            return value[first_key]

class DictView(QtWidgets.QWidget):
    def __init__(self):
        super(DictView, self).__init__()
        self.left_view = QtWidgets.QListView()
        self.right_view = QtWidgets.QListView()
        self.main_layout = QtWidgets.QGridLayout()
        self.setup()

    def setup(self):
        """
        This function initialize double view's layout
        """
        # set up left and right view
        self.setup_left_view()
        self.setup_right_view()

        # add all above to main layout
        self.main_layout.addWidget(self.left_view, 0, 0)
        self.main_layout.addWidget(self.right_view, 0, 1)
        self.setLayout(self.main_layout)

    def setModel(self, model):
        """
        This function set data for double view
        :param: (ConfigModel) model - the model that contains all data, logic, and algorithm
        """
        self.left_view.setModel(model)  # apply the model to the list view
        self.index_changed(model.index(0, 0))  # select the first item as default

    def setup_left_view(self):
        """
        This function initialize left view's event
        """
        self.left_view.clicked.connect(self.index_changed)

    def setup_right_view(self):
        """
        This function initialize right view's event
        """
        self.right_view.clicked.connect(self.index_changed)

    def index_changed(self, index):
        """
        This function updates the current index in list view and updates the right group based on the selected index
        :param: (QModelIndex) index - the index that need to be set
        """
        self.left_view.setCurrentIndex(index)
        self.update_right_view()

    def update_right_view(self):
        """
        This function updates the right group box according the list view's current selected item
        """
        index = self.left_view.currentIndex()
        model = index.model()
        info_dict = model.data(index, QtCore.Qt.UserRole)
        for key in info_dict:
            key_label = QtWidgets.QLabel(key)
            val_label = QtWidgets.QLabel(info_dict[key])
            key_label.setBuddy(val_label)

if __name__ == '__main__':
    student_list = [
        {'student1': {'height':'170cm', 'weight':'60kg'}},
        {'student2': {'height':'160cm', 'weight':'55kg'}}
    ]
    app = QtWidgets.QApplication(sys.argv)
    model = DictModel(student_list)
    view = DictView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec_())