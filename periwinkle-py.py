#!/usr/bin/python3

# Import libraries
from mpd import MPDClient
import platform

# Import different notification libraries for each operating system
if platform.system() == "Linux":
    pw_Manner = "dbus"
    import dbus

elif platform.system() == "Windows" and platform.release() == "10" or platform.release() == "11":
    pw_Manner = "win10"
    from windows_toasts import Toast, WindowsToaster
    pw_Toast = WindowsToaster("Periwinkle")
    
else:
    print("You're running on an unsupported platform. Exiting.")
    exit()

pw_Client = MPDClient()
pw_Client.timeout = None
pw_Client.idletimeout = None
pw_Client.connect("localhost", 6600)

def pw_Notify(title, subtitle, manner):
    if manner == "dbus":
        obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
        obj = dbus.Interface(obj, "org.freedesktop.Notifications")
        obj.Notify("", 
        0, 
        "", # Picture of the notification
        title, # Title
        subtitle, # Subtitle
        [], 
        {"urgency": 0}, 10000) # Urgency

    elif manner == "win10":
        newToast = Toast()
        if subtitle=="":
            newToast.text_fields = [title]

        else:
            newToast.text_fields = [title, subtitle]

        newToast.on_activated = lambda _: print('Toast clicked!')
        pw_Toast.show_toast(newToast)

def pw_Refresh():
    if pw_Client.currentsong() == {}:
        return False

    else:
        return True

if pw_Refresh():
    pw_Notify(
        f"[{pw_Client.status()['state']}] {pw_Client.currentsong()['title']}", # Title
        f"{pw_Client.currentsong()['artist']}\n{pw_Client.currentsong()['album']} ({pw_Client.currentsong()['date']})", # Subtitle
        pw_Manner # System used to display the notif
    ) 

else:
    pw_Notify("Stopped", "", pw_Manner)

