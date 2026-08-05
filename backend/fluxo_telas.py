import flet as ft

tela_anterior = None
tela_atual = None
tela_nova = None

tela_reserva1 = None
tela_reserva2 = None
tela_reserva3 = None

async def mudar_page(
    page: ft.Page,
    anterior = None, atual = None, nova = None,
    reserva1 = None, reserva2 = None, reserva3 = None
):
    global tela_anterior, tela_atual, tela_nova
    global tela_reserva1, tela_reserva2, tela_reserva3

    tela_anterior = anterior
    tela_atual = atual
    tela_nova = nova

    tela_reserva1 = reserva1
    tela_reserva2 = reserva2
    tela_reserva3 = reserva3
    
    if tela_atual is not None and tela_nova is not None:
        page.controls[0].content = tela_nova
        page.update()

    else:
        print('Falta uma tela ai man')