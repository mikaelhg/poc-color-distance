#!/usr/bin/python2
# -*- coding: utf-8 -*-

from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976, delta_e_cie1994, delta_e_cie2000
from colormath.color_objects import LabColor, AdobeRGBColor, sRGBColor
from flask import Flask

import model

app = Flask(__name__)

ORANGE = (255, 165, 0)

CLOSE_ENOUGH = 30.0


def uint24_to_rgb(uint):
    return (uint >> 16) & 255, (uint >> 8) & 255, uint & 255


def rgb_to_web(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


def calc_delta(rgb1=(0, 0, 0), rgb2=(0, 0, 0), algo=delta_e_cie2000):
    lab1 = convert_color(sRGBColor(*rgb1, is_upscaled=True), LabColor)
    lab2 = convert_color(sRGBColor(*rgb2, is_upscaled=True), LabColor)
    return algo(lab1, lab2)


@app.route('/')
def distance_from_orange():
    colors = model.colors()

    out = '<table style="border-collapse: collapse;">'

    out += """
            <tr style="border: solid 1px;">
                <td width="100" align="center">{0}</td>
                <td width="100" height="100" align="center" style="background: {1}">{1}</td>
                <td width="100" align="center" style="font-size: 5em">{2}</td>
                <td width="100" align="center">{3}</td>
                <td width="100" align="center">{4}</td>
                <td width="100" align="center">{5}</td>
            </tr>
    """.format('reference orange', rgb_to_web(*ORANGE), '', 'CIE 2000', 'CIE 1994', 'CIE 1976')

    for visitor_id, colorlist in colors:
        rgbs = [uint24_to_rgb(int(x)) for x in colorlist.split(',')]

        for (r, g, b) in rgbs:
            delta = calc_delta(ORANGE, (r, g, b), delta_e_cie2000)

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
                    <td width="100" align="center">{4}</td>
                    <td width="100" align="center">{5}</td>
                </tr>
            """.format(visitor_id, rgb_to_web(r, g, b), match,
                       int(delta),
                       int(calc_delta(ORANGE, (r, g, b), delta_e_cie1994)),
                       int(calc_delta(ORANGE, (r, g, b), delta_e_cie1976)))

    out += '</table>'

    return out


if __name__ == '__main__':
    app.run(use_debugger=False, debug=True, use_reloader=True, host='0.0.0.0')
