## https://gallery.pyecharts.org/#/Map/README
## https://pyecharts.org/#/zh-cn/intro
import json
import ssl

import numpy as np
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Bar, Grid, Map, Geo
from pyecharts.datasets import register_url
from pyecharts.faker import Faker
from pyecharts.globals import GeoType, ThemeType, ChartType, SymbolType
from pyecharts.render import make_snapshot

# load nanjing geojson
with open("nanjing.json", 'r', encoding='utf-8') as f:
    nanjing_geo = json.loads(f.read())

# read covid data
infection_frame = pd.read_csv('data.csv', header=0)
infection_map = dict(zip(infection_frame['district'], infection_frame['number']))
infection_list = list(zip(infection_frame['district'], infection_frame['number']))

data_range = [0, 100]

geo = Geo()  # width, height

# 注册地图类型为NanJing
geo.add_js_funcs("echarts.registerMap('NanJing', {});".format(nanjing_geo))

# 绘制南京地图
geo.add_schema(
    maptype="南京",
    label_opts=opts.LabelOpts(is_show=False),
    itemstyle_opts={
        "normal": {
            "areaColor": "#323c48",
            "borderColor": "#404a59"
        },
        "emphasis": {
            "areaColor": "rgba(255,255,255, 0.5)",
        }
    }
)

# 对应刚才的地图类型：NanJing
geo.add(
    series_name="",
    data_pair=infection_list,
    type_=ChartType.EFFECT_SCATTER,
    color='blue'
)

geo.set_global_opts(
    title_opts=opts.TitleOpts(
    title="南京疫情分布情况",
    subtitle="",
    pos_left="center",
    pos_top="top",
    title_textstyle_opts=opts.TextStyleOpts(font_size=25,
                                            color="rgba(255,255,255, 0.9)"),
    ),
    visualmap_opts=opts.VisualMapOpts(
        dimension=0,
        pos_left='left',
        pos_top='center',
        min_=data_range[0],
        max_=data_range[1],
        is_calculable=True,
        range_color=['lightskyblue', 'yellow', 'orangered'],
        textstyle_opts=opts.TextStyleOpts(color="#ddd")))

bar_x_data = [x[0] for x in infection_list]
# 这里注释的部分会导致 label 和 value 与 饼图不一致
# 使用下面的 List[Dict] 就可以解决这个问题了。
# bar_y_data = [x[1][0] for x in map_data]
bar_y_data = [{"name": x[0], "value": x[1]} for x in infection_list]
bar = Bar()
bar.add_xaxis(xaxis_data=bar_x_data)
bar.add_yaxis(
    series_name="",
    y_axis=bar_y_data,
    label_opts=opts.LabelOpts(is_show=True,
                              position="right",
                              formatter="{b}: {c}"),
)
bar.reversal_axis()
bar.set_global_opts(
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
    yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
    tooltip_opts=opts.TooltipOpts(is_show=False),
    visualmap_opts=opts.VisualMapOpts(
        is_calculable=True,
        dimension=0,
        pos_left="10",
        pos_top="top",
        range_text=["High", "Low"],
        range_color=["lightskyblue", "yellow", "orangered"],
        textstyle_opts=opts.TextStyleOpts(color="#ddd"),
        min_=data_range[0],
        max_=data_range[1],
    ))

grid_chart = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
grid_chart.add(
    bar,
    grid_opts=opts.GridOpts(pos_left="20",
                            pos_right="70%",
                            pos_top="40%",
                            pos_bottom="20"),
)
grid_chart.add(geo, grid_opts=opts.GridOpts())

geo.render_notebook()
#geo.render("tmp.html")
#grid_chart.render_notebook()
# 目前这个render html不行，无法使用自定义的类型，只能使用自建的南京，但南京的数据有误
#grid_chart.render('tmp.html')
