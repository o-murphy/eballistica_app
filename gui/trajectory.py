from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import QPointF
from qt_material import QtStyleTools
import pyqtgraph as pg

from calculate.calculate import calculate_traj, calculate_graph
from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, AtmoData


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent):
        if not self._data:
            return 0
        return len(self._data)

    def columnCount(self, parent):
        if not self._data or len(self._data) <= 0:
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
        self.headers = ['Range\nm', 'Path\ncm', 'Path\nMIL', 'Windage\ncm', 'Windage\nMIL', 'Velocity\nmps']
        self.init_ui(self)
        # self.display_data()

    def init_ui(self, trajTable):
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalHeader().setHidden(True)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        extra = dict(density_scale=-2)
        self.apply_stylesheet(self, extra=extra, theme='dark_blue.xml')

    def display_data(self, data=None):
        print(data)
        model = MyTableModel(data, self.headers)
        self.setModel(model)
        self.resizeColumnsToContents()


class TrajectoryGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TrajectoryGraph, self).__init__(parent)

    def display_data(self, points):
        self.vLayout = QtWidgets.QVBoxLayout(self)

        # Create a PlotWidget
        self.plot_widget = pg.PlotWidget(title='Drop at distance')
        self.vLayout.addWidget(self.plot_widget)

        # Add the data to the plot
        x = [p[0] for p in points]
        y = [p[1] for p in points]

        pen_color = '#FFA500'  # Custom pen color (red in this example)
        symbol_color = '#008080'

        self.plot_widget.plot(x, y, pen=pg.mkPen(color=pen_color), symbol='o', symbolBrush=symbol_color, symbolSize=5)

        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.setDisabled(True)
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.showAxis('bottom')
        self.plot_widget.showAxis('left')


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

    def display_data(self, edit_shot=None):

        rifle: RifleData = edit_shot.rifle
        ammo: AmmoData = edit_shot.ammo
        zerodata: ZeroData = ammo.zerodata
        target: Target = ammo.target
        atmo: AtmoData = ammo.atmo
        trajectory = calculate_traj(rifle, ammo, target, atmo, zerodata)
        self.table.display_data(trajectory)

        self.graph.display_data(calculate_graph(rifle, ammo, target, atmo, zerodata))

    def switch_view(self, index):
        if index == 0:
            self.stacked.setCurrentWidget(self.table)
        elif index == 1:
            self.stacked.setCurrentWidget(self.reticle)
        elif index == 2:
            self.stacked.setCurrentWidget(self.graph)

    def connect_ui(self, trajWidget):
        self.viewCmb.currentIndexChanged.connect(self.switch_view)
