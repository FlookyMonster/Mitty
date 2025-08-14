#!/usr/bin/python3

# Import libraries
from mpd import MPDClient
import platform
import sys
import subprocess
import os
import ffmpeg
import hashlib

mm_Client = MPDClient()
mm_Client.timeout = None
mm_Client.idletimeout = None
mm_Client.connect("127.0.0.1", 6600)

global mm_Manner

def mm_Help():
	help_text = "Help goes here"

def mm_AboutProgram():
	about = "Mitty - MPD client that's like Periwinkle but not"


def mm_SummonNotification(title, subtitle, cover=None):
    if mm_Manner == "dbus":
        obj = dbus.SessionBus().get_object("org.freedesktop.Notifications", "/org/freedesktop/Notifications")
        obj = dbus.Interface(obj, "org.freedesktop.Notifications")
        obj.Notify("", 
        0, 
        "", # Picture of the notification
        title, # Title
        subtitle, # Subtitle
        [], 
        {"urgency": 0}, 10000) # Urgency

    elif mm_Manner == "win10":
        newToast = Toast()

        try:
            newToast.AddImage(ToastDisplayImage.fromPath(cover))
        except TypeError:
            pass

        if subtitle=="":
            newToast.text_fields = [title]

        else:
            newToast.text_fields = [title, subtitle]

        newToast.on_activated = lambda _: print('Toast clicked!')
        mm_Toast.show_toast(newToast)

def mm_SaveAlbumCover(filename, output):
    try:
        out, err = (
            ffmpeg
            .input(filename)
            .output(output, an=None, vf='scale=256:256', vframes=1, format='image2', vcodec='png')
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print("FFmpeg stdout:")
        print(e.stdout.decode('utf-8'))
        print("FFmpeg stderr:")
        print(e.stderr.decode('utf-8'))


    #stdout=subprocess.PIPE,  # capture stdout
    #stderr=subprocess.PIPE   # capture stderr (FFmpeg writes most info here)


def mm_Refresh():
    if mm_Client.currentsong() == {}:
        return False

    else:
        return True

# Import different notification libraries for each operating system
if platform.system() == "Linux":
    mm_Manner = "dbus"
    mm_HomeDir = os.environ.get("HOME")
    import dbus

elif platform.system() == "Windows" and platform.release() == "10" or platform.release() == "11":
    mm_Manner = "win10"
    mm_HomeDir = os.environ.get("USERPROFILE")
    from windows_toasts import Toast, WindowsToaster, ToastDisplayImage
    mm_Toast = WindowsToaster("Mitty")
    
else:
    print("You're running on an unsupported platform. Exiting.")
    exit()

#mm_HomeDir = mm_HomeDir.replace('\\', '/')

print(mm_HomeDir)

mm_DirectoryAlbumCover=os.path.join(mm_HomeDir, "mitty")
mm_MusicDir=os.path.join(mm_HomeDir, "Music")

print(mm_MusicDir)

if os.path.exists(mm_DirectoryAlbumCover) == False:
    os.mkdir(mm_DirectoryAlbumCover)
    print(f"Directory created: {mm_DirectoryAlbumCover}")

try:
    mm_CurrentSong = f"{mm_Client.currentsong()['file']}"
except KeyError:
    mm_CurrentSong = ""

print(mm_CurrentSong)

if mm_CurrentSong != "":
    mm_CurrentSongDirectory = os.path.join(mm_MusicDir, mm_CurrentSong)
    mm_CurrentSongDirectory = mm_CurrentSongDirectory.replace('\\', '/')
    mm_HashedName = hashlib.sha256(mm_CurrentSong.encode('utf-8')).hexdigest()
    mm_OutputToSave = os.path.join(mm_DirectoryAlbumCover, f"{mm_HashedName}.png")

    if os.path.exists(mm_OutputToSave) == False:
        mm_SaveAlbumCover(mm_CurrentSongDirectory, mm_OutputToSave)
else:
    mm_CurrentSongDirectory, mm_OutputToSave = "", ""

if mm_Refresh():
    mm_SummonNotification(
        f"[{mm_Client.status()['state']}] {mm_Client.currentsong()['title']}", # Title
        f"{mm_Client.currentsong()['artist']}\n{mm_Client.currentsong()['album']} ({mm_Client.currentsong()['date']})", # Subtitle
        mm_OutputToSave
    ) 

else:
    mm_SummonNotification("Stopped", "")
