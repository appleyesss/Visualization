1. Pyecharts (0.5, 1.0)

```shell
pip install pyecharts # 必备，这个装的是1.x新版

# 新版本没有自带js文件，可以自己搜索下载geojson，也可以用pip下载
# Geojson文件常用下载网址：http://datav.aliyun.com/tools/atlas/index.html#&lat=33.521903996156105&lng=104.29849999999999&zoom=4
pip install echarts-countries-pypkg
pip install echarts-china-provinces-pypkg
pip install echarts-china-cities-pypkg
pip install echarts-china-counties-pypkg
pip install echarts-china-misc-pypkg
pip install echarts-united-kingdom-pypkg

# 如果需要导出文件，需要以下包
pip install snapshot-selenium 
# 或者是
pip install snapshot-phantomjs
```

[pyecharts文档](https://pyecharts.org/#/zh-cn/intro)

[pyecharts example](https://gallery.pyecharts.org/#/Map/README)

[GeoJson下载网址](http://datav.aliyun.com/tools/atlas/index.html#&lat=33.521903996156105&lng=104.29849999999999&zoom=4)

1. Folium

```bash
pip install folium
# 或者
conda install folium -c conda-forge
```

[Folium官网文档](https://python-visualization.github.io/folium/index.html)

[Folium例子](https://python-visualization.github.io/folium/quickstart.html)

1. Plotly

推荐。Plotly可以快速画各种图，可以参考官网的例子，以及gallery中网友上传的例子，生态很丰富。可以本地使用，也可以在线使用上传到官网

```bash
pip install plotly
# 或者
conda install -c plotly plotly
```

[Plotly各种例子](https://plotly.com/python/)

1. Basemap(deprecated) -> Cartopy

Cartopy替代了basemap，更专注专业画地图，没有详细了解。