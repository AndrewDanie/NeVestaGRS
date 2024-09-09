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
    season = window.get_data('combobox.season')
    seasons = {
        'Зима' : 1,
        'Весна' : 2,
        'Лето' : 3,
        'Осень' : 4
    }
    season_id = None
    if season in seasons:
        season_id = seasons[season]
    plot_wgt = window.widgets['plot']['plot']
    canvas = window.widgets['plot']['canvas']
    df = getattr(db, 'get_statistic_data_by_outlet_name')(window.widgets['combobox']['outlet'].widget.get(), season_id)
    if df is not None and not df.empty:
        plot_wgt.cla()

        plot_wgt.set_title('Plot 1: 1st degree curve', fontsize=15)
        y_axis = window.widgets['combobox']['quantity'].widget.get()
        plot_wgt.set_ylabel(y_axis)

        width = 30
        average = df[y_axis].rolling(width, center=True).mean()
        variance = df[y_axis].rolling(width, center=True).std()
        _3_sigma = 3 * variance
        df['upper_3_sigma'] = average + _3_sigma
        df['lower_3_sigma'] = average - _3_sigma
        df['average'] = df[y_axis].rolling(width, center=True).mean()
        df['variance'] = df[y_axis].rolling(width, center=True).std()
        y_data = df[y_axis]
        df.plot(x='date', y=[y_axis, 'average','upper_3_sigma', 'lower_3_sigma'], ax=plot_wgt)
        # plot_wgt.get_legend().remove()
        #
        # plot_wgt.plot(y_data, 'b-')
        # plot_wgt.plot(average, 'r-')
        plot_wgt.grid(linestyle=':')
        canvas.draw()