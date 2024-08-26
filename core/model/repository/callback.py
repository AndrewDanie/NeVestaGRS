
from model.repository.ORMModels import *


def get_grs_name_set():
    statement = select(GRS.name)
    name_set = Base.session.scalars(statement).fetchall()
    return name_set


def get_composition_set_by_grs_name(name):
    statement = select(Composition).where(Composition.grs_id.in_(
        Base.session.query(GRS.id).filter(GRS.name.in_([name])).subquery()
    ))
    comp_obj = Base.session.execute(statement).one()[0]

    composition_set = {
        'Methane': comp_obj.methane,
        'Ethane': comp_obj.ethane,
        'Propane': comp_obj.propane,
        'Isobutane': comp_obj.isobutane,
        'Butane': comp_obj.butane,
        'Isopentane': comp_obj.isopentane,
        'Pentane': comp_obj.pentane,
        'Hexane': comp_obj.hexane,
        'Oxygen': comp_obj.oxygen,
        'Nitrogen': comp_obj.nitrogen,
        'CarbonDioxide': comp_obj.carbon_dioxide,
    }
    print(composition_set)
    return composition_set