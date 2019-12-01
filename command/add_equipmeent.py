import os
import scene
import equip
import shelve
from interface import interface
import serial
import copy


def new_scenario(path_or_scName):
    "Not implement"


def add_equipment_into_scenario(path_or_equip):
    "增加一个设备进入测试"

    # input a absoult path
    if "\\" in path_or_equip:
        path = path_or_equip
        while True:
            equipment = input("Equipment:")
            # find shelve file in absolute path or workspace
            sc = scene.manageScenario._isinfile(path)  # if not a scnario folder,return
            if sc == -1:
                return 0
            with shelve.open("{}\\{}".format(path, sc)) as mfile:
                equips = mfile["support"]
            if equipment not in list(equips.keys()):
                print(
                    "Error: unkwon type of euqipment,support {}".format(
                        "|".join(list(equips.keys()))
                    )
                )
            else:
                break
    # input a equipment
    else:
        path = os.getcwd()
        equipment = path_or_equip

    # find shelve file in absolute path or workspace
    sc = scene.manageScenario._isinfile(path)  # if not a scnario folder,return
    if sc == -1:
        return 0

    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        equips = mfile["support"]

    # if input a unkwon equipment by cmd, return
    if equipment not in list(equips.keys()):
        print(
            "Error:unkwon type of euqipment,support {}".format(
                "|".join(list(equips.keys()))
            )
        )
        return 0
    while True:
        model = input("Model:")
        if model not in equips[equipment]:
            print(
                "Error:unkwon model of equipment,support {}".format(
                    "|".join(equips[equipment])
                )
            )
        else:
            break

    names = [] # all name
    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        print(sc)
        for equ in mfile["equip"]:
            names.append(equ.name)
    while(True):
        name = input("Name:")
        if name == "":
            name = "defaultName"
        if name in names:
            print("Error:equipment name conflict.")
        else:
            break

    hardver = input("Hardware version:")
    if hardver == "":
        hardver = "defalutHardver"

    softver = input("Software version:")
    if softver == "":
        softver = "defalultSoftver"

    checked = input("Checked:")
    if checked == "":
        checked = 1

    usermsg = input("User message:")
    if usermsg == "":
        usermsg = "defaultMessage"

    # ask whether to bind interface
    ser_paras = []
    count = 1
    break_sign = 0

    while True:
        if break_sign == 1:
            break
        if count == 1:  # only one time
            ask = input("Do you want to bind interface to the equipment?[y/N]")
        # YES
        if ask in ("y", "Y"):
            print(
                "You must choice interface type:0 serial, 1 tcp client, 2 tcp server, 3 visa ip."
            )
            print("You can input number or interface name,likes serial...")
            if count == 1:
                print(
                    "You are editing interface #{}.Usually used for cmd sending and receiving.".format(
                        count
                    )
                )
            if count == 2:
                print(
                    "You are editing interface #{}.Usually used for inputing diff.".format(
                        count
                    )
                )
            interface_type = input("Interface type:")
            if interface_type in ("0", "serial"):

                while True:  # port must exist
                    port = input("Serial Port              >")
                    try:
                        serial.Serial(port).close()
                        break
                    except Exception as e:
                        print("{} does not exist.".format(port))

                baudrate = input("baudrate(default 115200) >")
                parity = input("parity(default None)     >")
                byteszie = input("bytesize(default 8)      >")
                stopbits = input("stopbits(default 1)      >")
                timeout = input("timeout(default 0.5)     >")
                # default parameter of serial
                if baudrate == "":
                    baudrate = 115200
                if parity == "":
                    parity = "N"
                if byteszie == "":
                    byteszie = 8.0
                if stopbits == "":
                    stopbits = 1.0
                if timeout == "":
                    timeout = 0.5

                ser_paras.append(
                    [
                        str(port),
                        int(baudrate),
                        int(byteszie),
                        str(parity),
                        int(stopbits),
                        float(timeout),
                    ]
                )
                # add another
                while True:
                    another_ask = input("Do you have an another want to bind?[y/N]")
                    if another_ask in ("y", "Y"):
                        count = count + 1
                        into_confirm = 0
                        break
                    elif another_ask in ("n", "N") or count > 2:
                        print("Please confirm your binding interface:")
                        num = 1
                        for para in ser_paras:
                            print("  Interface{}_port     >{}".format(num, para[0]))
                            print("  Interface{}_baudrate >{}".format(num, para[1]))
                            print("  Interface{}_bytesize >{}".format(num, para[2]))
                            print("  Interface{}_parity   >{}".format(num, para[3]))
                            print("  Interface{}_stopbits >{}".format(num, para[4]))
                            print("  Interface{}_timeout  >{}".format(num, para[5]))
                            num = num + 1
                        into_confirm = 1
                        break
                    else:
                        print("Error:invalid value.")
                if into_confirm == 1:
                    # confirm
                    while True:
                        confirm_ask = input("Are you confirm?[y/N]")
                        if confirm_ask in ("y", "Y"):
                            break_sign = 1
                            break
                        elif confirm_ask in ("n", "N"):
                            count = 1
                            ser_paras = []
                            print("Rebind interface.Edit again...")
                            break
                        else:
                            print("Error:invalid value.")
        # NO
        elif ask in ("n", "N"):
            break
        # Invalid
        else:
            print("Error:invalid value")

    equipobj = equip.equipment()
    equipobj.id = scene.manageScenario._productID(path)
    equipobj.name = name
    equipobj.equipment = equipment
    equipobj.model = model
    equipobj.usermsg = usermsg
    equipobj.hardver = hardver
    equipobj.softver = softver
    equipobj.checked = checked
    interface_count = 1
    for para in ser_paras:
        if len(para) == 6:  # 参数长度为6，则认为是串口
            inter = interface(0)
            inter.paras = (para[0], para[1], para[2], para[3], para[4], para[5])
            inter.connect()
        if interface_count == 1:
            equipobj.connector1 = inter.interface
        if interface_count == 2:
            equipobj.connector2 = inter.interface

    # write into shelve
    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        temp = mfile["equip"]
        temp.append(equipobj)
        mfile["equip"] = temp

    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        print(mfile["equip"])


def del_quipment_by_name_or_id(path_or_point):
    "通过指定名称和ID删除测试场景中的设备"
    if "\\" in path_or_point:  # absolute path
        path = path_or_point
    else:
        path = os.getcwd()

    sc_file = scene.manageScenario._isinfile(path)

    shelve_file = "{}\\{}".format(path, sc_file)

    print("Please input id or name,just choice one of them")
    id = input("ID:")
    name = input("Name:")

    with shelve.open(shelve_file) as mfile:
        equips = mfile["equip"]
        for equip in equips:
            if (int(id) == equip.id) or (name == equip.name):
                while True:
                    _ask = "Are you sure to remove the equipment id-{},name-{}?[y/N]".format(equip.id, equip.name)
                    ask = input(_ask)
                    if ask in ("y", "Y"):
                        equips.remove(equip)
                        mfile["equip"] = equips
                        print("Delete equipment which id-{},name-{}".format(equip.id, equip.name))
                        break
                    elif ask in ("n", "N"):
                        print("Stop remove equipment.")
                        break
                    else:
                        print("Error:invalid value.")
                return
        print("Equipment you input does not exit.")


def show_equipment(path_or_point):
    "show"
    if "\\" in path_or_point:
        path = path_or_point
    else:
        path = os.getcwd()

    sc_file = scene.manageScenario._isinfile(path)
    if sc_file == -1:
        return -1
    shelve_file_path = "{}\\{}".format(path, sc_file)
    with shelve.open(shelve_file_path) as mfile:
        equips = mfile["equip"]
        if equips == []:
            print("WARN:No equipment in scenario-{}.".format(shelve_file_path))
            return
        print("#show equipment------------------------------------#")
        for equip in equips:
            id = equip.id
            name = equip.name
            model = equip.model
            equipment = equip.equipment
            checked = equip.checked
            connector1 = equip.connector1
            print(
                "ID-{:<2} Name-{:<10} Model-{:<5} Equipment-{:<5}  Checked-{:<2}  connector1-{:<5}".format(
                    id, name, model, equipment, checked, connector1
                )
            )


def edit_equipment(
    path_or_point=None,
    sname=None,
    id=None,
    name=None,
    equipment=None,
    model=None,
    usermsg=None,
    hardver=None,
    softver=None,
    checked=None,
    connector1=None,
    connector2=None,
    connector3=None,
    connector4=None,):
    # 绝对路径或当前工作路径，指定要修改的测试场景
    # name id  通过名称或者ID指定要修改的设备
    # modify   要修改项，形式如 XXX[修改项名称] = XXX[修改值]
    # -sc
    # -id
    # -name
    if path_or_point != None:
        if "\\" in path_or_point:
            path = path_or_point  # absolute path
        else:
            path = os.getcwd()  # current workspace
    else:
        path = os.getcwd()

    sc_file = scene.manageScenario._isinfile(path)  # search secnario shelve file
    if sc_file == -1:
        return -1
    sc_path = "{}\\{}".format(path, sc_file)

    wait_equipment = 0    # 修改后的设备
    remove_equipment = 0  # 修改前的设备
    ID = 0
    # check equipment exits
    if name == None and id == None:
        print("Error:Must specify at one of id or name.")
        return -1
    elif id != None:
        with shelve.open(sc_path) as mfile:
            match = 0
            equips = mfile["equip"]
            if equips == []:
                print("WARN:No equipment in scenario-{}.".format(sc_path))
                return
            for eqp in equips:
                if eqp.id == int(id):
                    print(
                        "Match a equipment which id is {},name is {}.".format(
                            eqp.id, eqp.name
                        )
                    )
                    wait_equipment = eqp  # 确认需要修改的设备
                    ID = wait_equipment.id
                    match = 1
                    break
            if match == 0:
                print("Error:No equipment's id is {}.".format(id))
                return -1
    else:
        with shelve.open(sc_path) as mfile:
            match = 0
            equips = mfile["equip"]
            if equips == []:
                print("WARN:No equipment in scenario-{}.".format(sc_path))
                return
            for eqp in equips:
                if eqp.name == name:
                    print(
                        "Match a equipment which name is {},id is {}.".format(
                            eqp.name, eqp.id
                        )
                    )
                    match = 1
                    wait_equipment = eqp  # 确认需要修改的设备
                    ID = wait_equipment.id
                    break
            if match == 0:
                print("Error:No equipment's name is {}.".format(eqp.name))
                return -1

    # check the value of connector
    ctrs = [connector1, connector2, connector3, connector4]
    for ctr in ctrs:
        if ctr != None:
            if ctr not in ['serial']:
                print("Error:Connector's value should be serial")
                return

    _paras = {
        'name':name,
        'equipment':equipment,
        'model':model,
        'usermsg':usermsg,
        'hardver':hardver,
        'softver':softver,
        'checked':checked,
        'connector1':connector1,
        'connector2':connector2,
        'connector3':connector3,
        'connector4':connector4,
    }

    _paras_nonone = {}
    keys = list(_paras.keys())
    print(keys)
    for key in keys:
        if _paras[key] != None:
            _paras_nonone[key] = _paras[key]
    #print(_paras_nonone)
    
    temp_sign = 'name','equipment','model','usermsg','hardver','softver','checked' in list(_paras.keys())
    print(temp_sign)
    temp_sign = temp_sign.count(True)
    if temp_sign >= 1:
        print("Please check equipemnt that you want change.")
        for key in list(_paras_nonone.keys()):
            print("{:<10}:{:>6} >>> {:<6}".format(key, eval("wait_equipment.{}".format(key)), _paras_nonone[key]))

        while(True):
            ask = input("Are you want to save the change except connector[y/N]?")
            if ask in ('y', 'Y'):
                # 删去修改前的类
                with shelve.open(sc_path) as mfile:
                    temp = mfile['equip']
                    for eqp in temp:
                        if eqp.id == ID:
                            temp.remove(eqp)
                            break
                    mfile['equip'] = temp
                for key in list(_paras_nonone.keys()):
                    if key == 'name':wait_equipment.name = name
                    if key == 'equipment':wait_equipment.equipment = equipment
                    if key == 'model':wait_equipment.model = model
                    if key == 'usermsg':wait_equipment.usermsg = usermsg
                    if key == 'hardver':wait_equipment.hardver = hardver
                    if key == 'softver':wait_equipment.softver = softver
                    if key == 'checked':wait_equipment.checked = checked
                # 添加修改后的类
                with shelve.open(sc_path) as mfile:
                    temp = mfile['equip']
                    temp.append(wait_equipment)
                    mfile['equip'] = temp
                break
            elif ask in ('n', 'N'):
                print("Stop change equpment message")
                break
            else:
                print("Error:invalid value.")

    def edit_connector(num):
        with shelve.open(sc_path) as mfile:
            equips = mfile["equip"]
            for eqp in equips:
                if eqp.id == ID:
                    wait_equipment = eqp  # 确认需要修改的设备

        break_sign = 0
        while(True):
            if break_sign == 1:
                break
            if connector1 == 'serial':
                while True:  # port must exist
                    port = input("Serial Port              >")
                    try:
                        serial.Serial(port)
                        break
                    except Exception as e:
                        e_str = str(e)
                        print('DEBUG:{}'.format(e))
                        if 'PermissionError' in e_str:
                            print("Error:{} has been open by other equipment.".format(port))
                        if 'FileNotFoundError' in e_str:
                            print("Error:{} does not exist.".format(port))
                break_ctr = 0
                while(True):
                    if break_ctr == 1:
                        break
                    baudrate = input("baudrate(default 115200) >")
                    parity =   input("parity(default None)     >")
                    byteszie = input("bytesize(default 8)      >")
                    stopbits = input("stopbits(default 1)      >")
                    timeout =  input("timeout(default 0.5)     >")

                    if baudrate == "":baudrate = 115200
                    if parity == "":parity = "N"
                    if byteszie == "":byteszie = 8.0
                    if stopbits == "":stopbits = 1.0
                    if timeout == "":timeout = 0.5

                
                    try:
                        para = [str(port), int(baudrate), float(byteszie), str(parity),  float(stopbits), float(timeout)]
                        inter = interface(0)
                        inter.paras = para
                        inter.connect()
                        break_sign = 1
                        
                    except Exception as e:
                        print("Error:Connect failed!Please confirm your editing of connector.")
                        return
                
                    print("Please confirm your editing:")
                    print("  Interface{}_port     >{}".format(num, para[0]))
                    print("  Interface{}_baudrate >{}".format(num, para[1]))
                    print("  Interface{}_bytesize >{}".format(num, para[2]))
                    print("  Interface{}_parity   >{}".format(num, para[3]))
                    print("  Interface{}_stopbits >{}".format(num, para[4]))
                    print("  Interface{}_timeout  >{}".format(num, para[5]))
                    while(True):
                        ask = input('Are you sure to change the connector?[y/N]')
                        if ask in ('y', 'Y'):
                            with shelve.open(sc_path) as mfile:
                                temp = mfile['equip']
                                for eqp in temp:
                                    if eqp.id == ID:
                                        temp.remove(eqp) 
                                        break
                                mfile['equip'] = temp
                            if num == 1:wait_equipment.connector1 = inter.interface
                            if num == 2:wait_equipment.connector2 = inter.interface
                            if num == 3:wait_equipment.connector3 = inter.interface
                            if num == 4:wait_equipment.connector4 = inter.interface
                            # 添加修改后的类
                            with shelve.open(sc_path) as mfile:
                                temp = mfile['equip']
                                print(temp)
                                temp.append(wait_equipment)
                            break_ctr = 1   
                            break

                        elif ask in ('n', 'N'):
                            print("Stop change equpment connector{}".format(num))
                            break_ctr = 1
                            break
                        else:
                            print("Error:invalid value.")
    if connector1 != None: # 输入接口1，则进行接口的配置，接口后面更接口类型，serial
        edit_connector(1)
    if connector2 != None: # 输入接口1，则进行接口的配置，接口后面更接口类型，serial
        edit_connector(2)
    if connector3 != None: # 输入接口1，则进行接口的配 置，接口后面更接口类型，serial
        edit_connector(3)
    if connector4 != None: # 输入接口1，则进行接口的配置，接口后面更接口类型，serial
        edit_connector(4)
           

        
if __name__ == "__main__":
    add_equipment_into_scenario(r"E:\project\tester\test\defaultScenario1")
    #show_equipment(r'E:\project\tester\test\defaultScenario1')
    # del_quipment_by_name_or_id(r'E:\project\easyTester\easyTester\test\defaultScenario1')
    # show_equipment(r'E:\project\tester\test\defaultScenario1')
    #edit_equipment(path_or_point= r'E:\project\tester\test\defaultScenario1', id = 1, name='serdial', connector1='serial')

