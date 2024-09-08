import pandas as pd
from core.model.repository.Model import *
from core.util.ConfigCache import ConfigCache


def get_grs_name_set():
    """
    Возвращает список ГРС
    """
    statement = select(GRS.name)
    name_set = Base.session.scalars(statement).fetchall()
    return name_set


def get_composition_set_by_grs_name(name):
    """
    Возвращает газовый состав по имени ГРС
    """
    if name is None or name == '':
        raise Exception('Выберите ГРС')
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
    return composition_set


def get_outlet_set_by_grs_name():
    """
    Возвращает список выходов по имени ГРС
    """
    name = ConfigCache.get_cache().get('window').get_data('combobox.composition')
    if name is None or name == '':
        return
    statement = select(GRSState.name_output).where(GRSState.grs_id.in_(
        Base.session.query(GRS.id).filter(GRS.name.in_([name])).subquery()
    )).distinct()
    outlet_set = Base.session.execute(statement).fetchall()
    outlet_set = [x[0] for x in outlet_set]

    return outlet_set


def get_statistic_data_by_outlet_name(name):
    statement = select(GRSState).where(GRSState.name_output.in_([name]))
    df = pd.read_sql(statement, Base.session.bind)
    return df

def load_combobox_config_by_name(name):
    statement = select(Combobox.values_getter).where(Combobox.name.in_([name]))
    callback_name = Base.session.execute(statement).fetchone()[0]
    return callback_name
