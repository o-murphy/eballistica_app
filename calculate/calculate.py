from statistics import median

from py_ballisticcalc.atmosphere import Atmosphere
from py_ballisticcalc.bmath.unit import *
from py_ballisticcalc.drag import DragTableG1, DragTableG7, BallisticCoefficient
from py_ballisticcalc.multiple_bc import MultipleBallisticCoefficient
from py_ballisticcalc.projectile import ProjectileWithDimensions, Ammunition
from py_ballisticcalc.shot_parameters import ShotParametersUnlevel
from py_ballisticcalc.trajectory_calculator import TrajectoryCalculator
from py_ballisticcalc.weapon import ZeroInfoWithAmmoAndAtmo, TwistInfo, TwistLeft, TwistRight, WeaponWithTwist
from py_ballisticcalc.wind import create_only_wind_info

from datatypes.dbworker import RifleData, AmmoData, ZeroData, Target, DragModel, AtmoData, TwistDir
# from units import Distance, Weight, Angular, Velocity, Pressure, Temperature


def bc_g7(ammo: AmmoData):
    list = [(i[1], i[0]) for i in ammo.bc7_list if i[0] > 0 and i[1] > 0]
    bc = MultipleBallisticCoefficient(
        DragTableG7,
        Distance(ammo.diameter, DistanceInch),
        Weight(ammo.weight, WeightGrain),
        list,
        int(VelocityMPS)
    )

    return bc.custom_drag_func()


def bc_g1(ammo: AmmoData):
    list = [(i[1], i[0]) for i in ammo.bc7_list if i[0] > 0 and i[1] > 0]
    bc = MultipleBallisticCoefficient(
        DragTableG1,
        Distance(ammo.diameter, DistanceInch),
        Weight(ammo.weight, WeightGrain),
        list,
        int(VelocityMPS)
    )

    return bc.custom_drag_func()


def cdm(ammo: AmmoData):
    bc = BallisticCoefficient(
        value=0,
        drag_table=0,
        weight=Weight(ammo.weight, WeightGrain),
        diameter=Distance(ammo.diameter, DistanceInch),
        custom_drag_table=ammo.cdm
    )

    return bc


def calculated_drag(ammo: AmmoData):
    if ammo.drag_model == DragModel.G1:
        cdm = bc_g1(ammo)
    elif ammo.drag_model == DragModel.G7:
        cdm = bc_g7(ammo)
    else:
        cdm = ammo.cdm
    return cdm


def calculate_traj(rifle: RifleData, ammo: AmmoData, target: Target, atmo: AtmoData, zerodata: ZeroData):
    calc = TrajectoryCalculator()

    cdm = calculated_drag(ammo)

    bc = BallisticCoefficient(
        value=0,
        drag_table=0,
        weight=Weight(ammo.weight, WeightGrain),
        diameter=Distance(ammo.diameter, DistanceInch),
        custom_drag_table=cdm
    )

    projectile = ProjectileWithDimensions(
        bc,
        Distance(ammo.diameter, DistanceInch),
        Distance(ammo.length, DistanceInch),
        Weight(ammo.weight, WeightGrain)
    )

    ammunition = Ammunition(projectile, Velocity(ammo.muzzle_velocity, VelocityMPS))
    zero_atmo = Atmosphere(
        Distance(zerodata.altitude, DistanceMeter),
        Pressure(zerodata.pressure, PressureMmHg),
        Temperature(zerodata.temperature, TemperatureCelsius),
        humidity=zerodata.humidity
    )

    zero_info = ZeroInfoWithAmmoAndAtmo(
        Distance(zerodata.zero_range, DistanceMeter),
        ammunition, zero_atmo
    )

    twist_info = TwistInfo(
        TwistRight if rifle.barrel_twist_dir == TwistDir.Right else TwistLeft,
        Distance(rifle.barrel_twist, DistanceInch)
    )

    weapon = WeaponWithTwist(
        Distance(rifle.sight_height, DistanceCentimeter),
        zero_info, twist_info
    )

    atmosphere = Atmosphere(
        Distance(atmo.altitude, DistanceMeter),
        Pressure(atmo.pressure, PressureMmHg),
        Temperature(atmo.temperature, TemperatureCelsius),
        humidity=atmo.humidity
    )

    sight_angle = calc.sight_angle(ammunition, weapon, atmosphere)

    shot_info = ShotParametersUnlevel(
        sight_angle,
        maximum_distance=Distance(target.distance + 1, DistanceMeter),
        step=Distance(zerodata.zero_range // 10, DistanceMeter),
        shot_angle=Angular(target.look_angle, AngularDegree),
        cant_angle=Angular(0, AngularDegree)
    )

    wind = create_only_wind_info(
        wind_velocity=Velocity(atmo.wind_speed, VelocityMPS),
        direction=Angular(atmo.wind_angle, AngularDegree),
    )

    data = calc.trajectory(ammunition, weapon, atmosphere, shot_info, wind)

    return cdm, data


def calculate_powder_sens(ret_list):

    def calculate_delta(v0, t0, v1, t1):
        # Step 1: Calculate the Temperature Difference
        temp_difference = t0 - t1

        # Step 2: Calculate the Speed Difference
        speed_difference = v0 - v1

        # Step 3: Calculate the Temperature Sensitivity Factor (TempModifier)
        temp_modifier = (speed_difference / temp_difference) * (15 / v0) * 100

        return temp_modifier

    coeffs = []
    for i in range(len(ret_list) - 1):
        t0, v0 = ret_list[i]
        t1, v1 = ret_list[i + 1]
        if v0 != 0 and v1 != 0:
            coeffs.append(calculate_delta(v0, t0, v1, t1))

    if len(coeffs) >= 1:
        val = round(median(coeffs), 3)
    else:
        val = None
    return val
