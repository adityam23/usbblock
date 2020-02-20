from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import usbblock
import sqlite3


# print(__file__)
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# os.path.join(BASE_DIR, "blocked_proc.db")
db_path = r'C:\Program Files\blockedUSB.db'
# db.execute('CREATE TABLE IF NOT EXISTS blocked_USB(Name TEXT, HardwareID TEXT PRIMARY KEY)')
# db.execute('CREATE TABLE IF NOT EXISTS USBList(Name TEXT, HardwareID TEXT PRIMARY KEY)')
# db.commit()

L_BLUE = '#e1f0fd'
GREEN = '#05a19c'
RED = '#e41749'

# root window
root = Tk()
root.title("USB Blocker")
root.geometry('700x600')
root.configure(bg=L_BLUE)
heading = Label(root, text="USB Blocker", font=(
    "Segoe UI ", 25), height="2", bg=L_BLUE)
heading.pack()

br = StringVar(value=' ')
res = StringVar(value=' ')
label = Label(root, font='Helvetica', textvariable=br, bg=L_BLUE)
label.pack()
under = Label(root, textvariable=res, font='Helvetica', bg=L_BLUE)
under.pack(side=BOTTOM)


# ------------------------------------------------------------------------------------------------


# notebook/tabs
tabs = ttk.Notebook(root)
act_tab = ttk.Frame(tabs)
bloc_tab = ttk.Frame(tabs)
tabs.add(act_tab, text='Connected USB')
tabs.add(bloc_tab, text='Blocked USB')
tabs.pack()


# ------------------------------------------------------------------------------------------------


# Blocked USB
Label(bloc_tab, text="Blocked USB").pack()
scrollbar = Scrollbar(bloc_tab)
scrollbar.pack(side=RIGHT, fill='y')
block_list = Listbox(bloc_tab, width=70, height=20)  # , selectmode=MULTIPLE
block_list.config(yscrollcommand=scrollbar.set)


def update_block_list():
    block_list.delete(0, END)
    '''db = sqlite3.connect(db_path)
    cur = db.cursor()
    cur.execute(
    'CREATE TABLE IF NOT EXISTS blocked(id INTEGER,application TEXT PRIMARY KEY)')
    blocked = cur.execute('SELECT * FROM blocked').fetchall()'''
    devices = usbblock.show_devices()
    if devices:
        for usb in devices:
            block_list.insert(END, usb[0])

    block_list.pack()


update_block_list()


def unblock_button():
    br.set('Unblocking USB')
    label.update()
    index = block_list.curselection()
    blocked = block_list.get(index)
    usbblock.unblockit(blocked)

    br.set(' ')
    label.update()
    update_block_list()


# for i in range(10):
#   block_list.insert(END, str(i))
#   block_list.pack()


unblock = Button(bloc_tab, text="Unblock",
                 command=unblock_button).pack(side=BOTTOM)


# ------------------------------------------------------------------------------------------------


# Connected USB
Label(act_tab, text="Connected USB").pack()
scrollbar = Scrollbar(act_tab)
scrollbar.pack(side=RIGHT, fill='y')
usb_list = Listbox(act_tab, width=70, height=20)  # , selectmode=MULTIPLE
usb_list.config(yscrollcommand=scrollbar.set)


def update_usb_list():
    usb_list.delete(0, END)
    devices = usbblock.find_devices_devcon()
    blocked = usbblock.show_devices()
    blcked = []
    if blocked:
        for x in blocked:
            blcked.append(x[0])
            blocked = blcked
    # print(blocked)
    if devices[1] != 0.0:
        sort = []
        for usb in devices[0]:
            if blocked:
                if usb['name'] not in blocked:
                    sort.append(usb['name'])

            else:
                # print('here-<')
                sort.append(usb['name'])
        # process_list.insert(END, proc['name'])

        sort = sorted(sort)
        for x in sort:
            usb_list.insert(END, x)

    usb_list.pack()
    # heading.after(5000, update_proc_list)


update_usb_list()


'''def terminate_button():
    br.set('Terminating process')
    label.configure(bg=GREEN)
    label.update()
    index = process_list.curselection()

    for i in index:
        proc = process_list.get(i)
        blocking.terminator(proc)
    for i in index:
        process_list.delete(i)

    br.set('Process Terminated')
    label.update()
    update_proc_list()
    br.set(' ')
    label.configure(bg=L_BLUE)
    label.update()


terminate = Button(act_tab, text="Terminate",
                   command=terminate_button).pack(expand=TRUE, side=LEFT, fill=X)'''


def block_button():
    br.set('Blocking USB')
    label.configure(bg=GREEN)
    label.update()
    index = usb_list.curselection()
    device = usb_list.get(index)
    usbblock.blockit(device)
    usb_list.delete(index)

    br.set('Device blocked')
    label.update()
    update_block_list()
    update_usb_list()
    br.set(' ')
    label.configure(bg=L_BLUE)
    label.update()
    update_usb_list()
    '''res.set('PLEASE RESTART YOUR PC AFTER BLOCKING PROCESS')
    under.configure(bg=RED)
    under.update()'''


block = Button(act_tab, text="Block", command=block_button).pack(
    expand=TRUE, side=RIGHT, padx=5, fill=X)


# ------------------------------------------------------------------------------------------------

def ref_button():
    br.set('Refreshing')
    label.update()
    update_block_list()
    update_usb_list()
    br.set(' ')
    label.update()


refresh = Button(root, text="Refresh", bg="#b1d8fa", font=(
    "Helvetica", 10), height="1", activebackground="#69b4f5", width="25", command=ref_button)
refresh.pack()

# ------------------------------------------------------------------------------------------------


def all_block_button():
    br.set('Blocking all storage devices')
    label.update()
    usbblock.block_store()
    # br.set(' Done ')
    # label.update()
    # br.set(' ')
    # label.update()


full_frame = Frame(root)
full_frame.pack(padx=20)

all_block = Button(full_frame, text="Block all", bg="#b1d8fa", font=(
    "Helvetica", 10), height="1", activebackground="#69b4f5", width="25", command=all_block_button).pack(side=LEFT)


def all_unblock_button():
    br.set('Unblocking all storage devices')
    label.update()
    usbblock.unblock_store()
    # br.set(' ')
    # label.update()


all_unblock = Button(full_frame, text="Unblock all", bg="#b1d8fa", font=(
    "Helvetica", 10), height="1", activebackground="#69b4f5", width="25", command=all_unblock_button).pack(side=RIGHT)


# ------------------------------------------------------------------------------------------------


# Run
try:
    usbblock.devcon_check()
except AssertionError:
    tabs.pack_forget()
    refresh.pack_forget()
    messagebox.showerror(
        'Error', 'Devcon not found. Please install devcon to a location pointed to by the PATH variable to disable individual devices')

root.mainloop()
