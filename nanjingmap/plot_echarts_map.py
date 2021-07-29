import json
import ssl

import pyecharts.options as opts
from pyecharts.charts import Map
from pyecharts.render import make_snapshot
from pyecharts.globals import ThemeType
from pyecharts.faker import Faker
from pyecharts.datasets import register_url
from pyecharts.charts import Grid, Bar


import asyncio
from aiohttp import TCPConnector, ClientSession

# https://mapshaper.org/
async def get_json_data(url: str) -> dict:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()

# 下载南京地图
#nanjing = asyncio.run(
#    get_json_data(
#        url="https://geo.datav.aliyun.com/areas_v3/bound/320100_full.json"))

with open("nanjing.json", 'r', encoding='utf-8') as f:
    nanjing = json.loads(f.read())
#loop = asyncio.get_event_loop()
#nanjing = loop.run_until_complete(
#    get_json_data(
#        url="https://geo.datav.aliyun.com/areas_v3/bound/320100_full.json"))

# 与 pyecharts 注册，当画香港地图的时候，用 echarts-china-cities-js
# 这种方法的地图有偏差，弃用了
#ssl._create_default_https_context = ssl._create_unverified_context
#register_url("https://echarts-maps.github.io/echarts-china-cities-js")

data = [
    ['六合区', 0],
    ['浦口区', 0],
    ['玄武区', 1],
    ['白下区', 0],
    ['秦淮区', 1],
    ['建邺区', 1],
    ['鼓楼区', 0],
    ['下关区', 0],
    ['栖霞区', 1],
    ['雨花台区', 0],
    ['江宁区', 77],
    ['溧水区', 6],
    ['高淳区', 1]
]

data_range = [0, 100]

m = Map(init_opts=opts.InitOpts(theme=ThemeType.DARK))  # width, height

# 注册地图类型为NanJing
m.add_js_funcs("echarts.registerMap('NanJing', {});".format(nanjing))

# 对应刚才的地图类型：NanJing
m.add(
    series_name="",
    data_pair=data,
    maptype='NanJing',
    is_map_symbol_show=True,
    itemstyle_opts={
        "normal": {
            "areaColor": "#323c48",
            "borderColor": "#404a59"
        },
        "emphasis": {
            "areaColor": "rgba(255,255,255, 0.5)",
        }
    },
    label_opts=opts.LabelOpts(is_show=True),
)

m.set_global_opts(
    title_opts=opts.TitleOpts(
        title="南京疫情分布情况",
        subtitle="",
        pos_left="center",
        pos_top="top",
        title_textstyle_opts=opts.TextStyleOpts(
            font_size=25,
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
        textstyle_opts=opts.TextStyleOpts(color="#ddd")
    )
)

bar_x_data = [x[0] for x in data]
# 这里注释的部分会导致 label 和 value 与 饼图不一致
# 使用下面的 List[Dict] 就可以解决这个问题了。
# bar_y_data = [x[1][0] for x in map_data]
bar_y_data = [{"name": x[0], "value": x[1]} for x in data]
bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
bar.add_xaxis(xaxis_data=bar_x_data)
bar.add_yaxis(
        series_name="",
        y_axis=bar_y_data,
        label_opts=opts.LabelOpts(
            is_show=True, position="right", formatter="{b}: {c}"
        ),
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
    )
)
#把图片并排
grid_chart = Grid(init_opts=opts.InitOpts(theme=ThemeType.DARK))
grid_chart.add(
    bar,
    grid_opts=opts.GridOpts(
        pos_left="20",
        pos_right="70%",
        pos_top="40%",
        pos_bottom="20"),
)
grid_chart.add(
    m,
    grid_opts=opts.GridOpts()
)

#m.render_notebook()
#m.render("tmp.html")
grid_chart.render_notebook()
# 目前这个render html不行，无法使用自定义的类型，只能使用自建的南京，但南京的数据有误
#grid_chart.render('tmp.html')