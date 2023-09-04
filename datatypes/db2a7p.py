from datetime import datetime

from a7p import A7PFactory, A7PFile, GType, profedit_pb2

from datatypes.dbworker import AmmoData, TwistDir
from datatypes.defines import DragModel
from units import Pressure


def drag_model2g_type(drag_model: DragModel):
    if drag_model == DragModel.G1:
        return GType.G1
    elif drag_model == DragModel.G7:
        return GType.G7
    elif drag_model == DragModel.CDM:
        return GType.CUSTOM


def curr_drag_model(ammo: AmmoData):
    if ammo.drag_model == DragModel.G1:
        return tuple(A7PFactory.DragPoint(p[1], p[0]) for p in ammo.bc_list)
    elif ammo.drag_model == DragModel.G7:
        return tuple(A7PFactory.DragPoint(p[1], p[0]) for p in ammo.bc7_list)
    elif ammo.drag_model == DragModel.CDM:
        return tuple(A7PFactory.DragPoint(p[1], p[0]) for p in ammo.cdm_list)


def ammo2a7p(ammo: AmmoData):
    payload = A7PFactory(
        meta=A7PFactory.Meta(
            name=f"{ammo.rifle.name} {ammo.name}",
            short_name_top='',
            short_name_bot='',
            user_note='Created with eBallistica app for Android',
        ),
        barrel=A7PFactory.Barrel(
            caliber='New caliber',
            sight_height=90,
            twist=9.,
            twist_dir=profedit_pb2.TwistDir.RIGHT
            if ammo.rifle.barrel_twist_dir == TwistDir.Right
            else profedit_pb2.TwistDir.LEFT,
        ),
        cartridge=A7PFactory.Cartridge(
            name=ammo.name,
            muzzle_velocity=ammo.muzzle_velocity,
            temperature=round(ammo.powder_temp),
            powder_sens=round(ammo.temp_sens)
        ),
        bullet=A7PFactory.Bullet(
            name="New bullet",
            diameter=ammo.diameter,
            weight=ammo.weight,
            length=ammo.length,
            drag_type=drag_model2g_type(ammo.drag_model),
            drag_model=curr_drag_model(ammo)
        ),
        zeroing=A7PFactory.Zeroing(
            distance=ammo.zerodata.zero_range,
        ),
        zero_atmo=A7PFactory.Atmosphere(
            temperature=round(ammo.zerodata.temperature),
            pressure=round(Pressure(ammo.zerodata.pressure, Pressure.MmHg).get_in(Pressure.HP)),
            humidity=round(ammo.zerodata.humidity)
        ),
        zero_powder_temp=round(ammo.zerodata.temperature),
        distances=A7PFactory.DistanceTable.LONG_RANGE,
    )
    return f'{ammo.rifle.name}-{ammo.name}-{datetime.now().strftime("%d-%m-%y--%H-%S")}.a7p', A7PFile.dumps(payload)
