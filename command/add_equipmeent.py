import os
import scene
import equip
import shelve
import interface
import serial

def add_equipment_into_scenario(path_or_equip):
    "增加一个设备进入测试"

    # input a absoult path
    if "\\" in path_or_equip: 
        path = path_or_equip
        while(True):
            equipment = input("Equipment:")
            if equipment not in list(equips.keys()):
                print("Error: unkwon type of euqipment,support {}".format("|".join(list(equips.keys()))))
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

    with shelve.open("{}\\{}".format(path, sc)) as mfile:equips = mfile['support']

    # if input a unkwon equipment by cmd, return
    if equipment not in list(equips.keys()):
        print("Error:unkwon type of euqipment,support {}".format("|".join(list(equips.keys()))))
        return 0
    while(True):
        model = input("Model:")
        if model not in equips[equipment]:
            print("Error:unkwon model of equipment,support {}".format("|".join(equips[equipment])))
        else:
            break

    name = input("Name:")
    if name == "":name = "defaultName"
    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        print(sc)
        for equ in mfile['equip']:
            if name == equ.name:
                print("Error:equipment name conflict.")
                return -1

    hardver = input("Hardware version:")
    if hardver == "":hardver = "defalutHardver"

    softver = input("Software version:")
    if softver == "":softver = "defalultSoftver"

    checked = input("Checked:")
    if checked == "":checked = 1

    usermsg = input("User message:")
    if usermsg == "":usermsg = "defaultMessage"

    # ask whether to bind interface
    ser_paras = []
    count = 1
    break_sign = 0
    
    while(True):
        if break_sign == 1:
            break
        if count == 1: # only one time
            ask = input("Do you want to bind interface to the equipment?[y/N]")
        # YES
        if ask in ('y', 'Y'):
            print("You must choice interface type:0 serial, 1 tcp client, 2 tcp server, 3 visa ip.")
            print("You can input number or interface name,likes serial...")
            if count == 1:
                print("You are editing interface #{}.Usually used for cmd sending and receiving.".format(count))
            if count == 2:
                print("You are editing interface #{}.Usually used for inputing diff.".format(count))
            interface_type = input("Interface type:")
            if interface_type in ('0', 'serial'):

                while(True): # port must exist
                    port     = input("Serial Port              >")
                    try:
                        serial.Serial(port).close()
                        break
                    except Exception as e:
                        print("{} does not exist.".format(port))

                baudrate = input("baudrate(default 115200) >")
                parity   = input("parity(default None)     >")
                byteszie = input("bytesize(default 8)      >")              
                stopbits = input("stopbits(default 1)      >")
                timeout  = input("timeout(default 0.5)     >")
                # default parameter of serial
                if baudrate == "":baudrate = 115200
                if parity == "":parity = 'N'
                if byteszie == "":byteszie = 8.0
                if stopbits == "":stopbits = 1.0
                if timeout == "":timeout = 0.5

                ser_paras.append([str(port), int(baudrate), int(byteszie), 
                    str(parity), int(stopbits), float(timeout)])
                # add another
                while(True):
                    another_ask = input("Do you have an another want to bind?[y/N]")
                    if another_ask in ('y', 'Y'):
                        count = count + 1
                        into_confirm = 0
                        break
                    elif another_ask in ('n', 'N') or count > 2:
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
                    while(True):
                        confirm_ask = input("Are you confirm?[y/N]")
                        if confirm_ask in ('y', 'Y'):
                            break_sign = 1
                            break
                        elif confirm_ask in ('n', 'N'):
                            count = 1
                            ser_paras = []
                            print("Rebind interface.Edit again...")
                            break
                        else:
                            print("Error:invalid value.")
        # NO
        elif ask in ('n', 'N'):
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
            inter = interface.interface(0)
            inter.paras = (para[0],para[1],para[2],para[3],para[4])
            inter.connect()
        if interface_count == 1:
            equipobj.connector1 = inter.interface
        if interface_count == 2:
            equipobj.connector2 = inter.interface

    # write into shelve
    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        temp = mfile['equip']
        temp.append(equipobj)
        mfile['equip'] = temp
    
    with shelve.open("{}\\{}".format(path, sc)) as mfile:
        print(mfile['equip'])
    
def del_quipment_by_name_or_id(path_or_point):
    "通过指定名称和ID删除测试场景中的设备"
    if '\\' in path_or_point: # absolute path
        path = path_or_point
    else:
        path = os.getcwd()

    sc_file = scene.manageScenario._isinfile(path)

    shelve_file = "{}\\{}".format(path, sc_file)
    
    print("Please input id or name,just choice one of them")
    id = input("ID:")
    name = input("Name:")

    with shelve.open(shelve_file) as mfile:
        equips = mfile['equip']
        for equip in equips:
            if (int(id) == equip.id) or (name == equip.name):
                while(True):
                    _ask = "Are you sure to remove the equipment id-{},name-{}?[y/N]".format(equip.id, equip.name)
                    ask = input(_ask)
                    if ask in ("y", "Y"):
                        equips.remove(equip)
                        mfile['equip'] = equips
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

    shelve_file_path = "{}\\{}".format(path, sc_file)
    with shelve.open(shelve_file_path) as mfile:
        equips = mfile['equip']
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
            print("ID-{:<2} Name-{:<10} Model-{:<5} Equipment-{:<5}  Checked-{:<2}".format(id, name, model, equipment, checked))

def edit_equipment(path_or_point = None, name = None, id = None,
    cname = None, equipment = None, model = None, usermsg = None, hardver = None,
    softver = None, checked = None, ctr1 = None, ctr2 = None, ctr3 = None, ctr4 = None):
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
            path = os.getcwd()    # current workspace
    else:
        path = os.getcwd()

    sc_file = scene.manageScenario._isinfile(path)  # search secnario shelve file
    sc_path = "{}\\{}".format(path, sc_file)

    wait_equipment = 0  # 待修改的设备

    # check equipment exits
    if name == None and id == None:
        print("Error:Must specify at one of id or name.")
        return -1
    elif id != None:
        with shelve.open(sc_path) as mfile:
            match = 0
            equips = mfile['equip']
            if equips == []:
                print("WARN:No equipment in scenario-{}.".format(sc_path))
                return
            for eqp in equips:
                if eqp.id == int(id):
                    print("Match a equipment which id is {},name is {}.".format(eqp.id, eqp.name))
                    wait_equipment = eqp     # 确认需要修改的设备
                    equips.remove(eqp)       # 将需要修改的设备移出列表
                    mfile['equip'] = equips  # 替换shelve文件中的设备
                    match = 1
                    break
            if match == 0:
                print("Error:No equipment's id is {}.".format(id))
                return -1
    else:
        with shelve.open(sc_path) as mfile:
            match = 0
            equips = mfile['equip']
            if equips == []:
                print("WARN:No equipment in scenario-{}.".format(sc_path))
                return
            for eqp in equips:
                if eqp.name == name:
                    print("Match a equipment which name is {},id is {}.".format(eqp.name, eqp.id))
                    match = 1
                    wait_equipment = eqp     # 确认需要修改的设备
                    equips.remove(eqp)       # 将需要修改的设备移出列表
                    mfile['equip'] = equips  # 替换shelve文件中的设备
                    break
            if match == 0:
                print("Error:No equipment's name is {}.".format(eqp.name))
                return -1
            
    if cname != None:wait_equipment.name = cname
    if equipment != None:wait_equipment.equipment = equipment
    
    



    






if __name__ == "__main__":
    # add_equipment_into_scenario(r'E:\project\easyTester\easyTester\test\defaultScenario1')
    # show_equipment(r'E:\project\easyTester\easyTester\test\defaultScenario1')
    # del_quipment_by_name_or_id(r'E:\project\easyTester\easyTester\test\defaultScenario1')
    # show_equipment('.')
    edit_equipment(id = 3)

    


