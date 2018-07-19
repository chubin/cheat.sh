"""
Colorize internal cheat sheets.
Will be merged with panela later.
"""

import re

from colorama import Fore, Back, Style
import colored

PALETTES = {
    0: {
        1: Fore.WHITE,
        2: Style.DIM,
    },
    1: {
        1: Fore.CYAN,
        2: Fore.GREEN,
        3: colored.fg('orange_3'),
        4: Style.DIM,
        5: Style.DIM,
    },
    2: {
        1: Fore.RED,
        2: Style.DIM,
    },
}



def _reverse_palette(code):
    return {
        1 : Fore.BLACK + _back_color(code),
        2 : Style.DIM 
    } 

def _back_color(code):
    if code == 0 or code.lower()=="white":
        return Back.WHITE
    if code == 1 or code.lower()=="cyan":
        return Back.WHITE
    if code == 2 or code.lower()=="red":
        return Back.WHITE

def colorize_internal(text, palette_number=1):
    """
    Colorize `text`, use `palette`
    """

    palette = PALETTES[palette_number]
    palette_reverse = _reverse_palette(palette_number)

    def _colorize_curlies_block(text):

        text = text.group()[1:-1]
        factor = 1
        if text.startswith('-'):
            text = text[1:]
            factor = -1
        stripped = text.lstrip('0123456789')
        color_number = int(text[:len(text)-len(stripped)])*factor
        if stripped.startswith('='):
            stripped = stripped[1:]

        reverse = (color_number < 0)
        if reverse:
            color_number = -color_number

        if reverse:
            stripped = palette_reverse[color_number] + stripped + Style.RESET_ALL
        else:
            stripped = palette[color_number] + stripped + Style.RESET_ALL

        return stripped

    def _colorize_headers(text):
        if text.group(0).endswith('\n'):
            newline = '\n'
        else:
            newline = ''

        color_number = 3
        return palette[color_number] + text.group(0).strip() + Style.RESET_ALL + newline

    text = re.sub("{.*?}", _colorize_curlies_block, text)
    text = re.sub("#(.*?)\n", _colorize_headers, text)
    return text
