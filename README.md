# usbblock
A USB drive blocker that can restrict drives from being able to connect to the computer till they are unblocked. Written in python. Also available in C# because idk



USB Blocker
This is an application that list the currently connected USB removable drives on the system, with the options to either block/unblock the given device. If the device is blocked, it won’t be detected by the system until it has been unblocked, even if the USB port is changed.

Features:
1.	Shows connected USB removable drives
2.	Can block/unblock them as per user needs
3.	Can be extended to block particular vendors or product models [Not implemented]
4.	Written in python/C#

Usage:
To use the application, run it as Administrator. 
1.	Select the drive to block from the list of connected devices shown
2.	If you connect another device after starting the application, refresh it and it should show up on the connected devices list
3.	Click ‘Block’ to block the USB device on the system. The device is instantly ejected and blocked by the system. Persistent across reboots.
4.	You should see the devices you blocked in the blocked devices list
5.	Select from the blocked devices list and click ‘Unblock’ to unblock
6.	If using the python version, all USB devices can be blocked/unblocked using the ‘Block All’/’Unblock All’ buttons. This disables removable drives on the system.


Made using:
1.	Implemented in 2 ways, using python and using C#
2.	For python, GUI made using tkinter, blocking all devices done via winreg and blocking individual devices implemented via DevCon utility
3.	For C#, GUI made using WinForms, getting list of devices done via WMI and blocking/unblocking done via PowerShell commands Disable-PnPDevice/Enable-PnPDevice


Pictures of the application in use: 

Python:
![img1](https://github.com/adityam23/usbblock/blob/master/Picture1.png)
![img2](https://github.com/adityam23/usbblock/blob/master/Picture2.png)
 ![img3](https://github.com/adityam23/usbblock/blob/master/Picture3.png)
 ![img4](https://github.com/adityam23/usbblock/blob/master/Picture4.png)
 
 
 










C#:
 
 ![img5](https://github.com/adityam23/usbblock/blob/master/Picture5.png)
 

Further extension:
We can add the functionality of blocking USB devices by a specific vendor and by the specific product model by utilizing the Vendor ID(VID) and Product ID(PID) of a given USB Device. 
To achieve this, there are 2 ways, but both are not straightforward and require some mixing and matching to implement properly. 

One way is to use the WMI (Windows Management Interface) and query Win32_PnpEntity to get a list of all Pnp Devices. Then, store the PnPDeviceID and the Hardware IDs associated with it. Then, the PnpDeviceID can be cross referenced with the database of devices connected to match the hardware ID and the device. This gives us the hardware ID for a particular device. The Hardware ID contains the substrings VID_vvvv&PID_pppp where vvvv is the 4-digit vendor ID and pppp is the 4 digit product ID. We can then use DevCon to disable the Vendor ID using command as devcon disable *VID_vvvv* 

The other way is to query Devcon with devcon find *VID_* and select the devices with the caption “USB Mass Storage Device” and note the given ID next to it. Then, using the Serial number given at the end of the ID, we can match it with the serial number saved in the database to match up the device with the ID. We can then extract the VID and PID mentioned within the ID in the form VID_vvvv&PID_pppp to get the VID and PID values. Using DevCon, as described above, we can disable the VID and PID to achieve the blocking action for a specific vendor and/or product. 

Since this task requires cross referencing multiple values and cannot be done without using the DevCon utility, the only other way to do this is using an advanced Group Policy that has the strings of VID/PID specified for matching against. This cannot be don’t programmatically. The values of VID/PID for a given device can be found using 
Device Manager->Selecting the Device->Properties->Details->Choosing the ‘Hardware ID’ property 
and noting down these values. To block using the Group Policy, further reading is given at the link:  https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc731387(v=ws.10) 
