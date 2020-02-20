import winreg
import re
import sqlite3
import subprocess

db = sqlite3.connect(r'C:\Program Files\blockedUSB.db')
db.execute(
    'CREATE TABLE IF NOT EXISTS blocked_USB(Name TEXT, HardwareID TEXT PRIMARY KEY)')
db.execute(
    'CREATE TABLE IF NOT EXISTS USBList(Name TEXT, HardwareID TEXT PRIMARY KEY)')
db.commit()
usb_key = r'SYSTEM\CurrentControlSet\Services\USBSTOR'


def block_store():
    b_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                           usb_key, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(b_key, 'Start', 0, winreg.REG_DWORD, 4)
    # print('usb storage devices blocked')
    winreg.CloseKey(b_key)


def unblock_store():
    b_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                           usb_key, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(b_key, 'Start', 0, winreg.REG_DWORD, 3)
    # print('usb storage devices unblocked')
    winreg.CloseKey(b_key)


def find_devices_devcon():
    cur = db.cursor()
    cur.execute('DROP TABLE USBList')
    db.commit()
    devcon = subprocess.run('powershell devcon hwids USBSTOR\DISK*',
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = devcon.stdout
    # print(devcon.stderr)
    line_list = output.split('\n')
    # line_list.remove('HTREE\\ROOT\\0') # unnamed value breaks splitting
    # remove ending text. Should have 14 lines for every device connected
    line_list = line_list[:-2]
    # 2nd item is name, 4th item is full hwid
    no_of_dev = len(line_list)
    # print(no_of_dev)
    assert no_of_dev % 14 == 0
    no_of_dev /= 14
    devlist, counter = [], 1
    dev = {}
    for line in line_list:
        # print('counter = {}'.format(counter))
        # print(line, end='----------\n')
        if counter == 2:
            name = line.split(':')[1].strip()
            dev['name'] = name

        if counter == 4:
            hwid = line.strip()
            dev['id'] = hwid
            # hwids.append(line)

        if counter == 14:
            counter = 0

        if len(dev) == 2:
            devlist.append(dev)
            dev = {}

        counter += 1

    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS USBList(Name TEXT, HardwareID TEXT PRIMARY KEY)')
    for dev in devlist:
        try:
            cur.execute(
                'INSERT INTO USBList(Name, HardwareID) VALUES(?,?)', (dev['name'], dev['id']))
        except sqlite3.IntegrityError:
            pass
        finally:
            db.commit()
    # print(devlist, no_of_dev)
    return (devlist, no_of_dev)


def show_devices():
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS blocked_USB(Name TEXT, HardwareID TEXT)')
    val = cur.execute('SELECT * FROM blocked_USB').fetchall()
    if val != []:
        # print(val, end='<')
        return val

    else:
        return None


def blockit(name):
    cur = db.cursor()
    dev = cur.execute(
        'SELECT HardwareID FROM USBList WHERE Name = (?)', (name,)).fetchone()
    if dev is not None:
        dev = dev[0]
        cur.execute(
            'CREATE TABLE IF NOT EXISTS blocked_USB(Name TEXT, HardwareID TEXT)')
        try:
            cur.execute('INSERT INTO blocked_USB values(?,?)', (name, dev))
            blocking = subprocess.run('powershell devcon disable {}'.format(
                dev), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except sqlite3.IntegrityError:
            pass
        finally:
            db.commit()

    # blocking = subprocess.run('powershell devcon disable {}'.format(name), stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=
    #    True)

    # print(blocking.output)


def unblockit(name):
    cur = db.cursor()
    dev = cur.execute(
        'SELECT HardwareID FROM blocked_USB WHERE Name = (?)', (name,)).fetchone()
    if dev is not None:
        dev = dev[0]
        # print(dev)
        blocking = subprocess.run('powershell devcon enable {}'.format(
            dev), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        cur.execute('DELETE FROM blocked_USB WHERE Name = (?)', (name,))
        db.commit()
        # print(blocking.stdout)


def devcon_check():
    devcon = subprocess.run('powershell devcon hwids USBSTOR\DISK*',
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert (devcon.stderr == '')


# devcon_check()
# print(find_devices_devcon())
# print(show_devices())
# unblockit('Kingston DataTraveler 2.0 USB Device')
# find_devices_devcon()
