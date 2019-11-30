# -*- coding: utf-8 -*-

from sqloperate import sqloperate
from action import action
from equip import equipment,order
import os

class boardAction(action, equipment):
    
    backbys = []        # 对象的数据存储列表

    def __init__(self, model):
        
        self.model = model               # 设备型号
        self.equipment = 'board'
        self.dbpath = self._dealPath()
        self.interface = 0
        self.buffer = 102400

    def getpro(self, proalias, check = 0):
        "get protocol"
        prosql = sqloperate(self.dbpath)
        prosql.connect()
        pro = prosql.get(self.equipment, proalias, self.model)
        
        command = order()
        command.pro = pro
        print(command.cmd)  # 必须要运行一次cmd才有值

        return command

    def baseAction(self, order):
        "发送-接收-判断"
        if self.interface == 0:
            print("Please build a instance of interface before doing acton.")
            return
        act = action(self.interface, order)
        act.send()
        act.read(self.buffer)
        act.response()

        return act._response

    def act_confirm_model(self):
        "get version of board"
        pro = self.getpro('VERSION')
        res = self.baseAction(pro)
        if res == 1:
            return pro.expect     

    def act_clear_gnss(self):
        pro = self.getpro('UNLOGALL')
        res = self.baseAction(pro)
        if res == 1:
            print('Clear success')
            return res
    
    def act_request_gnss(self, *alias:'协议别名', hz = None, **gnss):
        cmds = []
        default = {
            1:['GPGGA'],
            20:[]
        }

        # 默认频率
        if hz == None:  
            for n in alias:
                for key in list(default.keys()):
                    if n in default[key]:
                        order_struct = self.getpro(n)
                        order_struct.dealreplace('%{aHZ}%', str(key))
                        cmds.append(order_struct)
        else:
            for n in alias:
                order_struct = self.getpro(n)
                order_struct.dealreplace('%{aHZ}%', str(gnss[key]))
                cmds.append(order_struct)

        #传入协议和频率字典{协议：频率}
        if gnss != None:
            for key in list(gnss.keys()):
                order_struct = self.getpro(key)
                order_struct.dealreplace('%{aHZ}%', str(gnss[key]))
                cmds.append(order_struct)
        res = []
        for cmd in cmds:
            res.append(self.baseAction(cmd))

        return res
    
    def _dealPath(self):
        current_path = os.path.abspath(__file__)
        father_folder = current_path.split('\\')[:-1]
        dbName = 'command.db'
        father_folder.append(dbName)
        dbpath = '/'.join(father_folder)
        return dbpath

    def _dealcmd(self, cmd):
        "额外的处理"

        cmd = cmd.replace('\\r', '\r')
        cmd = cmd.replace('\\n', '\n')
        
        return cmd

if __name__ == "__main__":

    from interface import interface

    ser = interface(0)
    ser.paras = ('com18', 115200, 8, 'N', 1, 1)
    ser.connect()

    actboard = boardAction('UB4B0')
    actboard.interface = ser
    a = actboard.act_getVersion()
    # actboard.act_getVersion(1)
    print(a)


    test_pro = {'GPGGA':1}
    actboard.act_request_GNSS(**test_pro)
