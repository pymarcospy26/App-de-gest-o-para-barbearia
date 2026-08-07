import flet as ft
import colors as c
import icons as ic
import variaveis_globais as vg
from frontend.widgets_globais import alert_dialogs as diag
from backend import fluxo_telas as fx

class Tela_Home:
    def __init__(self, page: ft.Page):
        self.page = page
        self.agendamentos = {
            'João Guilherme': {
                'hora': '10:40',
                'setor': 'Estética',
                'servico': 'Design de Sobrancelha',
                'cor_urgencia': c.vermelho
            },

            'Maria Eduarda': {
                'hora': '13:20',
                'setor': 'Barbearia',
                'servico': 'Hidratação Capilar',
                'cor_urgencia': c.laranja
            },

            'Ana Carolina': {
                'hora': '16:15',
                'setor': 'Estética',
                'servico': 'Drenagem Linfática',
                'cor_urgencia': c.lilas
            }
        }

        self.acesso_rapido = ['Retirada', 'Fiados', 'Angendar']

    async def abrir_atendimento(self, e):
        alert_dialog = diag.AlertDialog_atendimento(self.page)
        await alert_dialog.inicializar()

        alert_dialog.abrir(e)

    async def tela(self):
        self.botao_configuracao = ft.Container(
            width = 74,
            height = 74,
            bgcolor = c.branco,
            border_radius = 28,
            shadow = c.shadow_leve(),
            margin = ft.Margin(left = vg.margin_left, top = vg.margin_top),

            alignment = ft.Alignment.CENTER,

            content = ic.svg_icon('configuracao', size = 30, color = c.preto_icons)
        )

        self.banner = ft.Container(
            height = 300,
            expand = True,
            border_radius = 34,
            # bgcolor = c.lilas,
            margin = ft.Margin(left = vg.margin_left, top = vg.margin_top, right = vg.margin_right),

            gradient = c.gradiente_top_bottom(c.gradiente_banner),
        )

        self.ferramentas = ft.ResponsiveRow(
            spacing = 0,
            columns = 3,
            expand = True,
            run_spacing = 0,
            
            alignment = ft.MainAxisAlignment.START,
            vertical_alignment = ft.CrossAxisAlignment.START,

            controls = []
        )

        def btns_ferramentas(titulo, icon, r = 0, l = 0, t = 0, b = 0, col = 1):
            self.ferramentas.controls.append(
                ft.Container(
                    col = col,
                    height = 140,
                    bgcolor = c.branco,
                    border_radius = 34,
                    margin = ft.Margin(left = l, right = r, top = t, bottom = b),

                    shadow = c.shadow_leve(),

                    alignment = ft.Alignment.CENTER,
                    
                    content = ft.Column(
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,

                        controls = [
                            ic.svg_icon(
                                icon,
                                size = 30,
                                color = c.lilas
                            ),
                            
                            ft.Text(
                                value = titulo,
                                size = 16, color = c.preto_icons,
                                font_family = 'inter', text_align = ft.TextAlign.CENTER
                            )
                        ]
                    )
                )
            )

        btns_ferramentas(self.acesso_rapido[0], 'retirada_caixa', l = vg.margin_left, r = vg.margin_right / 2, t = vg.margin_top, col = 1)
        btns_ferramentas(self.acesso_rapido[1], 'fiados', l = vg.margin_left / 2, r = vg.margin_right / 2, t = vg.margin_top, col = 1)
        btns_ferramentas(self.acesso_rapido[2], 'calendar_add', l = vg.margin_left / 2, r = vg.margin_right, t = vg.margin_top, col = 1)

        self.agendados_prox = ft.Column(
            spacing = 0,

            alignment = ft.MainAxisAlignment.START,
            horizontal_alignment = ft.CrossAxisAlignment.START,

            controls = [
                ft.Text(
                    value = 'Clientes agendados',
                    size = 20, color = c.preto_icons,
                    font_family = 'inter', margin = ft.Margin(
                        left = vg.margin_left, top = vg.margin_top, bottom = vg.margin_top / 2
                    )
                ),

                ft.ResponsiveRow(
                    columns = 2,
                    spacing = 0,
                    run_spacing = 16,

                    alignment = ft.MainAxisAlignment.START,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER
                )
            ]
        )

        cont = 0

        for cliente in self.agendamentos:
            if cont == 3:
                break

            else:
                cont += 1

            self.agendados_prox.controls[1].controls.append(
                ft.Container(
                    col = 1,
                    padding = ft.Padding(left = 26, top = 26, right = 26,  bottom = 20),
                    bgcolor = c.branco,
                    border_radius = 34,
                    margin = ft.Margin(
                        left = vg.margin_left / 2 if cont % 2 == 0 else vg.margin_left,
                        right = vg.margin_right /2 if cont % 2 != 0 else vg.margin_right,
                    ),

                    shadow = c.shadow_leve(),

                    alignment = ft.Alignment.CENTER,

                    content = ft.Column(
                        spacing = 0,
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment = ft.CrossAxisAlignment.START,

                        controls = [
                            ft.Row(
                                spacing = 0,
                                alignment = ft.MainAxisAlignment.START,
                                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                                controls = [
                                    ft.Container(
                                        width = 10,
                                        height = 10,
                                        border_radius = 5,
                                        margin = ft.Margin(right = 10),
                                        bgcolor = self.agendamentos[cliente]['cor_urgencia'],
                                    ),

                                    ft.Text(
                                        value = 'Em breve',
                                        size = 14, color = self.agendamentos[cliente]['cor_urgencia'],
                                        font_family = 'inter'
                                    ),

                                    
                                ]
                            ),

                            ft.Text(
                                value = self.agendamentos[cliente]['hora'],
                                size = 28, color = c.preto_icons,
                                font_family = 'inter', weight = ft.FontWeight.W_400,
                                margin = ft.Margin(top = 14),
                            ),

                            ft.Text(
                                expand = True,
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                margin = ft.Margin(top = 14),
                                value = f'{cliente}\n',
                                style = ft.TextStyle(
                                    size = 18, color = c.preto_icons,
                                    font_family = 'inter', weight = ft.FontWeight.W_500
                                ),
                            ),
 
                            ft.Text(
                                expand = True,
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                margin = ft.Margin(top = 6),
                                value = f'{self.agendamentos[cliente]['servico']}\n',
                                style = ft.TextStyle(
                                    size = 14, color = c.sub_textos,
                                    font_family = 'inter', weight = ft.FontWeight.W_300
                                ),
                            ),
 
                            ft.Text(
                                expand = True,
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                                margin = ft.Margin(top = 6, bottom = 18),
                                value = f'{self.agendamentos[cliente]['setor']}\n',
                                style = ft.TextStyle(
                                    size = 14, color = c.sub_textos,
                                    font_family = 'inter', weight = ft.FontWeight.W_300
                                ),
                            ),

                            ft.Stack(
                                width = 86,
                                height = 60,
                                margin = ft.Margin(right = 5),
                                alignment = ft.Alignment.CENTER,

                                controls = [
                                    ft.Container(
                                        left = 0,
                                        width = 45,
                                        height  = 45,
                                        border_radius = 45 / 2,
                                        bgcolor = c.cinza_fundo,
                                        alignment = ft.Alignment.CENTER,
            
                                        content = ic.svg_icon(
                                            'telefone',
                                            size = 25, color = c.sub_textos,
                                        )
                                    ),

                                    ft.Container(
                                        right = 0,
                                        padding = 3,
                                        border_radius = (45 + 3) / 2,
                                        bgcolor = c.branco,

                                        content = ft.Container(
                                            width = 45,
                                            height  = 45,
                                            border_radius = 45 / 2,
                                            bgcolor = c.verde_fundo,
                                            alignment = ft.Alignment.CENTER,
                                                            
                                            content = ic.svg_icon(
                                                'whatsapp_icon',
                                                size = 25, color = c.verde,
                                            )
                                        )
                                    ),
                                ]
                            )
                        ]
                    )
                )
            )

        self.button_bar_center = ft.Container(
            width = 90,
            height = 90,
            border_radius = 45,
            margin = ft.Margin(top = 20, bottom = 20),

            gradient = c.gradiente_top_bottom(c.gradiente_banner),

            shadow = ft.BoxShadow(
                blur_radius = 10,
                offset = ft.Offset(0, 4),
                color = ft.Colors.with_opacity(color = c.azul_violeta, opacity = 0.4)
            ),

            alignment = ft.Alignment.CENTER,

            content = ft.Icon(
                icon = ft.CupertinoIcons.SCISSORS_ALT,
                size = 35, color = c.branco
            ),

            ink = True,
            on_click = self.abrir_atendimento
        )

        self.control_bar = ft.Container(
            left = 0,
            right = 0,
            bottom = 0,

            bgcolor = c.branco,

            shadow = c.shadow_leve(0, -4),

            content = ft.Row(
                alignment = ft.MainAxisAlignment.SPACE_EVENLY,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,

                controls = [
                    ft.Column(
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        
                        controls = [
                            ic.svg_icon('home', size = 28, color = c.azul_violeta),
                            ft.Text(value = 'Home', size = 14, color = c.azul_violeta, font_family = 'inter')
                        ]
                    ),

                    
                    ft.Column(
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        
                        controls = [
                            ic.svg_icon('calendar', size = 28, color = c.cinza_gelo),
                            ft.Text(value = 'Agenda', size = 14, color = c.cinza_gelo, font_family = 'inter')
                        ]
                    ),

                    self.button_bar_center,

                    ft.Column(
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        
                        controls = [
                            ic.svg_icon('adm', size = 28, color = c.cinza_gelo),
                            ft.Text(value = 'Adm', size = 14, color = c.cinza_gelo, font_family = 'inter')
                        ]
                    ),
                    
                    ft.Column(
                        alignment = ft.MainAxisAlignment.CENTER,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        
                        controls = [
                            ic.svg_icon('configuracao', size = 32, color = c.cinza_gelo),
                            ft.Text(value = 'Ajustes', size = 14, color = c.cinza_gelo, font_family = 'inter')
                        ]
                    ),
                ]
            )
        )

        self.tela_scrol = ft.Column(
            top = 0,
            left = 0,
            right = 0,
            bottom = 0,
            
            expand = True,
            scroll = ft.ScrollMode.AUTO,

            controls = [
                ft.Row(
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    controls = [self.botao_configuracao]
                ),

                self.banner,
                self.ferramentas,
                self.agendados_prox,

                ft.Column(height = 200) #espaco pra empurrar os componentes a baixo da bar
            ]
        )

        self.estrutura = ft.Stack(
            expand = True,

            controls = [
                self.tela_scrol,
                self.control_bar,
            ]
        )

        return self.estrutura