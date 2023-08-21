import json
from sqlalchemy import create_engine, Column, Integer, Float, String, Enum, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates


from datatypes.defines import TwistDir, DragModel

Base = declarative_base()
engine = create_engine('sqlite:///local.sqlite3', echo=False)



class RifleData(Base):
    __tablename__ = 'rifle'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    name = Column(String(32), nullable=False)
    barrel_twist = Column(Float, nullable=False, default=9)
    barrel_twist_dir = Column(Enum(TwistDir), nullable=False, default=TwistDir.Right)
    sight_height = Column(Float, nullable=False, default=9)

    ammo = relationship("AmmoData", back_populates='rifle', cascade="all, delete-orphan")

    def __init__(self, name='', barrel_twist=9, barrel_twist_dir=TwistDir.Right, sight_height=9,
                 **kwargs):
        super(RifleData, self).__init__(name=name, barrel_twist=barrel_twist, barrel_twist_dir=barrel_twist_dir,
                                        sight_height=sight_height, **kwargs)

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

    bc = Column(String, nullable=True, default='[[0, 0]]')
    bc7 = Column(String, nullable=True, default='[[0, 0]]')
    cdm = Column(String, nullable=True, default='[[0, 0]]')

    rifle_id = Column(ForeignKey("rifle.id", ondelete="CASCADE"), nullable=False)
    rifle = relationship("RifleData", back_populates="ammo")

    zerodata = relationship("ZeroData", back_populates="ammo", uselist=False, cascade="all, delete-orphan")
    target = relationship("Target", back_populates="ammo", uselist=False, cascade="all, delete-orphan")
    atmo = relationship("AtmoData", back_populates="ammo", uselist=False, cascade="all, delete-orphan")

    def __init__(self, name='', diameter=0.338, weight=300, length=1.5, muzzle_velocity=800, temp_sens=1, powder_temp=15,
                 drag_model=DragModel.G7, bc=None, bc7=None, cdm=None, rifle=None, **kwargs):
        super(AmmoData, self).__init__(name=name, diameter=diameter, weight=weight, length=length,
                                       muzzle_velocity=muzzle_velocity, temp_sens=temp_sens, powder_temp=powder_temp,
                                       drag_model=drag_model, bc=bc, bc7=bc7, cdm=cdm, **kwargs)

        if rifle is None:
            raise ValueError("AmmoData must be associated with a RifleData.")

        self.rifle = rifle
        self.zerodata = ZeroData(ammo=self)
        self.target = Target(ammo=self)
        self.atmo = AtmoData(ammo=self)

    def get_bc(self):
        return json.loads(self.bc) if self.bc else None

    def set_bc(self, value):
        self.bc = json.dumps(value)

    def get_bc7(self):
        return json.loads(self.bc7) if self.bc7 else None

    def set_bc7(self, value):
        self.bc7 = json.dumps(value)

    def get_cdm(self):
        return json.loads(self.cdm) if self.cdm else None  # Deserialize the JSON to retrieve the list.

    def set_cdm(self, value):
        self.cdm = json.dumps(value)  # Serialize the list to JSON.

    bc_list = property(get_bc, set_bc)
    bc7_list = property(get_bc7, set_bc7)
    cdm_list = property(get_cdm, set_cdm)

    @validates('rifle_id')
    def validate_rifle_id(self, key, rifle_id):
        # with Session() as session:
        #     if not session.query(RifleData).filter_by(id=rifle_id).scalar():
        #         raise ValueError(f"RifleData with ID {rifle_id} does not exist in the database.")
        if not session.query(RifleData).filter_by(id=rifle_id).scalar():
            raise ValueError(f"RifleData with ID {rifle_id} does not exist in the database.")
        return rifle_id

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class ZeroData(Base):
    __tablename__ = 'zerodata'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    zero_range = Column(Float, nullable=False, default=100)
    zero_height = Column(Float, nullable=False, default=9)
    is_zero_atmo = Column(Boolean, nullable=False, default=True)
    altitude = Column(Float, nullable=False, default=0)
    pressure = Column(Float, nullable=False, default=760)
    temperature = Column(Float, nullable=False, default=15)
    humidity = Column(Float, nullable=False, default=50)

    ammo_id = Column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="zerodata")

    def __init__(self, zero_range=100, zero_height=9, is_zero_atmo=True,
                 altitude=0, pressure=760, temperature=15, humidity=50, ammo=None):
        super(ZeroData, self).__init__(zero_range=zero_range, zero_height=zero_height,
                                       is_zero_atmo=is_zero_atmo, altitude=altitude, pressure=pressure,
                                       temperature=temperature, humidity=humidity, ammo=ammo)

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    distance = Column(Float, nullable=False, default=1000)
    look_angle = Column(Float, nullable=False, default=0)
    move_speed = Column(Float, nullable=False, default=0)
    move_angle = Column(Float, nullable=False, default=0)

    ammo_id = Column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="target")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class AtmoData(Base):
    __tablename__ = 'atmo'

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    altitude = Column(Float, nullable=False, default=0)
    pressure = Column(Float, nullable=False, default=760)
    temperature = Column(Float, nullable=False, default=15)
    humidity = Column(Float, nullable=False, default=50)
    wind_speed = Column(Float, nullable=False, default=0)
    wind_angle = Column(Float, nullable=False, default=0)

    ammo_id = Column(ForeignKey("ammo.id", ondelete="CASCADE"), nullable=False, unique=True)
    ammo = relationship("AmmoData", back_populates="atmo")

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

class Worker:

    @staticmethod
    def list_rifles(**kwargs):
        # with Session() as session:
        #     rifles = session.query(RifleData).filter_by(**kwargs)
        # return rifles
        # session = Session()
        rifles = session.query(RifleData).filter_by(**kwargs)
        return rifles

    @staticmethod
    def get_rifle(uid, **kwargs):
        # with Session() as session:
        #     rifle = session.query(RifleData).get(uid, **kwargs)
        # return rifle
        # session = Session()
        rifle = session.query(RifleData).get(uid, **kwargs)
        return rifle

    @staticmethod
    def get_ammo(uid, **kwargs):
        # session = Session()
        ammo = session.query(AmmoData).get(uid, **kwargs)
        return ammo

    @staticmethod
    def rifle_add_or_update(*args, **kwargs):
        # with Session() as session:
        #     rifle = RifleData(*args, **kwargs)
        #     rifle = session.merge(rifle)
        #     session.commit()
        # session = Session()
        rifle = RifleData(*args, **kwargs)
        rifle = session.merge(rifle)
        session.commit()
        return rifle

    @staticmethod
    def delete_rifle(uid, **kwargs):
        session = Session()
        rifle = session.query(RifleData).get(uid)
        session.delete(rifle)
        session.commit()

    @staticmethod
    def list_ammos(**kwargs):
        session = Session()
        ammos = session.query(AmmoData).filter_by(**kwargs)
        return ammos

    @staticmethod
    def ammo_add(ammo):
        # session.merge(ammo)
        session.add(ammo)
        session.commit()

    @staticmethod
    def commit():
        session.commit()

    @staticmethod
    def delete_ammo(uid, **kwargs):
        ammo = session.query(AmmoData).get(uid)
        session.delete(ammo)
        session.commit()

