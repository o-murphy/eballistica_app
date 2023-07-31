from PySide6 import QtWidgets, QtCore
from py_ballisticcalc.drag import DragTableG1, DragTableG7
from py_ballisticcalc.profile import Profile
from py_ballisticcalc.trajectory_data import TrajectoryData
from qt_material import QtStyleTools

from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, DragModel, AtmoData, TwistDir
from units import Distance, Weight, Angular, Velocity, Pressure, Temperature


def calculate_traj(rifle: RifleData, ammo: AmmoData, target: Target, atmo: AtmoData, zerodata: ZeroData):
    if ammo.drag_model == DragModel.G1:

        list = [i for i in ammo.bc_list if i[0] > 0 and i[1] > 0]
        dm_props = dict(bc_value=1, multiple_bc_table=list, drag_table=DragTableG1)
    elif ammo.drag_model == DragModel.G7:
        list = [i for i in ammo.bc7_list if i[0] > 0 and i[1] > 0]
        dm_props = dict(bc_value=1, multiple_bc_table=list, drag_table=DragTableG7)
    else:
        dm_props = dict(bc_value=1, custom_drag_function=ammo.cdm_list, drag_table=None)

    shot_props = dict(
        bullet_diameter=(ammo.diameter, Distance.Inch),
        bullet_length=(ammo.length, Distance.Inch),
        bullet_weight=(ammo.weight, Weight.Grain),
        muzzle_velocity=(ammo.muzzle_velocity, Velocity.MPS),
        # altitude=(atmo.altitude, Angular.Degree),
        pressure=(atmo.pressure, Pressure.MmHg),
        temperature=(atmo.temperature, Temperature.Celsius),
        humidity=atmo.humidity,
        zero_distance=(zerodata.zero_range, Distance.Meter),
        twist=(rifle.barrel_twist, Distance.Inch),
        twist_direction=1 if rifle.barrel_twist_dir == TwistDir.Right else 2,
        sight_height=(rifle.sight_height, Distance.Centimeter),
        maximum_distance=(target.distance+1, Distance.Meter),
        distance_step=(zerodata.zero_range // 2, Distance.Meter),
        wind_velocity=(atmo.wind_speed, Velocity.MPS),
        wind_direction=(atmo.wind_angle, Angular.Degree),
        shot_angle=(target.look_angle, Angular.Degree),
    )

    print(shot_props)

    profile = Profile(**dm_props, **shot_props)
    data = []
    p: TrajectoryData
    for p in profile.calculate_trajectory():
        data.append((
            round(p.travelled_distance().get_in(Distance.Meter)),
            round(p.drop().get_in(Distance.Centimeter), Distance.accuracy(Distance.Centimeter)),
            round(p.drop_adjustment().get_in(Angular.Mil), Angular.accuracy(Angular.Mil)) if p.drop_adjustment() else 0,
            round(p.windage().get_in(Distance.Centimeter), Distance.accuracy(Distance.Centimeter)),
            round(p.windage_adjustment().get_in(Angular.Mil), Angular.accuracy(Angular.Mil)) if p.windage_adjustment() else 0,
            round(p.velocity().get_in(Velocity.MPS), Velocity.accuracy(Velocity.MPS))
        ))
    return data


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
        self.headers = ['Range', 'Drop\nin', 'Path\nmoa', 'Windage\nMIL', 'Windage\nMIL', 'Velocity']
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
