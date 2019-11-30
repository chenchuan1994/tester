"""
测试用例应该知道以下三点：
1.测试对象是什么？
2.需要用到什么测试仪器？
3.要控制的测试用例参数是什么？
"""




class case:

    def __init__(self, testObjType, *args):
        self.testObjType = testObjType   # 测试对象类型
        self.testDevice = args           # 必须的测试设备

        self._testobjs = []              # 测试对象列表
        self._testdevices = []           # 测试仪器列表
        print(self.testDevice)

    # 查看测试对象
    @property
    def testobjs(self):
        if self._testobjs == []:
            print('testobj is none')
            return
        testobjs = []
        for testobj in self._testobjs:
            test = '{}_{}_{}'.format(testobj.id, testobj.name, testobj.model)
            testobjs.append(test)
        for testobj in testobjs:
            print(testobj)

    # 重新传入测试对象列表
    @testobjs.setter
    def testobjs(self, testobjs):
        self._testobjs = testobjs

    # 查看测试设备
    @property
    def testdevices(self):
        if self._testdevices == []:
            print('testdevices is none')
            return
        testdevices = []  # 传入的设备类型
        for testdevice in self._testdevices:
            device = testdevice.equipment
            testdevices.append(device)
        lackdevices = []  # 缺少的设备类型
        for testdevice in self.testDevice:
            if testdevice not in testdevices:
                lackdevices.append(testdevice)

        if lackdevices != []:
            for testdevice in lackdevices:
                print(testdevice)
            return
        else:
            for testdevice in testdevices:
                print(testdevice)

    # 重新传入测试设备列表
    @testdevices.setter
    def testdevices(self, testdevs):
        self._testdevices = testdevs
            
    def readyAction(self):
        if self._testdevices == [] or self._testobjs == []:
            return
        


if __name__ == "__main__":
    test = case('board', 'power', 'simtest')
    test.testobjs
    test.testdevices