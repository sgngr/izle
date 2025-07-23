"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Menu module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""


import tkinter as tk
from tkinter import ttk

# ----------------------------------------------------------------------------------------------

# import tkinter.font as TkFont
from tkinter import font as tkFont


class MenuItem():
    def __init__(self, menu, order, text):
        self.menu = menu
        self.order = order
        self.text = text
        self.label = None
        self.submenu = None


class Submenu():
    def __init__(self, order, menu):
        self.order = order
        self.menu = menu


class Menu(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self['relief'] = 'raised'

        padding = (5, 5, 5, 5)
        if self.tk.call('tk', 'windowingsystem') == 'win32':
            padding = (5, 7, 5, 7)

        self["padding"] = padding

        self.parent = None
        self.app = None
        self.row = 0
        self.rowspan = 1
        self.column = 0
        self.columnspan = 1
        self.order = 0
        self.orient = tk.VERTICAL
        self.text = 'Menu item'
        self.position = (0, 0)

        if 'parent' in kwargs.keys():
            self.parent = kwargs["parent"]
        if 'app' in kwargs.keys():
            self.app = kwargs["app"]
        if 'row' in kwargs.keys():
            self.row = kwargs["row"]
        if 'rowspan' in kwargs.keys():
            self.rowspan = kwargs["rowspan"]
        if 'column' in kwargs.keys():
            self.column = kwargs["column"]
        if 'columnspan' in kwargs.keys():
            self.columnspan = kwargs["columnspan"]
        if 'order' in kwargs.keys():
            self.order = kwargs["order"]
        if 'orient' in kwargs.keys():
            self.orient = kwargs["orient"]
        if 'text' in kwargs.keys():
            self.text = kwargs["text"]
        if 'position' in kwargs.keys():
            self.position = kwargs["position"]

        self.showed_submenu = None
        self.disabled = False

        self.submenus = list()
        self.items = list()

        if self.parent is None:
            self.disabled = True
        else:
            self.disabled = False

        if self.parent is None:
            if self.orient == tk.HORIZONTAL:
                self.grid(row=self.row, column=self.column,
                          columnspan=self.columnspan, sticky=(tk.W, tk.N, tk.E, tk.S))
            else:
                self.grid(row=self.row, column=self.column,
                          rowspan=self.columnspan, sticky=(tk.W, tk.N, tk.E, tk.S))

        if self.parent is not None:
            self.parent.submenu(self.order, self)

    # ------------------------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.fontsize = 12  # as pixel
        self.font = tkFont.Font(
            family='Helvetica', size=-1*self.fontsize, weight='normal')
        self.font = tkFont.nametofont('TkMenuFont')
        self.font.config(size=-self.fontsize)

        self.style.configure('Menu.TLabel',
                             font=self.font
                             )
        self.style.map('Menu.TLabel',
                       background=[
                           ('hover', '#3daee9')],
                       foreground=[('hover', 'white')])
    # ------------------------------------------------------------

    def toggle_status(self, event, order):
        if self.parent is None:
            if self.disabled:
                self.disabled = False
                self.show_submenu(event=None, order=order)
            else:
                self.disabled = True
                self.hide_submenu()

    def get_position(self):
        self.update()
        if self.parent is None:
            bbox = self.master.grid_bbox(row=self.row, column=self.column)
            self.position = (bbox[0], bbox[1])
            self.size = (bbox[2], bbox[3])
        else:
            if self.parent.orient == tk.HORIZONTAL:
                bbox = self.parent.grid_bbox(row=0, column=self.order)
                item_position0 = bbox[0]-5
                position = (
                    self.parent.position[0]+item_position0, self.parent.position[1]+self.parent.size[1])
                self.position = position
            else:
                bbox = self.parent.grid_bbox(row=self.order, column=0)
                parent_width = bbox[2]+10
                item_position1 = bbox[1]-5
                position = (
                    self.parent.position[0]+parent_width, self.parent.position[1]+item_position1)
                self.position = position

    def add_item(self, order, text):
        item = MenuItem(self, order, text)
        item.label = ttk.Label(self, text=text, style='Menu.TLabel')
        if self.orient == tk.VERTICAL:
            item.label.grid(row=order, column=0, sticky=(tk.W,  tk.E))
        else:
            item.label.grid(row=0, column=order, sticky=(tk.W, tk.E))

        padding = (5, 0, 5, 0)
        if self.tk.call('tk', 'windowingsystem') == 'x11':
            padding = (5, 2, 5, 0)

        item.label["padding"] = padding

        item.label.bind("<Enter>", lambda event,
                        order=order: self.show_submenu(event, order))
        item.label.bind("<Button-1>", lambda event,
                        order=order: self.toggle_status(event, order))

        self.items.append(item)
        self.submenus.append(None)

    def show_submenu(self, event, order):
        self.hide_submenu()
        if not self.disabled and self.submenus[order] is not None:
            submenu = self.submenus[order]
            submenu.place(x=submenu.position[0], y=submenu.position[1])
            submenu.lift()
            self.showed_submenu = submenu

    def hide_submenu(self):
        showed_submenu = self.showed_submenu
        while showed_submenu is not None:
            showed_submenu.place_forget()
            showed_submenu.parent.showed_submenu = None
            showed_submenu = showed_submenu.showed_submenu

    def command(self, order, command):
        menuitem = self.items[order]
        menuitem.label.bind("<Button-1>", command)

    def submenu(self, order, submenu):
        self.submenus[order] = submenu
        self.app.submenus.append(submenu)

# ----------------------------------------------------------------------------------------------


if __name__ == '__main__':

    from tkinter import filedialog
    import pathlib

    # ----------------------------------------------------------------------------------------------
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
    # ----------------------------------------------------------------------------------------------
    txt1 = "These are the voyages of the Starship Enterprise.\n\nIts continuing mission, to explore strange new worlds, \nto seek out new life and new civilizations, \nto boldly go where no one has gone before.\nWe need to neutralize the homing signal. Each unit has total \nenvironmental control, gravity, temperature, atmosphere, light, \nin a protective field. Sensors show energy readings in your area.\nWe had a forced chamber explosion in the resonator coil.\nField strength has increased by 3,000 percent.\n\nDeflector power at maximum. Energy discharge in six seconds.\nWarp reactor core primary coolant failure. Fluctuate phaser \nresonance frequencies. Resistance is futile. Recommend we adjust \nshield harmonics to the upper EM band when proceeding.\nThese appear to be some kind of power-wave-guide conduits \nwhich allow them to work collectively as they perform ship functions.\nIncrease deflector modulation to upper frequency band.\n\nResistance is futile."
    txt2 = "These are the voyages of the Starship Enterprise.\n\nWe're acquainted with the wormhole phenomenon, but this... \nis a remarkable piece of bio-electronic engineering \nby which I see much of the EM spectrum ranging from heat and \ninfrared through radio waves, et cetera, and forgive me \nif I've said and listened to this a thousand times.\nThis planet's interior heat provides an abundance of geothermal \nenergy. We need to neutralize the homing signal.\n\nResistance is futile."
    # ----------------------------------------------------------------------------------------------

    class Shortcuts():
        def __init__(self, parent):
            self.parent = parent
            self.gui = tk.Toplevel()
            self.gui.state("withdrawn")

            # self.gui.iconphoto(False,PhotoImage(file='myapp.png'))
            self.gui.title("Shortcuts")

            self.frameShortcuts = ttk.Frame(self.gui)
            self.frameShortcuts.grid(row=0, column=0)
            self.frameShortcuts['relief'] = 'raised'
            self.frameShortcuts['padding'] = (5, 5, 5, 5)

            self.font = tkFont.Font(
                family='Helvetica', size=-11, weight='normal')

            labelShortcut00 = ttk.Label(
                self.frameShortcuts, text="Ctrl+O", font=self.font)
            labelShortcut00.grid(row=0, column=0, padx=(10, 5), sticky="e")
            labelShortcut01 = ttk.Label(
                self.frameShortcuts, text="Load text from file", font=self.font)
            labelShortcut01.grid(row=0, column=1, padx=(5, 10), sticky="w")

            labelShortcut20 = ttk.Label(
                self.frameShortcuts, text="Ctrl+S", font=self.font)
            labelShortcut20.grid(row=2, column=0, padx=(10, 5), sticky="e")
            labelShortcut21 = ttk.Label(
                self.frameShortcuts, text="Export text as file", font=self.font)
            labelShortcut21.grid(row=2, column=1, padx=(5, 10), sticky="w")

            labelShortcut50 = ttk.Label(
                self.frameShortcuts, text="Ctrl+Q / Q", font=self.font)
            labelShortcut50.grid(row=5, column=0, padx=(10, 5), sticky="e")
            labelShortcut51 = ttk.Label(
                self.frameShortcuts, text="Quit", font=self.font)
            labelShortcut51.grid(row=5, column=1, padx=(5, 10), sticky="w")

            self.gui.bind("<Key>", self.key)
            self.gui.resizable(False, False)
            self.gui.attributes('-topmost', True)

            self.gui.update()
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
    # ----------------------------------------------------------------------------------------------

    class About():
        def __init__(self, parent):
            self.parent = parent
            self.gui = tk.Toplevel()
            self.gui.state("withdrawn")

            # self.gui.iconphoto(False, tk.PhotoImage(file='myapp.png'))
            self.gui.title("About Testing Menu Class")

            self.frameAbout = ttk.Frame(self.gui)
            self.frameAbout.grid(row=0, column=0)
            self.frameAbout['relief'] = 'raised'
            self.frameAbout['padding'] = (5, 5, 5, 5)

            self.font1b = tkFont.Font(
                family='Helvetica', size=-14, weight='bold')
            self.font2 = tkFont.Font(
                family='Helvetica', size=-11, weight='normal')
            self.font2b = tkFont.Font(
                family='Helvetica', size=-11, weight='bold')

            labelVolumeView = ttk.Label(
                self.frameAbout, text="Testing Menu", font=self.font1b)
            labelVolumeView.grid(row=0, column=0, columnspan=2)

            labelVersion = ttk.Label(
                self.frameAbout, text="Version {}".format('0.1'), font=self.font2)
            labelVersion.grid(row=1, column=0, columnspan=2)

            labelAuthor0 = ttk.Label(
                self.frameAbout, text="Author:", font=self.font2)
            labelAuthor1 = ttk.Label(
                self.frameAbout, text="Sinan Güngör", font=self.font2)
            labelAuthor0.grid(row=2, column=0, sticky="e", padx=(10, 3))
            labelAuthor1.grid(row=2, column=1, sticky="w", padx=(0, 10))
            labelLicense0 = ttk.Label(
                self.frameAbout, text="License:", font=self.font2)
            labelLicense1 = ttk.Label(
                self.frameAbout, text="GNU General Public License, Version 3", font=self.font2)
            labelLicense0.grid(row=3, column=0, sticky="e", padx=(10, 3))
            labelLicense1.grid(row=3, column=1, sticky="w", padx=(0, 10))

            self.frameAbout.columnconfigure(1, minsize=200)

            self.gui.bind("<Key>", self.key)
            self.gui.resizable(False, False)
            self.gui.attributes('-topmost', True)

            self.gui.update()
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
    # ----------------------------------------------------------------------------------------------

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
                                width=20
                                )
            self.hscrollbar.config(command=self.text.xview)
            self.vscrollbar.config(command=self.text.yview)
            self.text.grid(row=0, column=0, sticky=tk.EW+tk.NS)
            self.hscrollbar.grid(row=1, column=0, sticky=tk.EW)
            self.vscrollbar.grid(row=0, column=1, sticky=tk.NS)
            self.columnconfigure(0, weight=100)
            self.columnconfigure(1, weight=0)
            self.rowconfigure(0, weight=100)
            self.rowconfigure(1, weight=0)

    # ----------------------------------------------------------------------------------------------

    class TestApp():
        def __init__(self):

            self.gui = tk.Tk()
            self.gui.state("withdrawn")
            self.gui.title("Testing Menu")
            self.gui.minsize(width=480, height=320)

            self.submenus = list()
            # ------------------------------------------------------
            self.build_gui()
            # ------------------------------------------------------

            self.gui.update()
            self.gui.deiconify()
            self.gui.focus_force()

            # ------------------------------------------------------
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
            self.gui.bind('<Key>', self.key)
            # ------------------------------------------------------

            self.gui.focus_set()
            self.gui.resizable(True, True)
            self.gui.mainloop()

        def build_gui(self):
            self.gui.columnconfigure(0, weight=1, minsize=480)
            self.gui.rowconfigure(0, weight=0)
            self.gui.rowconfigure(1, weight=1, minsize=320)
            textFrame = FrameText(self.gui)
            textFrame.grid(row=1, column=0, sticky=tk.NS+tk.EW)
            self.text = textFrame.text

            self.build_menu()

        def build_menu(self):
            mainMenu = Menu(self.gui, app=self,
                            orient=tk.HORIZONTAL, row=0, column=0)
            mainMenu.add_item(0, "File")
            mainMenu.add_item(1, "Help")
            mainMenu.get_position()
            self.mainMenu = mainMenu

            fileMenu = Menu(self.gui, app=self, parent=mainMenu, order=0)
            fileMenu.add_item(0, "Open")
            fileMenu.add_item(1, "Load Test Text")
            fileMenu.add_item(2, "Save")
            fileMenu.add_item(3, "Quit")
            fileMenu.command(0, lambda event: self.open(event))
            fileMenu.command(2, lambda event: self.save(event))
            fileMenu.command(3, lambda event: self.quit(event))
            fileMenu.get_position()
            self.fileMenu = fileMenu

            helpMenu = Menu(self.gui, app=self, parent=mainMenu, order=1)
            helpMenu.add_item(0, "Shortcuts")
            helpMenu.add_item(1, "About")
            helpMenu.command(0, lambda event: self.dialog_shortcuts(event))
            helpMenu.command(1, lambda event: self.dialog_about(event))
            helpMenu.get_position()
            self.helpMenu = helpMenu

            dataMenu = Menu(self.gui, app=self, parent=fileMenu, order=1)
            dataMenu.add_item(0, "Test Data 0")
            dataMenu.add_item(1, "Test Data 1")
            dataMenu.command(0, lambda event: self.load_text1(event))
            dataMenu.command(1, lambda event: self.load_text2(event))
            dataMenu.get_position()
            self.dataMenu = dataMenu

        def key(self, event):
            k = event.keysym

            if ctrl_shift:
                print('Key: <Ctrl>+<Shift>+{}'.format(k))
            if ctrl:
                print('Key: <Ctrl>+{}'.format(k))
            if shift:
                print('Key: <Shift>+{}'.format(k))
            if not ctrl and not shift and not ctrl_shift:
                print("Key: {}".format(k))

            if k == 'q' or k == 'Q' or (ctrl and k == 'q'):
                self.quit(None)
            if ctrl and k == 'o':
                self.open(self)
            if ctrl and k == 's':
                self.save(self)
            if k == 'Escape':
                self.mainMenu.hide_submenu()

        def open(self, event):
            self.mainMenu.hide_submenu()
            filePath = filedialog.askopenfilename(
                title="Select a text file", filetypes=[("Text file", "*.txt")])
            if filePath:
                extension = pathlib.Path(filePath).suffix
                stem = pathlib.Path(filePath).stem
                print("File to open:", f"{stem}{extension}")

                with open(filePath, "r") as f:
                    txt = f.read()
                print(txt)
                self.text.delete(1.0, tk.END)
                self.text.insert('end', txt)
                self.text.see('end')
            self.mainMenu.disabled = True

        def save(self, event):
            self.mainMenu.hide_submenu()
            filePath = filedialog.asksaveasfilename(initialfile="test.txt", title="Select a .txt file", filetypes=(
                ("Text files", "*.txt"), ("all files", "*.*")))
            if filePath:
                print("Text will be exported as:", filePath)

        def load_text1(self, event):
            self.mainMenu.hide_submenu()
            self.text.delete(1.0, tk.END)
            self.text.insert('end', txt1)
            self.mainMenu.disabled = True

        def load_text2(self, event):
            self.mainMenu.hide_submenu()
            self.text.delete(1.0, tk.END)
            self.text.insert('end', txt2)
            self.mainMenu.disabled = True

        def quit(self, event):
            print("Quit")
            self.gui.destroy()

        def dialog_about(self, event):
            self.mainMenu.hide_submenu()
            about = About(self.gui)
            self.gui.wait_window(about.gui)
            self.mainMenu.disabled = True

        def dialog_shortcuts(self, event):
            self.mainMenu.hide_submenu()
            shortcuts = Shortcuts(self.gui)
            self.gui.wait_window(shortcuts.gui)
            self.mainMenu.disabled = True

        # ------------------------------------------------------------------------------------------

    testApp = TestApp()
