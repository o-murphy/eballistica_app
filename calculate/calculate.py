from py_ballisticcalc.drag import DragTableG1, DragTableG7, BallisticCoefficient
from py_ballisticcalc.multiple_bc import MultipleBallisticCoefficient
from py_ballisticcalc.shot_parameters import ShotParametersUnlevel
from py_ballisticcalc.trajectory_data import TrajectoryData
from py_ballisticcalc.trajectory_calculator import TrajectoryCalculator
from py_ballisticcalc.projectile import ProjectileWithDimensions, Ammunition
from py_ballisticcalc.weapon import ZeroInfoWithAmmoAndAtmo, TwistInfo, TwistLeft, TwistRight, WeaponWithTwist
from py_ballisticcalc.atmosphere import Atmosphere
from py_ballisticcalc.wind import create_only_wind_info

from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, DragModel, AtmoData, TwistDir
from units import Distance, Weight, Angular, Velocity, Pressure, Temperature


def bc_g7(ammo: AmmoData):
    list = [(i[1], i[0]) for i in ammo.bc7_list if i[0] > 0 and i[1] > 0]
    bc = MultipleBallisticCoefficient(
        DragTableG7,
        Distance(ammo.diameter, Distance.Inch),
        Weight(ammo.weight, Weight.Grain),
        list,
        Velocity.MPS
    )

    return bc.custom_drag_func()


def bc_g1(ammo: AmmoData):
    list = [(i[1], i[0]) for i in ammo.bc7_list if i[0] > 0 and i[1] > 0]
    bc = MultipleBallisticCoefficient(
        DragTableG1,
        Distance(ammo.diameter, Distance.Inch),
        Weight(ammo.weight, Weight.Grain),
        list,
        Velocity.MPS
    )

    return bc.custom_drag_func()


def cdm(ammo: AmmoData):
    bc = BallisticCoefficient(
        value=0,
        drag_table=0,
        weight=Weight(ammo.weight, Weight.Grain),
        diameter=Distance(ammo.diameter, Distance.Inch),
        custom_drag_table=ammo.cdm
    )

    return bc


def calculate_pro(rifle: RifleData, ammo: AmmoData, target: Target, atmo: AtmoData, zerodata: ZeroData):

    calc = TrajectoryCalculator()

    if ammo.drag_model == DragModel.G1:
        cdm = bc_g1(ammo)
    elif ammo.drag_model == DragModel.G7:
        cdm = bc_g7(ammo)
    else:
        cdm = ammo.cdm

    bc = BallisticCoefficient(
        value=0,
        drag_table=0,
        weight=Weight(ammo.weight, Weight.Grain),
        diameter=Distance(ammo.diameter, Distance.Inch),
        custom_drag_table=cdm
    )

    projectile = ProjectileWithDimensions(
        bc,
        Distance(ammo.diameter, Distance.Inch),
        Distance(ammo.length, Distance.Inch),
        Weight(ammo.weight, Weight.Grain)
    )

    ammunition = Ammunition(projectile, Velocity(ammo.muzzle_velocity, Velocity.MPS))
    zero_atmo = Atmosphere(
        Distance(zerodata.altitude, Distance.Meter),
        Pressure(zerodata.pressure, Pressure.MmHg),
        Temperature(zerodata.temperature, Temperature.Celsius),
        humidity=zerodata.humidity
    )

    zero_info = ZeroInfoWithAmmoAndAtmo(
        Distance(zerodata.zero_range, Distance.Meter),
        ammunition, zero_atmo
    )

    twist_info = TwistInfo(
        TwistRight if rifle.barrel_twist_dir == TwistDir.Right else TwistLeft,
        Distance(rifle.barrel_twist, Distance.Inch)
    )

    weapon = WeaponWithTwist(
        Distance(rifle.sight_height, Distance.Centimeter),
        zero_info, twist_info
    )

    atmosphere = Atmosphere(
        Distance(atmo.altitude, Distance.Meter),
        Pressure(atmo.pressure, Pressure.MmHg),
        Temperature(atmo.temperature, Temperature.Celsius),
        humidity=atmo.humidity
    )

    sight_angle = calc.sight_angle(ammunition, weapon, atmosphere)

    shot_info = ShotParametersUnlevel(
        sight_angle,
        maximum_distance=Distance(target.distance+1, Distance.Meter),
        step=Distance(zerodata.zero_range // 2, Distance.Meter),
        shot_angle=Angular(target.look_angle, Angular.Degree),
        cant_angle=Angular(0, Angular.Degree)
    )

    wind = create_only_wind_info(
        wind_velocity=Velocity(atmo.wind_speed, Velocity.MPS),
        direction=Angular(atmo.wind_angle, Angular.Degree),
    )

    data = calc.trajectory(ammunition, weapon, atmosphere, shot_info, wind)

    return data


def calculate_graph(trajectory):

    p: TrajectoryData

    return [
        (
            round(p.travelled_distance().get_in(Distance.Meter)),
            round(p.drop().get_in(Distance.Centimeter), Distance.accuracy(Distance.Centimeter))
        ) for p in trajectory
    ]


def calculate_traj(trajectory):

    data = []

    p: TrajectoryData
    for p in trajectory:
        data.append((
            round(p.travelled_distance().get_in(Distance.Meter)),
            round(
                p.drop_adjustment().get_in(Angular.CmPer100M), Angular.accuracy(Angular.CmPer100M)
            ) if p.drop_adjustment() else '---',
            round(
                p.drop_adjustment().get_in(Angular.Mil), Angular.accuracy(Angular.Mil)
            ) if p.drop_adjustment() else '---',
            round(
                p.windage_adjustment().get_in(Angular.CmPer100M), Angular.accuracy(Angular.CmPer100M)
            ) if p.windage_adjustment() else '---',
            round(
                p.windage_adjustment().get_in(Angular.Mil), Angular.accuracy(Angular.Mil)
            ) if p.windage_adjustment() else '---',
            round(p.velocity().get_in(Velocity.MPS), Velocity.accuracy(Velocity.MPS))
        ))
    return data
