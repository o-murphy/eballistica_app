import enum
import json

from sqlalchemy import create_engine, Column, Integer, Float, String, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, mapped_column, validates

Base = declarative_base()
engine = create_engine('sqlite:///local.sqlite3', echo=False)


class TwistDir(enum.IntEnum):
    Right = 0
    Left = 1


class DragModel(enum.IntEnum):
    G1 = 0
    G7 = 1
    CDM = -1


class RifleData(Base):
    __tablename__ = 'rifle'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    barrel_twist = Column(Float, nullable=False, default=9)
    barrel_twist_dir = Column(Enum(TwistDir), nullable=False, default=TwistDir.Right)
    sight_height = Column(Float, nullable=False, default=90)
    sight_offset = Column(Float, nullable=False, default=9)

    ammo = relationship("AmmoData", back_populates='rifle', cascade="all, delete-orphan")

    def __init__(self, name='', barrel_twist=9, barrel_twist_dir=TwistDir.Right, sight_height=90,
                 sight_offset=9, **kwargs):
        super(RifleData, self).__init__(name=name, barrel_twist=barrel_twist, barrel_twist_dir=barrel_twist_dir,
                                        sight_height=sight_height, sight_offset=sight_offset, **kwargs)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class AmmoData(Base):
    __tablename__ = 'ammo'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    diameter = Column(Float, nullable=False, default=0.338)
    weight = Column(Float, nullable=False, default=300)
    length = Column(Float, nullable=False, default=1.5)
    muzzle_velocity = Column(Float, nullable=False, default=800)
    temp_sens = Column(Float, nullable=False, default=1)
    powder_temp = Column(Float, nullable=False, default=15)
    drag_model = Column(Enum(DragModel), nullable=False, default=DragModel.G7)

    bc = Column(Float, nullable=True, default=0.600)
    bc7 = Column(Float, nullable=True, default=0.381)
    cd = Column(String, nullable=True, default='[]')
    mach = Column(String, nullable=True, default='[]')

    rifle_id = mapped_column(ForeignKey("rifle.id", ondelete="CASCADE"), nullable=False)
    rifle = relationship("RifleData", back_populates="ammo")

    zerodata = relationship("ZeroData", back_populates="ammo", uselist=False, cascade="all, delete-orphan")
    target = relationship("Target", back_populates="ammo", uselist=False, cascade="all, delete-orphan")
    atmo = relationship("AtmoData", back_populates="ammo", uselist=False, cascade="all, delete-orphan")

    def __init__(self, name, diameter=0.338, weight=300, length=1.5, muzzle_velocity=800, temp_sens=1, powder_temp=15,
                 drag_model=DragModel.G7, bc=0.381, rifle=None, **kwargs):
        super(AmmoData, self).__init__(name=name, diameter=diameter, weight=weight, length=length,
                                       muzzle_velocity=muzzle_velocity, temp_sens=temp_sens, powder_temp=powder_temp,
                                       drag_model=drag_model, bc=bc, **kwargs)

        if rifle is None:
            raise ValueError("AmmoData must be associated with a RifleData.")

        self.rifle = rifle
        self.zerodata = ZeroData(ammo=self)
        self.target = Target(ammo=self)
        self.atmo = AtmoData(ammo=self)

    def get_cd(self):
        return json.loads(self.cd)  # Deserialize the JSON to retrieve the list.

    def set_cd(self, value):
        self.cd = json.dumps(value)  # Serialize the list to JSON.

    def get_mach(self):
        return json.loads(self.mach)  # Deserialize the JSON to retrieve the list.

    def set_mach(self, value):
        self.mach = json.dumps(value)  # Serialize the list to JSON.

    cd_list = property(get_cd, set_cd)
    mach_list = property(get_mach, set_mach)

    @validates('rifle_id')
    def validate_rifle_id(self, key, rifle_id):
        with Session() as session:
            if not session.query(RifleData).filter_by(id=rifle_id).scalar():
                raise ValueError(f"RifleData with ID {rifle_id} does not exist in the database.")
        return rifle_id

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class ZeroData(Base):
    __tablename__ = 'zerodata'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    zero_range = Column(Float, nullable=False, default=100)
    zero_height = Column(Float, nullable=False, default=90)
    zero_offset = Column(Float, nullable=False, default=0)
    is_zero_atmo = Column(Boolean, nullable=False, default=True)
    altitude = Column(Float, nullable=False, default=0)
    pressure = Column(Float, nullable=False, default=760)
    temperature = Column(Float, nullable=False, default=15)
    humidity = Column(Float, nullable=False, default=50)

    ammo_id = mapped_column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="zerodata")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

    @validates('ammo_id')
    def validate_ammo_id(self, key, ammo_id):
        with Session() as session:
            if not session.query(AmmoData).filter_by(id=ammo_id).scalar():
                raise ValueError(f"AmmoData with ID {ammo_id} does not exist in the database.")
        return ammo_id


class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    distance = Column(Float, nullable=False, default=1000)
    look_angle = Column(Float, nullable=False, default=0)
    move_speed = Column(Float, nullable=False, default=0)
    move_angle = Column(Float, nullable=False, default=0)

    ammo_id = mapped_column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="target")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

    @validates('ammo_id')
    def validate_ammo_id(self, key, ammo_id):
        with Session() as session:
            if not session.query(AmmoData).filter_by(id=ammo_id).scalar():
                raise ValueError(f"AmmoData with ID {ammo_id} does not exist in the database.")
        return ammo_id


class AtmoData(Base):
    __tablename__ = 'atmo'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    altitude = Column(Float, nullable=False, default=0)
    pressure = Column(Float, nullable=False, default=760)
    temperature = Column(Float, nullable=False, default=15)
    humidity = Column(Float, nullable=False, default=50)
    wind_speed = Column(Float, nullable=False, default=0)
    wind_angle = Column(Float, nullable=False, default=0)

    ammo_id = mapped_column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="atmo")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)

    @validates('ammo_id')
    def validate_ammo_id(self, key, ammo_id):
        with Session() as session:
            if not session.query(AmmoData).filter_by(id=ammo_id).scalar():
                raise ValueError(f"AmmoData with ID {ammo_id} does not exist in the database.")
        return ammo_id


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


class Worker:
    @staticmethod
    def list_rifles(*args, **kwargs):
        with Session() as session:
            rifles = session.query(RifleData).all()
        return rifles

    @staticmethod
    def add_or_update(*args, **kwargs):
        with Session() as session:
            rifle = RifleData(*args, **kwargs)
            session.merge(rifle)
            session.commit()

    @staticmethod
    def delete_rifle(uid, *args, **kwargs):
        with Session() as session:
            rifle = session.get(RifleData, uid)
            session.delete(rifle)
            session.commit()
