import sqlite3
import collections


class sqloperate:

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.sql = 0

    def connect(self):
        conn = sqlite3.connect(self.dbpath)
        print('Opened command database successfully.')
        self.sql = conn.cursor()

    def get(self, equipment, proalias, types, check = 1):
        "默认执行检查"
        equipment = equipment.upper()
        proalias = proalias.upper()
        types = types.upper()
        if self._isin(equipment, proalias, types) == 1:
            dbcmd = "SELECT CMD, EXPECT, END, ENCODE FROM {} WHERE PROALIAS == '{}' and TYPE == '{}'".format(equipment, proalias, types)
            pro = collections.namedtuple('pro', 'cmd expect end encode')
            res = self.sql.execute(dbcmd).fetchall()[0]
            pro = pro(*res)
            return pro
        else:
            # print("Proalias-{} do not match.".format(proalias))
            return

    def _intable(self, equipment):
        "判断数据库中是否含有名为[equipment]的数据表"
        if self.sql == 0:
            print("Please connect db firstly.")
            return
        
        dbcmd = "SELECT id from {}".format(equipment.upper())
        try:
            self.sql.execute(dbcmd)
        except Exception as e:
            print(e)
            print('{} not in DB.'.format(equipment.upper()))
        else:
            print('{} in DB.'.format(equipment.upper()))
            return 1

    def _isin(self, equipment, proalias, types, check = 1):
        "db is include equipment? proalias? types?"

        if self.sql == 0:
            print("_isin_Please connect db firstly.")
            return
        
        if self._intable(equipment) != 1:
            print("_isin_{} not in DB".format(equipment))
            return

        # 执行检查，输入的参数是否存在数据库中
        _proalias = 0   # 协议别名标志
        _types = 0      # 型号标志
        if check == 1:

            dbcmd = "SELECT * FROM {} WHERE TYPE == '{}'".format(equipment, types)
            res = self.sql.execute(dbcmd).fetchall()
            if res == []:
                print("type-{} not in db".format(types))
                return
            else:
                _types = 1

            dbcmd = "SELECT * FROM {} WHERE PROALIAS == '{}' AND TYPE == '{}'".format(equipment, proalias, types)
            res = self.sql.execute(dbcmd).fetchall()
            if res == []:
                print("proalias-{} not in db".format(proalias))
                return
            else:
                _proalias = 1
        else:
            _proalias = 1
            _types = 1
        
        if (_proalias == 1) and (_types == 1):
            return 1
      

if __name__ == "__main__":
    path = r'E:\project\easyTester\easyTester\module\base\command.db'
    test = sqloperate(path)
    test.connect()
    a = test.get('board', 'GPGGA', 'B380')
    b = test.get('board', 'VERSION', 'ub380')
    print(a)
    print(b)