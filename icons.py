import flet as ft
from pathlib import Path

LOCAL = Path(__file__).parent

def svg_icon(path, size = 90, color = '#ff0000', left = None, right = None, bottom = None, top = None):
    path_mod = LOCAL / 'assets' / 'icons' / f'{path}.svg'

    svg = open(path_mod, 'r', encoding = 'utf-8').read()

    svg = svg.replace('currentColor', color)
    svg = svg.replace('width = 24', '')
    svg = svg.replace('height = 24', '')
    svg = svg.replace('width="24"', '')
    svg = svg.replace('height="24"', '')

    return ft.Image(
        src = f'data:image/svg+xml;utf-8,{svg}',
        width = size,
        height = size,
        left = left,
        right = right,
        top = top,
        bottom = bottom
    )