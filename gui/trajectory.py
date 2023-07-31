from PySide6 import QtWidgets, QtCore

from qt_material import QtStyleTools


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        if len(self._data) <= 0:
            return 0
        return len(self._data[0])

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._headers[section]
            if orientation == QtCore.Qt.Vertical:
                return str(section + 1)
        return None


class TrajectoryTable(QtWidgets.QTableView, QtStyleTools):
    def __init__(self, parent=None):
        super(TrajectoryTable, self).__init__(parent)
        self.headers = ['Range', 'Path\nin', 'Path\nmoa', 'Drift\nin', 'Drift\nmoa', 'Velocity']
        self.init_ui(self)
        self.display_data()

    def init_ui(self, trajTable):
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalHeader().setHidden(True)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        extra = dict(density_scale=-2)
        self.apply_stylesheet(self, extra=extra, theme='dark_blue.xml')

    def display_data(self, data=None):
        model = MyTableModel([[1] * 6, ], self.headers)
        self.setModel(model)
        self.resizeColumnsToContents()


class TrajectoryGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TrajectoryGraph, self).__init__(parent)


class TrajectoryReticle(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TrajectoryReticle, self).__init__(parent)


class TrajectoryWidget(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(TrajectoryWidget, self).__init__(parent)
        self.init_ui(self)
        self.connect_ui(self)

    def init_ui(self, trajWidget):
        self.vLayout = QtWidgets.QVBoxLayout(self)

        self.table = TrajectoryTable(self)
        self.graph = TrajectoryGraph(self)
        self.reticle = TrajectoryReticle(self)

        self.viewCmb = QtWidgets.QComboBox(self)
        self.viewCmb.addItem('Table', 0)
        self.viewCmb.addItem('Reticle', 0)
        self.viewCmb.addItem('Graph', 0)

        self.stacked = QtWidgets.QStackedWidget(self)
        self.stacked.addWidget(self.table)
        self.stacked.addWidget(self.graph)
        self.stacked.addWidget(self.reticle)

        self.stacked.setCurrentWidget(self.table)

        self.vLayout.addWidget(self.viewCmb)
        self.vLayout.addWidget(self.stacked)

    def display_data(self, data=None):
        self.table.display_data(data)

    def switch_view(self, index):
        print(index)
        if index == 0:
            self.stacked.setCurrentWidget(self.table)
        elif index == 1:
            self.stacked.setCurrentWidget(self.reticle)
        elif index == 2:
            self.stacked.setCurrentWidget(self.graph)

    def connect_ui(self, trajWidget):
        self.viewCmb.currentIndexChanged.connect(self.switch_view)
