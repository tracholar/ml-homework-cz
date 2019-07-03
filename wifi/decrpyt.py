#coding:utf-8
from pywifi import PyWiFi

def get_wifi_interface():
    wifi = PyWiFi()
    if len(wifi.interfaces()) <= 0:
        print u'未找到无线网卡接口!'
        exit()
    if len(wifi.interfaces()) == 1:
        print u'无线网卡接口: %s'%(wifi.interfaces()[0].name())
        return wifi.interfaces()[0]
    else:
        print '%-4s   %s'%(u'序号',u'网卡接口名称')
        for i,w in enumerate(wifi.interfaces()):
            print '%-4s   %s'%(i,w.name())
        while True:
            iface_no = raw_input('请选择网卡接口序号:'.decode('utf-8').encode('gbk'))
            no = int(iface_no)
            if no>=0 and no < len(wifi.interfaces()):
                return wifi.interfaces()[no]

print get_wifi_interface()