#!/usr/bin/python2
# -*- coding: utf-8 -*-

from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1994
from colormath.color_objects import LabColor, AdobeRGBColor
from flask import Flask

import model

app = Flask(__name__)

ORANGE = convert_color(AdobeRGBColor(rgb_r=255, rgb_g=165, rgb_b=0), LabColor)

CLOSE_ENOUGH = 1000.0


def uint24_to_rgb(uint):
    return (uint >> 16) & 255, (uint >> 8) & 255, uint & 255


def rgb_to_web(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


@app.route('/')
def distance_from_orange():
    colors = model.colors()

    out = '<table style="border-collapse: collapse;">'

    for vid, clist in colors:
        rgbs = [uint24_to_rgb(int(x)) for x in clist.split(',')]

        for c in rgbs:
            c_lab = convert_color(AdobeRGBColor(*c), LabColor)
            delta = delta_e_cie1994(ORANGE, c_lab)
            color_hex = rgb_to_web(*c)

            if delta < CLOSE_ENOUGH:
                match = '&#11013;'
            else:
                match = ''

            out += """
                <tr style="border: solid 1px;">
                    <td width="100" align="center">{0:d}</td>
                    <td width="100" height="100" align="center" style="background: {1}">{1}</td>
                    <td width="100" align="center" style="font-size: 5em">{2}</td>
                    <td width="100" align="center">{3}</td>
                </tr>
            """.format(vid, color_hex, match, int(delta))

    out += '</table>'

    return out


if __name__ == '__main__':
    app.run(use_debugger=False, debug=True, use_reloader=True, host='0.0.0.0')
