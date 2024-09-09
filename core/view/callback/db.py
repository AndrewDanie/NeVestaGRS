from locale import windows_locale

import pandas as pd
from core.model.repository.Model import *
from core.util.ConfigCache import ConfigCache
from sqlalchemy.sql import extract
from sqlalchemy import or_


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
        Base.session.query(GRS.id).filter(GRS.name.in_([name]))
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
    window = ConfigCache.get_cache().get('window')
    name = window.get_data('combobox.composition')

    if name is None or name == '':
        return
    statement = select(GRSOutlet.name_output).where(GRSOutlet.grs_id.in_(
        Base.session.query(GRS.id).filter(GRS.name.in_([name]))
    )).distinct()
    outlet_set = Base.session.execute(statement).fetchall()
    outlet_set = [x[0] for x in outlet_set]
    if len(outlet_set) > 1:
        outlet_set.insert(0, 'Вход')
    return outlet_set


def get_statistic_data_by_outlet_name(name, season_id):
    statement = select(GRSOutletStatistic).where(GRSOutletStatistic.outlet_id.in_(
        Base.session.query(GRSOutlet.id).filter(GRSOutlet.name_output.in_([name]))
    ))
    if season_id is not None:
        i = season_id
        month_ids = [(i*3 - 4) % 12 + 1, i*3 - 2, i*3 - 1]
        extracted = extract('month', GRSOutletStatistic.date)
        statement = statement.filter(extracted.in_(month_ids))
    df = pd.read_sql(statement, Base.session.bind)
    return df

def load_combobox_config_by_name(name):
    statement = select(Combobox.values_getter).where(Combobox.name.in_([name]))
    callback_name = Base.session.execute(statement).fetchone()[0]
    return callback_name
