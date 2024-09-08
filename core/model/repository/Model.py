from typing import List
import datetime

import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):

    engine = db.create_engine('sqlite:///grs_database.db')
    session = Session(engine)


class Quantity(Base):
    """
    Настройки физических переменных
    """
    __tablename__ = "quantity"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    label_name: Mapped[str]
    unit: Mapped[str]
    convertion_order: Mapped[int]


class Combobox(Base):
    """
    Настройки переменных комбобокса
    """
    __tablename__ = "combobox"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    values_getter: Mapped[str]


class GRS(Base):
    __tablename__ = "grs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    company: Mapped[str]
    location: Mapped[str]
    capacity_before: Mapped[int]
    capacity_after: Mapped[int]
    inlet_design_pressure: Mapped[float]

    units: Mapped[List["GRSUnit"]] = relationship(cascade="all, delete-orphan")
    composition: Mapped[List["Composition"]] = relationship(cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (f"User(id={self.id!r}, "
                f"name={self.name!r}, "
                f"company={self.company!r}, "
                f"location={self.location!r}, "
                f"capacity_before={self.capacity_before!r}, "
                f"capacity_after={self.capacity_after!r}, "
                f"inlet_design_pressure={self.inlet_design_pressure!r},)"
            )


class GRSUnit(Base):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(primary_key=True)
    grs_id: Mapped["GRS"] = mapped_column(ForeignKey("grs.id"))
    name: Mapped[str]


class Composition(Base):
    __tablename__ = "composition"

    id: Mapped[int] = mapped_column(primary_key=True)
    grs_id: Mapped["GRS"] = mapped_column(ForeignKey("grs.id"))

    methane: Mapped[float]
    ethane: Mapped[float]
    propane: Mapped[float]
    isobutane: Mapped[float]
    butane: Mapped[float]
    isopentane: Mapped[float]
    pentane: Mapped[float]
    hexane: Mapped[float]
    oxygen: Mapped[float]
    nitrogen: Mapped[float]
    carbon_dioxide: Mapped[float]
    def __repr__(self) -> str:
        return (f"methane(id={self.methane!r}, "
                f"ethane={self.ethane!r}, "
                f"propane={self.propane!r}, "
                f"isobutane={self.isobutane!r}, "
            )


class GRSState(Base):
    __tablename__ = 'grs_statistic'

    id: Mapped[int] = mapped_column(primary_key=True)
    grs_id: Mapped["GRS"] = mapped_column(ForeignKey("grs.id"))

    name_output: Mapped[str]
    date: Mapped[datetime.datetime]
    nominal_capacity: Mapped[float]
    day_capacity: Mapped[float]
    hour_capacity: Mapped[float]
    pressure: Mapped[float]
    temperature: Mapped[float]
    actual_flow: Mapped[float]


if __name__ == '__main__':
    engine = db.create_engine('sqlite:///../../grs_database.db')
    Base.metadata.create_all(engine)
    conn = engine.connect()
    # comps = conn.execute(db.text("select * from grs_stat")).fetchall()
    #
    # session = Session(engine)
    # grses = session.scalars(select(GRS.name))
    # # for grs in grses:
    # #     print(grses.fetchall())
    # new_comps = []
    # for comp in comps:
    #     new_comp = GRS_state(
    #         grs_id=comp[1],
    #         name_output=comp[2],
    #         date=datetime.datetime.strptime(comp[3], "%Y-%m-%d %H:%M:%S"),
    #         nominal_capacity=comp[4],
    #         day_capacity=comp[5],
    #         hour_capacity=comp[6],
    #         pressure=comp[7],
    #         temperature=comp[8],
    #         actual_flow=comp[9],
    #     )
    #     new_comps.append(new_comp)
    #
    # session.add_all(new_comps)
    # session.commit()
    #
    # units = session.scalars(select(GRSUnit))
