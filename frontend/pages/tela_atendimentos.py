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

        self.cliente_servico_ROW = ft.ResponsiveRow(
            columns = 2,
            spacing = 0,
            run_spacing = 0,
            alignment = ft.MainAxisAlignment.START,
            vertical_alignment = ft.CrossAxisAlignment.CENTER
        )

        self.box_resumo = ft.Container(
            height = 260,
            expand = True,
            bgcolor = c.branco,
            border_radius = 34,
            shadow = c.shadow_leve(),
            margin = ft.Margin(left = vg.margin_left, right = vg.margin_right, top = vg.margin_top),

            content = ft.Column(
                spacing = 0,
                expand = True,
                alignment = ft.MainAxisAlignment.START,
                horizontal_alignment = ft.CrossAxisAlignment.START,

                controls = [
                    ft.Text(
                        value = 'Resumo',
                        size = 20, color = c.preto_icons,
                        font_family = 'inter',
                        margin = ft.Margin(left = 24, top = 24)
                    ),

                    ft.Column(
                        spacing = 0,
                        expand = True,
                        alignment = ft.MainAxisAlignment.START,
                        horizontal_alignment = ft.CrossAxisAlignment.START,

                        controls = []
                    )
                ]
            )
        )

    def radioButton_pagamaneto(
        self,
        titulo = 'Vazio',
        icon = 'circulo_alerta',
        option_icon: str = 'svg',
        top: int = 6, left: int = 0, right: int = 0,
    ):
        radio = ft.Container(
            width = 32,
            height = 32,
            bgcolor = c.branco,
            border_radius = 32 / 2,
            margin = ft.Margin(left = 14, top = 14),
            border = ft.Border.all(width = 2, color = c.bordas),
        )

        return ft.Container(
            bgcolor = c.branco,
            border_radius = 34,
            shadow = c.shadow_leve(),
            margin = ft.Margin(top = top, left = left, right = right),

            width = (self.page.width - (4 * 16)) / 3,

            data = {
                'radio': radio,
            },

            content = ft.Column(
                alignment = ft.MainAxisAlignment.START,
                horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.Row(
                        margin = ft.Margin(bottom = 10),
                        alignment = ft.MainAxisAlignment.START,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER,
                        controls = [
                            radio
                        ]
                    ),

                    ic.svg_icon(
                        path = icon,
                        size = 30, color = c.sub_textos
                    )

                    if option_icon == 'svg' else

                    ft.Icon(
                        icon = icon,
                        size = 30, color = c.sub_textos
                    ),

                    ft.Text(
                        value = titulo,
                        size = 16, color = c.sub_textos,
                        font_family = 'inter',
                        margin = ft.Margin(bottom = 54)
                    )
                ]
            )
        )

    async def add(self):
        self.cliente_servico_ROW.controls.extend([
            await wd.dropdown(
                page = self.page,
                text_interno = 'Cliente',
                icon = ic.svg_icon(
                    'user',
                    size = 25, color = c.sub_textos
                ),

                icon_status = 'triangulo_alerta',
                cor_tatus = c.vermelho,
                
                margin = ft.Margin(top = 6, left = vg.margin_left, right = vg.margin_right / 2)
            ),

            await wd.dropdown(
                page = self.page,
                text_interno = 'Serviços',
                icon = ft.Icon(
                    icon = ft.CupertinoIcons.SCISSORS_ALT,
                    size = 25, color = c.sub_textos
                ),

                icon_status = 'check',
                cor_tatus = c.verde,

                margin = ft.Margin(top = 6, left = vg.margin_left / 2, right = vg.margin_right)
            ),
        ])

        self.estrutura = ft.Column(
            expand = True,
            scroll = ft.ScrollMode.AUTO,
            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment = ft.CrossAxisAlignment.START,

            controls = [
                self.btn_exit,

                ft.Text(
                    value = 'Atendimento',
                    size = 24, color = c.preto_icons,
                    margin = ft.Margin(left = vg.margin_left, top = vg.margin_top + 6)
                ),

                self.cliente_servico_ROW,
                ft.Row([self.box_resumo], expand = True),

                # ft.Text(
                #     value = 'Pagamento',
                #     size = 24, color = c.preto_icons,
                #     margin = ft.Margin(left = vg.margin_left, top = vg.margin_top + 6)
                # ),

                ft.Row(
                    spacing = 16,
                    expand = True,
                    alignment = ft.MainAxisAlignment.CENTER,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,

                    controls = [
                        self.radioButton_pagamaneto(
                            titulo = 'Dinheiro',
                            icon = 'dinheiro',
                            left = vg.margin_left,
                        ),

                        self.radioButton_pagamaneto(
                            titulo = 'Pix',
                            option_icon = 'Icon',
                            icon = ft.Icons.PIX_OUTLINED,
                        ),

                        self.radioButton_pagamaneto(
                            titulo = 'Cartão',
                            icon = 'cartao',
                            right = vg.margin_right
                        ),
                    ]
                )
            ]
        )

        return self.estrutura
