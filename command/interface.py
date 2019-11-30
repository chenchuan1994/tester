import serial
import pyvisa
import socket
import collections
import time


class interface:

    def __init__(self, kind):
        self.kind = kind    # 类别 0 serial
        self._paras = ()    # 连接参数列表
        self.interface = 0  # 接口实例

    @property
    def paras(self):
        if self.kind == 0:
            print("The interface is serial.")
        elif self.kind == 1:
            print("The interface is socket tcp client")
        return self._paras

    @paras.setter
    def paras(self, args):
        # serial
        if self.kind == 0:
            serparas = collections.namedtuple('serial', 'port baudrate bytesize parity stopbits timeout')
            self._paras = serparas(*args)
        # tcp/ip cilent
        elif self.kind == 1:
            tcpClientparas = collections.namedtuple('tcpclient', 'ip port')
            self._paras = tcpClientparas(*args)
        # tcp/ip server
        elif self.kind == 2:
            print('Not implement')
        # pyvisa ip
        elif self.kind == 3:
            visaip = collections.namedtuple('visaip', 'ip')
        # pyvisa usb
        elif self.kind == 4:
            visausb = collections.namedtuple('visaip', 'usb')
        # pyvisa gpib
        elif self.kind == 5:
            visagpib = collections.namedtuple('visagpib', 'gpib')
        # wifi
        elif self.kind == 6:
            print('Not implement')
        # BT
        elif self.kind == 7:
            print('Not implement')
        # ntrip client
        elif self.kind == 8:
            ntripclient = collections.namedtuple('ntripclient', 'ip port mountpoint userid password')
            print('Not implement')
        # raise error
        else:
            raise IndexError('Not support,kind in (0, 7)')

    def connect(self):
        if self._paras == []:
            raise ValueError("Invalid interface parameter")
        # 串口实例化
        if self.kind == 0:
            ser = serial.Serial()
            ser.port = self._paras.port
            ser.baudrate = self._paras.baudrate
            ser.bytesize = self._paras.bytesize
            ser.parity = self._paras.parity
            ser.stopbits = self._paras.stopbits
            ser.timeout = self._paras.timeout
            ser.open()
            self.interface = ser

        # 客户端实例化
        elif self.kind == 1:
            s = socket.socket()
            addr = (self._paras.ip, self._paras.port)
            s.connect(addr)
            time.sleep(5)
            s.send(b'testing')
            self.interface = s

    def read(self, buffer, timeout = 1):
        # serial read
        if self.kind == 0:
            back = b''
            start = time.time()
            while(True):
                back = back + self.interface.read(1 or self.interface.in_waiting)
                if len(back) >= buffer:
                    break
                if time.time() - start >= 1:
                    break
            print(back)
            return back

    def write(self, cmd):
       
        if self.kind == 0:
            self.interface.write(cmd)

if __name__ == "__main__":
    test = interface(0)
    test.paras = ('com1', 115200, 8, 'N', 1, 1)  # serial
    test.connect()
    test.write('log version\\r\\n')
    test.read(1000)
    print(isinstance(test, interface))