# -*- coding: utf-8 -*-
"""
Project: LinkCal
Creator: tianx
Create time: 2020-01-04 21:15
IDE: PyCharm
Introduction:
"""
# from MainWindow import Ui_MainWindow as ui
import math, os, datetime, webbrowser, folium, copy
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import numpy as np
import pandas as pd
from folium.plugins import HeatMap
from  pyecharts.charts import Bar
from pyecharts import options as opts

def getVarDict(ui): #给全局变量（字典）赋值
    ui.varDict1['cityName'] = ui.ledit_bd_city.text()  # 本端发 站点名
    ui.varDict1['cityName_re'] = ui.ledit_dd_city.text()  # 对端收站点名
    #载波数据：
    infoRate_bd, infoRate_dd = getInfoRate(float(ui.ledit_bd_actualCarryingRate.text()),
                                           float(ui.ledit_bd_spendingRatio.text()),
                                           float(ui.ledit_dd_actualCarryingRate.text()),
                                           float(ui.ledit_bd_spendingRatio.text()))#信息速率
    ui.varDict1['infoRate'] = infoRate_bd  # 信息速率
    symbleRate_bd, symbleRate_dd = getSymbleRate(float(ui.ledit_bd_FECcode.text()),
                                                 float(ui.ledit_dd_FECcode.text()),
                                                 float(ui.ledit_bd_infoRate.text()),
                                                 float(ui.ledit_dd_infoRate.text()),
                                                 str(ui.cmbBox_bd_modu.currentText()),
                                                 str(ui.cmbBox_dd_modu.currentText()))#符号速率
    ui.varDict1['symbleRate'] = symbleRate_bd  # 符号速率
    ui.varDict1['CarNoiseBandwid'] = symbleRate_bd * 1.2 #载波噪声带宽 = 符号速率*要求的BT值：默认1.2
    ui.varDict1['CarBandwid'] = CarBandwid(symbleRate_bd,float(ui.ledit_bd_CarrierSpacingFactor.text()))#载波间隔
    #调制解调器数据：
    ui.varDict1['MX_errRt'] = float(ui.ledt_MX_errRt_dd.text())  # 门限误码率
    ui.varDict1['Eb_No'] = float(ui.ledt_dd_EbN0.text())  # 门限Eb/N0
    ui.varDict1['NoBdWid'] = 10*math.log(ui.varDict1['CarNoiseBandwid']*1000,10) #噪声带宽
    #卫星数据：
    ui.varDict1['erip_h'],ui.varDict1['erip_v'] = get_EIRP(ui.varDict1['cityName_re'])  # 转发器EIRP
    ui.varDict1['sat_log'] = float(ui.ledit_sat_log.text())  # 卫星定点经度
    ui.varDict1['sfd_h'],ui.varDict1['sfd_v'] = get_SFD(ui.varDict1['cityName'])  # 卫星饱和通量密度
    ui.varDict1['G_T'] = getGT(ui.varDict1['cityName'])#卫星G/T值
    ui.varDict1['zfq_bandwidth'] = float(ui.ledt_zfqwidth.text()) # 转发器带宽
    ui.varDict1['in_FB'] = float(ui.ledt_in_FB.text())  # 输入回退
    ui.varDict1['out_FB'] = float(ui.ledt_out_FB.text())  # 输出回退
    ui.varDict1['up_freq'] = float(ui.ledit_freq_tr_bd.text())  # 上行频率
    ui.varDict1['down_freq'] = float(ui.ledit_freq_Re_bd.text())  # 下行频率
    #接收系统数据：
    ui.varDict1['Atn_re_d'] = float(ui.ledt_atn_dd_d.text())  # 接收天线口径
    ui.varDict1['Atn_re_eff'] = float(ui.ledit_dd_Atnef.text())  # 接收天线效率
    ui.varDict1['Atn_re_Gain'] = 10*math.log(109.67*ui.varDict1['Atn_re_eff']*math.pow(ui.varDict1['down_freq'],2)*
                                             math.pow(ui.varDict1['Atn_re_d'],2),10)#接收天线增益
    ui.varDict1['Atn_re_JH'] = ui.coB_dd_re.text()  # 接收天线极化
    ui.varDict1['loss_f_lna'] = float(ui.ledt_loss_dd_lna.text())  # LNA前向损耗
    ui.varDict1['nT_lna'] = float(ui.ledt_t_n_dd_lna.text())  # LNA噪声温度
    ui.varDict1['nT_Atn'] = float(ui.ledt_t_n_dd.text())  # 天线噪声温度
    ui.varDict1['tol_NT'] = 10*math.log(ui.varDict1['nT_Atn']/math.pow(10,ui.varDict1['loss_f_lna']/10)+
                                        (1-1/math.pow(10,ui.varDict1['loss_f_lna']/10))*300+ui.varDict1['nT_lna'],10)#接收系统总噪声温度
    ui.varDict1['Re_GT'] = ui.varDict1['Atn_re_Gain']-ui.varDict1['loss_f_lna']-ui.varDict1['tol_NT']#接收系统G/T
    #站址数据：
    ui.varDict1['tr_sta_lat'], ui.varDict1['tr_sta_log'] = get_lat_log(city_Name=ui.varDict1['cityName'])  # 发射端地球站纬度、经度
    ui.varDict1['re_sta_lat'], ui.varDict1['re_sta_log'] = get_lat_log(city_Name=ui.varDict1['cityName_re'])  # 接收端站纬度、经度
    #链路损耗：
    ui.varDict1['loss_tr_err'] = float(ui.ledt_loss_err_bd.text())  # 发射端指向误差损耗
    ui.varDict1['loss_re_err'] = float(ui.ledt_loss_err_dd.text())  # 接收端指向误差损耗
    ui.varDict1['up_Atmph_loss'] = get_Atmph_loss(True, ui.varDict1['cityName'])  # 上行大气损耗
    ui.varDict1['down_Atmph_loss'] = get_Atmph_loss(False, ui.varDict1['cityName'])  #下行大气损耗
    ui.varDict1['UpFSpaceLoss'] = FSpaceLoss(ui.varDict1['up_freq'], ui.varDict1['tr_sta_lat'],
                                             ui.varDict1['sat_log'], ui.varDict1['tr_sta_log'])  # 上行自由空间损耗
    ui.varDict1['DownFSpaceLoss'] = FSpaceLoss(ui.varDict1['down_freq'], ui.varDict1['re_sta_lat'],
                                             ui.varDict1['sat_log'], ui.varDict1['re_sta_log'])  # 下行自由空间损耗
    #发射系统数据：
    ui.varDict1['Atn_tr_eff'] = float(ui.ledit_bd_Atnef.text())  # 发射天线效率
    ui.varDict1['Atn_tr_d'] = float(ui.ledt_atn_bd_d.text())  # 发射天线口径
    ui.varDict1['p_HPA'] = 15.8141194133667  # HPA要求功率/载波   ????????
    ui.varDict1['loss_Amplifier2feed'] = float(ui.ledt_loss_Amplifier2feed_bd.text())  # 功放至馈源间损耗
    ui.varDict1['AntTrGain'] = getAntTrGain(ui.varDict1['Atn_tr_eff'], ui.varDict1['up_freq'], ui.varDict1['Atn_tr_d'])#天线发射增益
    #上行链路数据：
    ui.varDict1['earthStationEIRP'] = getearthStationEIRP(ui.varDict1['AntTrGain'],ui.varDict1['p_HPA'],
                                                          ui.varDict1['loss_tr_err'],ui.varDict1['loss_Amplifier2feed'])# 地球站EIRP
    ui.varDict1['TotUpPathLoss'] = ui.varDict1['UpFSpaceLoss'] + ui.varDict1['up_Atmph_loss']  # 总上行线路径损耗
    ui.varDict1['upC_N'] =  ui.varDict1['earthStationEIRP']-ui.varDict1['TotUpPathLoss']-ui.varDict1['loss_tr_err']+\
                            ui.varDict1['G_T']+228.6-ui.varDict1['NoBdWid']-0  #上行C/N
    #转发器数据：
    ui.varDict1['antUnitAreaGain'] = 10 * math.log(400 * math.pi * math.pow(ui.varDict1['up_freq'], 2) / 9, 10)  # 天线单位面积增益
    ui.varDict1['CarFluDens'] = ui.varDict1['earthStationEIRP'] - ui.varDict1['TotUpPathLoss'] - \
                                ui.varDict1['loss_tr_err'] + ui.varDict1['antUnitAreaGain']   # 载波通量密度
    ui.varDict1['In_FBpCarrier'] = ui.varDict1['sfd_h'] - ui.varDict1['CarFluDens']  # 每载波输入回退
    ui.varDict1['Out_FBpCarrier'] = ui.varDict1['In_FBpCarrier'] - ui.varDict1['in_FB'] + ui.varDict1['out_FB']  # 每载波输出回退
    ui.varDict1['Rpt_out_PpCarrier'] = ui.varDict1['erip_h'] - ui.varDict1['Out_FBpCarrier']  # 每载波转发器输出功率:=转发器EIRP-每载波输出回退
    #下行链路数据：
    ui.varDict1['tol_DL_loss'] = ui.varDict1['down_Atmph_loss'] + ui.varDict1['DownFSpaceLoss']     # 总下行线路径损耗
    ui.varDict1['DL_C_N'] = ui.varDict1['Rpt_out_PpCarrier']-ui.varDict1['tol_DL_loss']-ui.varDict1['loss_re_err']\
                            +ui.varDict1['tol_NT']-0+228.6-ui.varDict1['NoBdWid']       #下行线C/N
    #空间段数据：
    ui.varDict1['bandWidthpCarrier'] = getbWidpCar(ui.varDict1['CarBandwid'], ui.varDict1['zfq_bandwidth'])#载波占转发器带宽
    TransPpCarrier = getPperCar(ui.varDict1['Out_FBpCarrier'], ui.varDict1['out_FB'], ui.varDict1['erip_h'])
    ui.varDict1['TransPpCarrier'] = TransPpCarrier      #每载波占转发器功率
    ui.varDict1['zfqClm_Plmt'] = round(1/ui.varDict1['TransPpCarrier']*100,0)      #转发器容量（功率受限）
    ui.varDict1['zfqClm_Blmt'] = round(ui.varDict1['zfq_bandwidth'] * 1000/ui.varDict1['CarBandwid'],0)      #转发器容量（功率受限）
    ui.varDict1['zfqClm_use'] = min(ui.varDict1['zfqClm_Plmt'], ui.varDict1['zfqClm_Blmt'] )     #有效转发器容量
    #系统指标：
    

    #对端到本端：
    ui.varDict2 = copy.copy(ui.varDict1) #深拷贝到VarDict2，若对端到本端有变化，只需变化相应值，其他不变
    ui.varDict2['infoRate'] = infoRate_dd  # 信息速率
    ui.varDict2['symbleRate'] = symbleRate_dd  # 符号速率
    ui.varDict2['G_T'] = getGT(ui.varDict1['cityName_re'])  # 卫星G/T值
    ui.varDict2['CarBandwid'] = CarBandwid(symbleRate_dd,float(ui.ledit_dd_CarrierSpacingFactor.text()))#载波间隔
    ui.varDict2['CarNoiseBandwid'] = symbleRate_dd * 1.2 #载波噪声带宽 = 符号速率*要求的BT值：默认1.2
    ui.varDict2['UpFSpaceLoss'] = FSpaceLoss(ui.varDict1['up_freq'], ui.varDict1['re_sta_lat'],
                                             ui.varDict1['sat_log'], ui.varDict1['re_sta_log'])  # 上行自由空间损耗
    ui.varDict2['DownFSpaceLoss'] = FSpaceLoss(ui.varDict1['down_freq'], ui.varDict1['tr_sta_lat'],
                                             ui.varDict1['sat_log'], ui.varDict1['tr_sta_log'])  # 下行自由空间损耗



#可视化功能：
def createHeatMap(ui):
    fileName1, filetype = QFileDialog.getOpenFileName(ui,"选取文件","./","All Files (*);;Text Files (*.txt)")
    posi = pd.read_excel(fileName1)
    row_total = posi.shape[0] - 1
    lat = np.array(posi["lat"][0:row_total])  # 获取纬度值
    lon = np.array(posi["lon"][0:row_total])  # 获取经度值
    data1 = [[lat[i], lon[i]] for i in range(row_total)]  # 将数据制作成[lats,lons,weights]的形式
    map_osm = folium.Map(location=[1, 2], zoom_start=1)  # 绘制Map，开始缩放程度是5倍
    HeatMap(data1).add_to(map_osm)  # 将热力图添加到前面建立的map里
    fileName2 = "热力图" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + '.html'
    file_path = os.path.join(r'C:\Users',os.getlogin(),'Desktop',fileName2)
    map_osm.save(file_path)  # 保存为html文件
    webbrowser.open(file_path)  # 默认浏览器打开

def createFreqMap(ui):
    fileName = ui.ledit_excelPath.text()
    print(fileName)
    start_FreQ = int(ui.lnedt_startFreq.text())
    end_FreQ = int(ui.lnedt_endFreq.text())
    isOcupied = False
    dict_excel = {'x_freq': [], }  # 'x_freq': ;isocupied 1,0
    data = pd.read_excel(fileName, 1, 0, usecols=[0, 1, 2])  # 读取前3列
    bandWidth_set = data.iloc[:, 0].values  # 带宽列
    freQ_set = data.iloc[:, 1].values  # 频率列
    ZFQ = data.iloc[:, 2].values  # 转发器列
    for zfq in list(set(ZFQ)):
        dict_excel[zfq] = []
    for t_freq in list(range(start_FreQ, end_FreQ, 100)):
        dict_excel['x_freq'].append(t_freq)
        for i in range(0, len(freQ_set)):
            if isOcupied:
                continue
            if abs(t_freq - (freQ_set[i] * 1000)) < bandWidth_set[i]:  # 如果在带宽范围内
                isOcupied = True
                for key in dict_excel.keys():  # 遍历字典 除了对应转发器 其他都填0
                    if key == 'x_freq': continue
                    if key == ZFQ[i]:
                        dict_excel[key].append(1)
                    else:
                        dict_excel[key].append(0)
        if not isOcupied:
            for key in dict_excel.keys():
                if key == 'x_freq': continue
                dict_excel[key].append(0)
        isOcupied = False
    # for k, v in dict_excel.items():
    #     print(k, len(v))
    #     print(k, v)
    bar = Bar(init_opts=opts.InitOpts(width='1400px'), )
    bar.add_xaxis(dict_excel['x_freq'])
    for key in dict_excel.keys():
        if key == 'x_freq': continue
        bar.add_yaxis(key, dict_excel[key], category_gap="2%")
    bar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    bar.set_global_opts(
        title_opts=opts.TitleOpts(title="中国移动卫星网 - 无线频谱图"),
        datazoom_opts=[opts.DataZoomOpts(is_zoom_lock=True)],
        yaxis_opts=opts.AxisOpts(min_=0, max_=2, ),

        )
    bar.render('无线频谱图.html')
    webbrowser.open('无线频谱图.html')  # 默认浏览器打开

def getFilePath(ui): #频率占用图 -文件名
    fileName, fileType = QFileDialog.getOpenFileName(ui, "选取文件", "./", "All Files (*);;Text Files (*.txt)")
    ui.ledit_excelPath.setText(fileName)
    return fileName

#功能函数
def getbWidpCar(CarrierSpacing, zfq_bandwidth):#每载波占转发器带宽
    bandWidthpCarrier = CarrierSpacing * zfq_bandwidth / 1000 * 100  # 每载波占转发器带宽
    return bandWidthpCarrier

def getPperCar(Out_FBpCarrier, out_FB, erip_h):#每载波占转发器功率
    Rpt_out_PpCarrier = erip_h - Out_FBpCarrier  # 每载波转发器输出功率:=转发器EIRP-每载波输出回退
    TransPpCarrier = round(100 * math.pow(10, (Rpt_out_PpCarrier - erip_h + out_FB) / 10), 3)  # 每载波占转发器功率
    return TransPpCarrier

def FSpaceLoss(freq,sta_lat,sat_log,sta_log): #计算自由空间损耗
    FreeSpaceLoss = 92.45 + 20 * math.log(freq, 10) + \
                   20 * math.log(42164.6 * math.sqrt(1.023 - 0.302 *
                                                     math.cos(sta_lat / 180 * math.pi) *
                                                     math.cos((sat_log - sta_log) / 180 * math.pi)), 10)  # 上行自由空间损耗
    return FreeSpaceLoss

def getAntTrGain(Atn_tr_eff, up_freq, Atn_tr_d):# 天线发射增益
    AntTrGain = 10 * math.log(109.67 * Atn_tr_eff * up_freq * up_freq * Atn_tr_d * Atn_tr_d, 10)
    return AntTrGain

def getearthStationEIRP(AntTrGain, p_HPA, loss_tr_err, loss_Amplifier2feed):  # 地球站EIRP
    earthStationEIRP = AntTrGain + 10 * math.log(p_HPA, 10) - loss_tr_err - loss_Amplifier2feed
    return earthStationEIRP

def getInfoRate(actualCarryingRate_bd,spendingRatio_bd, actualCarryingRate_dd, spendingRatio_dd):# 返回信息速率=实际承载信息速率*（1+开销比例）
    infoRate_bd = actualCarryingRate_bd * (1 + spendingRatio_bd)    # 本端
    infoRate_dd = actualCarryingRate_dd * (1 + spendingRatio_dd)    # 对端
    return infoRate_bd, infoRate_dd

def getSymbleRate(FEC_code_bd, FEC_code_dd, infoRate_bd, infoRate_dd, mod_bd_c, mod_dd_c):#符号速率
    modDic = {"QPSK": 2, "8PSK": 3, "8QAM": 3, "BPSK": 1, "16QAM": 4, "16APSK": 4, "64QAM": 6}    # 调制方式
    symbleRate_bd = round(infoRate_bd / FEC_code_bd / modDic[mod_bd_c], 2)
    symbleRate_dd = round(infoRate_dd / FEC_code_dd / modDic[mod_dd_c], 2)
    return symbleRate_bd, symbleRate_dd

def CarBandwid(CarSyRt, CarFact):#载波间隔（占用带宽）=载波符号速率*载波间隔系数
    return CarSyRt * CarFact

def get_lat_log(city_Name):  #查询城市经纬度
    fileName ='Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName,0,0,usecols=[0, 1, 2, 3])
    return data[data['CITY'] == city_Name]['LON'].values[0], data[data['CITY'] == city_Name]['LAT'].values[0]

def get_Atmph_loss(isUplink:bool,cityName): #查询城市的上行/下行 大气损耗
    fileName = 'Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName, 0, 0, usecols=[1, 5, 6])
    up_loss, down_loss = data[data['CITY'] == cityName]['UP_LOSS'].values[0], data[data['CITY'] == cityName]['DOWN_LOSS'].values[0]
    return up_loss if isUplink else down_loss

def get_SFD(cityName:str): #查询城市的卫星饱和通量密度
    fileName = 'Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName, 0, 0, usecols=[1, 7, 8])
    sfd_h, sfd_v = data[data['CITY'] == cityName]['SFD(H)'].values[0], data[data['CITY'] == cityName]['SFD(V)'].values[0]
    return sfd_h, sfd_v   #水平/垂直极化 SFD

def get_EIRP(cityName):#查询城市EIRP
    fileName = 'Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName, 0, 0, usecols=[1, 9, 10])
    erip_v, erip_h = data[data['CITY'] == cityName]['EIRP（中6A）V'].values[0], data[data['CITY'] == cityName]['EIRP（中6A）H'].values[0]
    return erip_h, erip_v

def getGT(cityName):
    fileName = 'Resource\\覆盖参数.xlsx'
    data = pd.read_excel(fileName, 0, 0, usecols=[1, 11, 12])
    GT_h, GT_v = data[data['CITY'] == cityName]['G/T（中6A）H'].values[0], \
                     data[data['CITY'] == cityName]['G/T（中6A）V'].values[0]
    return float(GT_h), float(GT_v)