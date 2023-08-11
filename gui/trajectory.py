import csv

import pyqtgraph as pg
from getqt import *
from qt_material import QtStyleTools

from calculate.calculate import calculate_traj, calculated_drag
from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, AtmoData
from gui.settings import SettingsWidget
from gui.widgets import GesturedTableView
from units import Distance, Angular, Velocity, Energy

pg.setConfigOption('background', '#31363B')
# pg.setConfigOption('foreground', '#4F5B62')


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


class TrajectoryTable(GesturedTableView, QtStyleTools):
    def __init__(self, parent=None):
        super(TrajectoryTable, self).__init__(parent)

        self.setupUi(self)
        # self.display_data()

    def setupUi(self, trajTable):
        super(TrajectoryTable, self).setupUi(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalHeader().setHidden(True)
        self.setSelectionMode(GesturedTableView.SelectionMode.NoSelection)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        extra = dict(density_scale=-1)
        self.apply_stylesheet(self, extra=extra, theme='dark_blue.xml')

        font = self.font()
        font.setPointSize(font.pointSize() - 2)
        self.horizontalHeader().setStyleSheet("QHeaderView::section { padding: 4px; font-size: 7pt;}")
        # self.horizontalHeader().setFont(font)

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def headers(self):
        settings = self.get_settings()
        headers = [
            f'Range\n{Distance.name(settings.distUnits.currentData())}',
            f'Path\n{Angular.name(Angular.CmPer100M)}',
            f'Path\n{Angular.name(settings.pathUnits.currentData())}',
            f'Wind.\n{Angular.name(Angular.CmPer100M)}',
            f'Wind.\n{Angular.name(settings.pathUnits.currentData())}',
            f'V\n{Velocity.name(settings.vUnits.currentData())}',
            f'Energy\n{Energy.name(settings.eUnits.currentData())}',
        ]
        return headers

    def display_data(self, data=None):
        data.sort(reverse=True)
        model = MyTableModel(data, self.headers())
        self.setModel(model)
        self.resizeColumnsToContents()

    def save_drag_table(self, data):
        riflename = self.window().edit_shot.rifle.name
        ammoname = self.window().edit_shot.ammo.name
        filename = f"{riflename}_{ammoname}"

        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', f'table_{filename}', filter="CSV (*.csv)"
        )
        if filename:
            with open(filename, 'unit_weight', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerows(data)

    def share(self):
        headers = [h.replace('\n', '_') for h in self.model()._headers.copy()]
        data = self.model()._data.copy()
        data.insert(0, headers)
        self.save_drag_table(data)


class TrajectoryGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TrajectoryGraph, self).__init__(parent)
        self.init_ui(self)
        # self.connect_ui(self)
        self.installEventFilter(self)

        self._drag = None

    def eventFilter(self, source, event):
        if source is self and event.type() == QtCore.QEvent.MouseButtonPress:
            widget = self.stacked.currentWidget()
            # if widget and isinstance(widget, PageWidget):
            widget_index = self.stacked.indexOf(widget)
            next_index = (widget_index + 1) % self.stacked.count()
            self.stacked.setCurrentIndex(next_index)
            return True

        return super().eventFilter(source, event)

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def init_ui(self, trajGraph):
        self.vLayout = QtWidgets.QVBoxLayout(self)

        self.stacked = QtWidgets.QStackedWidget(self)
        self.vLayout.addWidget(self.stacked)


        # Create a PlotWidget
        self.drop_plot = pg.PlotWidget(title='Drop at distance')
        self.drag_plot = pg.PlotWidget(title='Counted CDM')
        self.stacked.addWidget(self.drop_plot)
        self.stacked.addWidget(self.drag_plot)
    #
    # def connect_ui(self, trajGraph):
    #     for i in range(self.stacked.count()):
    #         page_widget = self.stacked.widget(i)
    #         page_widget.clicked.connect(lambda i=i: self.change_page(i))

    def change_page(self, index):
        self.stacked.setCurrentIndex(index)

    def display_data(self, drop, drag):
        self._drag = ((p['A'], p['B']) for p in drag)
        pen_color = '#008080'  # Custom pen color (red in this example)
        symbol_color = '#008080'

        # Add the data to the plot
        x = [p[0] for p in drop]
        y = [p[1] for p in drop]

        settings = self.get_settings()
        self.drop_plot.getAxis('bottom').setLabel(Distance.name(settings.distUnits.currentData()))
        self.drop_plot.getAxis('left').setLabel(Distance.name(settings.dropUnits.currentData()))

        self.drag_plot.getAxis('bottom').setLabel('mach')
        self.drag_plot.getAxis('left').setLabel('cd')

        self.drop_plot.plot(x, y, pen=pg.mkPen(color=pen_color, width=3), symbol='o', symbolBrush=symbol_color, symbolSize=5)

        x = [p['A'] for p in drag]
        y = [p['B'] for p in drag]

        self.drag_plot.plot(x, y, pen=pg.mkPen(color=pen_color, width=3), symbol='o', symbolBrush=symbol_color, symbolSize=5)

        self.drop_plot.setLabel('bottom')

        self.drop_plot.setMouseEnabled(x=False, y=False)
        self.drop_plot.setDisabled(True)
        self.drop_plot.showGrid(x=True, y=True)
        self.drop_plot.showAxis('bottom')
        self.drop_plot.showAxis('left')

        self.drag_plot.setMouseEnabled(x=False, y=False)
        self.drag_plot.setDisabled(True)
        self.drag_plot.showGrid(x=True, y=True)
        self.drag_plot.showAxis('bottom')
        self.drag_plot.showAxis('left')

        self.stacked.setCurrentWidget(self.drop_plot)

    def showContextMenu(self, pos=None):
        if pos is None:
            pos = self.mapFromGlobal(self.cursor().pos())

        context_menu = QtWidgets.QMenu(self)

        context_menu.addAction('Share drop graph', lambda: self.onContextMenuAction("ShareDropGraph"))
        context_menu.addAction('Share drag graph', lambda: self.onContextMenuAction("ShareDragGraph"))
        context_menu.addAction('Share drag table', lambda: self.onContextMenuAction("ShareDragTable"))
        context_menu.exec_(self.mapToGlobal(pos))

    def save_drop_graph(self):
        riflename = self.window().edit_shot.rifle.name
        ammoname = self.window().edit_shot.ammo.name
        filename = f"{riflename}_{ammoname}"
        if QT_BACKEND == QtBackend.PyQt5 or QT_BACKEND == QtBackend.PyQt6:
            self.screenshot = QtGui.QPixmap.grabWidget(self.drop_plot)
        else:
            self.screenshot = self.drop_plot.grab()
            self.painter = QtGui.QPainter(self.screenshot)
            self.painter.setPen(QtGui.QPen('white'))
            self.painter.drawText(QtCore.QPoint(30, 30), riflename)
            self.painter.drawText(QtCore.QPoint(30, 60), ammoname)
            del self.painter
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', f'drop_{filename}', filter="PNG (*.png)"
        )
        if filename:
            self.screenshot.save(filename)

    def save_drag_graph(self):
        riflename = self.window().edit_shot.rifle.name
        ammoname = self.window().edit_shot.ammo.name
        filename = f"{riflename}_{ammoname}"
        if QT_BACKEND == QtBackend.PyQt5 or QT_BACKEND == QtBackend.PyQt6:
            self.screenshot = QtGui.QPixmap.grabWidget(self.drag_plot)
        else:
            self.screenshot = self.drag_plot.grab()
            self.painter = QtGui.QPainter(self.screenshot)
            self.painter.setPen(QtGui.QPen('white'))
            self.painter.drawText(QtCore.QPoint(30, 30), riflename)
            self.painter.drawText(QtCore.QPoint(30, 60), ammoname)
            del self.painter
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', f'drag_{filename}', filter="PNG (*.png)"
        )
        if filename:
            self.screenshot.save(filename)

    def save_drag_table(self):
        riflename = self.window().edit_shot.rifle.name
        ammoname = self.window().edit_shot.ammo.name
        filename = f"{riflename}_{ammoname}"
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', f'drag_{filename}', filter="PNG (*.png)"
        )
        if filename:
            with open(filename, 'unit_weight', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['Mach', 'CD'])
                writer.writerows(self._drag)

    def onContextMenuAction(self, action):
        # Implement the code to handle context menu actions

        if action == "ShareDropGraph":
            self.save_drop_graph()
        elif action == 'ShareDragGraph':
            self.save_drag_graph()
        elif action == 'ShareDragTable':
            self.save_drag_table()

    def share(self):
        self.showContextMenu()


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
        self.viewCmb.addItem('Reticle', 1)
        self.viewCmb.addItem('Graph', 2)

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
        self.table.display_data(self.traj_in_units(trajectory))
        self.graph.display_data(self.drop_in_units(trajectory), calculated_drag(ammo))

    def get_settings(self) -> SettingsWidget:
        window = self.window()
        if window:
            settings: SettingsWidget = window.settings
            return settings

    def drop_in_units(self, trajectory):
        settings = self.get_settings()
        dist_units = settings.distUnits.currentData()
        drop_units = settings.dropUnits.currentData()

        return [
            (
                round(p.travelled_distance().get_in(dist_units)),
                round(p.drop().get_in(drop_units), Distance.accuracy(drop_units))
            ) for p in trajectory
        ]

    def traj_in_units(self, trajectory):
        data = []
        settings = self.get_settings()

        path_units = settings.pathUnits.currentData()
        def_path_units = Angular.CmPer100M
        v_units = settings.vUnits.currentData()
        e_units = settings.eUnits.currentData()

        for p in trajectory:
            data.append((
                round(p.travelled_distance().get_in(Distance.Meter)),
                round(
                    p.drop_adjustment().get_in(def_path_units), Angular.accuracy(def_path_units)
                ) if p.drop_adjustment() else '---',
                round(
                    p.drop_adjustment().get_in(path_units), Angular.accuracy(path_units)
                ) if p.drop_adjustment() else '---',
                round(
                    p.windage_adjustment().get_in(def_path_units), Angular.accuracy(def_path_units)
                ) if p.windage_adjustment() else '---',
                round(
                    p.windage_adjustment().get_in(path_units), Angular.accuracy(path_units)
                ) if p.windage_adjustment() else '---',
                round(p.velocity().get_in(v_units), Velocity.accuracy(v_units)),
                round(p.energy().get_in(e_units), Energy.accuracy(e_units))
            ))
        return data

    def switch_view(self, index):
        if index == 0:
            self.stacked.setCurrentWidget(self.table)
        elif index == 1:
            self.stacked.setCurrentWidget(self.reticle)
        elif index == 2:
            self.stacked.setCurrentWidget(self.graph)

    def share_clicked(self):

        if self.stacked.currentWidget() == self.table:
            self.table.share()
        elif self.stacked.currentWidget() == self.graph:
            self.graph.share()


    def connect_ui(self, trajWidget):
        self.viewCmb.currentIndexChanged.connect(self.switch_view)
