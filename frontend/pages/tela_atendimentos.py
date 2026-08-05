import flet as ft
import icons as ic
import colors as c
import variaveis_globais as vg

from backend import fluxo_telas as fx
from backend import estado_do_atendimento as cofre
from frontend.widgets_globais import inputs as wd

class Tela_Atendimento:
    def __init__(self, page: ft.Page):
        self.page = page

        self.widgets()

    def limpar_dados_atendimento(self):
        cofre.servicos_atendimento.clear()
        cofre.totais = 0

    async def mudar_page(self, e):
        self.limpar_dados_atendimento()
        anterior = fx.tela_atual

        await fx.mudar_page(
            self.page, atual = self, nova = await anterior.tela()
        )

    def atualizar_sugestoes(self, e):
        self.pesquisa_completa.height = 290
        self.pesquisa_completa.controls[0].bottom = 0
        self.pesquisa_completa.controls[0].height = 200

        self.pesquisa_completa.controls[0].content.controls.extend([
            ft.Text(value = 'Opcao', size = 14, color = c.preto_icons, expand = True),
            ft.Text(value = 'Opcao', size = 14, color = c.preto_icons, expand = True),
            ft.Text(value = 'Opcao', size = 14, color = c.preto_icons, expand = True),
        ])

        self.pesquisa_completa.update()

    def widgets(self):
        self.btn_exit = ft.Container(
            width = 74,
            height = 74,
            border_radius = 28,

            margin = ft.Margin(
                top = vg.margin_top,
                left = vg.margin_left,
            ),

            bgcolor = c.branco,
            shadow = c.shadow_leve(),
            alignment = ft.Alignment.CENTER,

            content = ic.svg_icon(
                'seta_exit',
                size = 30, color = c.preto_icons,
            ),

            on_click = self.mudar_page,
        )

        self.barra_peesquisa = ft.Column(
            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment = ft.CrossAxisAlignment.START,

            controls = [
                ft.Container(
                    height = 74,
                    border_radius = 34,
                    bgcolor = c.branco,
                    shadow = c.shadow_leve(),

                    alignment = ft.Alignment.CENTER,
                    margin = ft.Margin(
                        top = 2,
                        left = vg.margin_left,
                        right = vg.margin_right,
                    ),

                    on_click = self.atualizar_sugestoes,

                    content = ft.Stack(
                        height = 74,
                        alignment = ft.Alignment.CENTER,

                        controls = [
                            ft.TextField(
                                top = 0,
                                left = 0,
                                right = 0,
                                bottom = 0,
                                bgcolor = c.verde,
                                content_padding = 34,
                                border_color = ft.Colors.TRANSPARENT,

                                text_style = ft.TextStyle(
                                    size = 16, color = c.preto_icons,
                                    font_family = 'inter'
                                )
                            ),

                            ft.Container(
                                right = 0,
                                width = 58,
                                height = 58,
                                border_radius = 26,
                                bgcolor = c.azul_violeta,
                                alignment = ft.Alignment.CENTER,

                                content = ic.svg_icon(
                                    'lupa',
                                    size = 30, color = c.branco
                                ),

                                margin = ft.Margin(right = (74 - 58) / 2)
                            ),
                        ]
                    )
                )
            ]
        )

        self.sugestao = ft.Container(
            height = 0,
            width = self.page.width - (16 * 2),
            bgcolor = c.branco,
            border_radius = 34,
            shadow = c.shadow_leve(),
            alignment = ft.Alignment.CENTER,
            margin = ft.Margin(left = vg.margin_left, right = vg.margin_right),

            content = ft.Column(
                spacing = 0,
                alignment = ft.MainAxisAlignment.CENTER,
                horizontal_alignment = ft.CrossAxisAlignment.START,
            )
        )

        self.pesquisa_completa = ft.Stack(
            height = 74,

            controls = [
                self.sugestao,
                self.barra_peesquisa,
            ]
        )

    async def add(self):
        self.estrutura = ft.Column(
            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment = ft.CrossAxisAlignment.START,

            controls = [
                self.btn_exit,

                ft.Text(
                    value = 'Atendimento',
                    size = 24, color = c.preto_icons,
                    margin = ft.Margin(left = vg.margin_left, top = vg.margin_top + 6)
                ),

                self.pesquisa_completa,

                await wd.dropdown(
                    page = self.page,
                    titulo = 'Selecione os servicos',
                    hint_text = 'Toque para selcionar servicos',
                    margin = ft.Margin(left = vg.margin_left, right = vg.margin_right)
                )
            ]
        )

        return self.estrutura
