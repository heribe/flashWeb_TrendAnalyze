# -*- coding: utf-8 -*-
import numpy as np
# import time

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# 解决问题: UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position 0: ordinal not in range(128)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 计算趋势（线性回归）
def caseTrend(data, s):
    x = data[:, 0]
    y = data[:, 1]

    x_ = np.zeros((len(data), 2))
    x_[:, 1] = data[:, 0]
    x_[:, 0] = np.ones(len(x))
    w = np.linalg.inv(x_.T.dot(x_)).dot(x_.T).dot(y)

    return w


## 计算标准差
def calE(x, y, w):
    Ein = np.array([])
    for i in range(len(x)):
        Ein = np.append(Ein, (x[i].dot(w) - y[i]))
    return Ein


## 四分法计算异常点
def calTukeyTest(y0):
    y = np.sort(y0)
    q1 = y[len(y) / 4 - 1]
    q3 = y[len(y) * 3 / 4 - 1]
    dv = q3 - q1
    high = q3 + 1.5 * dv
    low = q1 - 1.5 * dv
    print "high=", high
    print "low=", low
    print y0


##标准差法寻找特殊点
def findException(data, w):
    x = data[:, 0]
    y = data[:, 1]
    x_ = np.zeros((len(data), 2))
    x_[:, 1] = data[:, 0]
    x_[:, 0] = np.ones(len(x))
    Eall = calE(x_, y, w)
    Ein = (np.sum(np.abs(Eall)) / len(data))
    out = np.array([])
    for index, e in enumerate(np.abs(Eall)):
        if e > 2 * Ein:
            out = np.append(out, index + 1)
    # print "方差法异常月份：", out
    return out.astype(np.int32)


## 判断总体趋势以及特殊点对趋势的影响(单个曲线)
def theEnd(data, s):
    s = 'label'
    x = data[:, 0]
    y = data[:, 1]
    w = caseTrend(data, s)  # 计算总趋势
    description = ""
    if w[1] > 0:
        description = description + "总体呈上升趋势\n"
    else:
        description = description + "总体呈下降趋势\n"
    excetPoint = findException(data, w)
    excetPoints = []  # 异常点的list,格式:[[month,w_value],[month,w_value],...]
    if len(excetPoint) > 0:
        for i in range(len(excetPoint)):
            point = excetPoint[i]
            data_ = np.append(data[:point - 1, :], data[point:, :], axis=0)  # 计算少了一个特殊月份后的数据
            w_ = caseTrend(data_, s + "_")  # 计算少了一个特殊月份后的趋势
            excetPoints.append([str(excetPoint[i]), str(w_[-1])])
            if w[1] > 0:
                if w_[1] > 0:
                    if w[1] > w_[1]:
                        description = description + "主要是%d月的影响使案件数量上升更明显\n" % point
                    else:
                        description = description + "因%d月的影响使案件数量上升变缓\n" % point
                else:
                    description = description + "因%d月的影响使案件数量从下降趋势变为了上升趋势\n" % point
            else:
                if w_[1] < 0:
                    if w[1] < w_[1]:
                        description = description + "主要是%d月的影响使案件数量下降更明显\n" % point
                    else:
                        description = description + "因%d月的影响使案件数量下降变缓\n" % point
                else:
                    description = description + "因%d月的影响使案件数量从上升趋势变为了下降趋势\n" % point
    return excetPoints, description


## 分析各个分趋势对总趋势的影响(多个曲线）
def theEnd2(data, dataSum):
    s = "data"
    ws = []
    wout = []
    for index, item in enumerate(data):
        x = item[:, 0]
        y = item[:, 1]
        # plt.plot(x, y, marker='o', label=s + str(index))
        w = caseTrend(item, s + str(index))
        wout.append(w[-1])
        ws.append(w)
        print ('w%d = %f' % (index, w[1]))
    x = dataSum[:, 0]
    y = dataSum[:, 1]
    # plt.plot(x, y, marker='o', label=s + 'Sum')
    wSum = caseTrend(dataSum, s + 'Sum')

    ## 分析趋势
    ws = np.array(ws)
    sout = ""
    temp = 0
    wSum = wSum[1]
    for index, _ in enumerate(ws):
        if wSum > 0 and _[1] > wSum:
            if temp == 1: sout += "和"
            sout += 'data' + str(index + 1)
            temp = 1
        if wSum < 0 and _[1] < wSum:
            if temp == 1: sout += "和"
            sout += 'data' + str(index + 1)
            temp = 1
    if sout == "": sout = "所有因素共同结果"
    if wSum > 0:
        description = "总结：影响总的上升趋势的主要是\"%s\"" % (sout)
    else:
        description = "总结：影响总的下降趋势的主要是\"%s\"" % (sout)
    return wout,wSum,description


# 主函数，对xml的解析以及返回总的处理结果
def treadAnalyze(xml):
    # 取得xml根节点
    root = ET.fromstring(xml)
    # 分别取得tag为‘fun','num','items'的节点
    fun = root.find('fun')  # 需要的函数，1表示单条曲线趋势，2表示多条曲线对总曲线趋势的影响
    num = root.find('num')  # 数据总量，当fun=2时，第一条数据为总量数据
    items = root.find('items').findall('item')
    assert fun != None
    assert num != None
    assert items != []
    fun = int(fun.text)
    num = int(num.text)
    assert len(items) == int(num)
    datas = []
    if fun == 2: dataSum = [] # 方法2比方法1多个dataSum的数据
    # for循环用于把datas格式转成如下模样:
    # [array([[  1, 600],[  2, 601],[  3, 400],[  4, 603],[  5, 345],[  6, 605],[  7, 606],[  8, 567],[  9, 608],[ 10, 643],[ 11, 610],[ 12, 611]]),
    #  array([[  1, 400],[  2, 478],[  3, 893],[  4, 403],[  5, 343],[  6, 405],[  7, 406],[  8, 407],[  9, 408],[ 10,  19],[ 11, 410],[ 12, 411]]),
    #  array([[  1, 169],[  2, 189],[  3, 202],[  4, 232],[  5, 256],[  6, 205],[  7, 266],[  8, 555],[  9, 208],[ 10,  11],[ 11, 267],[ 12, 211]]),
    #  array([[  1, 369],[  2, 413],[  3, 466],[  4, 503],[  5, 504],[  6, 533],[  7, 506],[  8, 507],[  9, 508],[ 10, 509],[ 11, 510],[ 12, 511]])]
    for index, item in enumerate(items):
        temp = np.array(item.text.split(','))
        datao = np.zeros((len(temp), 2))
        datao[:, 0] = range(1, len(temp) + 1)
        datao[:, 1] = temp
        datao = datao.astype(int)
        if fun == 2 and index == 0:
            dataSum = datao
        else:
            datas.append(datao)
    # 对不同的要求调用不同的函数计算结果
    if fun == 1:
        itemw = []
        itemd = []
        for _ in datas:
            exceptions, description = theEnd(_, 'data')
            itemw.append(exceptions)
            itemd.append(description)
        root = ET.Element('out')
        for index, exceptions in enumerate(itemw):
            item = ET.SubElement(root, 'item')
            item.set('id', str(index + 1))
            for point in exceptions:
                w = ET.SubElement(item, 'w')
                month = ET.SubElement(w, 'month')
                month.text = point[0]
                value = ET.SubElement(w, 'value')
                value.text = point[1]
            description = ET.SubElement(item, 'description')
            description.text = itemd[index]
        return ET.tostring(root, 'UTF-8', 'xml')

    if fun == 2:
        ws,wsum,description = theEnd2(datas, dataSum)
        root = ET.Element('out')
        for index,w_ in enumerate(ws):
            w = ET.SubElement(root,'w')
            w.set('id',str(index+1))
            w.text = str(w_)
        w_dataSum = ET.SubElement(root,'w_dataSum')
        w_dataSum.text = str(wsum)
        descriptione = ET.SubElement(root,'description')
        descriptione.text = description
        return ET.tostring(root,'utf-8','xml')


if __name__ == '__main__':
    # start = time.time()
    # for i in range(1):
    #     q1()
    #     q2()
    # elapsed = (time.time() - start)
    # print "time:",elapsed
    #     xml="""<data>
    #     <fun>2</fun>
    #     <num>5</num>
    #     <items>
    #         <item>1538,1681,1961,1741,1448,1748,1784,2036,1732,1182,1797,1744</item>
    #         <item>600,601,400,603,345,605,606,567,608,643,610,611</item>
    #         <item>400,478,893,403,343,405,406,407,408,19,410,411</item>
    #         <item>169,189,202,232,256,205,266,555,208,11,267,211</item>
    #         <item>369,413,466,503,504,533,506,507,508,509,510,511</item>
    #     </items>
    # </data>"""
    #     treadAnalyze(xml)
    print('hahahaha')
