"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Application main module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import os
import platform

if platform.system() == 'Windows':
    os.environ["PATH"] = os.path.dirname(
        __file__) + '\\dlls' + os.pathsep + os.environ["PATH"]

import mpv

from tkinter import font as tkFont
from tkinter import ttk
# from tkinter import Toplevel, PhotoImage
from tkinter import filedialog
from tkinter import PhotoImage
import tkinter as tk
from PIL import ImageTk

import ctypes.util
import sys
import pathlib
from copy import deepcopy

# from izle_gui import ctrl, shift, ctrl_shift
# from izle_gui import ctrl_on, ctrl_off, shift_on, shift_off
from izle_gui import resource_path

from icon_generator import IconGenerator
# from izle_gui import FrameText, FrameChannel, Progressindicator
from izle_gui import FrameText, Progressindicator
from izle_gui import StdoutRedirector
from izle_gui import DialogChannelRemove, ChannelAdd, ChannelEdit
from izle_gui import About, Shortcuts, ChannelEditor, SettingEditor
# from channels import Channels, Channel
from channels import Channels
from menu import Menu
# from channel_editor import ChannelEditor
from settings import Settings

# ----------------------------------------------------------------------------------------------


# ==============================================================================================

iconGenerator = IconGenerator()

# --------------------------------------------------------------


class Izle():
    def __init__(self, channels_file=None):
        self.settings = Settings()
        if channels_file is None:
            channels_file = self.settings.last_channel_list
        self.filename_channel = channels_file
        # if self.filename_channel is not None:
        #     self.filename_channel = "channels.xml"
        self.channel_list = Channels(self.filename_channel)
        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])

        self.gui = tk.Tk()
        self.gui.title("İzle")
        style = ttk.Style(self.gui)
        style.theme_use("clam")

        if self.gui.call('tk', 'windowingsystem') == 'win32':
            ttk.Style().configure("TCombobox", padding=(5, 3, 5, 2))
        else:
            ttk.Style().configure("TCombobox", padding=(5, 5, 5, 2))

        H = self.gui.winfo_screenheight()
        if H < 1024:
            self.kScale_max = 2
        else:
            self.kScale_max = 3

        self.kScale = self.kScale_max
        # ------------------------------------------------------
        self.showing_log = False
        self.loglevel = 2
        # ------------------------------------------------------
        self.build_gui()
        self.channelEdit = None
        self.channelAdd = None
        # ------------------------------------------------------
        sys.stdout = StdoutRedirector(self.frameLog.text)
        print("Environment path:", os.environ["PATH"])
        self.check_libraries()
        image_path = resource_path('izle.png')
        self.gui.iconphoto(False, PhotoImage(file=image_path))
        # self.channel_list.print()
        self.settings.print()
        self.set_player()
        # ------------------------------------------------------
        self.gui.bind("<Key>", self.key)
        self.gui.bind("<F10>", self.toggle_fs)
        self.gui.bind("<f>", self.toggle_fs)
        self.gui.bind("<F>", self.toggle_fs)
        self.gui.bind("<l>", self.toggle_log)
        self.gui.bind("<L>", self.toggle_log)
        self.gui.bind("<Down>", self.volume_down)
        self.gui.bind("<Up>", self.volume_up)
        self.gui.bind("<Escape>", self.escape)
        self.gui.bind("<q>", self.quit)
        self.gui.bind("<Q>", self.quit)
        self.frameControl.bind(
            "<Button-1>", lambda event: self.frameMenu.lower())

        # ------------------------------------------------------
        self.gui.resizable(False, False)
        # Before main loop we
        self.gui.update_idletasks()
        self.gui.mainloop()

    def check_libraries(self):
        mpv_library_path = None
        if self.gui.call('tk', 'windowingsystem') == 'x11':
            mpv_library_path = ctypes.util.find_library('mpv')
        if self.gui.call('tk', 'windowingsystem') == 'win32':
            mpv_library_path = ctypes.util.find_library('libmpv-2')
        if mpv_library_path is None:
            print("Required libraries are not found!")
        else:
            print("Mpv library:", mpv_library_path)

    def set_player(self):
        # === Player ===================================
        #  Video output drivers:
        #  (working but not embedding)
        #     working on Plasma Wayland: (gpu, gpu-next, wlshm, vaapi, drm), xv, x11
        # not working on Plasma Wayland: vdapu, dmabuf-wayland, caca, sixel, kitty
        #         working on Plasma X11: (), gpu, gpu-next,vdau, wlshm, xv, dmabuf-wayland, vaapi, x11, drm
        #     not working on Plasma X11: caca, sixel, kitty

        if self.gui.call('tk', 'windowingsystem') == 'win32':
            self.player = mpv.MPV(ytdl=True,
                                  input_default_bindings=False,
                                  input_vo_keyboard=False,
                                  log_handler=self.player_log)
        else:
            self.player = mpv.MPV(ytdl=True,
                                  input_default_bindings=False,
                                  input_vo_keyboard=False,
                                  log_handler=self.player_log,
                                  vo='xv,x11')

        self.player.set_loglevel('error')
        self.player.input_commands = 'cycle osc'
        self.loglevel = 2

        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])

        self.channel_play(self.channel)

        canvasID = self.canvas.winfo_id()
        self.player.wid = str(canvasID)
        self.player.video_aspect_override = 16/9

        self.volume_max = self.player.volume_max
        self.volume = self.player.volume

        if self.gui.call('tk', 'windowingsystem') == 'win32':
            self.canvas.bind('<MouseWheel>', self.mouse_wheel)
        else:
            self.player.keybind('WHEEL_UP', "add volume +5")
            self.player.keybind('WHEEL_DOWN', "add volume -5")
            # self.player.keybind('MBTN_RIGHT', "cycle pause")
            # self.player.keybind('MBTN_RIGHT', "cycle osc")

    def player_log(self, loglevel, component, message):
        print('Player > [{}] {}: {}'.format(loglevel, component, message))

    def build_gui(self):
        # ------------------------------------------------------
        if self.gui.call('tk', 'windowingsystem') == 'win32':
            self.paddingLabelLogLevel = (0, -3, 0, 0)
            self.padxComboboxLogLevel = (0, 4)
            self.padyComboboxLogLevel = (2, 2)
            self.padyComboboxChannel = (2, 2)
        else:
            self.paddingLabelLogLevel = (0, 0, 0, 0)
            self.padxComboboxLogLevel = (0, 4)
            self.padyComboboxLogLevel = (2, 2)
            self.padyComboboxChannel = (2, 2)
        # ------------------------------------------------------
        width = 240*16/9*self.kScale
        height = 240*self.kScale
        self.canvas = tk.Canvas(self.gui, width=width,
                                height=height, bg='black')
        # ------------------------------------------------------
        frameControl = ttk.Frame(self.gui)
        frameControl['relief'] = 'raised'
        frameControl['padding'] = (0, 0, 10, 0)
        frameControl.rowconfigure(0, minsize=24)
        frameControl.columnconfigure(1, weight=100, minsize=360)
        frameControl.columnconfigure(2, weight=0)
        frameControl.columnconfigure(1, weight=0)
        frameControl.columnconfigure(4, weight=100)
        self.frameControl = frameControl

        font1 = tkFont.Font(family='Helvetica', size=-12, weight='normal')
        # ------------------------------------------------------
        comboboxChannels = ttk.Combobox(self.frameControl)
        comboboxChannels['state'] = 'readonly'
        comboboxChannels['justify'] = 'center'
        comboboxChannels['font'] = font1
        comboboxChannels.bind('<<ComboboxSelected>>', self.channel_changed)
        self.comboboxChannels = comboboxChannels
        
        # --------------------------------------

        comboboxWatchlinks = ttk.Combobox(self.frameControl)
        comboboxWatchlinks['state'] = 'readonly'
        comboboxWatchlinks['justify'] = 'left'
        comboboxWatchlinks['font'] = font1
        comboboxWatchlinks.bind('<<ComboboxSelected>>', self.watchlink_changed)
        self.comboboxWatchlinks = comboboxWatchlinks

        # --------------------------------------

        self.indicatorUpdateLiveStreamVideoURL = Progressindicator(
            frameControl, self.channel_m3u8_url_update)

        # --------------------------------------

        self.indicatorUpdateWatchlinks = Progressindicator(
            frameControl, self.channel_watch_links_update)

        # --------------------------------------

        self.imgMinus = ImageTk.PhotoImage(
            iconGenerator.minus(size=14, margin=(0, 0, 0, 0)))
        labelRemoveChannel = ttk.Label(
            self.frameControl, compound="image", image=self.imgMinus)
        labelRemoveChannel.bind('<Button-1>', self.channel_delete)
        self.labelRemoveChannel = labelRemoveChannel

        # --------------------------------------

        self.imgPlus = ImageTk.PhotoImage(
            iconGenerator.plus(size=14, margin=(0, 0, 0, 0)))
        labelAddChannel = ttk.Label(
            self.frameControl, compound="image", image=self.imgPlus)
        labelAddChannel.bind('<Button-1>', self.channel_add)
        self.labelAddChannel = labelAddChannel

        # --------------------------------------

        self.imgQuestion = ImageTk.PhotoImage(
            iconGenerator.question(size=14, margin=(0, 0, 0, 0)))
        labelHelp = ttk.Label(
            self.frameControl, compound="image", image=self.imgQuestion)
        labelHelp.bind('<Button-1>', self.menu)
        self.labelHelp = labelHelp

        # --------------------------------------

        self.labelLoglevel = ttk.Label(
            self.frameControl, text="Log level:", padding=self.paddingLabelLogLevel)
        self.labelLoglevel['font'] = font1

        comboboxLoglevel = ttk.Combobox(self.frameControl)
        comboboxLoglevel['state'] = 'readonly'
        comboboxLoglevel['justify'] = 'center'
        comboboxLoglevel['width'] = 10
        comboboxLoglevel['font'] = font1
        comboboxLoglevel.bind('<<ComboboxSelected>>', self.log_level_changed)
        self.values_log_level1 = [' No ', ' Fatal ', ' Error ',
                                  ' Warn ', ' Info ', ' Verbose ',
                                  ' Debug ', ' Trace ']
        self.values_log_level = ['no', 'fatal', 'error',
                                 'warn', 'info', 'v', 'debug', 'trace']

        comboboxLoglevel['values'] = self.values_log_level1
        comboboxLoglevel.set(self.values_log_level1[self.loglevel])
        self.comboboxLoglevel = comboboxLoglevel

        # ------------------------------------------------------
        frameMenu = Menu(self.gui)
        frameMenu.add_item(0, "About")
        frameMenu.add_item(1, "Shortcuts")
        frameMenu.add_item(2, "Settings")
        frameMenu.add_item(3, "Channel editor")
        frameMenu.add_item(4, "Quit")
        frameMenu.command(0, lambda event: self.dialog_about(event))
        frameMenu.command(1, lambda event: self.dialog_shortcuts(event))
        frameMenu.command(2, lambda event: self.setting_editor(event))
        frameMenu.command(3, lambda event: self.channel_editor(event))
        frameMenu.command(4, lambda event: self.quit(event))
        self.frameMenu = frameMenu
        # ------------------------------------------------------
        self.frameLog = FrameText(self.gui)
        if self.showing_log:
            self.show_log_widgets()
        # ------------------------------------------------------
        self.canvas.grid(row=0, column=0, sticky=(tk.NS))
        self.frameControl.grid(row=1, column=0, sticky=tk.EW)
        self.frameMenu.place(x=0, y=0)
        self.frameMenu.lower()
        
        self.gui_update()
        self.gui.attributes('-topmost', True)
        # self.set_geometry()

    # ------------------------------------------------------------------------------------------

    def set_geometry(self):
        self.gui.update_idletasks()
        w = self.gui.winfo_width()
        h = self.gui.winfo_height()
        # W = self.gui.winfo_screenwidth(
        # )-self.settings.screen_padding[0]-self.settings.screen_padding[2]
        # H = self.gui.winfo_screenheight(
        # )-self.settings.screen_padding[1]-self.settings.screen_padding[3]
        W = self.gui.winfo_screenwidth()
        H = self.gui.winfo_screenheight()
        x = (W-w)//2
        y = (H-h)//2
        self.gui.geometry("+{}+{}".format(x, y))
        print("Root window geometry: {}x{}+{}+{}".format(w, h, x, y))

    def gui_update(self):
        values_channel_list = ["" for i in range(
            len(self.channel_list.channels))]
        for i in range(len(self.channel_list.channels)):
            item = " {name} "
            values_channel_list[i] = item.format(
                name=self.channel_list.channels[i].name)

        self.values_channel_list = values_channel_list
        # self.values_channel_list = values_channel_list
        self.comboboxChannels['values'] = values_channel_list
        self.comboboxChannels.set(
            values_channel_list[self.iChannel])

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
            self.comboboxWatchlinks.set(
                values_watchlinks[self.channel.iWatchlink])

        self.comboboxChannels.grid(row=0, column=0,
                                   padx=2, pady=self.padyComboboxChannel,
                                   ipadx=2, ipady=0, sticky=tk.NS+tk.EW)

        if not self.showing_log:
            self.labelHelp.grid(column=6, row=0)

        match self.channel.channel_type:
            case 0:
                self.frameControl.columnconfigure(1, weight=0, minsize=0)
                self.labelRemoveChannel.grid(row=0, column=3,
                                             padx=(6, 2), pady=(0, 0),
                                             sticky=tk.W)
                self.labelAddChannel.grid(row=0, column=4,
                                          padx=(2, 0), pady=(0, 0),
                                          sticky=tk.W)
                self.comboboxWatchlinks.grid_forget()
                self.indicatorUpdateLiveStreamVideoURL.grid_forget()
                self.indicatorUpdateWatchlinks.grid_forget()
            case 1:
                self.frameControl.columnconfigure(1, weight=0, minsize=0)
                self.indicatorUpdateLiveStreamVideoURL.grid(row=0, column=2,
                                                            padx=2, pady=(1, 1),
                                                            sticky=tk.EW)
                self.labelRemoveChannel.grid(row=0, column=3,
                                             padx=(2, 2), pady=(0, 0),
                                             sticky=tk.W)
                self.labelAddChannel.grid(row=0, column=4,
                                          padx=(2, 0), pady=(0, 0),
                                          sticky=tk.W)
                self.comboboxWatchlinks.grid_forget()
                self.indicatorUpdateWatchlinks.grid_forget()
            case 2:
                self.frameControl.columnconfigure(1, weight=0, minsize=360)
                self.comboboxWatchlinks.grid(row=0, column=1,
                                             padx=2,
                                             pady=self.padyComboboxChannel,
                                             ipadx=2, ipady=0,
                                             sticky=tk.NS+tk.EW)
                self.indicatorUpdateWatchlinks.grid(row=0, column=2,
                                                    padx=2, pady=(1, 1),
                                                    sticky=tk.EW)
                self.indicatorUpdateLiveStreamVideoURL.grid_forget()
                self.labelRemoveChannel.grid(row=0, column=3,
                                             padx=(2, 2), pady=(0, 0),
                                             sticky=tk.W)
                self.labelAddChannel.grid(row=0, column=4,
                                          padx=(2, 0), pady=(0, 0), sticky=tk.W)

    def scale_canvas(self, k):
        self.kScale = k
        width = 240*16/9*self.kScale
        height = 240*self.kScale
        self.canvas['width'] = width
        self.canvas['height'] = height

    def toggle_fs(self, event=None):
        state = False if self.gui.attributes('-fullscreen') else True
        if state:
            self.frameControl.grid_forget()
            self.labelLoglevel.grid_forget()
            self.comboboxLoglevel.grid_forget()
            self.frameLog.grid_forget()
            W = self.gui.winfo_screenwidth()
            H = self.gui.winfo_screenheight()
            self.canvas['width'] = W
            self.canvas['height'] = H
            self.gui.attributes('-fullscreen', state)
        else:
            self.frameControl.grid(row=1, column=0, sticky=tk.EW)
            self.gui.attributes('-fullscreen', state)
            self.gui.wm_state('normal')
            self.gui.wm_focusmodel('active')

            # In Tk, there is a utility command, wm, for interacting with the window manager.
            # Options to the wm command allow you to control things like titles, placement, icon bitmaps,
            # and the like. In tkinter, these commands have been implemented as methods on the Wm class.
            # Toplevel widgets are subclassed from the Wm class, and so can call the Wm methods directly.
            # self.gui.state('normal')
            # self.gui.focusmodel('active')

            self.scale_canvas(self.kScale)

    # --- Log widgets ------------------------------------------

    def show_log_widgets(self):
        self.labelHelp.grid_forget()
        self.frameLog.grid(row=3, column=0, sticky=tk.EW)
        self.labelLoglevel.grid(column=5, row=0, padx=(
            40, 2), pady=(8, 0), sticky=tk.N+tk.EW)
        self.comboboxLoglevel.grid(column=6, row=0,
                                   padx=self.padxComboboxLogLevel,
                                   pady=self.padyComboboxLogLevel,
                                   ipadx=4, ipady=0, sticky=tk.NS+tk.EW)
        self.showing_log = True

    def hide_log_widgets(self):
        self.labelLoglevel.grid_forget()
        self.comboboxLoglevel.grid_forget()
        self.frameLog.grid_forget()
        self.showing_log = False
        self.labelHelp.grid(column=6, row=0)

    def toggle_log(self, event=None):
        self.frameMenu.lower()
        fs = True if self.gui.attributes('-fullscreen') else False
        if not fs:
            if self.showing_log:
                self.hide_log_widgets()
            else:
                self.show_log_widgets()

    def dialog_about(self, event):
        self.frameMenu.lower()
        about = About(self.gui)
        self.gui.wait_window(about.gui)

    def dialog_shortcuts(self, event):
        self.frameMenu.lower()
        shortcuts = Shortcuts(self.gui)
        self.gui.wait_window(shortcuts.gui)


    def setting_editor(self, event):
        self.frameMenu.lower()
        settingEditor = SettingEditor(self.gui, self)
        self.gui.wait_window(settingEditor.gui)


    def channel_editor(self, event):
        self.frameMenu.lower()
        self.player.input_commands = "cycle pause up"
        print("Channel editor running...")
        channelEditor = ChannelEditor(self.gui, self, self.channel_list)
        self.gui.wait_window(channelEditor.gui)
        print("Channel editor closed.")
        print("New channel list", self.channel_list.file_channel_list)
        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])
        self.gui_update()
        self.player.input_commands = "cycle pause"
        self.channel_play(self.channel)

    # --- Menu -------------------------------------------------

    def menu(self, event):
        self.frameMenu.update()
        x = self.gui.winfo_width() - self.frameMenu.winfo_width() - 1
        hgui = self.gui.winfo_height()
        hfC = self.frameControl.winfo_height()
        y = hgui - hfC - self.frameMenu.winfo_height() - 1
        self.frameMenu.place_configure(x=x, y=y)
        # self.frameMenu.tkraise()
        self.frameMenu.lift()

    # ==========================================================

    def volume_up(self, event=None):
        volume = self.player.volume
        volume += 5
        if volume > self.volume_max:
            volume = self.volume_max
        self.player.input_commands = "set volume {}".format(volume)
        print("Volume:", volume)

    def volume_down(self, event=None):
        volume = self.player.volume
        volume -= 5
        if volume < 0:
            volume = 0
        self.player.input_commands = "set volume {}".format(volume)
        print("Volume:", volume)

    # --- Mouse event handler ------------------------------------
    # def mouse(event):
    #     print("Mouse:", event)

    def mouse_wheel(self, event):
        print("Mouse:", event)
        if event.delta > 0:
            self.volume_up()
        else:
            self.volume_down()

    def mouse_scroll(self, event):
        print("Mouse:", event)

    # --- Key event handler ------------------------------------

    def key(self, event):
        print("Key:", event.keysym)
        ks = event.keysym

        # if ks == 'q' or ks == 'Q':
        #     self.channel_list.iChannel = self.iChannel
        #     self.channel_list.write(self.channel_list.file_channel_list)
        #     self.gui.destroy()

        if ks == 'Left':
            if self.iChannel > 0:
                self.iChannel -= 1
            else:
                self.iChannel = self.channel_list.nChannel-1
            self.channel_list.iChannel = self.iChannel
            self.comboboxChannels.set(self.values_channel_list[self.iChannel])
            self.channel = self.channel_list.channels[self.iChannel]
            self.gui_update()
            print("Channel changed!")
            print("Current channel: {} > {}".format(
                self.comboboxChannels.current(),
                self.channel_list.channels[self.iChannel].name))
            self.channel_play(self.channel)

        if ks == 'Right':
            if self.iChannel < self.channel_list.nChannel-1:
                self.iChannel += 1
            else:
                self.iChannel = 0
            self.channel_list.iChannel = self.iChannel
            self.channel = self.channel_list.channels[self.iChannel]
            self.comboboxChannels.set(self.values_channel_list[self.iChannel])
            self.gui_update()
            print("Channel changed!")
            print("Current channel: {} > {}".format(
                self.comboboxChannels.current(),
                self.channel_list.channels[self.iChannel].name))
            self.channel_play(self.channel)

        if ks == 'Up':
            self.volume_up()
        if ks == 'Down':
            self.volume_down()
        if ks == 'm' or ks == 'M':
            self.player.mute = not self.player.mute
            print("Mute:", self.player.mute)

        if ks == '1':
            self.scale_canvas(1)
        if ks == '2':
            self.scale_canvas(2)
        if ks == '3':
            if self.kScale_max >= 3:
                self.scale_canvas(3)

        # if ks == 'f' or ks == 'F' or ks == 'F10':
        #     self.toggle_fs()

        if ks == 'o':
            self.channellist_load(event)
        if ks == 'c':
            self.channel_editor(event)
        if ks == 'u':
            self.channel_update(event)
        if ks == 'p':
            self.channel_play_pause()
        if ks == 'e':
            self.channel_edit(event)
        if ks == 'a':
            self.channel_add(event)
        if ks == 'd':
            self.channel_delete(event)

    def log_level_changed(self, event):
        self.loglevel = self.comboboxLoglevel.current()
        self.player.set_loglevel(self.values_log_level[self.loglevel])
        self.frameControl.focus()
        self.comboboxLoglevel.selection_clear()
        print(
            f"Player log level: {self.loglevel}{self.values_log_level1[self.loglevel]}")

    def watchlink_changed(self, event):
        self.frameControl.focus()
        self.comboboxChannels.selection_clear()
        self.channel.iWatchlink = self.comboboxWatchlinks.current()
        self.channel_list.channels[self.iChannel] = deepcopy(self.channel)
        print("Watchlink changed!")
        print("Current watchlink: {} > {}".format(self.comboboxWatchlinks.current(),
                                                  self.comboboxWatchlinks['values'][self.channel.iWatchlink]))
        self.gui_update()
        self.channel_play(self.channel)

    def channel_changed(self, event):
        self.frameControl.focus()
        self.comboboxChannels.selection_clear()
        # self.frameLog.text.delete('1.0', END)
        self.channel_list.iChannel = self.comboboxChannels.current()
        self.iChannel = self.channel_list.iChannel
        self.channel = deepcopy(self.channel_list.channels[self.iChannel])
        print("Channel changed!")
        print("Current channel: {} > {}".format(self.comboboxChannels.current(),
                                                self.channel_list.channels[self.iChannel].name))
        # self.player.pause = True

        self.gui_update()
        self.channel_play(self.channel)

    def quit(self, event):
        self.channel_list.iChannel = self.iChannel
        self.channel_list.write(self.channel_list.file_channel_list)
        self.settings.last_channel_list = self.channel_list.file_channel_list
        self.settings.write(self.settings.file_settings)
        self.gui.destroy()

    def escape(self, event):
        self.frameMenu.lower()

    def channellist_load(self, event):
        self.channel_list.iChannel = self.iChannel
        self.channel_list.write(self.channel_list.file_channel_list)

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
            self.channel_play(self.channel)
            self.channel_list = deepcopy(self.channel_list)

    def channel_edit(self, event):
        self.channelEdit = ChannelEdit(self.gui, self)
        self.gui.wait_window(self.channelEdit.gui)
        if self.channelEdit.edited:
            print("Channel edited!")
        self.channelEdit = None

    def channel_add(self, event):
        self.channelAdd = ChannelAdd(self.gui, self)
        self.gui.wait_window(self.channelAdd.gui)
        if self.channelAdd.added:
            print("Channel added!")
        self.channelAdd = None

    def channel_delete(self, event):
        print("Channel remove!")
        channel = self.channel_list.channels[self.iChannel]
        print(channel.name)
        d = DialogChannelRemove(self.gui, channel)
        print("'Channel Remove' dialog is opened, waiting to respond")
        self.gui.wait_window(d.gui)
        print('End of wait_window, back in MainWindow code')
        print('got data: {yn}'.format(yn=d.yesNo))
        if d.yesNo == 'Yes':
            if self.channel_list.nChannel > 1:
                self.channel_list.remove_channel(self.channel_list.iChannel)
                self.iChannel = self.channel_list.iChannel
                self.channel = self.channel_list.channels[self.iChannel]
                self.gui_update()

    def channel_update(self, event):
        if self.channel.channel_type == 1:
            self.indicatorUpdateLiveStreamVideoURL.start_progress(event)
        if self.channel.channel_type == 2:
            self.indicatorUpdateWatchlinks.start_progress(event)
        self.gui_update()
        self.channel_play(self.channel)

    def channel_m3u8_url_update(self):
        load_timeout = self.settings.page_load_timeout
        capture_duration = self.settings.capture_duration
        self.channel.m3u8_url_update(load_timeout, capture_duration)
        self.channel_list.channels[self.iChannel] = deepcopy(self.channel)
        self.indicatorUpdateLiveStreamVideoURL.stop_progress()
        if self.channelEdit is not None:
            self.channelEdit.frameChannel.indicatorUpdateLiveStreamVideoURL.stop_progress()
            self.channelEdit.frameChannel.update(self.channel)
        self.gui_update()
        self.channel_play(self.channel)

    def channel_watch_links_update(self):
        load_timeout = self.settings.page_load_timeout
        self.channel.watch_links_update(load_timeout)
        self.channel_list.channels[self.iChannel] = deepcopy(self.channel)
        self.indicatorUpdateWatchlinks.stop_progress()
        if self.channelAdd is not None:
            self.channelAdd.frameChannel.indicatorUpdateWatchlinks.stop_progress()
            self.channelAdd.frameChannel.update(self.channel)
        if self.channelEdit is not None:
            self.channelEdit.frameChannel.indicatorUpdateWatchlinks.stop_progress()
            self.channelEdit.frameChannel.update(self.channel)
        self.gui_update()
        self.channel_play(self.channel)

    def channel_play(self, channel):
        videoURL = None
        if channel.channel_type < 2:
            print(f"Playing channel: {channel.name} ({channel.video})")
            videoURL = channel.video
        else:
            if len(channel.watchlinks) > 0:
                watchlink = channel.watchlinks[channel.iWatchlink]
                videoURL = watchlink.href
                print(
                    f"Playing channel: {channel.name} - {watchlink.title} ({watchlink.href})")
        if videoURL is not None:
            self.player["loop-playlist"] = "force"
            self.player.play(videoURL)
        else:
            print("No video URL!")

    def channel_play_pause(self):
        if self.player.pause:
            self.player.input_commands = "cycle pause up"
            print("Playing kept on!")
        else:
            self.player.input_commands = "cycle pause"
            print("Playing paused!")


# # ==============================================================================================
# channels = "channels.xml"
# izle = Izle(channels_file=channels)
izle = Izle()
