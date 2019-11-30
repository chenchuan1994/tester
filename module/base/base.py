class equipment:

    def __init__(self):
        self._id = 0                    
        self._name = 'default name'
        self._checked = False
        self._userMsg = 'nomessage'
        self._hardver = 'default0.0.0'
        self._softver = 'defalut0.0.0'
        self._connector = None             # 常规接口
        self._nonconnector = None          # 非常规接口

    @property
    def id(self):
        print('getter id')
        return self._id
    
    @id.setter
    def id(self, id):
        print('setter id = {}'.format(id))
        self._id = id

    @property
    def name(self):
        print('getter name')
        return self._name

    @name.setter
    def name(self, name):
        print('setter name = {}'.format(name))
        self._name = name

    @property
    def checked(self):
        print('getter checked')
        return self._checked
    
    @checked.setter
    def checked(self, boolnum):
        if boolnum == 0:
            self._checked = False
        elif boolnum == 1:
            self._checked = True
        else:
            raise IndexError('input should be 0 or 1')
        print('setter checked = {}'.format(self._checked))

    @property
    def usermsg(self):
        print('getter userMsg')
        return self._userMsg
    
    @usermsg.setter
    def usermsg(self, msg):
        self._userMsg = msg
        print('setter usermsg:{}'.format(self._userMsg))
    
    @property
    def softver(self):
        return self._softver

    @softver.setter
    def softver(self, version):
        self._softver = version
        print('setter softver:{}'.format(self._softver))

    @property
    def hardver(self):
        self._hardver = version
        print('setter hardver:{}'.format(self._hardver))

    @hardver.setter
    def hardver(self, version):
        self._hardver = version
        print('setter hardver:{}'.format(self._hardver))

    @property
    def connector(self):
        return self._connector

    @connector.setter
    def connector(self, interface_isinstance):
        self._connector = interface_isinstance  # 接口实例
    
    @property
    def nonconnector(self):
        return self._nonconnector

    @nonconnector.setter
    def nonconnector(self, interface_isinstance):
        self._nonconnector = interface_isinstance


class testBoardObj(equipment):
    """
    板卡专有测试对象类
    """
    def __init__(self, board):
        self.board = board     # 板卡具体型号

class testRadioObj(equipment):
    """
    电台专有测试对象类
    """
    def __init__(self, radio):
        self.radio = radio     # 电台具体型号

class testRtkObj(equipment):
    """
    RTK专有测试对象类
    """
    def __init__(self, rtk):
        self.rtk = rtk         # RTK整机具体型号


if __name__ == "__main__":
    test = testObj()
    print(test.id, test.name, test.checked, test.usermsg, test.connector, test.nonconnector)