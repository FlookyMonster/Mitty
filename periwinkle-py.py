

# Import libraries
from mpd import MPDClient
import gi
gi.require_version('Gio', '2.0')
from gi.repository import Gio

client = MPDClient()
client.timeout = None
client.idletimeout = None
client.connect("localhost", 6600)

def pw_Notify(title, subtitle):
    Application = Gio.Application.new("hello.world", Gio.ApplicationFlags.FLAGS_NONE)
    Application.register()
    Notification = Gio.Notification.new(str(title))
    Notification.set_body(str(subtitle))
    Icon = Gio.ThemedIcon.new("dialog-information")
    Notification.set_icon(Icon)
    Application.send_notification(None, Notification)

def pw_Refresh():
    global pw_CurrentSong
    pw_CurrentSong=client.currentsong()
    if pw_CurrentSong == {}:
        return False

#print(client.currentsong()['title'])

if pw_Refresh():
    pw_Notify(1,2)
else:
    pw_Notify("Stopped",2)
    

