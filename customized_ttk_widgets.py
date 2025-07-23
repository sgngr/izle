"""
=======================================
Customized Ttk Widgets
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw
from io import BytesIO

# ------------------------------------------------------------------------------


class CheckbuttonCustomized(ttk.Checkbutton):
    counter = 0

    def __init__(self, master, **kwargs):

        self.master = master
        self.kwargs = kwargs

        style = ttk.Style(self.master)
        style.theme_use('clam')

        self.indicatorsize = 16
        if 'indicatorsize' in kwargs.keys():
            self.indicatorsize = kwargs['indicatorsize']
            self.kwargs.pop('indicatorsize')

        self.indicatormargin = (0, 0, 0, 0)
        if 'indicatormargin' in kwargs.keys():
            self.indicatormargin = kwargs['indicatormargin']
            self.kwargs.pop('indicatormargin')

        self.indicatorborder = "black"
        if 'indicatorborder' in kwargs.keys():
            self.indicatorborder = kwargs['indicatorborder']
            self.kwargs.pop('indicatorborder')

        self.indicatorfill = "white"
        if 'indicatorfill' in kwargs.keys():
            self.indicatorfill = kwargs['indicatorfill']
            self.kwargs.pop('indicatorfill')

        self.indicatorcheck = "black"
        if 'indicatorcheck' in kwargs.keys():
            self.indicatorcheck = kwargs['indicatorcheck']
            self.kwargs.pop('indicatorcheck')

        data_unselected = self.create_indicator_image(
            size=self.indicatorsize, margin=self.indicatormargin, border=self.indicatorborder, fill=self.indicatorfill, check=self.indicatorcheck)
        self.img_unselected = tk.PhotoImage(
            f"checkbutton_unselected_{CheckbuttonCustomized.counter}", master=self.master, data=data_unselected)

        data_selected = self.create_indicator_image(checked=True,
                                                    size=self.indicatorsize, margin=self.indicatormargin, border=self.indicatorborder, fill=self.indicatorfill, check=self.indicatorcheck)
        self.img_selected = tk.PhotoImage(
            f"checkbutton_selected_{CheckbuttonCustomized.counter}", master=self.master, data=data_selected)

        style.element_create(f'custom.cb_indicator_{CheckbuttonCustomized.counter}', 'image', f"checkbutton_unselected_{CheckbuttonCustomized.counter}",
                             ('selected', '!disabled', f"checkbutton_selected_{CheckbuttonCustomized.counter}"))

        style.layout(
            f'custom_indicator_{CheckbuttonCustomized.counter}.TCheckbutton', [
                ('Checkbutton.padding',
                    {'sticky': 'nswe',
                     'children': [
                         (f'custom.cb_indicator_{CheckbuttonCustomized.counter}',
                          {
                          'side': 'left', 'sticky': ''}),
                         ('Checkbutton.focus',
                          {'side': 'left', 'sticky': 'w', 'children': [
                              ('Checkbutton.label', {'sticky': 'nswe'})
                          ]
                          }
                          )
                     ]
                     }
                 )
            ]
        )

        super().__init__(self.master, **kwargs,
                         style=f'custom_indicator_{CheckbuttonCustomized.counter}.TCheckbutton')

        CheckbuttonCustomized.counter += 1

    def create_indicator_image(self, checked=False, size=16, margin=(0, 0, 0, 0), border="black", fill="white", check="black"):
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = 128/size
        W = int(128+k*(margin[0]+margin[2]))
        H = int(128+k*(margin[1]+margin[3]))
        x0 = int(k*margin[0])
        y0 = int(k*margin[1])

        image = Image.new("RGBA", (W, H))
        drawing = ImageDraw.Draw(image)
        drawing.rounded_rectangle(
            [x0+2, y0+2, x0+126, y0+126],
            radius=20,
            fill=fill,
            outline=border,
            width=8,
        )
        if checked:
            drawing.rectangle(
                [x0+30, y0+30, x0+98, y0+98],
                fill=check,
                outline=check
            )
        image = image.resize((w, h), Image.LANCZOS)
        pngImage = BytesIO()
        image.save(pngImage, format="png")
        return bytes(pngImage.getbuffer())


# ------------------------------------------------------------------------------

class RadiobuttonCustomized(ttk.Radiobutton):
    counter = 0

    def __init__(self, master, **kwargs):

        self.master = master
        self.kwargs = kwargs

        style = ttk.Style(self.master)
        style.theme_use('clam')

        self.indicatorsize = 16
        if 'indicatorsize' in kwargs.keys():
            self.indicatorsize = kwargs['indicatorsize']
            self.kwargs.pop('indicatorsize')

        self.indicatormargin = (0, 0, 0, 0)
        if 'indicatormargin' in kwargs.keys():
            self.indicatormargin = kwargs['indicatormargin']
            self.kwargs.pop('indicatormargin')

        self.indicatorborder = "black"
        if 'indicatorborder' in kwargs.keys():
            self.indicatorborder = kwargs['indicatorborder']
            self.kwargs.pop('indicatorborder')

        self.indicatorfill = "white"
        if 'indicatorfill' in kwargs.keys():
            self.indicatorfill = kwargs['indicatorfill']
            self.kwargs.pop('indicatorfill')

        self.indicatorcheck = "black"
        if 'indicatorcheck' in kwargs.keys():
            self.indicatorcheck = kwargs['indicatorcheck']
            self.kwargs.pop('indicatorcheck')

        data_unselected = self.create_indicator_image(
            size=self.indicatorsize, margin=self.indicatormargin, border=self.indicatorborder, fill=self.indicatorfill, check=self.indicatorcheck)
        self.img_unselected = tk.PhotoImage(
            f"radiobutton_unselected_{RadiobuttonCustomized.counter}", master=self.master, data=data_unselected)

        data_selected = self.create_indicator_image(checked=True,
                                                    size=self.indicatorsize, margin=self.indicatormargin, border=self.indicatorborder, fill=self.indicatorfill, check=self.indicatorcheck)
        self.img_selected = tk.PhotoImage(
            f"radiobutton_selected_{RadiobuttonCustomized.counter}", master=self.master, data=data_selected)

        style.element_create(f'custom.rb_indicator_{RadiobuttonCustomized.counter}', 'image', f"radiobutton_unselected_{RadiobuttonCustomized.counter}",
                             ('selected', '!disabled', f"radiobutton_selected_{RadiobuttonCustomized.counter}"))

        style.layout(
            f'custom_indicator_{RadiobuttonCustomized.counter}.TRadiobutton', [
                ('Radiobutton.padding',
                    {'sticky': 'nswe',
                     'children': [
                         (f'custom.rb_indicator_{RadiobuttonCustomized.counter}', {
                          'side': 'left', 'sticky': ''}),
                         ('Radiobutton.focus',
                          {'side': 'left', 'sticky': 'w', 'children': [
                              ('Radiobutton.label', {
                                  'sticky': 'nswe'})
                          ]
                          }
                          )
                     ]
                     }
                 )
            ]
        )

        super().__init__(self.master, **kwargs,
                         style=f'custom_indicator_{RadiobuttonCustomized.counter}.TRadiobutton')

        RadiobuttonCustomized.counter += 1

    def create_indicator_image(self, checked=False, size=16, margin=(0, 0, 0, 0), border="black", fill="white", check="black"):
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = 128/size
        W = int(128+k*(margin[0]+margin[2]))
        H = int(128+k*(margin[1]+margin[3]))
        x0 = int(k*margin[0])
        y0 = int(k*margin[1])

        image = Image.new("RGBA", (W, H))
        drawing = ImageDraw.Draw(image)

        drawing.circle(
            [x0+64, y0+64],
            radius=62,
            fill=fill,
            outline=border,
            width=8,
        )
        if checked:
            drawing.circle(
                [x0+64, y0+64],
                radius=34,
                fill=check,
                outline=check,
                width=8,
            )

        image = image.resize((w, h), Image.LANCZOS)
        pngImage = BytesIO()
        image.save(pngImage, format="png")
        return bytes(pngImage.getbuffer())


# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    root = tk.Tk()
    root.title('Customized Ttk Widgets')
    root.geometry('300x250')

    style = ttk.Style()
    style.theme_use('clam')

    # ----------------------------------------------------------

    def print_cb_vars():
        print("Checkbutton variable 1:", cb_var1.get())
        print("Checkbutton variable 2:", cb_var2.get())

    cb_var1 = tk.IntVar()
    cb_var1.set(1)
    c1 = CheckbuttonCustomized(root, onvalue=1, offvalue=0, takefocus=False, variable=cb_var1, command=print_cb_vars,
                               text="Checkbutton 1", indicatorsize=32, indicatormargin=(0, 0, 5, 4), indicatorborder="blue", indicatorfill="gold", indicatorcheck="red", padding=(5, 4, 5, 0))
    c1.grid(sticky=tk.W)

    cb_var2 = tk.IntVar()
    cb_var2.set(0)
    c2 = CheckbuttonCustomized(root, onvalue=1, offvalue=0, takefocus=False, variable=cb_var2, command=print_cb_vars,
                               text="Checkbutton 2", indicatorsize=16, indicatormargin=(0, 0, 5, 4), indicatorborder="red", padding=(10, 20, 20, 20))
    c2.grid(sticky=tk.W)

    # ----------------------------------------------------------

    def print_rb_var():
        print("Radiobutton variable:", rb_var.get())

    rb_var = tk.IntVar()
    rb_var.set(1)

    r1 = RadiobuttonCustomized(root, takefocus=False, value=1, variable=rb_var, command=print_rb_var,  text='Radiobutton 1',  indicatorsize=32, indicatormargin=(
        0, 0, 5, 4), indicatorborder="blue", indicatorfill="gold", indicatorcheck="red", padding=(5, 4, 5, 0))

    r2 = RadiobuttonCustomized(root, takefocus=False, value=2, variable=rb_var, command=print_rb_var, text='Radiobutton 2',
                               indicatorsize=16, indicatormargin=(0, 0, 5, 4), indicatorborder="red", padding=(10, 20, 20, 20))
    r1.grid(padx=10, pady=(10, 2))
    r2.grid(padx=10, pady=(2, 10))

    # ----------------------------------------------------------

    root.mainloop()
