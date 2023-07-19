import dataclasses
from enum import IntFlag


@dataclasses.dataclass
class RifleData:

    __slots__ = ('name', 'barrel_twist', 'barrel_twist_dir', 'sight_height', 'sight_offset')

    name: str
    barrel_twist: float
    barrel_twist_dir: float
    sight_height: float
    sight_offset: float


class DragModel(IntFlag):
    G1 = 0
    G7 = 1
    CDM = 2


@dataclasses.dataclass
class BulletData:

    __slots__ = ('name', 'diameter', 'weight', 'length', 'muzzle_velocity', 'temp_sens', 'powder_temp',
                 'drag_model', 'bc', 'zero_range', 'zero_height', 'zero_offset', 'is_zero_atmo', 'altitude',
                 'pressure', 'temperature', 'humidity')

    name: str
    diameter: float
    weight: float
    length: float
    muzzle_velocity: float
    temp_sens: float
    powder_temp: float
    drag_model: DragModel
    bc: float
    zero_range: float
    zero_height: float
    zero_offset: float
    is_zero_atmo: bool
    altitude: float
    pressure: float
    temperature: float
    humidity: float
