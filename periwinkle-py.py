# Import libraries
from mpd import MPDClient

import os
import platform

if platform.system() == "Linux":
    pw_Manner="dbus"
    print("dis is a linux")
    import gi
    gi.require_version('Gio', '2.0')
    from gi.repository import Gio
    import dbus

elif platform.system() == "Windows":
    pw_Manner="win10"
    from win10toast import ToastNotifier
    pw_Toaster=ToastNotifier()

else:
    print("You're running on an unsupported platform. Exiting.")
    exit()

pw_Client = MPDClient()
pw_Client.timeout = None
pw_Client.idletimeout = None
pw_Client.connect("localhost", 6600)

def pw_Notify(title, subtitle, manner):
    if manner=="gi":
        Application = Gio.Application.new("hello.world", Gio.ApplicationFlags.FLAGS_NONE)
        Application.register()
        Notification = Gio.Notification.new(str(title))
        Notification.set_body(str(subtitle))
        Icon = Gio.ThemedIcon.new("dialog-information")
        Notification.set_icon(Icon)
        Application.send_notification(None, Notification)
    elif manner=="dbus":
        obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
        obj = dbus.Interface(obj, "org.freedesktop.Notifications")
        obj.Notify("", 0, "dialog-information", title, subtitle, [], {"urgency": 1}, 10000)
    elif manner=="win10":
        pw_Toaster.show_toast(f"{title}",
                              f"{subtitle}",
                              duration=10,
                              threaded=True)

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
    pw_Notify("Stopped"," ",pw_Manner)

