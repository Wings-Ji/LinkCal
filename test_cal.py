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
import math


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

def createHeatMap2():
    posi = pd.read_excel('超级基站分布和经纬度.xls')
    row_total = posi.shape[0] - 1
    lat = np.array(posi["lat"][0:row_total])  # 获取纬度值
    lon = np.array(posi["lon"][0:row_total])  # 获取经度值
    data1 = [[lat[i], lon[i]] for i in range(row_total)]  # 将数据制作成[lats,lons,weights]的形式
    map_osm = folium.Map(location=[30, 99], zoom_start=4)  # 绘制Map，开始缩放程度是5倍
    HeatMap(data1).add_to(map_osm)  # 将热力图添加到前面建立的map里
    MarkerCluster(data1).add_to((map_osm))
    fileName2 = "超站热力图" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    file_path = os.path.join(r'C:\Users',os.getlogin(),'Desktop',fileName2)
    map_osm.save(file_path)  # 保存为html文件
    webbrowser.open(file_path)  # 默认浏览器打开

def getAtnDirect(sat_log, tr_st_log,tr_st_lat):
    Azimuth = 180-math.atan(math.tan((sat_log-tr_st_log)*0.01745)/math.sin(tr_st_lat*0.01745))/0.01745 #方位角
    Elevation = math.atan((math.cos(tr_st_lat*0.01745)*math.cos((sat_log-tr_st_log)*0.01745)-0.151)/math.sqrt(1-math.pow(math.cos(tr_st_lat*0.01745)*math.cos((sat_log-tr_st_log)*0.01745),2)))/0.01745   #俯仰角
    return Azimuth, Elevation

def getTotl_C_N(upC_N,DL_C_N,up_jh_Inf,up_lx_Inf,down_jh_Inf,down_lx_Inf,C_jt_Inf,):
    return 10 * math.log(1 / (1 / math.pow(10, upC_N / 10) + 1 / math.pow(10, DL_C_N / 10) +
                      1 / math.pow(10, up_jh_Inf / 10) + 1 / math.pow(10,up_lx_Inf / 10) +
                      1 / math.pow(10, down_jh_Inf/ 10) + 1 / math.pow(10, down_lx_Inf / 10) +
                      1 / math.pow(10, C_jt_Inf/ 10)), 10)  # 系统总C / N

if __name__ == '__main__':
    # get_lat_log('天津')
    # createHeatMap()
    # createHeatMap2()
    # geoHeatmap()

    print(getTotl_C_N(1,2,3,2,3,2,3))