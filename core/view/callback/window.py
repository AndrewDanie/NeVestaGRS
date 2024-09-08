from core.util.ConfigCache import ConfigCache
from core.view.callback import db


def update_outlet_combobox(e):
    window = ConfigCache.get_cache().get('window')
    outlet_combobox = window.widgets['combobox']['outlet'].widget
    values = db.get_outlet_set_by_grs_name()
    outlet_combobox['values'] = db.get_outlet_set_by_grs_name()
    if len(values) > 0:
        outlet_combobox.current(0)
    else:
        outlet_combobox.set('')


def draw_plot(e):
    window = ConfigCache.get_cache().get('window')
    plot_wgt = window.widgets['plot']['plot']
    canvas = window.widgets['plot']['canvas']
    df = getattr(db, 'get_statistic_data_by_outlet_name')(window.widgets['combobox']['outlet'].widget.get())
    if df is not None and not df.empty:
        plot_wgt.cla()
        y_axis = window.widgets['combobox']['quantity'].widget.get()
        df.plot(x='date', y=y_axis, ax=plot_wgt)
        canvas.draw()