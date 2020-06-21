# -*- coding: utf-8 -*- 
"""
Project: LinkCal
Creator: tianx
Create time: 2020-05-31 15:44
IDE: PyCharm
Introduction:
"""
import pandas as pd
import numpy as np
import folium, os, datetime, webbrowser
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster, BoatMarker
from pyecharts import options as opts
from pyecharts.charts import Geo
from example.commons import Faker
from pyecharts.globals import ChartType


def get_lat_log(cityname):
    fileName = 'Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName, 0, 0, usecols=[0, 1, 2,3])
    # print(data['CITY'] == cityname)
    print(data[data['CITY'] == cityname]['LON'].values[0])
    # print(type(data.iloc[1, :].values))

def createHeatMap():
    posi = pd.read_excel('heatData.xlsx')
    row_total = posi.shape[0] - 1
    lat = np.array(posi["lat"][0:row_total])  # 获取纬度值
    lon = np.array(posi["lon"][0:row_total])  # 获取经度值
    data1 = [[lat[i], lon[i]] for i in range(row_total)]  # 将数据制作成[lats,lons,weights]的形式
    map_osm = folium.Map(location=[30, 99], zoom_start=4)  # 绘制Map，开始缩放程度是5倍
   # HeatMap(data1).add_to(map_osm)  # 将热力图添加到前面建立的map里
    MarkerCluster(data1).add_to((map_osm))
    fileName2 = "热力图" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    file_path = os.path.join(r'C:\Users',os.getlogin(),'Desktop',fileName2)
    map_osm.save(file_path)  # 保存为html文件
    webbrowser.open(file_path)  # 默认浏览器打开

def geoHeatmap():
    c = (
        Geo()
            .add_schema(maptype="china")
            .add(
            "geo",
            [list(z) for z in zip(Faker.provinces, Faker.values())],
            type_=ChartType.HEATMAP,
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="Geo-HeatMap"),
        )
        .render('GeoHeatMap_test.html')
    )
    webbrowser.open('GeoHeatMap_test.html')  # 默认浏览器打开..

def scatterMap():
    pass


if __name__ == '__main__':
    # get_lat_log('天津')
    createHeatMap()
    # geoHeatmap()
