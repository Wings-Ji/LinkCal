from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType

c = (
    Geo(init_opts = opts.InitOpts(width = '1000px',
                                  height='600px'))
    .add_schema(maptype="china",
                is_roam=False)
    .add(
        series_name = "geo",
        data_pair = [['北京',28],['江苏',24]],
        type_=ChartType.EFFECT_SCATTER,
        symbol_size = 60,
        color="#FF0000",
        )
    .add(
        series_name = "geo1",
        data_pair = [['北京',28],['江西',24]],
        type_=ChartType.EFFECT_SCATTER,
        symbol_size = 50,
        color='#FFA500')
    .add(
        series_name = "geo2",
        data_pair = [['北京',28],['江西',24]],
        type_=ChartType.EFFECT_SCATTER,
        symbol_size = 20,
        color='#FFE4B5')#FF0000

    .set_series_opts(label_opts=opts.LabelOpts(is_show=False),)
    .set_global_opts(title_opts=opts.TitleOpts(title="Geo-EffectScatter"),
                     # datazoom_opts = [opts.DataZoomOpts(is_zoom_lock = True)],
                     )
    .render("geo_effectscatter.html")
)
