import flet as ft
from tela_atual import ativar_tela

tela_atual = None
proxima_tela = None
tela_anterior = None

tela_reserva1 = None
tela_reserva2 = None
tela_reserva3 = None

tela_login = None
tela_home = None

def mudanca_tela(
    page: ft.Page,
    atual = None, proxima = None, anterior = None,
    reserva_1 = None, reserva_2 = None, reserva_3 = None,
    login = None, home = None
):

    global tela_atual, proxima_tela, tela_anterior
    global tela_reserva1, tela_reserva2, tela_reserva3
    global tela_ativa_in_page, tela_login, tela_home

    tela_atual = atual
    proxima_tela = proxima
    tela_anterior = anterior

    tela_reserva1 = reserva_1
    tela_reserva2 = reserva_2
    tela_reserva3 = reserva_3

    tela_login = login
    tela_home = home

    ativar_tela.content = proxima_tela
    page.page.update()