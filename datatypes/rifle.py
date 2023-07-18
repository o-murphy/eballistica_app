import dataclasses


@dataclasses.dataclass
class RifleData:

    __slots__ = ('name', 'barrel_twist', 'barrel_twist_dir', 'sight_height', 'sight_offset')

    name: str
    barrel_twist: float
    barrel_twist_dir: float
    sight_height: float
    sight_offset: float

