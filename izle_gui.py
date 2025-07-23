"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Application GUI module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from PIL import Image, ImageTk
from tkinter import Toplevel, PhotoImage
from tkinter import filedialog

import sys
import os
import pathlib
import time
from copy import deepcopy
from threading import Thread

import mpv

from menu import Menu
from icon_generator import IconGenerator
from customized_ttk_widgets import CheckbuttonCustomized
from channels import Channels, Channel

ctrl = False
shift = False
ctrl_shift = False


def ctrl_on(event):
    global ctrl, shift, ctrl_shift
    ctrl = True
    if shift:
        ctrl_shift = True
        ctrl = False
        shift = False
    else:
        ctrl_shift = False


def ctrl_off(event):
    global ctrl, shift, ctrl_shift
    ctrl = False
    ctrl_shift = False


def shift_on(event):
    global ctrl, shift, ctrl_shift
    shift = True
    if ctrl:
        ctrl_shift = True
        ctrl = False
        shift = False
    else:
        ctrl_shift = False


def shift_off(event):
    global ctrl, shift, ctrl_shift
    shift = False
    ctrl_shift = False


def resource_path(relative_path):
    """ Get absolute path to resources, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # base_path = sys._MEIPASS
        base_path = os.path.join(sys._MEIPASS, "img")
    except Exception:
        base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)
    print("Resource path:", path)
    return path


# ----------------------------------------------------------------------------------------------


iconGenerator = IconGenerator()


class Progressindicator(ttk.Frame):
    def __init__(self, master, task, **kwargs):
        super().__init__(master, **kwargs)

        self.main_task = task

        # self['relief'] = 'raised'

        self['padding'] = (0, 0, 0, 0)

        self.size = (16, 16)

        self.theta = 0
        self.deltatheta = 60

        self.images_from_generator(self.size)
        # try:
        #     image_path = sys._MEIPASS + os.sep + 'icons' + os.sep + 'sync.svg'
        # except  :
        #     image_path = "icons/sync.svg"
        # print("Image path:",image_path)
        # self.images_from_svg(image_path,self.size)

        self.label = ttk.Label(self, image=self.photoimage)
        self.label.grid()
        self.label.bind("<Button-1>", self.start_progress)

        self.progressing = False

    def start_progress(self, event):
        if self.progressing is False:
            self.progressing = True

            self.indicator_thread = Thread(target=self.rotate_image)
            self.indicator_thread.start()

            self.main_thread = Thread(target=self.main_task)
            self.main_thread.start()

    def stop_progress(self):
        if self.progressing:
            self.progressing = False
            self.indicator_thread.join()

    def rotate_image(self):
        print('Indicator started.\n')
        while self.progressing:
            self.theta = (self.theta+self.deltatheta) % 360
            image = self.image.rotate(
                self.theta, Image.NEAREST, expand=0).resize(self.size)
            self.photoimage = ImageTk.PhotoImage(image)
            self.label.configure(image=self.photoimage)
            time.sleep(0.05*2)
        print("Indicator stopped.")

    def images_from_generator(self, output_size):
        iconGenerator = IconGenerator()
        self.image = iconGenerator.sync(size=256)
        self.photoimage = ImageTk.PhotoImage(self.image.resize(output_size))


class FrameText(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.text = tk.Text(self,
                            xscrollcommand=self.hscrollbar.set,
                            yscrollcommand=self.vscrollbar.set,
                            wrap=tk.NONE,
                            height=10,
                            width=20, padx=10, pady=5
                            )
        self.hscrollbar.config(command=self.text.xview)
        self.vscrollbar.config(command=self.text.yview)
        self.text.grid(row=0, column=0, sticky="we")
        self.hscrollbar.grid(row=1, column=0, sticky='we')
        self.vscrollbar.grid(row=0, column=1, sticky='ns')

        self.columnconfigure(0, weight=100)
        self.columnconfigure(1, weight=0)

        self.rowconfigure(0, weight=100)
        self.rowconfigure(1, weight=0)


class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text = text_widget

    def write(self, string):
        self.text.insert('end', string)
        self.text.see('end')

    def flush(self):
        pass


class FrameChannel(ttk.Frame):
    def __init__(self, master, **kwargs):
        self.kwargs = kwargs

        self.app = None
        if 'app' in kwargs.keys():
            self.app = kwargs['app']
            kwargs.pop('app')
        self.channel = self.app.channel
        self.channel_added = False

        super().__init__(master, **kwargs)

        self['relief'] = 'raised'
        self['padding'] = (2, 4, 2, 2)

        # style = ttk.Style(self)
        # layout = style.layout('TFrame')
        # print("Frame layout:", layout)
        # print("Border options:", style.element_options('Frame.border'))
        # style.configure('TFrame', bordercolor="green",
        #                 borderwidth=1, relief="flat")

        # ------------------------------------------------------

        labelType = ttk.Label(self, text="Type:", padding=(0, -4, 0, 0))
        labelName = ttk.Label(self, text="Channel name:")
        labelVideo = ttk.Label(self, text="Playlist URL:")
        labelWebUrl = ttk.Label(self, text="Web site:")
        labelWatchlinks = ttk.Label(self, text="Watchlinks:")

        self.labelWebUrl = labelWebUrl
        self.labelWatchlinks = labelWatchlinks
        self.labelVideo = labelVideo

        labelType.grid(row=0, column=0, padx=(4, 2), pady=(6, 2), sticky=tk.E)
        labelName.grid(row=1, column=0, padx=(4, 2), pady=(6, 2), sticky=tk.E)
        labelWebUrl.grid(row=2, column=0, padx=(
            4, 2), pady=(4, 4), sticky=tk.E)
        labelVideo.grid(row=3, column=0, padx=(4, 2), pady=(4, 2), sticky=tk.E)
        labelWatchlinks.grid(row=5, column=0, padx=(4, 2),
                             pady=(4, 2), sticky=tk.E)

        # ------------------------------------------------------

        frameType = ttk.Frame(self)

        self.channelType = tk.IntVar(self, 0)
        r1 = ttk.Radiobutton(frameType, value=0, variable=self.channelType,
                             takefocus=False, text='Basic')
        r2 = ttk.Radiobutton(frameType, value=1,  variable=self.channelType,
                             takefocus=False, text='Live stream')
        r3 = ttk.Radiobutton(frameType, value=2,  variable=self.channelType,
                             takefocus=False, text='Youtube watch')

        r1.grid(row=0, column=1, sticky=tk.EW)
        r2.grid(row=0, column=2, sticky=tk.EW)
        r3.grid(row=0, column=3, sticky=tk.EW)

        self.channelType.trace_add('write', self.channel_type_changed)

        self.frameType = frameType

        # ----------------------

        self.name = tk.StringVar()
        entryName = ttk.Entry(self, textvariable=self.name)

        # ----------------------

        self.web = tk.StringVar()
        entryWebUrl = ttk.Entry(self, textvariable=self.web)
        self.entryWebUrl = entryWebUrl

        # ----------------------

        self.video = tk.StringVar()
        entryVideo = ttk.Entry(self, textvariable=self.video)
        self.entryVideo = entryVideo

        # ----------------------

        frameUpdateLiveStream = ttk.Frame(self)
        self.frameUpdateLiveStream = frameUpdateLiveStream

        self.first_last = tk.IntVar()

        radioButtonF = ttk.Radiobutton(frameUpdateLiveStream, value=0,
                                       variable=self.first_last,
                                       takefocus=False, text='First m3u8')
        radioButtonL = ttk.Radiobutton(frameUpdateLiveStream, value=-1,
                                       variable=self.first_last,
                                       takefocus=False, text='Last m3u8')
        self.indicatorUpdateLiveStreamVideoURL = Progressindicator(
            frameUpdateLiveStream, self.app.channel_m3u8_url_update)

        radioButtonF.grid(row=0, column=0, padx=2,
                          pady=(0, 0), sticky=tk.NS+tk.W)
        radioButtonL.grid(row=0, column=1, padx=2,
                          pady=(0, 0), sticky=tk.NS+tk.W)
        self.indicatorUpdateLiveStreamVideoURL.grid(row=0, column=3,
                                                    padx=(10, 2),
                                                    pady=(0, 0),
                                                    sticky=tk.NS+tk.W)
        frameUpdateLiveStream.columnconfigure(3, weight=1)

        # ----------------------

        font1 = tkFont.Font(family='Helvetica', size=-12, weight='normal')
        comboboxWatchlinks = ttk.Combobox(self)
        # comboboxWatchlinks.grid(
        #     column=0, row=0, columnspan=4, padx=(2, 10), pady=(2, 2), ipadx=0, ipady=0, sticky=(tk.EW, tk.N))
        comboboxWatchlinks['state'] = 'readonly'
        comboboxWatchlinks['justify'] = 'left'
        comboboxWatchlinks['font'] = font1
        comboboxWatchlinks.bind('<<ComboboxSelected>>', self.watchlink_changed)
        self.comboboxWatchlinks = comboboxWatchlinks

        # ----------------------

        frameUpdateWatchlinks = ttk.Frame(self)
        self.frameUpdateWatchlinks = frameUpdateWatchlinks

        labelMaxLinks = ttk.Label(frameUpdateWatchlinks, text="Max. links")
        labelMaxLinks.grid(row=0, column=0)

        self.maxLink = tk.IntVar()
        self.maxLink.trace_add('write', self.max_link_changed)
        entryMaxLink = ttk.Entry(frameUpdateWatchlinks,
                                 textvariable=self.maxLink, width=2)
        entryMaxLink.grid(row=0, column=1,
                          padx=(2, 4), pady=(2, 4), sticky=tk.W)

        self.indicatorUpdateWatchlinks = Progressindicator(frameUpdateWatchlinks,
                                                           self.app.channel_watch_links_update)
        self.indicatorUpdateWatchlinks.grid(row=0, column=3,
                                            padx=(10, 2), pady=(2, 0),
                                            sticky=tk.NS+tk.W)

        # ------------------------------------------------------

        frameType.grid(row=0, column=1, sticky=tk.EW)
        entryName.grid(row=1, column=1, columnspan=4,
                       padx=(2, 4), pady=(4, 2), sticky=tk.EW)
        entryWebUrl.grid(row=2, column=1, columnspan=4,
                         padx=(2, 4), pady=(2, 4), sticky=tk.EW)
        entryVideo.grid(row=3, column=1, columnspan=4,
                        padx=(2, 4), pady=(2, 2), sticky=tk.EW)
        frameUpdateLiveStream.grid(row=4, column=1, sticky=tk.EW)
        comboboxWatchlinks.grid(row=5, column=1, columnspan=4,
                                padx=(2, 15), pady=(2, 2), sticky=tk.EW)
        frameUpdateWatchlinks.grid(row=6, column=1,
                                   padx=(2, 4), pady=(2, 4), sticky=tk.EW)

        # ------------------------------------------------------

        framePlayer = ttk.Frame(self, relief="raised", borderwidth=2)
        framePlayer.grid(row=7, column=1, padx=(
            2, 2), pady=(2, 5), sticky=tk.W)

        width = 192*16/9
        height = 192
        self.canvas = tk.Canvas(framePlayer, width=width,
                                height=height, bg='black')
        self.canvas.grid()
        # any_widget._root() / any_widget.winfo_toplevel().master
        # if self._root().call('tk', 'windowingsystem') == 'win32':
        if self.winfo_toplevel().master.call('tk', 'windowingsystem') == 'win32':
            self.player = mpv.MPV(ytdl=True,
                                  input_default_bindings=False,
                                  input_vo_keyboard=False,
                                  log_handler=self.player_log)
        else:
            self.player = mpv.MPV(ytdl=True,
                                  input_default_bindings=False,
                                  input_vo_keyboard=False,
                                  log_handler=self.player_log, vo='xv,x11')

        self.player.set_loglevel('error')
        canvasID = self.canvas.winfo_id()
        self.player.wid = str(canvasID)

        # ------------------------------------------------------
        if self.app.gui.call('tk', 'windowingsystem') == 'win32':
            self.canvas.bind(
                '<MouseWheel>', lambda event: self.player_volume_up_down(event))
            self.canvas.bind(
                '<Button-1>', lambda event: self.player_cycle_pause(event))
        else:
            self.player.keybind('MBTN_LEFT', "cycle pause")
            self.player.keybind('WHEEL_UP', "add volume +5")
            self.player.keybind('WHEEL_DOWN', "add volume -5")
        # ------------------------------------------------------
        self.imgSave = ImageTk.PhotoImage(
            iconGenerator.check(size=18, margin=(0, 0, 0, 0)))
        labelSaveChannel = ttk.Label(
            self, compound="image", image=self.imgSave)
        labelSaveChannel.grid(row=8, column=2,
                              padx=(0, 10), pady=(0, 8), sticky=tk.E)
        labelSaveChannel.bind('<Button-1>', self.save_channel)
        # ------------------------------------------------------

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

    def player_log(self, loglevel, component, message):
        print('Mini player > [{}] {}: {}'.format(loglevel, component, message))

    def watchlink_changed(self, event):
        self.channel.iWatchlink = self.comboboxWatchlinks.current()
        self.app.channel_play(self.channel)

    def channel_type_changed(self, var, index, mode):
        # print(f"|{var}| |{index}| |{mode}|")
        self.channel.channel_type = self.channelType.get()
        self.update(self.channel)

    def max_link_changed(self, var, index, mode):
        try:
            maxLink = int(self.maxLink.get())
        except Exception:
            maxLink = self.channel.max_watchlink
            self.maxLink.set(maxLink)
        if maxLink < 1 or maxLink > 99:
            maxLink = self.channel.max_watchlink
            self.maxLink.set(maxLink)
        self.channel.max_watchlink = maxLink

    def update(self, channel):
        self.channel = channel
        match self.channel.channel_type:
            case 0:
                self.labelWebUrl.grid_forget()
                self.entryWebUrl.grid_forget()
                self.frameUpdateLiveStream.grid_forget()
                self.labelWatchlinks.grid_forget()
                self.comboboxWatchlinks.grid_forget()
                self.frameUpdateWatchlinks.grid_forget()
                self.labelVideo["text"] = "Video URL:"
                self.labelVideo.grid(row=3, column=0, padx=(4, 2), pady=(4, 2),
                                     sticky=tk.E)
                self.entryVideo.grid(row=3, column=1, columnspan=4, padx=(2, 4),
                                     pady=(2, 2), sticky=tk.EW)
            case 1:
                self.labelWatchlinks.grid_forget()
                self.comboboxWatchlinks.grid_forget()
                self.frameUpdateWatchlinks.grid_forget()
                self.labelWebUrl.grid(row=2, column=0, padx=(4, 2), pady=(4, 4),
                                      sticky=tk.E)
                self.entryWebUrl.grid(row=2, column=1,  columnspan=4,
                                      padx=(2, 4), pady=(2, 4), sticky=tk.EW)
                self.labelVideo["text"] = "Playlist URL:"
                self.labelVideo.grid(row=3, column=0, padx=(4, 2), pady=(4, 2),
                                     sticky=tk.E)
                self.entryVideo.grid(row=3, column=1, columnspan=4, padx=(2, 4),
                                     pady=(2, 2), sticky=tk.EW)
                self.frameUpdateLiveStream.grid(row=4, column=1, sticky=tk.EW)
            case 2:
                self.labelVideo.grid_forget()
                self.entryVideo.grid_forget()
                self.frameUpdateLiveStream.grid_forget()
                self.labelWebUrl.grid(row=2, column=0, padx=(4, 2), pady=(4, 4),
                                      sticky=tk.E)
                self.entryWebUrl.grid(row=2, column=1,  columnspan=4,
                                      padx=(2, 4), pady=(2, 4), sticky=tk.EW)
                self.labelWatchlinks.grid(row=5, column=0, padx=(4, 2),
                                          pady=(4, 2), sticky=tk.E)
                self.comboboxWatchlinks.grid(row=5, column=1, columnspan=4,
                                             padx=(2, 15), pady=(2, 2), sticky=tk.EW)
                self.frameUpdateWatchlinks.grid(row=6, column=1, padx=(2, 4),
                                                pady=(2, 4), sticky=tk.EW)
            case _:
                pass

        self.channelType.set(self.channel.channel_type)

        if self.channel.name is not None:
            self.name.set(self.channel.name)
        else:
            self.name.set("")

        if self.channel.video is not None:
            self.video.set(self.channel.video)
        else:
            self.video.set("")

        if self.channel.web is not None:
            self.web.set(self.channel.web)
        else:
            self.web.set("")

        self.first_last.set(self.channel.first_last)
        self.maxLink.set(self.channel.max_watchlink)

        values_watchlinks = []
        self.comboboxWatchlinks['values'] = values_watchlinks
        self.comboboxWatchlinks.set('')

        if len(self.channel.watchlinks) > 0:
            values_watchlinks = ["" for i in range(
                len(self.channel.watchlinks))]
            for i in range(len(self.channel.watchlinks)):
                item = " {title} "
                values_watchlinks[i] = item.format(
                    title=self.channel.watchlinks[i].title)
            self.comboboxWatchlinks['values'] = values_watchlinks
            self.comboboxWatchlinks.set(values_watchlinks[0])

    def save_channel(self, event):
        self.channel.channel_type = self.channelType.get()
        self.channel.name = self.name.get()
        if self.channel.channel_type < 2:
            self.channel.video = self.video.get()
        else:
            self.channel.video = None
        if self.channel.channel_type > 0:
            self.channel.web = self.web.get()
        else:
            self.channel.web = None
        if self.channel.channel_type == 1:
            self.channel.first_last = self.first_last.get()
        else:
            self.channel.first_last = -1
        if self.channel.channel_type == 2:
            try:
                maxLink = self.maxLink.get()
            except Exception:
                maxLink = 10
            self.channel.max_watchlink = maxLink
        else:
            self.channel.max_watchlink = 10

        if len(self.channel.name) == 0:
            self.channel.name = "Unknown"
        # if len(self.channel.web) == 0:
        #     self.channel.web = None
        # if len(self.channel.video) == 0:
        #     self.channel.video = None

        print("Channel updated:")
        print("   Channel name:", self.channel.name)
        print("   Channel type:", self.channel.channel_type)
        if self.channel.channel_type > 0:
            print("       Web page:", self.channel.web)
        if self.channel.channel_type == 1:
            if self.channel.first_last == 0:
                print("                 First m3u8")
            else:
                print("                 Last m3u8")
        if self.channel.channel_type < 2:
            print("      Video URL:", self.channel.video)
        if self.channel.channel_type == 2:
            print("                 Max. Watchlink:",
                  self.channel.max_watchlink)
            if len(self.channel.watchlinks) > 0:
                print(
                    f"     Watchlinks: {self.channel.watchlinks[0].title} : ({self.channel.watchlinks[0].href})")
                for i in range(1, len(self.channel.watchlinks)):
                    print(
                        f"                 {self.channel.watchlinks[i].title} : ({self.channel.watchlinks[i].href})")

        if self.app.channelAdd and not self.channel_added:
            self.app.channel_list.add_channel(self.channel)
            iChannel = self.app.channel_list.iChannel
            self.channel_added = True
        else:
            iChannel = self.app.channel_list.iChannel
            self.app.channel_list.channels[iChannel] = self.channel

        self.app.gui_update()


class DialogChannelRemove(object):
    def __init__(self, parent, channel):
        # self.channel = channel
        self.yesNo = 'No'
        self.gui = tk.Toplevel(parent)
        self.gui.state("withdrawn")
        self.gui.transient(parent)
        self.gui.bind('<Key>', self.key)
        p1 = tk.PhotoImage(file='izle.png')
        self.gui.iconphoto(False, p1)
        self.gui.title("Remove channel")
        self.gui.resizable(False, False)

        self.style = ttk.Style(self.gui)
        self.style.theme_use('clam')

        self.helv12pxb = tkFont.Font(family='Helvetica', size=-12,
                                     weight='bold')

        self.frameChannelRemove = ttk.Frame(self.gui)
        self.frameChannelRemove['padding'] = (10, 10, 10, 8)
        self.frameChannelRemove['relief'] = 'sunken'
        self.frameChannelRemove['width'] = 302
        self.frameChannelRemove.grid(
            padx=5, pady=5, sticky=tk.W+tk.N+tk.E+tk.S)

        self.frameChannelRemove.columnconfigure(0, minsize=141)
        self.frameChannelRemove.columnconfigure(1, minsize=141)

        msg = "Are you sure to remove the channel"
        self.labelQuestion1 = ttk.Label(self.frameChannelRemove, text=msg)
        self.labelQuestion1['padding'] = (5, 5, 5, 0)
        self.labelQuestion1['font'] = self.helv12pxb
        self.labelQuestion1.grid(row=0, columnspan=2)

        msg = "Channel : {name}"
        msg = msg.format(name=channel.name)

        self.labelQuestion2 = ttk.Label(self.frameChannelRemove, text=msg)
        self.labelQuestion2['padding'] = (5, 0, 5, 5)
        self.labelQuestion2['font'] = self.helv12pxb
        self.labelQuestion2.grid(row=1, columnspan=2)

        self.buttonYes = ttk.Button(
            self.frameChannelRemove, text="Yes", command=self.Yes)
        self.buttonYes.focus()
        self.buttonYes.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.buttonNo = ttk.Button(
            self.frameChannelRemove, text="No", command=self.No)
        self.buttonNo.grid(row=2, column=1, padx=10, sticky=tk.W)

        self.gui.update()
        self.gui.update_idletasks()
        self.gui.deiconify()

        W = parent.winfo_width()
        H = parent.winfo_height()
        X = parent.winfo_x()
        Y = parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

    def key(self, event):
        k = event.keysym
        print("Key: {k}".format(k=k))
        if k == 'Escape':
            self.gui.grab_release()
            self.gui.destroy()

    def Yes(self):
        self.yesNo = "Yes"
        self.gui.grab_release()
        self.gui.destroy()

    def No(self):
        self.yesNo = "No"
        self.gui.grab_release()
        self.gui.destroy()


class Shortcuts():
    def __init__(self, parent):
        self.parent = parent
        self.gui = Toplevel()
        self.gui.state("withdrawn")

        self.gui.iconphoto(False, PhotoImage(file='izle.png'))
        self.gui.title("Shortcuts")

        self.frameShortcuts = ttk.Frame(self.gui)
        self.frameShortcuts.grid(row=0, column=0)
        self.frameShortcuts['relief'] = 'raised'
        self.frameShortcuts['padding'] = (5, 5, 5, 5)

        self.font = tkFont.Font(family='Helvetica', size=-11, weight='normal')
        
        self.frameShortcuts.columnconfigure(2, minsize=50)


        labelKeyMouse =  ttk.Label(self.frameShortcuts, text="Key / Mouse", font=self.font)
        labelKeyMouse.grid(row=0, column=0, padx=(0, 1), pady=(0,1), sticky=tk.EW)

        labelKeyMouse['padding'] = (10,0,5,0)
        labelKeyMouse['background'] = '#1e94f1'
        labelKeyMouse['foreground'] = 'white'

        
        labelShortcut =  ttk.Label(self.frameShortcuts, text="Shortcut", font=self.font)
        labelShortcut.grid(row=0, column=1, padx=(1, 0), pady=(0,1), sticky=tk.EW)
        
        
        labelShortcut['padding'] = (5,0,10,0)
        labelShortcut['background'] = '#1e94f1'
        labelShortcut['foreground'] = 'white'



        rowGUI=1
        labelGUI = ttk.Label(self.frameShortcuts, text="GUI", font=self.font)
        labelGUI.grid(row=rowGUI, column=0, columnspan=3,  pady=(1,0), sticky=(tk.W, tk.N, tk.E, tk.S))
        
        labelGUI['padding'] = (0,0,5,0)
        labelGUI['background'] = '#1e94f1'
        labelGUI['foreground'] = 'white'
        labelGUI['anchor'] = tk.E
        
        labelGUI10 = ttk.Label(
            self.frameShortcuts, text="Q", font=self.font)
        labelGUI10.grid(row=rowGUI+1, column=0, padx=(10, 5), sticky="e")
        labelGUI11 = ttk.Label(
            self.frameShortcuts, text="Quit application (izle / Channel editor)", font=self.font)
        labelGUI11.grid(row=rowGUI+1, column=1, padx=(5, 10), sticky="w")

        labelGUI20 = ttk.Label(
            self.frameShortcuts, text="Esc", font=self.font)
        labelGUI20.grid(row=rowGUI+2, column=0, padx=(10, 5), sticky="e")
        labelGUI21 = ttk.Label(
            self.frameShortcuts, text="Close dialog or menu", font=self.font)
        labelGUI21.grid(row=rowGUI+2, column=1, padx=(5, 10), sticky="w")
    
        labelGUI30 = ttk.Label(
            self.frameShortcuts, text="1 / 2 / 3", font=self.font)
        labelGUI30.grid(row=rowGUI+3, column=0, padx=(10, 5), sticky="e")
        labelGUI31 = ttk.Label(
            self.frameShortcuts, text="Scale GUI", font=self.font)
        labelGUI31.grid(row=rowGUI+3, column=1, padx=(5, 10), sticky="w")
    

        labelGUI40 = ttk.Label(
            self.frameShortcuts, text="F / F10", font=self.font)
        labelGUI40.grid(row=rowGUI+4, column=0, padx=(10, 5), sticky="e")
        labelGUI41 = ttk.Label(
            self.frameShortcuts, text="Toggle full screen", font=self.font)
        labelGUI41.grid(row=rowGUI+4, column=1, padx=(5, 10), sticky="w")


        labelGUI50 = ttk.Label(
            self.frameShortcuts, text="L", font=self.font)
        labelGUI50.grid(row=rowGUI+5, column=0, padx=(10, 5), sticky="e")
        labelGUI51 = ttk.Label(
            self.frameShortcuts, text="Toggle log frame", font=self.font)
        labelGUI51.grid(row=rowGUI+5, column=1, padx=(5, 10), sticky="w")



        rowChannel = 7
        labelChannel = ttk.Label(self.frameShortcuts, text="Channel", font=self.font)
        labelChannel.grid(row=rowChannel, column=0, columnspan=3, sticky=(tk.W, tk.N, tk.E, tk.S))
        
        labelChannel['padding'] = (0,0,5,0)
        labelChannel['background'] = '#1e94f1'
        labelChannel['foreground'] = 'white'
        labelChannel['anchor'] = tk.E
        
    
        labelChannel10 = ttk.Label(
            self.frameShortcuts, text="A", font=self.font)
        labelChannel10.grid(row=rowChannel+1, column=0, padx=(10, 5), sticky="e")
        labelChannel11 = ttk.Label(
            self.frameShortcuts, text="Channel add", font=self.font)
        labelChannel11.grid(row=rowChannel+1, column=1, padx=(5, 10), sticky="w")

        labelChannel20 = ttk.Label(
            self.frameShortcuts, text="E", font=self.font)
        labelChannel20.grid(row=rowChannel+2, column=0, padx=(10, 5), sticky="e")
        labelChannel21 = ttk.Label(
            self.frameShortcuts, text="Channel edit", font=self.font)
        labelChannel21.grid(row=rowChannel+2, column=1, padx=(5, 10), sticky="w")

        labelChannel30 = ttk.Label(
            self.frameShortcuts, text="D", font=self.font)
        labelChannel30.grid(row=rowChannel+3, column=0, padx=(10, 5), sticky="e")
        labelChannel31 = ttk.Label(
            self.frameShortcuts, text="Channel delete", font=self.font)
        labelChannel31.grid(row=rowChannel+3, column=1, padx=(5, 10), sticky="w")

        labelChannel40 = ttk.Label(
            self.frameShortcuts, text="U", font=self.font)
        labelChannel40.grid(row=rowChannel+4, column=0, padx=(10, 5), sticky="e")
        labelChannel41 = ttk.Label(self.frameShortcuts,
                                   text="Channel update (m3u8 URL / YouTube watchlinks)",
                                   font=self.font)
        labelChannel41.grid(row=rowChannel+4, column=1, padx=(5, 10), sticky="w")

        labelChannel50 = ttk.Label(
            self.frameShortcuts, text="Left", font=self.font)
        labelChannel50.grid(row=rowChannel+5, column=0, padx=(10, 5), sticky="e")
        labelChannel51 = ttk.Label(
            self.frameShortcuts, text="Previous channel", font=self.font)
        labelChannel51.grid(row=rowChannel+5, column=1, padx=(5, 10), sticky="w")

        labelChannel60 = ttk.Label(
            self.frameShortcuts, text="Right", font=self.font)
        labelChannel60.grid(row=rowChannel+6, column=0, padx=(10, 5), sticky="e")
        labelChannel61 = ttk.Label(
            self.frameShortcuts, text="Next channel", font=self.font)
        labelChannel61.grid(row=rowChannel+6, column=1, padx=(5, 10), sticky="w")

        labelChannel70 = ttk.Label(
            self.frameShortcuts, text="O", font=self.font)
        labelChannel70.grid(row=rowChannel+7, column=0, padx=(10, 5), sticky="e")
        labelChannel71 = ttk.Label(
            self.frameShortcuts, text="Load channel list", font=self.font)
        labelChannel71.grid(row=rowChannel+7, column=1, padx=(5, 10), sticky="w")

        rowPlayer = 16
        labelPlayer = ttk.Label(self.frameShortcuts, text="Player", font=self.font)
        labelPlayer.grid(row=rowPlayer, column=0, columnspan=3, sticky=(tk.W, tk.N, tk.E, tk.S))

        labelPlayer['padding'] = (0,0,5,0)
        labelPlayer['background'] = '#1e94f1'
        labelPlayer['foreground'] = 'white'
        labelPlayer['anchor'] = tk.E

        labelPlayer10 = ttk.Label(self.frameShortcuts,
                                  text="P", font=self.font)
        labelPlayer10.grid(row=rowPlayer+1, column=0, padx=(10, 5), sticky="e")
        labelPlayer11 = ttk.Label(self.frameShortcuts,
                                  text="Toggle Pause / Play", font=self.font)
        labelPlayer11.grid(row=rowPlayer+1, column=1, padx=(5, 10), sticky="w")

        labelPlayer20 = ttk.Label(self.frameShortcuts,
                                  text="M", font=self.font)
        labelPlayer20.grid(row=rowPlayer+2, column=0, padx=(10, 5), sticky="e")
        labelPlayer21 = ttk.Label(self.frameShortcuts,
                                  text="Toggle Mute / Unmute", font=self.font)
        labelPlayer21.grid(row=rowPlayer+2, column=1, padx=(5, 10), sticky="w")

        labelPlayer30 = ttk.Label(self.frameShortcuts,
                                  text="Up", font=self.font)
        labelPlayer30.grid(row=rowPlayer+3, column=0, padx=(10, 5), sticky="e")
        labelPlayer31 = ttk.Label(self.frameShortcuts,
                                  text="Volume up", font=self.font)
        labelPlayer31.grid(row=rowPlayer+3, column=1, padx=(5, 10), sticky="w")

        labelPlayer40 = ttk.Label(self.frameShortcuts,
                                  text="Down", font=self.font)
        labelPlayer40.grid(row=rowPlayer+4, column=0, padx=(10, 5), sticky="e")
        labelPlayer41 = ttk.Label(self.frameShortcuts,
                                  text="Volume down", font=self.font)
        labelPlayer41.grid(row=rowPlayer+4, column=1, padx=(5, 10), sticky="w")

        labelPlayer50 = ttk.Label(self.frameShortcuts,
                                  text="Wheel", font=self.font)
        labelPlayer50.grid(row=rowPlayer+5, column=0, padx=(10, 5), sticky="e")
        labelPlayer51 = ttk.Label(self.frameShortcuts,
                                  text="Volume up / down", font=self.font)
        labelPlayer51.grid(row=rowPlayer+5, column=1, padx=(5, 10), sticky="w")



        self.gui.bind("<Key>", self.key)
        self.gui.resizable(False, False)
        self.gui.attributes('-topmost', True)

        self.gui.update()
        self.gui.update_idletasks()
        self.gui.deiconify()

        W = parent.winfo_width()
        H = parent.winfo_height()
        X = parent.winfo_x()
        Y = parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

        self.gui.focus_set()

    def key(self, event):
        k = event.keysym
        if k == 'Escape':
            self.gui.destroy()
            self.parent.focus_set()


class About():
    def __init__(self, parent):
        self.parent = parent
        self.gui = Toplevel()
        self.gui.state("withdrawn")

        self.gui.iconphoto(False, PhotoImage(file='izle.png'))
        self.gui.title("About izle")

        self.frameAbout = ttk.Frame(self.gui)
        self.frameAbout.grid(row=0, column=0)
        self.frameAbout['relief'] = 'raised'
        self.frameAbout['padding'] = (5, 5, 5, 5)

        self.font1b = tkFont.Font(family='Helvetica', size=-16, weight='bold')
        self.font2 = tkFont.Font(family='Helvetica', size=-11, weight='normal')
        self.font2b = tkFont.Font(family='Helvetica', size=-11, weight='bold')

        labelIzle = ttk.Label(
            self.frameAbout, text="izle", font=self.font1b)
        labelIzle.grid(row=0, column=0, columnspan=2)

        labelSoftware1 = ttk.Label(
            self.frameAbout, text="mpv Graphical user interface",
            font=self.font2)
        labelSoftware1.grid(row=1, column=0, columnspan=2)

        labelSoftware2 = ttk.Label(
            self.frameAbout,
            text="for watching live streams and Youtube videos",
            font=self.font2)
        labelSoftware2.grid(row=2, column=0, columnspan=2)

        labelVersion = ttk.Label(
            self.frameAbout, text="Version {}".format('0.1'), font=self.font2)
        labelVersion.grid(row=3, column=0, columnspan=2)

        labelAuthor0 = ttk.Label(
            self.frameAbout, text="Author:", font=self.font2)
        labelAuthor1 = ttk.Label(
            self.frameAbout, text="Sinan Güngör", font=self.font2)
        labelAuthor0.grid(row=4, column=0, sticky="e", padx=(10, 3))
        labelAuthor1.grid(row=4, column=1, sticky="w", padx=(0, 10))
        labelLicense0 = ttk.Label(
            self.frameAbout, text="License:", font=self.font2)
        labelLicense1 = ttk.Label(
            self.frameAbout, text="GNU General Public License, Version 3",
            font=self.font2)
        labelLicense0.grid(row=5, column=0, sticky="e", padx=(10, 3))
        labelLicense1.grid(row=5, column=1, sticky="w", padx=(0, 10))

        self.frameAbout.columnconfigure(1, minsize=200)

        self.gui.bind("<Key>", self.key)
        self.gui.resizable(False, False)
        self.gui.attributes('-topmost', True)

        self.gui.update()
        self.gui.update_idletasks()
        self.gui.deiconify()
        W = parent.winfo_width()
        H = parent.winfo_height()
        X = parent.winfo_x()
        Y = parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

        self.gui.focus_set()

    def key(self, event):
        k = event.keysym
        if k == 'Escape':
            self.gui.destroy()
            self.parent.focus_set()


class SettingEditor():
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.gui = Toplevel()
        self.gui.state("withdrawn")

        self.gui.iconphoto(False, PhotoImage(file='izle.png'))
        self.gui.title("Settings")

        self.frameSettings = ttk.Frame(self.gui)
        self.frameSettings.grid(row=0, column=0)
        self.frameSettings['relief'] = 'raised'
        self.frameSettings['padding'] = (5, 5, 5, 5)

        self.font1 = tkFont.Font(family='Helvetica', size=-12, weight='normal')

        labelUseLegacyDriver = ttk.Label(self.frameSettings,
                                         text="Use legacy video output driver:",
                                         font=self.font1)
        labelUseLegacyDriver.grid(row=0, column=0,
                                  padx=(0, 0), pady=(4, 0), sticky=tk.E)

        indicatormargin = (0, 0, 4, 3)
        padding = (5, 4, 0, 0)
        if self.parent.call('tk', 'windowingsystem') == 'win32':
            indicatormargin = (0, 1, 4, 0)
            padding = (5, 2, 0, 2)

        # ------------------------------------------------------
        self.useLegacyDriver = tk.BooleanVar()
        self.useLegacyDriver.set(self.app.settings.use_legacy_vo)
        self.useLegacyDriver.trace_add('write', self.use_legacy_driver)

        cButtonUseLegacyDriver = CheckbuttonCustomized(self.frameSettings,
                                                       compound=None,
                                                       onvalue=True,
                                                       offvalue=False,
                                                       takefocus=False,
                                                       variable=self.useLegacyDriver,
                                                       # command=self.use_legacy_driver,
                                                       indicatorsize=14,
                                                       indicatorborder="#3daee9",
                                                       indicatorcheck="#3daee9",
                                                       indicatormargin=indicatormargin,
                                                       padding=padding)
        cButtonUseLegacyDriver.grid(row=0, column=1,
                                    padx=(0, 0), pady=(0, 0), sticky=tk.W)

        labelPageLoadTimeout = ttk.Label(self.frameSettings, text="Web driver page load timeout in s:",
                                         font=self.font1)
        labelPageLoadTimeout.grid(row=1, column=0, sticky=tk.E)

        # ------------------------------------------------------
        self.loadTimeout = tk.IntVar()
        self.loadTimeout.set(self.app.settings.page_load_timeout)
        self.loadTimeout.trace_add('write', self.load_timeout_changed)
        entryLoadTimeout = ttk.Entry(self.frameSettings,
                                     textvariable=self.loadTimeout, width=3)
        entryLoadTimeout.grid(row=1, column=1,
                              padx=(4, 4), pady=(2, 4), sticky=tk.W)

        labelCaptureDuration = ttk.Label(self.frameSettings, text="Network log capture duration for m3u8 links in s:",
                                         font=self.font1)
        labelCaptureDuration.grid(row=2, column=0, sticky=tk.E)

        self.captureDuration = tk.IntVar()
        self.captureDuration.set(self.app.settings.capture_duration)
        self.captureDuration.trace_add('write', self.capture_duration_changed)
        entryCaptureDuration = ttk.Entry(self.frameSettings,
                                         textvariable=self.captureDuration, width=3)
        entryCaptureDuration.grid(row=2, column=1,
                                  padx=(4, 4), pady=(2, 4), sticky=tk.W)

        # ------------------------------------------------------
        self.imgSave = ImageTk.PhotoImage(
            iconGenerator.check(size=18, margin=(0, 0, 0, 0)))
        labelSaveSettings = ttk.Label(self.frameSettings, compound="image",
                                      image=self.imgSave)
        labelSaveSettings.grid(row=3, column=1,
                               padx=(0, 5), pady=(8, 0), sticky=tk.E)
        labelSaveSettings.bind('<Button-1>', self.save_settings)
        # ------------------------------------------------------

        self.gui.bind("<Key>", self.key)
        self.gui.resizable(False, False)
        self.gui.attributes('-topmost', True)

        self.gui.update()
        self.gui.update_idletasks()
        self.gui.deiconify()
        W = parent.winfo_width()
        H = parent.winfo_height()
        X = parent.winfo_x()
        Y = parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

        self.gui.focus_set()

    def use_legacy_driver(self, var, index, mod):
        useLegacyDriver = self.useLegacyDriver.get()
        print("Legacy driver:", useLegacyDriver)
        self.app.settings.use_legacy_vo = useLegacyDriver

    def load_timeout_changed(self, var, index, mode):
        try:
            loadTimeout = int(self.loadTimeout.get())
        except Exception:
            loadTimeout = self.app.settings.page_load_timeout
        if loadTimeout < 1:
            loadTimeout = 1
        if loadTimeout > 99:
            loadTimeout = 99

        self.loadTimeout.set(loadTimeout)
        print("Page timeout:", loadTimeout)
        self.app.settings.page_load_timeout = loadTimeout

    def capture_duration_changed(self, var, index, mode):
        try:
            captureDuration = int(self.captureDuration.get())
        except Exception:
            captureDuration = self.app.settings.capture_duration

        if captureDuration < 1:
            captureDuration = 1
        if captureDuration > 99:
            captureDuration = 99

        self.captureDuration.set(captureDuration)
        print("Capture duration:", captureDuration)
        self.app.settings.capture_duration = captureDuration

    def save_settings(self, event):
        print("Save settings")
        self.app.settings.use_legacy_driver = self.useLegacyDriver.get()
        self.app.settings.print()
        self.app.settings.write(self.app.settings.file_settings)

    def key(self, event):
        k = event.keysym
        if k == 'Escape':
            self.gui.destroy()
            self.parent.focus_set()


class ChannelAdd():
    def __init__(self, parent, app):
        print(parent)
        self.parent = parent
        self.app = app
        self.channel_list = self.app.channel_list

        self.added = False
        self.gui = tk.Toplevel()
        self.gui.transient(self.parent)
        self.gui.title("Channel add")

        image_path = resource_path('izle.png')
        self.gui.iconphoto(False, tk.PhotoImage(file=image_path))

        self.frameChannel = FrameChannel(self.gui, app=app)
        self.frameChannel.grid()

        self.gui.bind("<Key>", self.key)
        self.gui.protocol("WM_DELETE_WINDOW", self.gui.destroy)
        # self.gui.resizable(False, False)
        self.gui.attributes('-topmost', True)

        newChannel = Channel()
        newChannel.name = "New channel"

        self.frameChannel.update(newChannel)
        self.set_geometry()

    def set_geometry(self):
        self.gui.update()
        self.gui.update_idletasks()

        W = self.parent.winfo_width()
        H = self.parent.winfo_height()
        X = self.parent.winfo_x()
        Y = self.parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

    def key(self, event):
        k = event.keysym
        if k == 'Escape':
            self.gui.destroy()


class ChannelEdit():
    def __init__(self, parent, app):
        print(parent)
        self.parent = parent
        self.app = app
        self.channel = self.app.channel

        self.edited = False

        self.gui = tk.Toplevel()
        self.gui.transient(self.parent)
        self.gui.title("Channel edit")

        image_path = resource_path('izle.png')
        self.gui.iconphoto(False, tk.PhotoImage(file=image_path))

        self.frameChannel = FrameChannel(self.gui, app=app)
        self.frameChannel.grid()

        self.gui.bind("<Key>", self.key)
        self.gui.protocol("WM_DELETE_WINDOW", self.gui.destroy)
        self.gui.resizable(False, False)
        self.gui.attributes('-topmost', True)

        self.frameChannel.update(self.channel)

        self.gui.update()
        self.gui.update_idletasks()
        W = parent.winfo_width()
        H = parent.winfo_height()
        X = parent.winfo_x()
        Y = parent.winfo_y()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        x = X+(W-w)//2
        y = Y+(H-h)//2
        self.gui.geometry("{}x{}+{}+{}".format(w, h, x, y))

    def key(self, event):
        k = event.keysym
        if k == 'Escape':
            self.gui.destroy()


class ChannelEditor():
    def __init__(self, parent, app, channel_list):
        self.parent = parent
        self.app = app
        self.channel_list = channel_list
        self.channel_list.read()
        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])
        self.submenus = list()
        # ------------------------------------------------------
        self.gui_build()
        self.gui_bindings()
        self.gui_update()
        self.gui.attributes('-topmost', True)
        # ------------------------------------------------------
        # self.gui.resizable(False, False)
        self.play_channel(self.channel)

    def gui_bindings(self):
        self.gui.event_add(
            '<<ControlOn>>',  '<KeyPress-Control_L>',   '<KeyPress-Control_R>')
        self.gui.event_add(
            '<<ControlOff>>', '<KeyRelease-Control_L>', '<KeyRelease-Control_R>')
        self.gui.event_add(
            '<<ShiftOn>>',    '<KeyPress-Shift_L>',     '<KeyPress-Shift_R>')
        self.gui.event_add(
            '<<ShiftOff>>',   '<KeyRelease-Shift_L>',   '<KeyRelease-Shift_R>')

        self.gui.bind('<<ControlOn>>', ctrl_on)
        self.gui.bind('<<ControlOff>>', ctrl_off)
        self.gui.bind('<<ShiftOn>>', shift_on)
        self.gui.bind('<<ShiftOff>>', shift_off)
        # ------------------------------------------------------

        self.gui.bind("<Key>", self.key)
        self.gui.bind("<q>", self.quit)

    def gui_build(self):
        self.gui = tk.Toplevel()
        self.gui.iconphoto(False, PhotoImage(file='izle.png'))
        self.gui.title("Channel Editor")
        self.gui.minsize(width=480, height=320)
        self.gui.protocol("WM_DELETE_WINDOW", self.quit)
        style = ttk.Style(self.gui)
        style.theme_use("clam")

        # layout = style.layout('TRadiobutton')
        # print("Radiobutton layout:", layout)
        # print("Padding options:", style.element_options('Radiobutton.padding'))
        # print("Indicator options:", style.element_options('Radiobutton.indicator'))
        # print("Focus options:", style.element_options('Radiobutton.focus'))
        # print("Label options:", style.element_options('Radiobutton.label'))

        if self.parent.call('tk', 'windowingsystem') == 'win32':
            ttk.Style().configure("TCombobox", padding=(5, 3, 5, 2))
        else:
            ttk.Style().configure('TCombobox', padding=(5, 6, 5, 2))
            ttk.Style().configure('TEntry', padding=(5, 4, 5, 2))
            ttk.Style().configure('TRadiobutton', indicatormargin=(3, 3, 3, 5))
        self.gui.columnconfigure(0, weight=1)
        self.gui.rowconfigure(0, weight=0)
        self.gui.rowconfigure(1, weight=1)

        frameMain = ttk.Frame(self.gui)
        frameMain['padding'] = (2, 3, 2, 2)
        frameMain['relief'] = 'raised'
        frameMain.grid(sticky=(tk.EW, tk.NS))
        frameMain.rowconfigure(0, weight=0)
        frameMain.rowconfigure(0, weight=1)
        frameMain.grid(row=1, column=0, sticky=tk.NS+tk.EW)
        # ------------------------------------------------------
        font1 = tkFont.Font(family='Helvetica', size=-12, weight='normal')
        comboboxChannels = ttk.Combobox(frameMain)
        comboboxChannels.grid(
            column=0, row=0, padx=(2, 2), pady=(2, 2), ipadx=20, ipady=0, sticky=(tk.EW, tk.N))
        comboboxChannels['state'] = 'readonly'
        comboboxChannels['justify'] = 'center'
        comboboxChannels['font'] = font1
        comboboxChannels.bind('<<ComboboxSelected>>', self.channel_changed)
        self.comboboxChannels = comboboxChannels

        # ------------------------------------------------------

        frameMain.columnconfigure(0, weight=0)
        frameMain.columnconfigure(1, weight=1, minsize=640)
        frameMain.columnconfigure(2, weight=0)

        frameChannel = FrameChannel(frameMain, app=self.app)
        frameChannel.grid(row=0, column=1, padx=(
            2, 2), pady=(2, 2), ipadx=0, sticky=tk.NSEW)

        frameChannel.update(self.channel)
        self.frameChannel = frameChannel
        self.player = self.frameChannel.player
        self.canvas = self.frameChannel.canvas

        # if self.parent.call('tk', 'windowingsystem') == 'win32':
        #     self.canvas.bind(
        #         '<MouseWheel>', lambda event: self.player_volume_up_down(event))
        #     self.canvas.bind(
        #         '<Button-1>', lambda event: self.player_cycle_pause(event))
        # else:
        #     self.player.keybind('MBTN_LEFT', "cycle pause")
        #     self.player.keybind('WHEEL_UP', "add volume +5")
        #     self.player.keybind('WHEEL_DOWN', "add volume -5")
        # # ------------------------------------------------------
        frameLog = FrameText(self.gui)
        frameLog.grid(sticky=tk.EW)
        self.frameLog = frameLog

        sys.stdout = StdoutRedirector(self.frameLog.text)
        self.build_menu()

    def channel_names(self):
        channelNames = ["" for i in range(
            len(self.channel_list.channels))]
        for i in range(len(self.channel_list.channels)):
            item = " {name} "
            channelNames[i] = item.format(
                name=self.channel_list.channels[i].name)
        return channelNames

    def player_volume_up_down(self, event):
        if event.delta > 0:
            volume = self.player.volume
            volume += 5
            if volume > self.player.volume_max:
                volume = self.player.volume_max
            self.player.input_commands = "set volume {}".format(volume)
        else:
            volume = self.player.volume
            volume -= 5
            if volume < 0:
                volume = 0
            self.player.input_commands = "set volume {}".format(volume)

    def player_cycle_pause(self, event):
        if self.player.pause:
            self.player.input_commands = "cycle pause up"
        else:
            self.player.input_commands = "cycle pause"

    def build_menu(self):
        mainMenu = Menu(self.gui, app=self,
                        orient=tk.HORIZONTAL, row=0, column=0)
        mainMenu.add_item(0, "File")
        mainMenu.add_item(1, "Channels")
        mainMenu.get_position()
        self.mainMenu = mainMenu

        fileMenu = Menu(self.gui, app=self, parent=mainMenu, order=0)
        fileMenu.add_item(0, "Open")
        fileMenu.add_item(1, "Save")
        fileMenu.add_item(2, "Save as")
        fileMenu.add_item(3, "Quit")
        fileMenu.command(0, lambda event: self.open(event))
        fileMenu.command(1, lambda event: self.save(event))
        fileMenu.command(2, lambda event: self.saveas(event))
        fileMenu.command(3, lambda event: self.quit(event))
        fileMenu.get_position()
        self.fileMenu = fileMenu

        channelMenu = Menu(self.gui, app=self, parent=mainMenu, order=1)
        channelMenu.add_item(0, "Add channel")
        channelMenu.add_item(1, "Delete channel")
        channelMenu.command(0, lambda event: self.add(event))
        channelMenu.command(1, lambda event: self.delete(event))
        channelMenu.get_position()
        self.channelMenu = channelMenu

    def key(self, event):
        ks = event.keysym
        if ctrl_shift:
            print('Key: <Ctrl>+<Shift>+{}'.format(ks))
        if ctrl:
            print('Key: <Ctrl>+{}'.format(ks))
        if shift:
            print('Key: <Shift>+{}'.format(ks))
        if not ctrl and not shift and not ctrl_shift:
            print("Key: {}".format(ks))
        if ks == 'Escape':
            self.mainMenu.hide_submenu()

    def gui_update(self):
        self.comboboxChannels['values'] = self.channel_names()
        valueChannel = self.comboboxChannels['values'][self.iChannel]
        self.comboboxChannels.set(valueChannel)

    def channel_changed(self, event):
        self.channel_list.iChannel = self.comboboxChannels.current()
        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])
        self.frameChannel.update(self.channel)
        self.player.pause = True
        self.play_channel(self.channel)

    def play_channel(self, channel):
        videoURL = None
        if channel.channel_type < 2:
            print(
                f"Mini player > Playing channel {channel.name} : ({channel.video})")
            videoURL = channel.video
        else:
            if len(channel.watchlinks) > 0:
                watchlink = channel.watchlinks[channel.iWatchlink]
                videoURL = watchlink.href
                print(
                    f"Mini player > Playing channel {channel.name} - {watchlink.title} : ({watchlink.href})")
        if videoURL is not None:
            self.player["loop-playlist"] = "force"
            self.player.play(videoURL)
        else:
            print("No video URL!")

    def channel_play(self):
        # self.iChannel = self.channel_list.iChannel
        # channel = self.channel_list.channels[self.iChannel]
        videoURL = None
        if self.channel.channel_type < 2:
            print(
                f"Playing channel {self.channel.name} : ({self.channel.video})")
            videoURL = self.channel.video
        else:
            if len(self.channel.watchlinks) > 0:
                watchlink = self.channel.watchlinks[self.channel.iWatchlink]
                videoURL = watchlink.href
                print(
                    f"Playing channel {self.channel.name} - {watchlink.title} : ({watchlink.href})")
        if videoURL is not None:
            self.player["loop-playlist"] = "force"
            self.player.play(videoURL)
        else:
            print("No video URL!")

    def open(self, event):
        self.mainMenu.hide_submenu()
        filePath = filedialog.askopenfilename(parent=self.gui,
                                              title="Select a channel list file",
                                              filetypes=[("Xml file", "*.xml")])
        if filePath:
            extension = pathlib.Path(filePath).suffix
            stem = pathlib.Path(filePath).stem
            print("File to open:", f"{stem}{extension}")
            self.channel_list = Channels(filePath)
            self.channel_list.read()
            self.iChannel = self.channel_list.iChannel
            self.channel = self.channel_list.channels[self.iChannel]
            self.gui_update()
            self.frameChannel.update(self.channel)
            self.channel_play()
            self.app.channel_list = deepcopy(self.channel_list)
        self.mainMenu.disabled = True

    def save(self, event):
        self.mainMenu.hide_submenu()
        self.channel_list.iChannel = self.iChannel
        self.channel_list.write(self.channel_list.file_channel_list)

    def saveas(self, event):
        self.mainMenu.hide_submenu()
        filePath = filedialog.asksaveasfilename(parent=self.gui,
                                                initialfile="channels.xml",
                                                title="Select a .xml file",
                                                filetypes=(
                                                    ("Xml files", "*.xml"), ("all files", "*.*"))
                                                )
        if filePath:
            print("Channel list will be save as:", filePath)
            self.channel_list.write(filePath)

    def quit(self, event=None):
        self.channel_list.iChannel = self.iChannel
        self.channel_list.write(self.channel_list.file_channel_list)
        self.app.channe_list = deepcopy(self.channel_list)
        self.player.input_commands = "cycle pause"
        sys.stdout = StdoutRedirector(self.app.frameLog.text)
        self.gui.destroy()
        self.parent.focus_set()

    def add(self, event):
        self.mainMenu.hide_submenu()
        newChannel = Channel()
        newChannel.name = "New channel"
        self.channel_list.channels.append(newChannel)
        self.channel_list.nChannel += 1
        self.iChannel = len(self.channel_list.channels)-1
        self.channel_list.iChannel = self.iChannel
        self.channel = newChannel
        self.gui_update()
        self.frameChannel.update(self.channel)

    def delete(self, event):
        self.mainMenu.hide_submenu()
        print("Channel remove!")
        channel = self.channel_list.channels[self.iChannel]
        print(channel.name)
        d = DialogChannelRemove(self.gui, channel)
        print("'Channel Remove' dialog is opened, waiting to respond")
        self.gui.wait_window(d.root)
        print("End of 'Channel Remove' dialog, back in MainWindow code")
        print("Dialog response: {yn}".format(yn=d.yesNo))
        if d.yesNo == 'Yes':
            if self.channel_list.nChannel > 1:
                self.channel_list.remove_channel(self.channel_list.iChannel)
                self.iChannel = self.channel_list.iChannel
                self.channel = self.channel_list.channels[self.iChannel]
                self.gui_update()
                self.frameChannel.update(self.channel)

    def channel_m3u8_url_update(self):
        load_timeout = self.app.settings.page_load_timeout
        capture_duration = self.app.settings.capture_duration
        self.channel.m3u8_url_update(load_timeout, capture_duration)
        self.channel_list.channels[self.iChannel] = deepcopy(self.channel)
        self.frameChannel.indicatorUpdateLiveStreamVideoURL.stop_progress()
        self.frameChannel.update(self.channel)
        self.play_channel(self.channel)

    def channel_watch_links_update(self):
        self.channel.watch_links_update()
        self.channel_list.channels[self.iChannel] = deepcopy(self.channel)
        self.frameChannel.indicatorUpdateWatchlinks.stop_progress()
        self.frameChannel.update(self.channel)
        self.play_channel(self.channel)
