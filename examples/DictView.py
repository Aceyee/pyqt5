import sys
import collections
import qtpy.QtGui as QtGui
import qtpy.QtWidgets as QtWidgets
import qtpy.QtCore as QtCore

class DictModel(QtGui.QStandardItemModel):
    def __init__(self, student_dict=dict()):
        super(DictModel, self).__init__()
        self.student_dict = student_dict
        self.dict = {}
        self.setup_model()

    def setup_model(self):
        for key in self.student_dict:
            key_item = QtGui.QStandardItem(key)
            model = QtGui.QStandardItemModel()
            self.appendRow(key_item)
            self.dict[key] = model
            for attr in self.student_dict[key]:
                value = self.student_dict[key][attr]
                attr_item = QtGui.QStandardItem(attr)
                value_item = QtGui.QStandardItem(value)
                model.appendRow([attr_item, value_item])
            item = QtGui.QStandardItem()
            item.setData(model, QtCore.Qt.UserRole)
            key_item.appendRow(item)
            
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return QtGui.QStandardItemModel.data(self, index, role)
        if role == QtCore.Qt.UserRole:
            key = index.data()
            return self.dict[key]

class DictView(QtWidgets.QWidget):
    def __init__(self):
        super(DictView, self).__init__()
        self.left_view = QtWidgets.QListView()
        self.right_view = QtWidgets.QTreeView()
        self.main_layout = QtWidgets.QGridLayout()
        self.setup()

    def setup(self):
        """
        This function initialize double view's layout
        """
        # set up left view
        self.setup_left_view()

        # add two views to main layout
        self.main_layout.addWidget(self.left_view, 0, 0)
        self.main_layout.addWidget(self.right_view, 0, 1)
        self.setLayout(self.main_layout)

    def setModel(self, model):
        """
        This function set data for double view
        :param: (ConfigModel) model - the model that contains all data, logic, and algorithm
        """
        self.left_view.setModel(model)  # apply the model to the list view
        # self.index_changed(model.index(0, 0))  # select the first item as default

    def setup_left_view(self):
        """
        This function initialize left view's event
        """
        self.left_view.clicked.connect(self.index_changed)

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
        model = index.data(QtCore.Qt.UserRole)
        self.right_view.setModel(model)

if __name__ == '__main__':
    student_dict = collections.OrderedDict()
    student_dict['student1'] = {
            'height':'170cm',
            'weight':'60kg'
            }
    student_dict['student2'] = {
            'height':'160cm',
            'weight':'55kg'
            }
    app = QtWidgets.QApplication(sys.argv)
    model = DictModel(student_dict)
    view = DictView()
    view.setModel(model)
    view.show()
    sys.exit(app.exec_())
