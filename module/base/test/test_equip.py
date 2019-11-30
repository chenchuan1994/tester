import os
import sys

# 相对路径获取测试文件equip.py
current_path = os.path.abspath(__file__)
father_folder = current_path.split('\\')[:-2]
equip_path = '/'.join(father_folder)
sys.path.append(equip_path)

from boardAction import boardAction   # 测试目标
from interface import interface

ser = interface(0)
ser.paras = ('com18', 115200, 8, 'N', 1, 1)
ser.connect()

actboard = boardAction('ub4b0')
actboard.interface = ser    # 绑定接口

def test_act_getVersion():
    ver = actboard.act_confirm_model()
    print(ver)

def test_act_request_GNSS():
    # 单协议传入
    pro1 = 'GPGGA'
    gnss1 = actboard.act_request_gnss(pro1)

    pro2 = 'GPGGA'
    hz2 = '2'
    gnss2 = actboard.act_request_gnss(pro2, hz2)

    pro3 = {'GPGGA':1}
    gnss3 = actboard.act_request_gnss(**pro3)

    print(gnss1, gnss2, gnss3)

test_act_getVersion()
test_act_request_GNSS()