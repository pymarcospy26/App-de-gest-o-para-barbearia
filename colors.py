import flet as ft

branco = '#FFFFFF'
background = '#F8F8FC'
textos = '#171717'
sub_textos = '#878787'
bordas = '#E9E7EE'
inputs = '#F3F1F5'
verde = '#22B77A'
verde_fundo = "#C8FFE8"
vermelho = '#E23D3D'
amarelo = '#E0A94A'
selecao = "#E6AFFF"
cinza_claro = "#f9f9f9"
cinza_fundo = '#e5e5e5'
lilas_calmo = '#b39ef5'
cinza_gelo = "#A6ABB6"
preto_icons = '#4f4f4f'
preto_icons1 = '#6f6f6f'
sombra = '#D8D8F8'

lilas = "#9F84FF"
azul_violeta = '#8B6CFB'
laranja = '#FFB47D'
rosa = '#FF8FA3'

gradiente_botoes = [lilas, azul_violeta]

borda_erro_0 = '#5c0000'
borda_erro_1 = '#F94449'

gradiente_banner = [lilas, azul_violeta]

def gradiente_top_bottom(colors):
    return ft.LinearGradient(
        begin = ft.Alignment.TOP_LEFT,
        end = ft.Alignment.BOTTOM_RIGHT,
        colors = colors,
    )

def gradiente_linear_normal(colors):
    return ft.LinearGradient(
        begin = ft.Alignment.TOP_CENTER,
        end = ft.Alignment.BOTTOM_CENTER,
        colors = colors,
    )

def gradiente_circular():
    return ft.RadialGradient(
        radius = 10,
        colors = [lilas, lilas_calmo],
        # stops = [0, 0.5, 1]
    )

def shadow_leve(x = 0, y = 4, blr = 6, opc = 0.2):
    return ft.BoxShadow(
        blur_radius = blr,
        offset = ft.Offset(x, y),
        color = ft.Colors.with_opacity(color = sombra, opacity = opc)
    )