"""
================================================================
izle - mpv GUI for watching live streams and YouTube's channels
Icon generator module
================================================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, ImageDraw, Image

# from PIL import ImageFont
# from PIL import ImageColor
# from PIL import Image, ImageDraw

# from io import BytesIO
import math


class IconGenerator():

    def rectangle_check(self, checked=False, size=16, margin=(0, 0, 0, 0),
                        checktype='square', border="black", fill="white",
                        check="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        draw.rounded_rectangle(
            [-S/2+x0, -S/2+y0, S/2+x0, S/2+y0],
            radius=20,
            fill=fill,
            outline=border,
            width=8,
        )
        if checked:
            if checktype == 'square':
                w_check = 72
                draw.rectangle(
                    [round(-w_check/2.0+x0), round(-w_check/2.0+y0),
                     round(w_check/2.0+x0), round(w_check/2.0+y0)],
                    fill=check,
                    outline=check
                )
            if checktype == 'check':
                w_check = 72
                t_check = 12
                h_check = 2.0/3.0*w_check+t_check/math.sqrt(2)

                p0 = (round(-w_check/2.0+w_check/3.0+x0), round(h_check/2.0+y0))
                p1 = (p0[0]-round(w_check/3), p0[1]-round(w_check/3))
                p2 = (p1[0]+round(t_check/math.sqrt(2)),
                      p1[1]-round(t_check/math.sqrt(2)))
                p3 = (p0[0], p0[1]-round(math.sqrt(2)*t_check))
                p5 = (p0[0]+round(2.0/3.0*w_check),
                      p0[1]-round(2.0/3.0*w_check))
                p4 = (p5[0]-round(t_check/math.sqrt(2)),
                      p5[1]-round(t_check/math.sqrt(2)))
                # draw.polygon([p0,p1,p2,p3,p4,p5,p0],fill=check, outline=check, width=10)
                p12 = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
                p03 = ((p0[0]+p3[0])/2, (p0[1]+p3[1])/2)
                p54 = ((p5[0]+p4[0])/2, (p5[1]+p4[1])/2)
                draw.line([p12, p03, p54], fill=check, width=12, joint="curve")

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def circular_check(self, checked=False, size=16, margin=(0, 0, 0, 0),
                       checktype='cicle', border="black", fill="white",
                       check="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        # draw.circle(
        #     [x0+64,y0+64],
        #     radius=62,
        #     fill=fill,
        #     outline=border,
        #     width=8,
        # )
        # if checked :
        #     draw.circle(
        #         [x0+64,y0+64],
        #         radius=34,
        #         fill=check,
        #         outline=check,
        #         width=8,
        #     )

        # draw.rounded_rectangle(
        #     [-S/2+x0, -S/2+y0, S/2+x0, S/2+y0],
        #     radius=20,
        #     fill=fill,
        #     outline=border,
        #     width=8,
        # )

        draw.circle(
            [0+x0, 0+y0],
            radius=64,
            fill=fill,
            outline=border,
            width=8,
        )

        if checked:
            if checktype == 'circle':
                draw.circle(
                    [0+x0, 0+y0],
                    radius=36,
                    fill=check,
                    outline=check,
                    width=8,
                )

            if checktype == 'check':
                w_check = 72
                t_check = 12
                h_check = 2.0/3.0*w_check+t_check/math.sqrt(2)

                p0 = (round(-w_check/2.0+w_check/3.0+x0), round(h_check/2.0+y0))
                p1 = (p0[0]-round(w_check/3), p0[1]-round(w_check/3))
                p2 = (p1[0]+round(t_check/math.sqrt(2)),
                      p1[1]-round(t_check/math.sqrt(2)))
                p3 = (p0[0], p0[1]-round(math.sqrt(2)*t_check))
                p5 = (p0[0]+round(2.0/3.0*w_check),
                      p0[1]-round(2.0/3.0*w_check))
                p4 = (p5[0]-round(t_check/math.sqrt(2)),
                      p5[1]-round(t_check/math.sqrt(2)))
                # draw.polygon([p0,p1,p2,p3,p4,p5,p0],fill=check, outline=check, width=10)
                p12 = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
                p03 = ((p0[0]+p3[0])/2, (p0[1]+p3[1])/2)
                p54 = ((p5[0]+p4[0])/2, (p5[1]+p4[1])/2)
                draw.line([p12, p03, p54], fill=check, width=12, joint="curve")

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def check(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        w_check = 14*8
        t_check = 16
        h_check = 2.0/3.0*w_check+t_check/math.sqrt(2)

        p0 = (round(-w_check/2.0+w_check/3.0+x0), round(h_check/2.0+y0))
        p1 = (p0[0]-round(w_check/3), p0[1]-round(w_check/3))
        p2 = (p1[0]+round(t_check/math.sqrt(2)),
              p1[1]-round(t_check/math.sqrt(2)))
        p3 = (p0[0], p0[1]-round(math.sqrt(2)*t_check))
        p5 = (p0[0]+round(2.0/3.0*w_check), p0[1]-round(2.0/3.0*w_check))
        p4 = (p5[0]-round(t_check/math.sqrt(2)),
              p5[1]-round(t_check/math.sqrt(2)))

        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def minus(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 16
        l = 14*8

        p0 = (l/2+x0, -t/2+y0)
        p1 = (p0[0]-l, p0[1])
        p2 = (p1[0], p1[1]+t)
        p3 = (p2[0]+l, p2[1])

        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def plus(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 16
        l = round((14*8-t)/2)

        p0 = (t/2+x0, 0-t/2+y0)
        p1 = (p0[0], p0[1]-l)
        p2 = (p1[0]-t, p1[1])
        p3 = (p2[0], p1[1]+l)
        p4 = (p3[0]-l, p3[1])
        p5 = (p4[0], p4[1]+t)
        p6 = (p5[0]+l, p5[1])
        p7 = (p6[0], p6[1]+l)
        p8 = (p7[0]+t, p7[1])
        p9 = (p8[0], p8[1]-l)
        p10 = (p9[0]+l, p9[1])
        p11 = (p10[0], p10[1]-t)

        draw.polygon([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                     p11, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def cross(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 16
        l = round((S-t)/2)

        p0 = (round(t/math.sqrt(2))+x0, 0+y0)
        p3 = (0+x0, -round(t/math.sqrt(2))+y0)
        p6 = (-round(t/math.sqrt(2))+x0, 0+y0)
        p9 = (0+x0, +round(t/math.sqrt(2))+y0)

        lx = round(l*math.cos(math.radians(45)))
        ly = round(l*math.cos(math.radians(45)))

        p1 = (p0[0]+lx, p0[1]-ly)
        p2 = (p3[0]+lx, p3[1]-ly)
        p4 = (p3[0]-lx, p3[1]-ly)
        p5 = (p6[0]-lx, p6[1]-ly)
        p7 = (p6[0]-lx, p6[1]+ly)
        p8 = (p9[0]-lx, p9[1]+ly)
        p10 = (p9[0]+lx, p9[1]+ly)
        p11 = (p0[0]+lx, p0[1]+ly)

        draw.polygon([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                     p11, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def down(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        h_down = l1+l2

        p0 = (x0, round(h_down/2.0+y0))
        p1 = (p0[0]+l2, p0[1]-l2)
        p2 = (p1[0]-l1, p1[1]-l1)
        p3 = (p0[0], p0[1]-2*l1)
        p5 = (p0[0]-l2, p0[1]-l2)
        p4 = (p5[0]+l1, p5[1]-l1)

        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def go_down(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        h_down = l1+l2+t

        p0 = (x0, round(h_down/2.0-t+y0))
        p1 = (p0[0]+l2, p0[1]-l2)
        p2 = (p1[0]-l1, p1[1]-l1)
        p3 = (p0[0], p0[1]-2*l1)
        p5 = (p0[0]-l2, p0[1]-l2)
        p4 = (p5[0]+l1, p5[1]-l1)
        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        p0 = (l2+x0, round(h_down/2.0-t+y0))
        p1 = (p0[0]-2*l2, p0[1])
        p2 = (p1[0], p1[1]+t)
        p3 = (p0[0], p0[1]+t)
        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def up(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        h_up = l1+l2

        p0 = (x0, round(-h_up/2.0+y0))
        p1 = (p0[0]-l2, p0[1]+l2)
        p2 = (p1[0]+l1, p1[1]+l1)
        p3 = (p0[0], p0[1]+2*l1)
        p5 = (p0[0]+l2, p0[1]+l2)
        p4 = (p5[0]-l1, p5[1]+l1)
        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def go_up(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        h_up = l1+l2+t

        p0 = (x0, round(-h_up/2.0+t+y0))
        p1 = (p0[0]-l2, p0[1]+l2)
        p2 = (p1[0]+l1, p1[1]+l1)
        p3 = (p0[0], p0[1]+2*l1)
        p5 = (p0[0]+l2, p0[1]+l2)
        p4 = (p5[0]-l1, p5[1]+l1)
        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        p0 = (l2+x0, round(-h_up/2.0+y0))
        p1 = (p0[0]-2*l2, p0[1])
        p2 = (p1[0], p1[1]+t)
        p3 = (p0[0], p0[1]+t)
        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def right(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        w_left = l1+l2

        p0 = (round(w_left/2.0+x0), y0)
        p1 = (p0[0]-l2, p0[1]-l2)
        p2 = (p1[0]-l1, p1[1]+l1)
        p3 = (p0[0]-2*l1, p0[1])
        p5 = (p0[0]-l2, p0[1]+l2)
        p4 = (p5[0]-l1, p5[1]-l1)

        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def go_right(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        w_left = l1+l2+t

        p0 = (round(w_left/2.0-t+x0), y0)
        p1 = (p0[0]-l2, p0[1]-l2)
        p2 = (p1[0]-l1, p1[1]+l1)
        p3 = (p0[0]-2*l1, p0[1])
        p5 = (p0[0]-l2, p0[1]+l2)
        p4 = (p5[0]-l1, p5[1]-l1)
        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        p0 = (round(w_left/2.0+x0), y0-l2)
        p1 = (p0[0]-t, p0[1])
        p2 = (p1[0], p1[1]+2*l2)
        p3 = (p0[0], p0[1]+2*l2)
        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def left(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        w_right = l1+l2

        p0 = (round(-w_right/2.0+x0), y0)
        p1 = (p0[0]+l2, p0[1]+l2)
        p2 = (p1[0]+l1, p1[1]-l1)
        p3 = (p0[0]+2*l1, p0[1])
        p5 = (p0[0]+l2, p0[1]-l2)
        p4 = (p5[0]+l1, p5[1]+l1)

        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def go_left(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 2*8
        l1 = round(t/math.sqrt(2))
        l2 = 7*8
        w_left = l1+l2+t

        p0 = (round(-w_left/2.0+t+x0), y0)
        p1 = (p0[0]+l2, p0[1]+l2)
        p2 = (p1[0]+l1, p1[1]-l1)
        p3 = (p0[0]+2*l1, p0[1])
        p5 = (p0[0]+l2, p0[1]-l2)
        p4 = (p5[0]+l1, p5[1]+l1)
        draw.polygon([p0, p1, p2, p3, p4, p5, p0],
                     fill=fill, outline=border, width=5)

        p0 = (round(-w_left/2.0+t+x0), y0-l2)
        p1 = (p0[0]-t, p0[1])
        p2 = (p1[0], p1[1]+2*l2)
        p3 = (p0[0], p0[1]+2*l2)
        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def sync(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)

        margin_left = round(k*margin[0])
        margin_up = round(k*margin[1])

        if test:
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        draw.point([(x0, y0)])

        t = 12
        l1 = 4
        l3 = 3*8
        l2 = int(l3-t/2)

        draw.arc(
            [(margin_left+(l1+l2), margin_up+(l1+l2)),
             (margin_left+S-(l1+l2), margin_up+S-(l1+l2))],
            -90,
            45,
            fill="black",
            width=t,
        )

        draw.arc(
            [(margin_left+(l1+l2), margin_up+(l1+l2)),
             (margin_left+S-(l1+l2), margin_up+S-(l1+l2))],
            90,
            225,
            fill="black",
            width=t,
        )

        p0 = (0+x0, -S/2+l1+y0)
        p1 = (p0[0]-l3, p0[1]+l3)
        p2 = (p1[0]+l3, p1[1]+l3)
        draw.polygon([p0, p1, p2, p0], fill=fill, outline=border, width=5)

        p0 = (0+x0, S/2-l1+y0)
        p1 = (p0[0]+l3, p0[1]-l3)
        p2 = (p1[0]-l3, p1[1]-l3)
        draw.polygon([p0, p1, p2, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def play(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        l = 12*8
        p0 = (l/2+x0, 0+y0)
        p1 = (p0[0]-l, p0[1]-l/2)
        p2 = (p1[0], p1[1]+l)

        draw.polygon([p0, p1, p2, p0], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def pause(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        ly = 12*8
        lx0 = 2*8
        lx1 = 5*8

        p0 = (lx0/2+lx1+x0, -ly/2+y0)
        p1 = (p0[0]-lx1, p0[1])
        p2 = (p1[0], p1[1]+ly)
        p3 = (p2[0]+lx1, p2[1])

        p4 = (p0[0]-lx1-lx0, p0[1])
        p5 = (p1[0]-lx1-lx0, p1[1])
        p6 = (p2[0]-lx1-lx0, p2[1])
        p7 = (p3[0]-lx1-lx0, p3[1])

        draw.polygon([p0, p1, p2, p3, p0], fill=fill, outline=border, width=5)

        draw.polygon([p4, p5, p6, p7, p4], fill=fill, outline=border, width=5)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def question(self, size=16, margin=(0, 0, 0, 0), border="black", fill="black", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle(
                [margin_left, margin_up, margin_left+S, margin_up+S], fill="white")

        t = 16
        p0 = (-t/2+x0, 7*8+y0)
        p1 = (p0[0]+t, p0[1])
        p2 = (p1[0], p1[1]-t)
        p3 = (p0[0], p2[1])

        p4 = (p0[0], p3[1]-t)
        p5 = (p4[0]+t, p4[1])
        p6 = (p5[0], p5[1]-t)
        # p7 = (p6[0]+1.5*t, p6[1]-2*t)
        p7 = (p6[0]+2*t, p6[1]-1.5*t)
        p8 = (p7[0]-t, p7[1])
        p9 = (p4[0], p6[1])
        p10 = (x0-2.5*t, p7[1]-2.5*t)
        p11 = (p7[0], p7[1]+2.5*t)

        draw.polygon([p0, p1, p2, p3, p0],
                     fill=fill, outline=border, width=5)
        draw.polygon([p4, p5, p6, p7, p8, p9, p4],
                     fill=fill, outline=border, width=5)
        draw.arc([p10, p11], 180, 0,
                 fill=fill, width=t)

        image = image.resize((w, h), Image.LANCZOS)
        return image

    def circle(self, checked=False, size=16, margin=(0, 0, 0, 0),
               border="black", fill="white", test=False):
        S = 128
        w = size+(margin[0]+margin[2])
        h = size+(margin[1]+margin[3])
        k = S/size
        W = round(S+k*(margin[0]+margin[2]))
        H = round(S+k*(margin[1]+margin[3]))
        x0 = round(k*margin[0]+S/2)
        y0 = round(k*margin[1]+S/2)

        image = Image.new("RGBA", (W, H))
        draw = ImageDraw.Draw(image)
        if test:
            margin_left = round(k*margin[0])
            margin_up = round(k*margin[1])
            draw.rectangle([0, 0, W, H], fill="gold")
            draw.rectangle([margin_left, margin_up, margin_left+S, margin_up+S],
                           fill="white")

        r = 7*8
        draw.circle(
            [0+x0, 0+y0],
            radius=r,
            fill=fill,
            outline=border,
            width=4,
        )

        image = image.resize((w, h), Image.LANCZOS)
        return image


if __name__ == '__main__':

    root = tk.Tk()
    root.title('Icon generator test')

    style = ttk.Style()
    style.theme_use('clam')

    iconGenerator = IconGenerator()

    sync = iconGenerator.sync(size=128, margin=(5, 5, 5, 5))
    sync.save('sync-generated-icon.png', 'png')

    img01 = ImageTk.PhotoImage(iconGenerator.rectangle_check(
        size=32, margin=(5, 5, 5, 5), checked=True, check="green", test=True))
    img01c = ImageTk.PhotoImage(iconGenerator.rectangle_check(size=32, margin=(
        5, 5, 5, 5), checked=True, checktype='check', check="green", test=True))

    img02 = ImageTk.PhotoImage(iconGenerator.circular_check(size=32, margin=(
        5, 5, 5, 5), checked=True, checktype='circle', check="green", test=True))
    img02c = ImageTk.PhotoImage(iconGenerator.circular_check(size=32, margin=(
        5, 5, 5, 5), checked=True, checktype='check', check="green", test=True))

    img03 = ImageTk.PhotoImage(iconGenerator.check(
        size=32, margin=(5, 5, 5, 5), test=True))
    img04 = ImageTk.PhotoImage(iconGenerator.plus(
        size=32, margin=(5, 5, 5, 5), test=True))
    img05 = ImageTk.PhotoImage(iconGenerator.minus(
        size=32, margin=(5, 5, 5, 5), test=True))
    img06 = ImageTk.PhotoImage(iconGenerator.cross(
        size=32, margin=(5, 5, 5, 5), test=True))

    img07 = ImageTk.PhotoImage(iconGenerator.down(
        size=32, margin=(5, 5, 5, 5), test=True))
    img08 = ImageTk.PhotoImage(iconGenerator.up(
        size=32, margin=(5, 5, 5, 5), test=True))

    img09 = ImageTk.PhotoImage(iconGenerator.left(
        size=32, margin=(5, 5, 5, 5), test=True))
    img10 = ImageTk.PhotoImage(iconGenerator.right(
        size=32, margin=(5, 5, 5, 5), test=True))

    img11 = ImageTk.PhotoImage(iconGenerator.go_down(
        size=32, margin=(5, 5, 5, 5), test=True))
    img12 = ImageTk.PhotoImage(iconGenerator.go_up(
        size=32, margin=(5, 5, 5, 5), test=True))

    img13 = ImageTk.PhotoImage(iconGenerator.go_left(
        size=32, margin=(5, 5, 5, 5), test=True))
    img14 = ImageTk.PhotoImage(iconGenerator.go_right(
        size=32, margin=(5, 5, 5, 5), test=True))

    img15 = ImageTk.PhotoImage(iconGenerator.sync(
        size=32, margin=(5, 5, 5, 5), test=True))

    img16 = ImageTk.PhotoImage(iconGenerator.play(
        size=32, margin=(5, 5, 5, 5), test=True))
    img17 = ImageTk.PhotoImage(iconGenerator.pause(
        size=32, margin=(5, 5, 5, 5), test=True))

    img18 = ImageTk.PhotoImage(iconGenerator.question(
        size=32, margin=(5, 5, 5, 5), test=True))

    img19 = ImageTk.PhotoImage(iconGenerator.circle(
        size=32, margin=(5, 5, 5, 5), border="gold", fill="blue", test=True))

    labelImg01 = ttk.Label(root, compound="right", image=img01,
                           text="Checkbox", font=("Helvetica", 14))
    labelImg01c = ttk.Label(root, compound="image", image=img01c)

    labelImg02 = ttk.Label(root, compound="image", image=img02)
    labelImg02c = ttk.Label(root, compound="image", image=img02c)
    labelImg03 = ttk.Label(root, compound="image", image=img03)
    labelImg04 = ttk.Label(root, compound="image", image=img04)
    labelImg05 = ttk.Label(root, compound="image", image=img05)
    labelImg06 = ttk.Label(root, compound="image", image=img06)
    labelImg07 = ttk.Label(root, compound="image", image=img07)
    labelImg08 = ttk.Label(root, compound="image", image=img08)
    labelImg09 = ttk.Label(root, compound="image", image=img09)
    labelImg10 = ttk.Label(root, compound="image", image=img10)
    labelImg11 = ttk.Label(root, compound="image", image=img11)
    labelImg12 = ttk.Label(root, compound="image", image=img12)
    labelImg13 = ttk.Label(root, compound="image", image=img13)
    labelImg14 = ttk.Label(root, compound="image", image=img14)
    labelImg15 = ttk.Label(root, compound="image", image=img15)

    labelImg16 = ttk.Label(root, compound="image", image=img16)

    labelImg17 = ttk.Label(root, compound="image", image=img17)

    labelImg18 = ttk.Label(root, compound="image", image=img18)
    labelImg19 = ttk.Label(root, compound="image", image=img19)

    labelImg01.grid(row=0, column=0, sticky=tk.E)
    labelImg01c.grid(row=0, column=1, sticky=tk.W)
    labelImg02.grid(row=1, column=0, sticky=tk.E)
    labelImg02c.grid(row=1, column=1, sticky=tk.W)
    labelImg03.grid(row=2, column=0, sticky=tk.E)
    labelImg04.grid(row=3, column=1, sticky=tk.W)
    labelImg05.grid(row=3, column=0, sticky=tk.E)
    labelImg06.grid(row=2, column=1, sticky=tk.W)
    labelImg07.grid(row=4, column=0, sticky=tk.E)
    labelImg08.grid(row=4, column=1, sticky=tk.W)

    labelImg09.grid(row=5, column=0, sticky=tk.E)
    labelImg10.grid(row=5, column=1, sticky=tk.W)

    labelImg11.grid(row=6, column=0, sticky=tk.E)
    labelImg12.grid(row=6, column=1, sticky=tk.W)

    labelImg13.grid(row=7, column=0, sticky=tk.E)
    labelImg14.grid(row=7, column=1, sticky=tk.W)

    labelImg15.grid(row=8, column=0, sticky=tk.E)

    labelImg16.grid(row=9, column=0, sticky=tk.E)

    labelImg17.grid(row=9, column=1, sticky=tk.W)

    labelImg18.grid(row=10, column=0, sticky=tk.E)
    labelImg19.grid(row=10, column=1, sticky=tk.W)

    root.columnconfigure(0, minsize=256)
    root.columnconfigure(1, minsize=256)

    root.mainloop()
