from interface import interface
import binascii
import collections


class equipment:

    _id = 0            # 序号
    _name = 0          # 设备名称
    _equipment = 0     # 设备类型,power,simtest
    _model = 0         # 设备型号
    _usermsg = 0       # 用户备注信息
    _hardver = 0       # 硬件版本
    _softver = 0       # 软件版本
    _checked = 0       # 是否被选中
    _connector1 = 0    # 常规连接接口[协议收发口]
    _connector2 = 0    # 非常规连接接口[差分输入口]
    _connector3 = 0    # 非常规连接接口[差分输入口]
    _connector4 = 0    # 非常规连接接口[差分输入口]
    _actionBox = 0     # 动作盒子[虚的，直接继承了boardAction]

    
    # 设备序号(ID) GET
    @property
    def id(self):
        "get value of id"
        print('getattr id = {}'.format(self._id))
        return self._id
    
    # 设备序号(ID) SET
    @id.setter
    def id(self, num):
        if type(num) == int:
            print('setattr id = {}'.format(num))
            self._id = num  
        else:
            print('ERROR:setattr id = {} failed.'.format(num))

    # 设备名称(name) GET
    @property
    def name(self):
        print('getattr name = {}'.format(self._name))
        return self._name

    # 设备名称(name) SET
    @name.setter
    def name(self, namemsg):
        if type(namemsg) == str:
            print('setattr name = {}'.format(namemsg))
            self._name = namemsg
        else:
            print('ERROR:setattr name = {} failed'.format(namemsg))

    # 设备类型(equipment) GET
    @property
    def equipment(self):
        print('getattr equipment = {}'.format(self._equipment))
        return self._equipment

    # 设备类型(equipment) SET
    @equipment.setter
    def equipment(self, equipment_name):
        eq_name = equipment_name
        EQUIPMENT = ['board', 'radio', 'rtk']
        if type(eq_name) == str:
            if eq_name.lower() in EQUIPMENT:
                print('setattr equipment = {}'.format(eq_name))
                self._equipment = eq_name.lower()
                return
        print('ERROR:setattr equipment = {} failed'.format(eq_name))

    # 设备型号(model) GET
    @property
    def model(self):
        print('getattr model = {}'.format(self._model))
        return self._model

    # 设备型号(model) SET
    @model.setter
    def model(self, mod):
        BOARD = ['b380', 'b380d',
                 'ub380', 'ub4b0', 'ub4b0m', 'um4b0',
                 'oem618', 'oem729',
                 'bd970', 'bd990']
        RADIO = ['d352']
        RTK = []
        
        if type(mod) == str:
            if mod.lower() in (BOARD or RADIO or RTK):
                print('setattr model = {}'.format(mod))
                self._model = mod.lower()
                return
        
        print('ERROR:setattr model = {} failed'.format(mod))

    # 设备自定义用户信息 GET
    @property
    def usermsg(self):
        print('getattr usermsg = {}'.format(self._usermsg))
        return self._usermsg

    # 设备自定义用户信息 SET
    @usermsg.setter
    def usermsg(self, msg):
        print('setattr usermsg = {}'.format(msg))
        self._usermsg = msg

    # 设备硬件版本 GET
    @property
    def hardver(self):
        print('getattr hardver = {}'.format(self._hardver))
        return self._hardver

    # 设备硬件版本 SET
    @hardver.setter
    def hardver(self, msg):
        print('setattr usermsg = {}'.format(msg))
        self._hardver = msg

    # 设备固件（软件）版本 GET
    @property
    def softver(self):
        print('getattr softver = {}'.format(self._hardver))
        return self._softver

    # 设备固件（软件）版本 SET
    @softver.setter
    def softver(self, msg):
        print('setattr softver = {}'.format(msg))
        self._softver = msg

    # 设备是否被选中 GET[1 checked;0 unchecked]
    @property
    def checked(self):
        print('getattr checked = {}'.format(self._checked))
        return self._checked

    # 设备是否被选中 SET
    @checked.setter
    def checked(self, num):
        if num == 0 or 1:
            self._checked = num
            print('setattr checked = {}'.format(self._checked))
        else:
            print('ERROR:setattr checked = {} failed'.format(num))

    # 通信接口 #1 GET
    @property
    def connector1(self):
        print('getattr connector1 = {}'.format(self._connector1))
        return self._connector1

    # 通信接口 #1 SET
    @connector1.setter
    def connector1(self, interface_class):
        if isinstance(interface_class, interface):
            self._connector1 = interface_class
            print('setattr connector1 = {}'.format(interface_class.interface))
            return
        print('ERROR:setattr connector1 = {} failed'.format(interface_class))

    # 通信接口 #2 GET
    @property
    def connector2(self):
        print('getattr connector2 = {}'.format(self._connector2))
        return self._connector2

    # 通信接口 #2 SET
    @connector2.setter
    def connector2(self, interface_class):
        if isinstance(interface_class, interface):
            self._connector2 = interface_class
            print('setattr connector2 = {}'.format(interface_class.interface))
            return
        print('ERROR:setattr connector2 = {} failed'.format(interface_class))

    # 通信接口 #3 GET
    @property
    def connector3(self):
        print('getattr connector3 = {}'.format(self._connector3))
        return self._connector3

    # 通信接口 #3 SET
    @connector3.setter
    def connector3(self, interface_class):
        if isinstance(interface_class, interface):
            self._connector3 = interface_class
            print('setattr connector3 = {}'.format(interface_class.interface))
            return
        print('ERROR:setattr connector3 = {} failed'.format(interface_class))

    # 通信接口 #4 GET
    @property
    def connector4(self):
        print('getattr connector4 = {}'.format(self._connector4))
        return self._connector4

    # 通信接口 #4 SET
    @connector4.setter
    def connector4(self, interface_class):
        if isinstance(interface_class, interface):
            self._connector4 = interface_class
            print('setattr connector4 = {}'.format(interface_class.interface))
            return
        print('ERROR:setattr connector4 = {} failed'.format(interface_class))

class order:

    _pro = 0
    _cmd = 0
    _expect = 0
    _encode = 0

    @property
    def pro(self):
        return self._pro

    @pro.setter
    def pro(self, input_pro):
        """
        INPUT：pro(cmd='log version', expect='B380', end='\\r\\n', encode='ascii')
        """
        _pros = collections.namedtuple('pro', 'cmd expect end encode')
        _pros = _pros(cmd='log version', expect='B380', end='\\r\\n', encode='ascii')

        if ('pro' in str(type(input_pro))):
            print('setattr pro = {}'.format(input_pro))
            self._pro = input_pro
        else:
            raise TypeError("input type is error")

    # 指令 GET 根据编码方式，反馈不同的指令
    @property
    def cmd(self):
        if self._pro == 0:
            print('no command cmd = {}'.format(self._cmd))
            return
        
        if self._pro.encode == 0:
            print('WARMING:No encode,can not get valid command')

        if self._cmd == 0:
            self._cmd = self._pro.cmd + self._pro.end
        else:
            self._cmd = self._cmd
        self._dealcmd()  # 对self._cmd 做特殊处理
        
        if self._pro.encode == 'ascii':
            return bytes(self._cmd, 'ascii')

        if self._pro.encode == 'hex':
            return bytes.fromhex(self._cmd)

    # 替代字处理
    def dealreplace(self, breplace:'before replace', areplace:'after replace'):
        print(self._cmd)
        self._cmd = self._cmd.replace(breplace, str(areplace))

        return self._cmd
    # 期待反馈的字符串 GET 统一小写
    @property
    def expect(self, bys = 1):
        if bys == 1:
            return bytes(self._pro.expect.lower(), 'ascii')
        if bys == 0:
            return self._pro.expect.lower()
    
    # 编码方式 GET
    @property
    def encode(self):
        return self._pro._encode

    def _dealcmd(self):
        cmd = self._cmd
        cmd = cmd.replace('\\r', '\r')
        cmd = cmd.replace('\\n', '\n')
        self._cmd = cmd

# class testBoardObj(equipment, boardAction):

#     def __init__(self, model):
#         boardAction.__init__(self, model)
#         self.model = self._model(model)
    
#     @property
#     def connector(self):
#         '查看常规接口'

#         return self._connector

#     @connector.setter
#     def connector(self, interface_instance):
#         '常规接口赋值'

#         self._connector = interface_instance
#         self.interface = interface_instance

#     def _model(self, model):        
#         "未支持的型号，实例化失败"

#         chc = ['b380', 'b380d']
#         hx = ['ub380', 'ub4b0', 'ub4b0m', 'um4b0']
#         novatel = ['oem618', 'oem729']
#         trimble = ['bd970', 'bd990']

#         isin = model.lower() in chc, hx, novatel, trimble

#         if True in isin:
#             return model
#         else:
#             raise ValueError('Not support the model-{}'.format(model))

if __name__ == "__main__":
    eq = equipment()
    eq.id = 10.0
    eq.name
    eq.name = 10
    eq.equipment = 'BOARD'
    eq.equipment
    
    eq.model = 'B380D'
    eq.model

    eq.usermsg

    eq.connector1 = interface(0)
    print('-------华丽分割线--------')

    orde = order()
    pro = collections.namedtuple('pro', 'cmd expect end encode')
    a = pro('1', '2', '3', '4')

    b = pro(cmd='log version', expect='B380', end='\\r\\n', encode='ascii')
    orde.pro
    a = str(type(pro))
    print(a)