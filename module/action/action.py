"""
动作定义的概念还有点模糊：
板卡 + 协议 + 接口 = 板卡的动作
板卡实际上是一个空概念，换个方式 板卡的协议 + 接口 = 板卡的动作
实际动作又需要有接口配合，所以动作的函数应该留出接口作为输入参数，不同板卡有不同的型号
所以 action(board, interface_instance)
"""

class action:

    def __init__(self, kind, interface_instance, cmd):

        self.kind = kind                       # 设备类别
        self.interface = interface_instance    # 通信接口
        self.cmd = cmd                         # 协议

    def set(self):
        
        