"""
动作定义的概念还有点模糊：
板卡 + 协议 + 接口 = 板卡的动作
板卡实际上是一个空概念，换个方式 板卡的协议 + 接口 = 板卡的动作
实际动作又需要有接口配合，所以动作的函数应该留出接口作为输入参数，不同板卡有不同的型号
所以 action(board, interface_instance)
"""

class action:

    def __init__(self, interface_instance, order):

        self.interface = interface_instance    # 通信接口
        self.cmd = order.cmd                   # 协议
        self.expect = order.expect
        self._response = 0
        self.back = b''

    def send(self):
        "发送协议"
        print('INFO:interface send {}'.format(self.cmd))
        self.interface.write(self.cmd)

    def read(self, buffer):
        self.back = self.interface.read(buffer)
        return self.back

    def response(self):
        back = self.back.lower()
        expect = self.expect
        if expect in back:
            self._response = 1
        else:
            self._response = 0


if __name__ == "__main__":
    from equip import order
    import serial
    import collections

    test_pro = collections.namedtuple('pro', 'cmd expect end encode')
    tem_pro = test_pro(cmd='log version', expect='B380', end='\\r\\n', encode='ascii')  
    one_order = order()
    one_order.pro = tem_pro    # 赋予协议

    ser = serial.Serial(port = 'COM18', baudrate = 115200, timeout = 1)
    
    act = action(ser,one_order)
    act.send()
    print(act.read(1024))