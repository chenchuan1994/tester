import shelve
import os
import datetime
from equip import equipment


class scenario:

    def __init__(self):
        self._name = 'default'
        self._date = '1990-01-01 00:00:00'
        self._author = 'default'
        self._note = 'default'

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, nm):
        self._name = nm

    @property
    def date(self):
        return self._date
    @date.setter
    def date(self, mtime):
        self._date = mtime

    @property
    def author(self):
        return self._author
    @author.setter
    def author(self, auth):
        self._author = auth

    @property
    def note(self):
        return self._note
    @note.setter
    def note(self, note):
        self._note = note

class manageScenario:

    @staticmethod
    def buildScenario(folder, scname, author = None, note = None):
        "build a new scenario"
        """
            folder  文件夹路径，必须存在
            scname  测试场景名称
            author  场景建立者
            note    备注信息
        """
        # 未输入场景名称，则按照默认名称叠加
        if scname == "":
            scname = "defaultScenario%{i}%"
            i = 1
            while(True):
                scname = scname.replace('%{i}%', str(i))
                new_sc_folder = "{}/{}".format(folder, scname)
                print(new_sc_folder)
                res = manageScenario._isdir(new_sc_folder, -1)  # -1 文件夹存在
                print(res)
                if res == 0:
                    scname = scname.replace('%{i}%', str(i))
                else:
                    break
                i = i + 1
                scname = "defaultScenario%{i}%"

        if "\\" not in folder:
            new_sc_folder = scname
        else:    
            new_sc_folder = "{}\\{}".format(folder, scname)                 # 场景文件夹

        res = manageScenario._isdir(new_sc_folder, 0)
        # 若文件夹已经存在，直接退出
        if res == -1: 
            return -1
        new_sc_shl = "{}\\{}\\{}_shl".format(folder, scname, scname)     # 场景shelve文件
        print(new_sc_shl)

        sc = scenario()
        sc.name = scname
        if author != (None or ""):
            sc.author = author
        if note != (None or ""):
            sc.note = note
        sc.note = note
        sc.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with shelve.open(new_sc_shl) as myfile:
            # sc.name = scname
            myfile['sc'] = sc
            myfile['test'] = []
            myfile['equip'] = []
            myfile['case'] = []
            myfile['support'] = {
                'board':['b380','b380d',
                        'ub380', 'ub4b0', 'ub4b0m', 'ub4b0',
                        'oem618', 'oem729',
                        'bd970', 'bd990',],
                'radio':['d352','dl9',],
                'rtk':'',
                'power':['db811a', 'spd3303x'],
                'signal':[],
                'analyer':[],
                'simulator':[],
                'rfpower':[],            
                }

    @staticmethod
    def addEquipment(sc_path=None, id=0, name=0, equip=0, 
        model=0, usermsg=0, hardver=0, softver=0, checked=0):
        "add equipment to a scenario"
        # 判断传入的路径是否是一个场景，若非场景，直接退出
        res = manageScenario._isinfile(sc_path)   # 若有shelve文件，则返回文件名

        if res == -1:return -1
        
        # add a equip
        eq = equipment()    # 设备属性类

        # 自主维护，遍历shelve文件，在最大的ID上+1,
        eq.id = manageScenario._productID(sc_path)

        # 设备名称
        if name == "":
            eq.name = "default"
        else:
            eq.name = name
        
        equips = {
            'board':['b380','b380d',
                     'ub380', 'ub4b0', 'ub4b0m', 'ub4b0',
                     'oem618', 'oem729',
                     'bd970', 'bd990',],
            'radio':['d352','dl9',],
            'rtk':'',
            'power':['db811a', 'spd3303x'],    
        }
        if equip == "":
            return -1
        else:
            eq.equip = equip
        eq.model = model
        eq.usermsg = usermsg
        eq.hardver = hardver
        eq.softver = softver
        eq.checked = checked

        with shelve.open("{}\\{}".format(sc_path, res)) as myfile:
            # 遍历设备的name 和 ID,要求输入的名称和ID不可重复
            temp = myfile['equip']
            for eqpt in temp:
                if (eqpt.name == name) or (eqpt.id == id):
                    print("Error:Name(or id) is repeatedly.")
                    return -1
            temp.append(eqpt)
            myfile['equip'] = temp
            
        with shelve.open("{}\\{}".format(sc_path, res)) as myfile:
            print(myfile['equip'])
        
        return 0

    @staticmethod
    def delAllEquipment(sc_path = None):
        "Not Implement"
    
    @staticmethod
    def _isdir(folder, makedir = -1):
        "判断文件夹是否存在，若有必要则创建"
        # 仅判断文件夹是否存在
        if makedir == -1:   
            if os.path.isdir(folder):
                return 0  # 文件夹存在
            return -1  #文件夹不存在
        elif makedir == 0:
            if not os.path.exists(folder):
                os.makedirs(folder)
                return 0
            else:
                print("Error: folder has been exit.")
                return -1
        else:
            return -1
        
    @staticmethod
    def _isinfile(folder, search = '_shl.dat'):
        "判断文件下是否包含_shl.dat的文件，存在则认为是场景文件"
        files_dirs = os.listdir(folder)
        for mfile in files_dirs:
            # print(mfile)
            if search in mfile:
                return mfile.split('.')[0]
        print("Error: The folder is not a scenario folder.")
        print("Error Path:{}".format(folder))
        return -1

    @staticmethod
    def _productID(folder):
        "自动生成ID号"
        mfile = manageScenario._isinfile(folder)
        file_path = "\\".join([folder, mfile])
        with shelve.open(file_path) as mfile:
            ids = []
            equips = mfile['equip']
            if equips != []:
                for equip in equips:
                    ids.append(equip.id)
                return max(ids) + 1
            else:
                return 1

# folder = r'E:\project\easyTester\easyTester\test'
# name = 'mytest'

# manageScenario.newScenario(folder, name)
if __name__ == "__main__":
    #test new
    path = r'E:\project\easyTester\easyTester\test'
    scname = ""
    manageScenario.buildScenario(path, scname)
